import pathlib
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
import subprocess
import csv
import pandas as pd


def get_repair_lines(file_path):
    # 出力ごとに処理を行う.
    file_paths = glob.glob("{file_path}/**/".format(file_path=file_path), recursive=True)
    dicts = {}
    for output_dir in file_paths:
        # diffでの"+""-"の合計を計算し、辞書に登録.
        diffs = glob.glob("{output_dir}/*.diff".format(output_dir=output_dir), recursive=True)
        count = 0
        output_number = 0
        for diff in diffs:
            sub_dirname = os.path.basename(os.path.dirname(diff))  # パス文字列の出力番号部分の摘出.
            number = sub_dirname.split()  # 出力番号.
            output_number = int(number[0])
            with open(diff) as d:
                for line in d:
                    if line.startswith("- "):
                        count += 1
                    else:
                        if line.startswith("+") and not (line.startswith("+++")):
                            count += 1
        if not output_number in dicts:
            dicts[output_number] = list()
        dicts[output_number].append(count)
    return dicts
    # ソートしてグラフを書く.
    # sorted(dicts.items())
    # dicts = sorted(dicts.items())
    # dicts = dict((x, y) for x, y in dicts)
    # draw_graph(dicts, num)


# グラフを書く
def draw_graph(dicts: dict, num):
    plt.figure()
    x = dicts.keys()
    y = dicts.values()
    plt.title("seed%d" % (num))
    plt.xticks(np.arange(1, 101, step=5))
    plt.plot(x, y)
    plt.savefig("seed%d.png" % (num))
    # plt.show()


# lizardで分析し、csvファイルを出力.
def analyze_code(file_path):
    count = sum(os.path.isdir(os.path.join(file_path, name)) for name in os.listdir(file_path)) + 1
    for i in range(1, count):
        # ファイルが存在したら消去.
        if os.path.exists("{file_path}/{i}/analyze.csv".format(file_path=file_path, i=i)):
            os.remove("{file_path}/{i}/analyze.csv".format(file_path=file_path, i=i))

        subprocess.run(
            "lizard {file_path}/{i}/ -l java --csv >> {file_path}/{i}/analyze.csv".format(file_path=file_path, i=i),
            shell=True)
        header = ["nloc", "ccn", "token_count", "parameter_count", "length", "location", "filepath", "method_name",
                  "method_long_name", "start_line", "end_line"]
        df = pd.read_csv("{file_path}/{i}/analyze.csv".format(file_path=file_path, i=i), names=header)
        df.to_csv("{file_path}/{i}/analyze.csv".format(file_path=file_path, i=i))


# defects4j分析用.
def defects4j_analyze_code(file_path):
    if os.path.exists("{file_path}/analyze.csv".format(file_path=file_path)):
        os.remove("{file_path}/analyze.csv".format(file_path=file_path))

    subprocess.run("lizard {file_path}/ -l java --csv >> {file_path}/analyze.csv".format(file_path=file_path),
                   shell=True)
    header = ["nloc", "ccn", "token_count", "parameter_count", "length", "location", "filepath", "method_name",
              "method_long_name", "start_line", "end_line"]
    df = pd.read_csv("{file_path}/analyze.csv".format(file_path=file_path), names=header)
    df.to_csv("{file_path}/analyze.csv".format(file_path=file_path))


# 出力結果の分析結果の合計と名前簡略化の出力.
def analyze_element(file_path):
    count = sum(os.path.isdir(os.path.join(file_path, name)) for name in os.listdir(file_path)) + 1
    dicts = {}
    repair_lines_dicts = get_repair_lines(file_path)
    file_name = ""
    for i in range(1, count):
        df = pd.read_csv("{file_path}/{i}/analyze.csv".format(file_path=file_path, i=i))
        df_metrics = pd.DataFrame(columns=["nloc", "ccn", "token", "parameter", "length", "repairLines", "filename"])
        nloc = 0
        ccn = 0
        token = 0
        parameter = 0
        length = 0
        index = 1
        for j in range(len(df) - 1):
            # メトリクスの合計を取得.
            file_name = df.iat[j, 7]
            if file_name == df.iat[j + 1, 7]:
                nloc += df.iat[j, 1]
                ccn += df.iat[j, 2]
                token += df.iat[j, 3]
                parameter += df.iat[j, 4]
                length += df.iat[j, 5]
            else:
                nloc += df.iat[j, 1]
                ccn += df.iat[j, 2]
                token += df.iat[j, 3]
                parameter += df.iat[j, 4]
                length += df.iat[j, 5]
                # ファイル名を取得(org.apache.~~.java).
                file_name = df.iat[j, 7]
                file_name = file_name.split("/")
                file_name = file_name[9]
                repair_lines = repair_lines_dicts[i]
                dicts = {"nloc": nloc, "ccn": ccn, "token": token, "parameter": parameter, "length": length,
                         "repairLines": repair_lines, "filename": file_name}
                s = pd.DataFrame(dicts, index=[index])
                nloc = 0
                ccn = 0
                token = 0
                parameter = 0
                length = 0
                index += 1
                df_metrics = pd.concat([df_metrics, s])
        # 最終行の計算.
        nloc += df.iat[j + 1, 1]
        ccn += df.iat[j + 1, 2]
        token += df.iat[j + 1, 3]
        parameter += df.iat[j + 1, 4]
        length += df.iat[j + 1, 5]
        file_name = file_name.split("/")
        file_name = file_name[9]
        repair_lines = repair_lines_dicts[i]
        dicts = {"nloc": nloc, "ccn": ccn, "token": token, "parameter": parameter, "length": length,
                 "repairLines": repair_lines, "filename": file_name}
        s = pd.DataFrame(dicts, index=[index])
        df_metrics = pd.concat([df_metrics, s])

        df_metrics.to_csv("{file_path}/{i}/metrics.csv".format(file_path=file_path, i=i))


