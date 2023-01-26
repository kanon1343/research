
import pathlib
import os
import glob
import pprint
import matplotlib.pyplot as plt
import japanize_matplotlib  

def get_contents(file_path):
    # 出力ごとに処理を行う.
    file_paths = glob.glob("{file_path}/**/".format(file_path=file_path), recursive=True)
    dicts = {}
    
    for outputDir in file_paths:
        # diffでの"+""-"の合計を計算し、辞書に登録.
        diffs = glob.glob("{outputDir}/*.diff".format(outputDir=outputDir), recursive=True)
        count = 0
        outputNumber = 0
        for diff in diffs:
            subDirname = os.path.basename(os.path.dirname(diff)) # パス文字列の出力番号部分の摘出.
            number = subDirname.split() # 出力番号.
            outputNumber = int(number[0])
            with open(diff) as d:
                for line in d:
                    if line.startswith("- "):
                        count += 1
                    else:
                        if line.startswith("+") and not(line.startswith("+++")):
                            count += 1
        if not outputNumber in dicts:
            dicts[outputNumber] = list()
        dicts[outputNumber].append(count)

    #ソートしてグラフを書く.
    sorted(dicts.items())
    dicts = sorted(dicts.items())
    dicts = dict((x, y) for x, y in dicts)
    drawGraph(dicts)
    


    
def drawGraph(dicts):
    x = dicts.keys()
    y = dicts.values()
    plt.title("seed0")
    plt.plot(x, y)
    plt.savefig("seed0.png")
    # plt.show()
    


def main():
    # file_paths = glob.glob("../math46_seed0/", recursive=True)
    # seedごとに処理を行う.
    # for file_path in file_paths:
    p = pathlib.Path("/Users/haradakanon/Desktop/研究/実験データ/math49//math49_seed0/")
    get_contents(file_path=p.resolve())

if __name__ == "__main__":
    main()