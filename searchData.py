import os
import pathlib
import subprocess


def main():
    # seedごとに処理を行う.
    for i in range(4, 100):
        file_path = pathlib.Path("/Users/haradakanon/Downloads/kGenProg-1.8.2/example/QUICKSORT".format(i=i))
        kgenprog_jarfile = pathlib.Path("/Users/haradakanon/Downloads/kGenProg-1.8.2.jar")
        cmd = "java -jar {kgenprog_jarfile} --config {file_path}/kgenprog-quicksort.toml"\
            .format(kgenprog_jarfile=kgenprog_jarfile, file_path=file_path)
        subprocess.run("{cmd} --random-seed {i} >> {file_path}/seed{i}"
                       .format(cmd=cmd, i=i, file_path=file_path), shell=True)
        # 名前を変更し、出力ファイルの数をターミナルにプリント.
        os.rename("{file_path}/kgenprog-out".format(file_path=file_path),
                  "{file_path}/seed{i}}".format(file_path=file_path, i=i))
        output_dir = "{file_path}/seed{i}".format(file_path=file_path, i=i)
        file_sum = sum(os.path.isfile(os.path.join(output_dir, name)) for name in os.listdir(output_dir))
        print(f"seed{i}の出力は{file_sum}です.".format(i=i, file_sum=file_sum))


if __name__ == "__main__":
    main()
