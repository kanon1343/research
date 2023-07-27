import os
import csv


def detect_consecutive_duplicate_lines(program):
    lines = program.strip().split('\n')
    consecutive_duplicates = []
    prev_line = None  # 前の行を格納する変数

    for line in lines:
        # 統合差分形式の指示子とコメント行、および-で始まる行を重複チェックから除外
        if line.startswith(('+++', '---', '@@', '//')):
            continue
        # 空白を除いた行を重複チェックの対象とする
        cleaned_line = line.strip().replace(" ", "").replace("\t", "")
        if not cleaned_line:  # 空行をスキップ
            continue

        if cleaned_line.startswith("-"):  # マイナス行スキップ
            continue

        if cleaned_line.startswith("+"):  # プラスは""に置き換え.
            cleaned_line = cleaned_line.replace("+", "", 1)

        # 波括弧など特定の文字が含まれている行は重複としない
        # また、空行も重複とみなさない
        if "{" in cleaned_line or "}" in cleaned_line or not cleaned_line:
            prev_line = None
            continue

        if prev_line == cleaned_line:
            # 前の行と同じ場合は連続している重複行として追加
            if cleaned_line not in consecutive_duplicates:
                consecutive_duplicates.append(cleaned_line)
        prev_line = cleaned_line

    return consecutive_duplicates


def search_java_files(folder_path):
    java_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".diff"):
                java_file_path = os.path.join(root, file)
                java_files.append(java_file_path)
    return java_files


def main():
    # 対象のフォルダパスを指定してください
    folder_path = "/Users/haradakanon/Downloads/research/被験者実験データ/math85(出力)"
    java_files = search_java_files(folder_path)

    # CSVファイルに結果を出力
    output_csv_file = "/Users/haradakanon/Downloads/research/被験者実験データ/math85(出力)/duplicate_lines_report.csv"
    with open(output_csv_file, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["File Path"])

        for java_file in java_files:
            with open(java_file, "r") as file:
                program = file.read()

            has_consecutive_duplicates = detect_consecutive_duplicate_lines(
                program)
            if has_consecutive_duplicates:
                writer.writerow([java_file])

    # print(f"CSVファイル {output_csv_file} に結果を出力しました。")


if __name__ == "__main__":
    main()
