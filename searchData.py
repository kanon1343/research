import os
import pathlib
import subprocess


def repair(cmd, i, file_path):
    subprocess.run("{cmd} --random-seed {i} >> {file_path}/seed{i}"
                   .format(cmd=cmd, i=i, file_path=file_path), shell=True)


# 名前を変更し、出力ファイルの数をターミナルにプリント.
def output_sum(file_path, i):
    os.rename("{file_path}/kgenprog-out".format(file_path=file_path),
              "{file_path}/seed{i}".format(file_path=file_path, i=i))
    output_dir = "{file_path}/seed{i}".format(file_path=file_path, i=i)
    print("seed{i}の出力数".format(i=i))
    print(sum(os.path.isdir(os.path.join(output_dir, name)) for name in os.listdir(output_dir)))


def remove_comment(file_path):
    """EntityArrays.java には utf-8 でない文字が含まれており kGenProg の実行がうまくいかないため，
    それらを削除する．
    """

    # file_path = path + '/src/main/java/org/apache/commons/lang3/text/translate/EntityArrays.java'
    with open(file_path, 'r', encoding='iso-8859-1') as f:
        code = f.readlines()

    for i in range(len(code)):
        if '//' in code[i]:
            comment_idx = code[i].index('//')
            code[i] = code[i][: comment_idx]

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(code)

def main():
    # seedごとに処理を行う.
    file_path = pathlib.Path('/Users/haradakanon/Downloads/kGenProg-1.8.2/example/math49')
    # remove_comment(file_path)
    kgenprog_jarfile = pathlib.Path("/Users/haradakanon/Downloads/kGenProg-1.8.2.jar")
    output_file_path = "/Users/haradakanon/Desktop/research"
    for i in range(1, 5):
        cmd = "java -jar {kgenprog_jarfile} --config {file_path}/kgenprog-49.toml" \
            .format(kgenprog_jarfile=kgenprog_jarfile, file_path=file_path)
        repair(cmd, i, file_path)
        output_sum(output_file_path, i)


if __name__ == "__main__":
    main()
