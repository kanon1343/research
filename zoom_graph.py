import pathlib
import matplotlib.pyplot as plt
import numpy as np

# グラフを書く


def draw_graph(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, file_path, project):
    plt.figure()
    fig, ax = plt.subplots(figsize=[6.4, 4.8])

    # 各サブプロットにデータをプロット
    ax.plot(x1, y1, label="Accept505025")
    ax.plot(x2, y2, label="Accept10010050")
    ax.plot(x3, y3, label="Accept200200100")
    ax.plot(x4, y4, label="Output505025")
    ax.plot(x5, y5, label="Output10010050")
    ax.plot(x6, y6, label="Output200200100")

    ax.legend()  # 凡例を表示

    axins = ax.inset_axes([0.6, 0.07, 0.38, 0.1])
    axins.plot(x1, y1, label="Accept505025")
    axins.plot(x2, y2, label="Accept10010050")
    axins.plot(x3, y3, label="Accept200200100")
    axins.set_xlim(0, 3000)
    axins.set_ylim(0, 50)
    ax.indicate_inset_zoom(axins)
    # axins = ax.inset_axes([0.07, 0.42, 0.3, 0.2])
    # axins.plot(x1, y1, label="A50")
    # axins.plot(x2, y2, label="A100")
    # axins.plot(x3, y3, label="A200")
    # axins.set_xlim(70000, 86400)
    # axins.set_ylim(15, 23)
    # ax.indicate_inset_zoom(axins)
    # グラフを表示
    plt.savefig(
        "{file_path}/{project}.png".format(file_path=file_path, project=project))


def main():
    projects = ["codec9"]
    for project in projects:
        # 505025
        # correct
        file_path = pathlib.Path(
            "/Users/haradakanon/Downloads/research/505025/{project}log/".format(project=project))
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

        # output
        file_path = pathlib.Path(
            "/Users/haradakanon/Downloads/research/505025/{project}log/".format(project=project))
        with open("{file_path}/output_summarize.csv".format(file_path=file_path), 'r') as file:
            log = file.read()

        # Split the log into lines
        lines = log.split('\n')
        x4 = []
        y4 = []

        for line in lines:
            if line.startswith(',') or not line:
                continue
            x4.append(int(line.split(",")[1]))
            y4.append(int(line.split(",")[2]))

        # 10010050
        # correct
        file_path = pathlib.Path(
            "/Users/haradakanon/Downloads/research/10010050/{project}log/".format(project=project))
        with open("{file_path}/seed_summarize.csv".format(file_path=file_path), 'r') as file:
            log = file.read()

        # Split the log into lines
        lines = log.split('\n')
        x2 = []
        y2 = []

        for line in lines:
            if line.startswith(',') or not line:
                continue
            x2.append(int(line.split(",")[1]))
            y2.append(int(line.split(",")[0]) + 1)

        # output
        file_path = pathlib.Path(
            "/Users/haradakanon/Downloads/research/10010050/{project}log/".format(project=project))
        with open("{file_path}/output_summarize.csv".format(file_path=file_path), 'r') as file:
            log = file.read()

        # Split the log into lines
        lines = log.split('\n')
        x5 = []
        y5 = []

        for line in lines:
            if line.startswith(',') or not line:
                continue
            x5.append(int(line.split(",")[1]))
            y5.append(int(line.split(",")[2]))

        # 200200100
        # correct
        file_path = pathlib.Path(
            "/Users/haradakanon/Downloads/research/200200100/{project}log/".format(project=project))
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

        # output
        file_path = pathlib.Path(
            "/Users/haradakanon/Downloads/research/200200100/{project}log/".format(project=project))
        with open("{file_path}/output_summarize.csv".format(file_path=file_path), 'r') as file:
            log = file.read()

        # Split the log into lines
        lines = log.split('\n')
        x6 = []
        y6 = []

        for line in lines:
            if line.startswith(',') or not line:
                continue
            x6.append(int(line.split(",")[1]))
            y6.append(int(line.split(",")[2]))

        file_path = pathlib.Path(
            "/Users/haradakanon/Downloads/research/")
        draw_graph(x1, y1, x2, y2, x3, y3, x4, y4,
                   x5, y5, x6, y6, file_path, project)


if __name__ == "__main__":
    main()
