import pathlib


def remove_lines_with_keyword(input_file, output_file, keyword1, keyword2):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # "OpenIntToDoubleHashMap"を含まない行だけを新しいリストに格納
    new_lines = []
    for line in lines:
        if keyword1 in line and keyword2 in line:
            continue
        new_lines.append(line)

    with open(output_file, 'w') as file:
        file.writelines(new_lines)


def main():
    projects = ["49", "82"]
    for project in projects:
        input_file_path = pathlib.Path(
            "/Users/haradakanon/Downloads/research/200200100/math{project}log/selection".format(
                project=project)
        )
        output_file_path = pathlib.Path("/Users/haradakanon/Downloads/research/200200100/math{project}log/selection".format(
            project=project))
        keyword1 = "OpenIntToDoubleHashMap"
        keyword2 = "Empty while statement"
        remove_lines_with_keyword(
            input_file_path, output_file_path, keyword1, keyword2)


if __name__ == "__main__":
    main()