# defects4j分析結果の合計と名前簡略化の出力.
def defects4j_analyze_element(file_path):
    df = pd.read_csv("{file_path}/analyze.csv".format(file_path=file_path))
    df_metrics = pd.DataFrame(columns=["nloc", "ccn", "token", "parameter", "length", "filename"])
    nloc = 0
    ccn = 0
    token = 0
    parameter = 0
    length = 0
    index = 1
    file_name = ""
    for i in range(len(df) - 1):
        # メトリクスの合計を取得.
        file_name = df.iat[i, 7]
        if file_name == df.iat[i + 1, 7]:
            nloc += df.iat[i, 1]
            ccn += df.iat[i, 2]
            token += df.iat[i, 3]
            parameter += df.iat[i, 4]
            length += df.iat[i, 5]
        else:
            nloc += df.iat[i, 1]
            ccn += df.iat[i, 2]
            token += df.iat[i, 3]
            parameter += df.iat[i, 4]
            length += df.iat[i, 5]
            # ファイル名を取得(org.apache.~~.java).
            file_name = file_name.split("/", 3)
            file_name = file_name[3].replace("/", ".")
            dicts = {"nloc": nloc, "ccn": ccn, "token": token, "parameter": parameter, "length": length,
                     "filename": file_name}
            s = pd.DataFrame(dicts, index=[index])
            nloc = 0
            ccn = 0
            token = 0
            parameter = 0
            length = 0
            index += 1
            df_metrics = pd.concat([df_metrics, s])
    # 最終行の計算.
    nloc += df.iat[i + 1, 1]
    ccn += df.iat[i + 1, 2]
    token += df.iat[i + 1, 3]
    parameter += df.iat[i + 1, 4]
    length += df.iat[i + 1, 5]
    file_name = file_name.split("/", 3)
    file_name = file_name[3].replace("/", ".")
    dicts = {"nloc": nloc, "ccn": ccn, "token": token, "parameter": parameter, "length": length, "filename": file_name}
    s = pd.DataFrame(dicts, index=[index])
    df_metrics = pd.concat([df_metrics, s])

    # csvファイルへ出力
    df_metrics.to_csv("{file_path}/metrics.csv".format(file_path=file_path))


# 出力ファイルあたりのポイントを計算し、グラフ出力.
def get_point(file_path, defects4j, seed):
    count = sum(os.path.isdir(os.path.join(file_path, name)) for name in os.listdir(file_path)) + 1
    df_origin = pd.read_csv("{defects4j}/metrics.csv".format(defects4j=defects4j), index_col=0)
    dicts = {}
    # originとrepairのdiffをとってcsv出力.
    for i in range(1, count):
        df_repair = pd.read_csv("{file_path}/{i}/metrics.csv".format(file_path=file_path, i=i), index_col=0)
        df = pd.merge(df_origin, df_repair, suffixes=["_o", "_r"], on=["filename"])
        df.to_csv("{file_path}/{i}/diff.csv".format(file_path=file_path, i=i))

    # diff.csvから得点化し、グラフへプロット.
    nloc = 0
    ccn = 0
    token = 0
    repair_lines = 0
    num = 0
    dicts = {}
    for i in range(1, count):
        df_diff = pd.read_csv("{file_path}/{i}/diff.csv".format(file_path=file_path, i=i), index_col=0)
        repair_lines = df_diff.iat[0, 11]
        for j in range(len(df_diff)):
            nloc += max([df_diff.iat[j, 0], df_diff.iat[j, 6]]) - min(df_diff.iat[j, 0], df_diff.iat[j, 6])
            ccn += df_diff.iat[j, 7] - df_diff.iat[j, 1]
            token += max([df_diff.iat[j, 2], df_diff.iat[j, 8]]) - min([df_diff.iat[j, 2], df_diff.iat[j, 8]])
        token = token / 10
        num = nloc + ccn + token + repair_lines
        nloc = 0
        ccn = 0
        token = 0
        repair_lines = 0
        if not i in dicts:
            dicts[i] = list()
        dicts[i].append(num)
    # ソートしてグラフを書く.
    sorted(dicts.items())
    dicts = sorted(dicts.items())
    dicts = dict((x, y) for x, y in dicts)
    print("seed{seed}".format(seed=seed))
    print(dicts)
    draw_graph(dicts, seed)


def clean(file_path):
    count = sum(os.path.isdir(os.path.join(file_path, name)) for name in os.listdir(file_path)) + 1
    for i in range(1, count):
        # ファイルが存在したら消去.
        if os.path.exists("{file_path}/{i}/analyze 2.csv".format(file_path=file_path, i=i)):
            os.remove("{file_path}/{i}/analyze 2.csv".format(file_path=file_path, i=i))


def main():
    # file_paths = glob.glob("../math46_seed0/", recursive=True)
    # seedごとに処理を行う.
    # for i in range(10):
    #     p = pathlib.Path("/Users/haradakanon/Desktop/研究/実験データ/math85/math85_seed%d/"%(i))
    p = pathlib.Path("/Users/haradakanon/Desktop/研究/実験データ/research/math85_seed3")
    # clean(p)
    analyze_code(p)
    defects4j = pathlib.Path("./math85/java")
    analyze_element(p)
    get_point(p, defects4j, 3)


if __name__ == "__main__":
    main()
