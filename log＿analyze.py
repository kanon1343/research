import difflib
import pathlib
import os
import subprocess
import pandas as pd
import re


def extract_generation_with_max_fitness(file_path):
    with open(file_path, 'r') as file:
        log = file.read()

    # Split the log into lines
    lines = log.split('\n')

    data = []
    count = 0

    # Iterate over the lines
    for line in lines:
        # Check if the line contains the "entered the era" information
        if "entered the era" in line:
            generation = line.split(' ')[-2]  # Extract the generation number
        # Check if the line contains the max fitness information
        if "Fitness: max 1(" in line:
            fitness_generation = generation
            output = line.split('(')[1].split(')')[0]
            # print(fitness_generation, output, count)
            d = [fitness_generation, output, count]
            data.append(d)
            count = count + int(output)

        if "GA stopped" in line:
            break
    return data


def summarize(file_path, i, data):
    # ファイルが存在したら消去.
    if os.path.exists("{file_path}/seed{i}_summarize.csv".format(file_path=file_path, i=i)):
        os.remove(
            "{file_path}/seed{i}_summarize.csv".format(file_path=file_path, i=i))

    column = ["世代", "出力数", "前世代までの合計"]
    df = pd.DataFrame(data, columns=column)

    df.to_csv(
        "{file_path}/seed{i}_summarize.csv".format(file_path=file_path, i=i))


def atoi(text):
    return int(text) if text.isdigit() else text

# 文字列を数値にソートするための変換.


def natural_keys(text):
    return [atoi(c) for c in re.split(r'(\d+)', text)]


def selected(file_path):
    with open(file_path, 'r') as file:
        input_data = file.read()
    # 入力データを行ごとに分割してリストに格納
    data_list = input_data.strip().split('\n')

    # ファイルパス部分を抽出してリストに格納
    select_list = [line.split()[0].split('/', 2)[2] for line in data_list]
    output_list = set(select_list)

    # ソートをしてリストをデータフレームに変換
    df = pd.DataFrame(sorted(output_list, key=natural_keys), columns=['name'])

    # CSVファイルに出力
    df.to_csv('{file_path}.csv'.format(
        file_path=file_path), index=False)


def main():
    # for i in range(10):
    #     file_path = pathlib.Path(
    #         "/Users/haradakanon/Downloads/kGenProg-1.8.2/example/math78/seed{i}".format(i=i))
    #     summarize_file_path = pathlib.Path(
    #         "/Users/haradakanon/Downloads/kGenProg-1.8.2/example/math78")
    #     data = extract_generation_with_max_fitness(file_path)
    #     summarize(summarize_file_path, i, data)
    file_path = pathlib.Path(
        "/Users/haradakanon/Downloads/research/200200100/math466log/selection")
    selected(file_path)
    file_path = pathlib.Path(
        "/Users/haradakanon/Downloads/research/200200100/math72log/selection")
    selected(file_path)


if __name__ == "__main__":
    main()
