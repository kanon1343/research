import difflib
import pathlib
import os
import pandas as pd


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


def main():
    for i in range(10):
        file_path = pathlib.Path(
            "/Users/haradakanon/Downloads/kGenProg-1.8.2/example/math78/seed{i}".format(i=i))
        summarize_file_path = pathlib.Path(
            "/Users/haradakanon/Downloads/kGenProg-1.8.2/example/math78")
        data = extract_generation_with_max_fitness(file_path)
        summarize(summarize_file_path, i, data)


if __name__ == "__main__":
    main()
