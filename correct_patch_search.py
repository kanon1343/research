import glob
import pathlib
import re
import pandas as pd
import os


def atoi(text):
    return int(text) if text.isdigit() else text

# 文字列を数値にソートするための変換.


def natural_keys(text):
    return [atoi(c) for c in re.split(r'(\d+)', text)]


def correct_patch_search(selection_file_path, file_path, project, seed, output_file_path):
    subdirectories_count = 0
    # サブディレクトリの数をカウント
    for name in os.listdir(file_path):
        if os.path.isdir(os.path.join(file_path, name)):
            subdirectories_count += 1

    with open(selection_file_path, 'r') as file:
        log = file.read()

    # Split the log into lines
    lines = log.split('\n')

    plausible_list = []
    output_list = []

    # ヘッダと最後の空行は除く.
    for line in lines:
        if line == 'name':
            continue
        if not line:
            continue
        plausible_list.append(line.split(' ')[0])
    for i in range(subdirectories_count+1):
        a = "seed{seed}/{i}".format(
            project=project, seed=seed, i=str(i))
        if i == 0:
            continue
        if a not in plausible_list:
            output_list.append(
                "seed{seed}/{i}".format(
                    project=project, seed=seed, i=str(i))
            )

    df = pd.DataFrame(sorted(output_list, key=natural_keys), columns=None)
    # CSVファイルに出力
    df.to_csv('{file_path}{seed}.csv'.format(
        file_path=output_file_path, seed=seed), index=False)


def summary(file_path):
    all_files = glob.glob(str(file_path) + "/correct*")
    # CSVファイルを読み込んでDataFrameとして結合
    df_list = []
    for file in all_files:
        if os.path.getsize(file) == 1:
            print(file)
            continue
        df = pd.read_csv(file)
        df_list.append(df)

    # DataFrameを連結（ヘッダーとインデックスを無視）
    combined_df = pd.concat(df_list)

    # ソートして出力.
    output_list = combined_df['0'].to_list()
    output_df = pd.DataFrame(
        sorted(output_list, key=natural_keys), columns=None)
    output_df.to_csv('{file_path}correct_summary'.format(
        file_path=file_path), index=False)


def main():
    # correct_patch_search
    projects = ["49", "80", "82"]
    for project in projects:
        for seed in range(10):
            selection_file_path = pathlib.Path(
                "/Users/haradakanon/Downloads/research/10010050/math{project}log/selection.csv".format(project=project))
            file_path = pathlib.Path(
                "/Users/haradakanon/Downloads/research/10010050/math{project}/seed{seed}".format(
                    project=project, seed=str(seed))
            )
            output_file_path = pathlib.Path(
                "/Users/haradakanon/Downloads/research/10010050/math{project}log/correct_patch".format(project=project))
            correct_patch_search(selection_file_path,
                                 file_path, project, seed, output_file_path)

    # summary
    projects = ["49", "80", "82"]
    for project in projects:
        file_path = pathlib.Path(
            "/Users/haradakanon/Downloads/research/10010050/math{project}log".format(
                project=project)
        )
        summary(file_path)


if __name__ == "__main__":
    main()
