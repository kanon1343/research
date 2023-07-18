import logging
import os
import shutil
from pathlib import Path


def _get_root():
    """プロジェクトのルートディレクトリを取得する"""

    dirs = Path(os.getcwd()).parts
    return '/'.join(dirs[:dirs.index('project') + 1])[1:]


ROOT = _get_root()
JUNIT_CP = f'{ROOT}/tools/hamcrest-core-1.3.jar:' \
    f'{ROOT}/tools/junit-4.12.jar'

logging.basicConfig(level=logging.DEBUG)


def bug_path(identifier, bug_id, ppath=False):
    """Return path to project. If path == True, return PosixPath.

    :param str identifier:
    :param int bug_id:
    :param bool ppath:
    :return:
    """

    p = f'{ROOT}/bugs/{identifier}/{upper_case(identifier)}_{bug_id}_buggy'
    if ppath:
        return Path(p)
    else:
        return p


def upper_case(s):
    return s[0].upper() + s[1:]


def set_java_version(ver):
    """javaのバージョンを`ver`に変更する．
    """
    if ver == 7:
        os.environ['JAVA_HOME'] = "/Library/Java/JavaVirtualMachines/jdk1.7.0_80"
    elif ver == 8:
        os.environ['JAVA_HOME'] = "/Library/Java/JavaVirtualMachines/jdk1.8.0_191.jdk/Contents/Home"
    elif ver == 11:
        os.environ['JAVA_HOME'] = "/Library/Java/JavaVirtualMachines/adoptopenjdk-11.jdk/Contents/Home"
    elif ver == 14:
        os.environ['JAVA_HOME'] = "/Library/Java/JavaVirtualMachines/openjdk-14.jdk/Contents/Home"
    else:
        raise AttributeError(f"Java version: {ver} not found")

    # subprocess.run(['java', '-version'])


def move_error_message(ident, bug_id):
    """output/test/info_stdout.txtを移動する
    """

    shutil.copy(
        f'{bug_path(ident, bug_id)}/output/test/info_stderr.txt',
        f'{ROOT}/src/chart_error_message/{bug_id}_err.txt'
    )


def path(*args):
    """引数の値を全て連結させたパスを返す
    """

    res = None
    for dir_ in args:
        dir_ = Path(dir_) if type(dir_) == str else dir_
        if res is None:
            res = Path(dir_)
        else:
            res = res.joinpath(dir_)
    return res


def bug_dir_name(project_id, bug_id):
    return f'{upper_case(project_id)}_{bug_id}_buggy'


def new_project(project_id, bug_id):
    from src import defects4j
    from src.project.math_project import MathProject
    from src.project.sample_project import SampleProject
    from src.project.chart_project import ChartProject
    from src.project.closure_project import ClosureProject
    from src.project.lang_project import LangProject
    from src.project.cli_project import CliProject
    from src.project.codec_project import CodecProject
    from src.project.collections_project import CollectionsProject
    from src.project.csv_project import CsvProject
    from src.project.gson_project import GsonProject
    from src.project.jackson_core_project import JacksonCoreProject
    from src.project.jackson_databind_project import JacksonDatabindProject
    from src.project.jackson_xml_project import JacksonXmlProject
    from src.project.jsoup_project import JsoupProject
    from src.project.jxpath_project import JxPathProject
    from src.project.time_project import TimeProject
    from src.project.mockito_project import MockitoProject
    from src.project.compress_project import CompressProject
    m = {
        'chart': ChartProject,
        'cli': CliProject,
        'closure': ClosureProject,
        'codec': CodecProject,
        'collections': CollectionsProject,
        'compress': CompressProject,
        'csv': CsvProject,
        'gson': GsonProject,
        'jacksonCore': JacksonCoreProject,
        'jacksonDatabind': JacksonDatabindProject,
        'jacksonXml': JacksonXmlProject,
        'jsoup': JsoupProject,
        'jxPath': JxPathProject,
        'lang': LangProject,
        'math': MathProject,
        'mockito': MockitoProject,
        'time': TimeProject,
        'sample': SampleProject,
    }
    if not bug_path(project_id, bug_id, True).exists():
        defects4j.clone(project_id, bug_id)
    return m[project_id](bug_id)


