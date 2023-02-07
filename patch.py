import pathlib
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib  
import subprocess
import csv
import pandas as pd

def get_contents(num, file_path):
    # 出力ごとに処理を行う.
    file_paths = glob.glob("{file_path}/**/".format(file_path=file_path), recursive=True)
    dicts = {}
    for output_dir in file_paths:
        # diffでの"+""-"の合計を計算し、辞書に登録.
        diffs = glob.glob("{output_dir}/*.diff".format(output_dir=output_dir), recursive=True)
        count = 0
        output_number = 0
        for diff in diffs:
            sub_dirname = os.path.basename(os.path.dirname(diff)) # パス文字列の出力番号部分の摘出.
            number = sub_dirname.split() # 出力番号.
            output_number = int(number[0])
            with open(diff) as d:
                for line in d:
                    if line.startswith("- "):
                        count += 1
                    else:
                        if line.startswith("+") and not(line.startswith("+++")):
                            count += 1
        if not output_number in dicts:
            dicts[output_number] = list()
        dicts[output_number].append(count)

    #ソートしてグラフを書く.
    sorted(dicts.items())
    dicts = sorted(dicts.items())
    dicts = dict((x, y) for x, y in dicts)
    draw_graph(dicts, num)
    
# グラフを書く
def draw_graph(dicts: dict, num):
    plt.figure()
    x = dicts.keys()
    y = dicts.values()
    plt.title("seed%d"%(num))
    plt.xticks(np.arange(0, 100, step=5))
    plt.plot(x, y)
    plt.savefig("seed%d.png"%(num))
    plt.show()
    

# lizardで分析し、csvファイルを出力.
def analyze_code(num, file_path):
    count = sum(os.path.isdir(os.path.join(file_path, name)) for name in os.listdir(file_path)) + 1
    print(count-1)
    for i in range(1,count):
        # ファイルが存在したら消去.
        if os.path.exists("{file_path}/{i}/analyze.csv".format(file_path=file_path, i=i)):
            os.remove("{file_path}/{i}/analyze.csv".format(file_path=file_path, i=i))

        subprocess.run("lizard {file_path}/{i}/ -l java --csv >> {file_path}/{i}/analyze.csv".format(file_path=file_path, i=i), shell=True)
        header = ["nloc","ccn","token_count","parameter_count","length","location","filepath","method_name","method_long_name","start_line","end_line"]
        df = pd.read_csv("{file_path}/{i}/analyze.csv".format(file_path=file_path, i=i), names=header)
        df.to_csv("{file_path}/{i}/analyze.csv".format(file_path=file_path, i=i))
    print("{file_path} is complete!".format(file_path=file_path))
    analyze_element(num, file_path, count)


# defects4j分析用.
def analyze_defects4j(file_path):
    if os.path.exists("{file_path}/analyze.csv".format(file_path=file_path)):
        os.remove("{file_path}/analyze.csv".format(file_path=file_path))

    subprocess.run("lizard {file_path}/ -l java --csv >> {file_path}/analyze.csv".format(file_path=file_path), shell=True)
    header = ["nloc","ccn","token_count","parameter_count","length","location","filepath","method_name","method_long_name","start_line","end_line"]
    df = pd.read_csv("{file_path}/analyze.csv".format(file_path=file_path), names=header)
    df.to_csv("{file_path}/analyze.csv".format(file_path=file_path))


# defects4j分析結果の合計と名前簡略化の出力.
def sum_file_metrics(file_path):
    df = pd.read_csv("{file_path}/analyze.csv".format(file_path=file_path))
    df_metrics = pd.DataFrame(columns=["nloc", "ccn", "token", "parameter", "length", "filename"])
    nloc = 0
    ccn = 0
    token = 0
    parameter = 0
    length = 0
    file_name = ""
    for i in range(len(df) - 1):
        # メトリクスの合計を取得.
        file_name = df.iat[i,7]
        if file_name == df.iat[i+1,7]:
            nloc += df.iat[i,1]
            ccn += df.iat[i,2]
            token += df.iat[i,3]
            parameter += df.iat[i,4]
            length += df.iat[i,5]
        else:
            nloc += df.iat[i,1]
            ccn += df.iat[i,2]
            token += df.iat[i,3]
            parameter += df.iat[i,4]
            length += df.iat[i,5]
            # ファイル名を取得(org.apache.~~.java).
            file_name = file_name.split("/", 3)
            file_name = file_name[3].replace("/", ".")
            dicts = {"nloc":nloc, "ccn":ccn, "token":token, "parameter":parameter, "length":length, "filename":file_name}
            s = pd.DataFrame(dicts, index=[0])
            nloc = 0
            ccn = 0
            token = 0
            parameter = 0
            length = 0
            df_metrics = pd.concat([df_metrics, s])
    # 最終行の計算.
    nloc += df.iat[i+1,1]
    ccn += df.iat[i+1,2]
    token += df.iat[i+1,3]
    parameter += df.iat[i+1,4]
    length += df.iat[i+1,5]
    file_name = file_name.split("/", 3)
    file_name = file_name[3].replace("/", ".")
    dicts = {"nloc":nloc, "ccn":ccn, "token":token, "parameter":parameter, "length":length, "filename":file_name}
    s = pd.DataFrame(dicts, index=[0])
    df_metrics = pd.concat([df_metrics, s])

    # csvファイルへ出力
    df_metrics.to_csv("{file_path}/metrics.csv".format(file_path=file_path))





# 各要素の比較
def analyze_element(num, file_path, count):
    dicts = {}
    for i in range(1, count):
        df = pd.read_csv("{file_path}/{i}/analyze.csv".format(file_path=file_path, i=i))
        sum = df["ccn"].sum()
        if not i in dicts:
            dicts[i] = list()
        dicts[i].append(sum)
    sorted(dicts.items())
    dicts = sorted(dicts.items())
    dicts = dict((x, y) for x, y in dicts)
    print(dicts)
    draw_graph(dicts, num)
    



def main():
    # file_paths = glob.glob("../math46_seed0/", recursive=True)
    # seedごとに処理を行う.
    for i in range(10):
        p = pathlib.Path("/Users/haradakanon/Desktop/研究/実験データ/math85/math85_seed%d/"%(i))
        # get_contents(i, file_path=p.resolve())
        # analyze_code(i, p)
    defects4j = pathlib.Path("./math85/src/java")
    # analyze_defects4j(defects4j)
    # sum_file_metrics(defects4j)


if __name__ == "__main__":
    main()