import copy
import datetime
import glob
import logging
import random
import re
import shutil
import subprocess
from abc import ABCMeta, abstractmethod
from pathlib import Path

import toml

from research import util, defects4j

toml_template = """
root-dir = "./"
src = []
test = []
cp = []
exec-test = []
out-dir = "./output"
log-level = "INFO"
mutation-generating-count = 40
crossover-generating-count = 40
headcount = 20
max-generation = 120
time-limit = 43200
test-time-limit = 180
required-solutions = 1
random-seed = 0
"""

jar = f'{util.ROOT}/tools/kGenProg-priority/kGenProg-1.6.1.jar'
debug_jar = f'{util.ROOT}/tools/kGenProg-priority/build/libs/kGenProg-1.6.1.jar'

logger = logging.getLogger(__name__)


class Project(metaclass=ABCMeta):
    def __init__(self, v, b):
        """
        :param str v: プロジェクトID
        :param int b: バグID
        """

        util.set_java_version(8)
        self.project = v
        self.bug_id = b
        self.dir = util.bug_path(v, b)
        self.prop = self._read_prop()
        self.java_ver = self._get_java_version()

    def _read_prop(self):
        """defects4j.build.propertiesをdictにして返す
        """

        with open(f'{self.dir}/defects4j.build.properties', mode='r') as f:
            lines = []
            for line in f.readlines():
                lines.append(line.replace('\n', ''))

        res = {}
        for line in lines:
            if '#' in line:
                continue

            name, value = line.split('=')
            if 'id' in name:
                continue
            else:
                name = name.split('.')[-1]

            if 'modified' in name or 'relevant' in name or 'trigger' in name:
                value = value.split(',')

            res[name] = value

        return res

    def _get_java_version(self):
        """build.xmlやpom.xmlなどから頑張ってjavaのバージョンを探す
        :return: version
        :rtype: float
        """

        def contains(line, strings):
            for string in strings:
                if string in line:
                    return True
            return False

        def find_version_statement(file_name, fragments):
            path = Path(self.dir).joinpath(file_name)
            if path.exists():
                with open(path, 'r') as f:
                    for line in f.readlines():
                        if contains(line, fragments):
                            return line
            return None

        targets = [
            [
                'maven-build.properties',
                [
                    'javac.src.version',
                    'maven.compiler.target'
                ]
            ],
            [
                'build.xml',
                [
                    'ant.build.javac.source',
                ]
            ],
            [
                'pom.xml',
                [
                    '<maven.compile.target>',
                    '<maven.compiler.target>',
                    '<java.version>',
                    '<target>',
                    '<targetJdk>',

                ]
            ],
            [
                'build.gradle',
                [
                    'sourceCompatibility'
                ]
            ],
            [
                'ant/build.xml',
                [
                    'target="'
                ]
            ],
            [
                'project.properties',
                [
                    'maven.compile.source'
                ]
            ]
        ]

        p = re.compile(r'1[.]\d')
        for target in targets:
            version = find_version_statement(target[0], target[1])
            if version is not None:
                return float(p.findall(version)[0])

        if self.project == 'sample':
            return 1.8

        raise Exception(self.project, self.bug_id)

    def get_path_to_source_file(self):
        """プロジェクト内の全てのプログラムへのパスを返す"""

        return [i for i in glob.glob(
            f'{self.dir}/{self.prop["classes"]}/**/*.java',
            recursive=True
        )]

    def get_path_to_test_file(self):
        """プロジェクト内の全てのテストファイルへのパスを返す"""

        return [i for i in glob.glob(
            f'{self.dir}/{self.prop["tests"]}/**/*.java',
            recursive=True
        )]

    @abstractmethod
    def get_test_fqns(self):
        """プロジェクト内の全てのテスト名を返す"""

        tests = []
        dirs_count = len(util.ROOT.split('/')) - 1 + 4 + len(self.prop['tests'].split('/'))
        for test in self.get_path_to_test_file():
            # テストクラスではないクラスや抽象クラスは除外
            if test[-9:] != 'Test.java':
                continue
            if test[-9:] == 'Test.java':
                with open(test, mode='r') as f:
                    if 'public abstract class' in f.read():
                        continue

            dirs = test.split('/')
            tests.append('.'.join(dirs[dirs_count:])[:-5])

        return tests

    def _get_test_fqns(self, includes_str, excludes_str):
        """プロジェクト内のテストの名前を返す
        :type includes_str: list[str]
        :type excludes_str: list[str]
        """

        includes = [re.compile(s) for s in includes_str]
        excludes = [re.compile(s) for s in excludes_str]

        def is_exclude_file(file_name):
            for exclude in excludes:
                if exclude.match(file_name):
                    return True

            for include in includes:
                if include.match(file_name):
                    return False

            return True

        fqns = []
        dirs_count = len(util.ROOT.split('/')) - 1 + 4 + len(self.prop['tests'].split('/'))
        for test in self.get_path_to_test_file():
            if is_exclude_file(test):
                continue

            dirs = test.split('/')
            fqns.append('.'.join(dirs[dirs_count:])[:-5])

        return fqns

    def compile(self):
        """ソースコードとテストコードをコンパイルする"""

        # ソースコードのコンパイル
        classes_dest = Path(self.dir).joinpath('build')
        if not classes_dest.exists():
            classes_dest.mkdir()

        command = [
            'javac',
            '-Xlint:-options',
            '-source', f'{self.java_ver}',
            '-target', f'{self.java_ver}',
            '-cp', self.get_class_path(),
            '-d', str(classes_dest),
            '-encoding', 'UTF-8'
        ]
        command.extend(self.get_path_to_source_file())

        error_message = []
        proc = subprocess.run(command, cwd=self.dir, stderr=subprocess.PIPE)
        for line in proc.stderr.decode().split('\n')[:-1]:
            if 'Note:' not in line:
                error_message.append(line)

        # テストコードのコンパイル
        test_dest = Path(self.dir).joinpath('build-tests')
        if not test_dest.exists():
            test_dest.mkdir()

        command = [
            'javac',
            '-Xlint:-options',
            '-source', f'{self.java_ver}',
            '-target', f'{self.java_ver}',
            '-cp', self.get_class_path() + ':build',
            '-d', str(test_dest),
            '-encoding', 'UTF-8'
        ]
        command.extend(self.get_path_to_test_file())
        proc = subprocess.run(command, cwd=self.dir, stderr=subprocess.PIPE)
        for line in proc.stderr.decode().split('\n')[:-1]:
            if 'Note:' not in line:
                error_message.append(line)

        if len(error_message) != 0:
            print('\n'.join(error_message))

        logger.debug(f'{self.project}-{self.bug_id} Compiled')

    def test_fqn(self, fqn):
        """１つのクラスファイルを実行する．デバッグに使う"""

        command = [
            'java',
            '-XX:ReservedCodeCacheSize=1G',
            '-cp', f'.:build:build-tests:{self.get_class_path()}:{util.JUNIT_CP}',
            'org.junit.runner.JUnitCore', fqn
        ]

        subprocess.run(
            command,
            cwd=self.dir,
            timeout=5
        )

    def test(self, debug: bool = False):
        """テストを実行する

        :param bool debug: trueのとき，失敗テストの詳細を表示する
        :return: 成功したテストの数，失敗したテストの数，打ち切ったテストクラス
        :rtype: int, int, list[str]
        """

        command = [
            'java',
            '-XX:ReservedCodeCacheSize=1G',
            '-cp', f'.:build:build-tests:{self.get_class_path()}:{util.JUNIT_CP}',
            'org.junit.runner.JUnitCore',
        ]

        pass_tests = 0
        fail_tests = 0
        timeout_tests = []
        fqns = self.get_test_fqns()

        re_ok = re.compile(r'OK \(\d+ test[s]*\)')
        re_test_count = re.compile(r'Tests run: \d+')
        re_fail_count = re.compile(r'Failures: \d+')
        for idx, fqn in zip(range(len(fqns)), fqns):
            print(f'\rRunning Tests: {idx} / {len(fqns)}  (pass: {pass_tests}, fail: {fail_tests})', end='')
            exec_command = copy.copy(command)
            exec_command.append(fqn)

            try:
                proc = subprocess.run(
                    exec_command,
                    cwd=self.dir,
                    stdout=subprocess.PIPE,
                    timeout=60 * 5
                )
                stdout = proc.stdout.decode()
                if debug:
                    print('\n', fqn, '\n', stdout)

                if re_ok.findall(stdout):
                    pass_tests += int(re_ok.findall(stdout)[0][4:-6])
                else:
                    test_count = int(re_test_count.findall(stdout)[0][11:])
                    fail_count = int(re_fail_count.findall(stdout)[0][10:])
                    pass_tests += test_count - fail_count
                    fail_tests += fail_count

            except subprocess.TimeoutExpired:
                # raise Exception(f'{fqn} Reach time limit')
                timeout_tests.append(fqn)

        print('\r\r')
        logger.debug(f'{self.project}-{self.bug_id} Tested\n'
                     f'\t\tpass tests: {pass_tests}\n'
                     f'\t\tfail tests: {fail_tests}\n'
                     f'\t\ttimeout classes: {len(timeout_tests)}'
                     )
        return pass_tests, fail_tests, timeout_tests

    def fail_test_count_check(self):
        """失敗テストの数が想定した数かを確かめる"""

        _, actual, _ = self.test()
        expect = len(self.prop['trigger'])
        if expect == actual:
            logger.debug('Test maybe correct')
        else:
            raise Exception(f'Fail test\nExpect: {expect}\nActual: {actual}')

    def fail_test_check(self):
        """kGenProgのテストで，想定したテストケースが落ちているかを確かめる"""

        stdout = self.debug_run(True)
        fail_fqns = set()
        is_fqn_line = False
        for line in stdout.split('\n'):
            if is_fqn_line:
                if '[INFO]' in line:
                    break
                fail_fqns.add(line)
            else:
                if 'Failed Test FQNs from the initial variant' in line:
                    is_fqn_line = True

        trigger_tests = set()
        for i in self.prop['trigger']:
            trigger_tests.add(i.replace('::', '.'))

        if fail_fqns == trigger_tests:
            logger.debug('kGenProg maybe working correct')
        else:
            raise Exception(f'triggerのテストケースとkGenProgの実行結果が異なっている\n'
                            f'Expect: {sorted(trigger_tests)}\n'
                            f'Actual: {sorted(fail_fqns)}')

    def comment_out_stdout(self):
        """テストファイルに含まれる出力コードの行をコメントアウトする
        上書きする
        """

        tests = self.get_path_to_test_file()
        for test in tests:
            try:
                with open(test, mode='r', encoding='utf-8') as f:
                    code = f.read()
            except UnicodeDecodeError as e:
                print(test)
                raise e

            while True:
                begin = code.find('System.out.print')
                if begin == -1:
                    break

                end = begin
                is_string = False
                while True:
                    if is_string:
                        if code[end] == '"':
                            is_string = False
                    else:
                        if code[end] == '"':
                            is_string = True
                        if code[end] == ';':
                            break
                    end += 1

                code = code[:begin] + code[end + 1:]

            with open(test, mode='w', encoding='utf-8') as f:
                f.write(code)

    def _get_class_path(self, jar_dirs, dirs, connect):
        """
        :type jar_dirs: list[str]
        :type dirs: list[str]
        :type connect: bool
        """

        res = []
        for jar_dir in jar_dirs:
            for depend_jar in Path(self.dir).joinpath(jar_dir).glob('*.jar'):
                depend_jar = str(depend_jar)
                res.append(depend_jar[depend_jar.find('buggy') + 6:])

        for dir_ in dirs:
            res.append(dir_)

        if connect:
            return ':'.join(res)
        else:
            return res

    @abstractmethod
    def get_class_path(self, connect=True):
        raise NotImplementedError

    def generate_toml(self, output_dir, selector, ratio):
        """tomlを生成する

        :param str output_dir: <self.dir>/output/<output_dir>にkGenProgの実行結果が生成される
        :param Selector selector: 実行するテストを選択する手法
        :param ratio: 修正に使用するテストの割合
        """

        ktoml = toml.loads(toml_template)
        ktoml['src'].append(self.prop['classes'])
        ktoml['test'].append(self.prop['tests'])
        ktoml['exec-test'] = selector.run()
        ktoml['cp'] = self.get_class_path(False)
        ktoml['out-dir'] = output_dir
        ktoml['random-seed'] = random.randint(0, 100000)
        ktoml['jdk-version'] = f'{self.java_ver}'
        ktoml['test-activity-ratio'] = ratio

        return ktoml

    def write_toml(self, ktoml):
        with open(f'{self.dir}/kgenprog.toml', mode='w') as f:
            toml.dump(ktoml, f)

    def debug_run(self, output=False):
        """正しくkGenProgが実行されるかを確認するための関数．
        """

        ktoml = self.generate_toml('output/test', util.get_selector('no_selection')(self), -1)
        ktoml['mutation-generating-count'] = 2
        ktoml['crossover-generating-count'] = 2
        ktoml['headcount'] = 1
        ktoml['max-generation'] = 2
        ktoml['test-time-limit'] = 100
        self.write_toml(ktoml)

        if output:
            proc = subprocess.run(['java', '-jar', debug_jar], cwd=self.dir, stdout=subprocess.PIPE)
            return proc.stdout.decode()
        else:
            subprocess.run(['java', '-jar', debug_jar], cwd=self.dir)

    def run(self, selector, loop=0, ratio=-1):
        """kGenProgを実行する．loopがゼロの時，デバッグのための実行を行う．

        :param selector: exec-testに与えるテストの選択手法
        :param int loop: kGenProgの実行回数
        :param int ratio: テスト優先順位→テスト選択をする際，全体のテストクラスのうち何％利用するか．
        """

        selector = selector(self)
        logger.debug(f'{self.project}-{self.bug_id} {selector.name()} {ratio} kGenProg start')

        if loop == 0:
            output_dir = Path(self.dir).joinpath('output/test')
            if not output_dir.exists():
                output_dir.mkdir(parents=True)

            ktoml = self.generate_toml('output/test', selector, ratio)
            ktoml['mutation-generating-count'] = 2
            ktoml['crossover-generating-count'] = 2
            ktoml['headcount'] = 1
            ktoml['max-generation'] = 2
            ktoml['test-time-limit'] = 10
            self.write_toml(ktoml)

            proc = subprocess.run(['java', '-jar', jar],
                                  cwd=self.dir,
                                  # stdout=subprocess.PIPE,
                                  # stderr=subprocess.PIPE
                                  )
            # with open(output_dir.joinpath('info_stdout.txt'), mode='w') as f:
            #    f.write(proc.stdout.decode())
            # with open(output_dir.joinpath('info_stderr.txt'), mode='w') as f:
            #    f.write(proc.stderr.decode())
        else:
            for _ in range(int(loop)):
                output_dir = Path(f'{util.ROOT}/repair_result/{self.project}/'
                                  f'{util.upper_case(self.project)}_{self.bug_id}_buggy')
                if ratio == -1:
                    output_dir = output_dir.joinpath(f'{selector.name()}')
                else:
                    output_dir = output_dir.joinpath(f'{selector.name()}_mutation_{ratio}')
                output_dir = output_dir.joinpath(f'{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}')

                if not output_dir.exists():
                    output_dir.mkdir(parents=True)

                self.write_toml(
                    self.generate_toml(str(output_dir), selector, ratio)
                )
                try:
                    proc = subprocess.run(
                        ['java', '-XX:ReservedCodeCacheSize=1G', '-Xmx8G', '-jar', jar],
                        cwd=self.dir,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        timeout=60 * 60 * 9  # 9でタイムアウト
                    )

                    with open(output_dir.joinpath('info_stdout.txt'), mode='w') as f:
                        f.write(proc.stdout.decode())
                    with open(output_dir.joinpath('info_stderr.txt'), mode='w') as f:
                        f.write(proc.stderr.decode())
                    with open(output_dir.joinpath('test_selection_time.txt'), mode='w') as f:
                        f.write(f'{selector.exec_time()} min\n')
                except subprocess.TimeoutExpired:
                    with open(output_dir.joinpath('timeout.txt'), mode='w') as f:
                        f.write('Timeout: 15 hours')

        logger.debug(f'{self.project}-{self.bug_id} {selector.name()} {ratio} kGenProg end')

    def reset_modify_files(self):
        defects4j.reset_modify_files(self.project, self.bug_id)

    def change_buggy_version(self):
        defects4j.checkout_buggy(self.project, self.bug_id)

    def change_fixed_version(self):
        defects4j.checkout_fixed(self.project, self.bug_id)

    def _rename_files(self, exclude_files):
        """コンパイルや実行がうまくいかないファイルをリネームしてビルドやテスト対象から外す．
        """

        for file in exclude_files:
            shutil.move(f'{self.dir}/{file}', f'{self.dir}/{file}.bak')

    def rename_files(self):
        pass

    def initialize(self):
        self.reset_modify_files()
        # self.comment_out_stdout()
        self.rename_files()
        self.copy_dependencies()

    def copy_dependencies(self):
        """依存関係があるjarをダウンロードする"""

        if Path(f'{self.dir}/lib').exists() or not Path(f'{self.dir}/pom.xml').exists():
            return

        subprocess.run(['mvn', 'dependency:copy-dependencies', '-D outputDirectory=lib'],
                       cwd=self.dir)

    def show_file_count_and_loc(self):
        """*.javaファイルの数とLOCを表示する"""

        def get_loc(files):
            sum = 0
            for file in files:
                with open(file, 'r') as f:
                    sum += len(f.readlines())
            return sum

        source_files = self.get_path_to_source_file()
        print('source file', len(source_files), get_loc(source_files))

        test_files = self.get_path_to_test_file()
        print('test file', len(test_files), get_loc(test_files))

        print('use tests count', len(self.get_test_fqns()))


def delete_project(project_id, bug_id):
    project_dir = Path(util.bug_path(project_id, bug_id))
    if not project_dir.exists():
        raise FileNotFoundError

    subprocess.run(['rm', '-rf', project_dir])


def reset_project(project_id, bug_id):
    delete_project(project_id, bug_id)
    defects4j.clone(project_id, bug_id)


if __name__ == '__main__':
    pass