def get_selector(selection_method):
    from src.test_selection.coverage_selection import CoverageSelection
    from src.test_selection.failed_only import FailedOnly
    from src.test_selection.no_selection import NoSelection
    from src.test_selection.relative_selection import RelativeSelection
    selector = {
        'failed_only': FailedOnly,
        'no_selection': NoSelection,
        'relative_selection': RelativeSelection,
        'coverage_selection': CoverageSelection,
    }
    return selector[selection_method]


def find(str_list, substr):
    """substr in str_list[i] == true -> return str_list[i]
    """

    for str_ in str_list:
        if substr in str_:
            return str_

    return None


# 修正できそうなバグ番号を集めた．
bug_ids = {
    'cli': [37], # 40],
    'codec': [16],
    #'collections': [26],
    'compress': [42], #, 45],
    'lang': [7],
    'math': [49], # 50, 73],
    'jacksonCore': [21],

    # 修正ができなかったプロジェクト
    'jacksonDatabind': [3],  # OK
    'chart': [7, 12, 13, 15, 25],
    'csv': [13, 14, 15, 16],
    'gson': [16, 17, 18],
    'jacksonXml': [1, 2, 3, 4],#, 5, 6],
    'jsoup': [90, 91, 92, 93],
    'mockito': [31, 32, 33, 34, 35, 36, 37, 38],
    'time': [22, 23, 24, 25, 26, 27],
}

repair_types = [
    'failed_only',
    'no_selection',
    'no_selection_mutation_20',
    'no_selection_mutation_50',
    'no_selection_mutation_80',
    'relative_selection',
    'relative_selection_mutation_20',
    'relative_selection_mutation_50',
    'relative_selection_mutation_80',
    'coverage_selection',
]


def show_result_count(show_50=False):
    for project_id, bug_id_list in bug_ids.items():
        for bug_id in bug_id_list:
            for repair_type in repair_types:
                dir_ = f'{ROOT}/repair_result/{project_id}/{bug_dir_name(project_id, bug_id)}/{repair_type}'
                try:
                    count = len([i for i in Path(dir_).iterdir()])
                    if count == 50 and not show_50:
                        continue
                    print(count, bug_dir_name(project_id, bug_id), repair_type)
                except FileNotFoundError as e:
                    print(e)
            print()


def make_figure_table(file_name, subcaption, label, all_caption, all_label, all_caption_2, all_label_2):
    figure = []
    for project_id, bug_id_list in bug_ids.items():
        for bug_id in bug_id_list:
            figure.append(
                r"""\begin{minipage}{0.5\hsize}
  \begin{center}
    \includegraphics[bb=0 0 432 360, scale=0.45]{./img/%s/%s.png}
    \subcaption{%s-%s%s}
    \label{%s %s-%s}
  \end{center}
\end{minipage}""" % (
                    bug_dir_name(project_id, bug_id),
                    file_name,
                    project_id,
                    bug_id,
                    subcaption,
                    label,
                    project_id,
                    bug_id
                )
            )

    print(r"""\begin{figure}[t]
\begin{center}""")
    for i in range(0, 6, 2):
        print(r"""\begin{tabular}{c}
%s
%s
\end{tabular}""" % (figure[i], figure[i + 1]), end='\n\n')

    print(r"""\end{center}
\caption{%s}
\label{%s}
\end{figure}""" % (all_caption, all_label))

#    print(r"""\begin{tabular}{c}
#%s
#\end{tabular}""" % (figure[-1]))
#    print(r"""\end{center}
#\caption{%s}
#\label{%s}
#\end{figure}""" % (all_caption_2, all_label_2))

if __name__ == '__main__':
    #for project_id, bug_ids in bug_ids.items():
    #    for bug_id in bug_ids:
    #        tmp = new_project(project_id, bug_id)
    #        print(tmp.prop['trigger'])
    show_result_count()
    # tmp = new_project('jacksonCore', 21)
    # tmp.reset_modify_files()
    # tmp.show_file_count_and_loc()

    #make_figure_table('exec_time', 'での実行時間', 'fig:exec time',
    #                  '実行時間の一覧 (a)-(f)', 'fig:exec time a-f',
    #                  '実行時間の一覧 (g)-(l)', 'fig:exec time g-l')
    #make_figure_table('patch', 'でのプログラム生成数', 'fig:patch',
    #                  'プログラム生成数の一覧 (a)-(f)', 'fig:patch a-f',
    #                  'プログラム生成数の一覧 (g)-(l)', 'fig:patch g-l')
