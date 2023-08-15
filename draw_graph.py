import pathlib
import matplotlib.pyplot as plt
import numpy as np
import japanize_matplotlib

# グラフを書く


def draw_graph(x1, y1, x3, y3, file_path, project):
    plt.figure()
    # 各サブプロットにデータをプロット
    plt.plot(x1, y1, label="505025")
    # plt.plot(x2, y2, label="10010050")
    plt.plot(x3, y3, label="200200100")

    plt.legend()  # 凡例を表示
    plt.title("math{project}".format(project=project))
    # グラフを表示
    plt.savefig(
        "{file_path}/math{project}.png".format(file_path=file_path, project=project))


def main():
    projects = ["49", "82"]
    for project in projects:
        # 505025
        file_path = pathlib.Path(
            "/Users/haradakanon/Downloads/research/505025/math{project}log/".format(project=project))
        with open("{file_path}/seed_summarize.csv".format(file_path=file_path), 'r') as file:
            log = file.read()

        # Split the log into lines
        lines = log.split('\n')
        x1 = []
        y1 = []

        for line in lines:
            if line.startswith(',') or not line:
                continue
            x1.append(int(line.split(",")[1]))
            y1.append(int(line.split(",")[0]) + 1)

        # # 10010050
        # file_path = pathlib.Path(
        #     "/Users/haradakanon/Downloads/research/10010050/math{project}log/".format(project=project))
        # with open("{file_path}/seed_summarize.csv".format(file_path=file_path), 'r') as file:
        #     log = file.read()

        # # Split the log into lines
        # lines = log.split('\n')
        # x2 = []
        # y2 = []

        # for line in lines:
        #     if line.startswith(',') or not line:
        #         continue
        #     x2.append(int(line.split(",")[1]))
        #     y2.append(int(line.split(",")[0]) + 1)

        # 200200100
        file_path = pathlib.Path(
            "/Users/haradakanon/Downloads/research/200200100/math{project}log/".format(project=project))
        with open("{file_path}/seed_summarize.csv".format(file_path=file_path), 'r') as file:
            log = file.read()

        # Split the log into lines
        lines = log.split('\n')
        x3 = []
        y3 = []

        for line in lines:
            if line.startswith(',') or not line:
                continue
            x3.append(int(line.split(",")[1]))
            y3.append(int(line.split(",")[0]) + 1)

        file_path = pathlib.Path(
            "/Users/haradakanon/Downloads/research/")
        draw_graph(x1, y1, x3, y3, file_path, project)


if __name__ == "__main__":
    main()
