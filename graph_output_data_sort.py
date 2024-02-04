import os
import pathlib
import re
from numpy import sort
import pandas as pd

# 正規表現を使用して時間の値を抽出して秒に変換


def convert_time_to_seconds(time_string):
    pattern = r'(\d+)\s*hours?\s*(\d+)\s*minutes?\s*(\d+)\s*seconds?'
    matches = re.match(pattern, time_string)

    if matches:
        hours = int(matches.group(1))
        minutes = int(matches.group(2))
        seconds = int(matches.group(3))

        total_seconds = (hours * 3600) + (minutes * 60) + seconds
        return total_seconds
    else:
        return 0  # エラー時は0秒として扱う


def parse_and_convert_time(time_string):
    if re.match(r'\d+\s*hours?\s*\d+\s*minutes?\s*\d+\s*seconds?', time_string):
        return convert_time_to_seconds(time_string)
    elif re.match(r'\d+\s*minutes?\s*\d+\s*seconds?', time_string):
        return convert_time_to_seconds("0 hours " + time_string)
    elif re.match(r'\d+\s*hours?\s*\d+\s*seconds?', time_string):
        return convert_time_to_seconds(time_string.split()[0] + " " + time_string.split()[1] + " 0 minutes " + time_string.split()[2] + " " + time_string.split()[3])
    elif re.match(r'\d+\s*seconds?', time_string):
        return convert_time_to_seconds("0 hours 0 minutes " + time_string)
    else:
        return 0


def merge_file(file_path, summarize_file_path):
    # ファイルが存在したら消去.
    if os.path.exists("{summarize_file_path}/merge.csv".format(summarize_file_path=summarize_file_path)):
        os.remove(
            "{summarize_file_path}/merge.csv".format(summarize_file_path=summarize_file_path))

    data = []
    # ファイルを開いてデータを読み込み、3つ目の時間の値でソート
    for i in range(10):
        # 出力ファイルのデータ読み込み.
        with open("{file_path}/seed{i}_summarize.csv".format(file_path=file_path, i=i), 'r') as file:
            log = file.read()
        # Split the log into lines
        lines = log.split('\n')

        # 正しい出力の時刻を取得する.
        for line in lines:
            if line.startswith(",") or not line:
                continue
            data.append(line.split(",")[1:])

    column = ["世代", "時間", "出力数", "前世代までの合計"]
    df = pd.DataFrame(data, columns=column)

    df.to_csv(
        "{summarize_file_path}/merge.csv".format(summarize_file_path=summarize_file_path))


def input_file(file_path, summarize_file_path):
    # ファイルが存在したら消去.
    if os.path.exists("{summarize_file_path}/sort.csv".format(summarize_file_path=summarize_file_path)):
        os.remove(
            "{summarize_file_path}/sort.csv".format(summarize_file_path=summarize_file_path))

    with open("{file_path}/merge.csv".format(file_path=file_path), 'r') as file:
        log = file.read()

    data = []
    # Split the log into lines
    lines = log.split('\n')
    sorted_data = []
    for line in lines:
        if line.startswith(","):
            continue
        if not line:
            continue
        data.append(line)
    sorted_data = sorted(
        data, key=lambda x: parse_and_convert_time(x.split(',')[2].strip()))

    column = ["", "世代", "時間", "出力数", "前世代までの合計"]
    output_data = [item.split(",") for item in sorted_data]
    df = pd.DataFrame(output_data, index=None, columns=column)
    df.to_csv(
        "{summarize_file_path}/sort.csv".format(summarize_file_path=summarize_file_path))
    # ファイルが存在したら消去.
    if os.path.exists("{summarize_file_path}/merge.csv".format(summarize_file_path=summarize_file_path)):
        os.remove(
            "{summarize_file_path}/merge.csv".format(summarize_file_path=summarize_file_path))


def count_output(file_path, summarize_file_path):
    with open("{file_path}/sort.csv".format(file_path=file_path), 'r') as file:
        log = file.read()

    count = 0
    data = []
    # Split the log into lines
    lines = log.split('\n')
    for line in lines:
        if line.startswith(","):
            continue
        if not line:
            continue
        count = count + int(line.split(',')[4])
        d = [parse_and_convert_time(line.split(',')[3].strip()), count]
        data.append(d)
    df = pd.DataFrame(data)
    df.to_csv(
        "{summarize_file_path}/output_summarize.csv".format(summarize_file_path=summarize_file_path))
    if os.path.exists("{summarize_file_path}/sort.csv".format(summarize_file_path=summarize_file_path)):
        os.remove(
            "{summarize_file_path}/sort.csv".format(summarize_file_path=summarize_file_path))


def main():
    options = ["505025", "10010050", "200200100"]
    projects = ["codec9"]
    for option in options:
        for project in projects:
            file_path = pathlib.Path(
                "/Users/haradakanon/Downloads/research/{option}/{project}log/".format(option=option, project=project))
            summarize_file_path = pathlib.Path(
                "/Users/haradakanon/Downloads/research/{option}/{project}log".format(option=option, project=project))
            merge_file(file_path, summarize_file_path)
            input_file(file_path, summarize_file_path)
            count_output(file_path, summarize_file_path)


if __name__ == "__main__":
    main()
