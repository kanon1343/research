import pathlib
import subprocess


def main():
    # file_paths = glob.glob("../math46_seed0/", recursive=True)
    # seedごとに処理を行う.
    for i in range(100):
        file_path = pathlib.Path("/Users/haradakanon/Downloads/kGenProg-1.8.2/example/LIS".format(i=i))
        kgenprog_jarfile = pathlib.Path("/Users/haradakanon/Downloads/kGenProg-1.8.2.jar")
        cmd = "java -jar {kgenprog_jarfile} --config {file_path}/kgenprog-lis.toml"\
            .format(kgenprog_jarfile=kgenprog_jarfile, file_path=file_path)
        subprocess.run("{cmd} --random-seed {i} >> {file_path}/seed{i} ".format(cmd=cmd, i=i, file_path=file_path),
                       shell=True)


if __name__ == "__main__":
    main()
