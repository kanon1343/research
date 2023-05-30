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


def main():
    # seedごとに処理を行う.
    file_path = pathlib.Path("/Users/haradakanon/Downloads/kGenProg-1.8.2/example/QUICKSORT")
    kgenprog_jarfile = pathlib.Path("/Users/haradakanon/Downloads/kGenProg-1.8.2.jar")
    output_file_path = "/Users/haradakanon/Desktop/研究/実験データ/research"
    for i in range(4, 100):
        cmd = "java -jar {kgenprog_jarfile} --config {file_path}/kgenprog-quicksort.toml" \
            .format(kgenprog_jarfile=kgenprog_jarfile, file_path=file_path)
        repair(cmd, i, file_path)
        output_sum(output_file_path, i)


if __name__ == "__main__":
    main()
