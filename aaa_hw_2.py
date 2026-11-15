import csv

INPUT_FILE = "Corp_Summary.csv"
OUTPUT_FILE = "departmental_summary.csv"


def read_csv_file(filepath=INPUT_FILE):
    with open(filepath, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=";")
        return list(reader)


def hierarchy_report(data):
    hierarchy = {}

    for row in data[1:]:
        department = row[1]
        division = row[2]
        post = row[3]

        if department not in hierarchy:
            hierarchy[department] = {}

        if division not in hierarchy[department]:
            hierarchy[department][division] = set()

        hierarchy[department][division].add(post)

    return hierarchy


def print_hierarchy(hierarchy):
    for department, divisions in sorted(hierarchy.items()):
        print(f"{department}:")
        for division, posts in sorted(divisions.items()):
            posts_str = ", ".join(sorted(posts))
            print(f"  - {division}: {posts_str}")


def departmental_summary(data):
    summary = {}
    for row in data[1:]:
        department = row[1]
        salary = float(row[-1])
        if department not in summary:
            summary[department] = {"number_of_employees": 0,
                                   "min_salary": salary,
                                   "max_salary": salary,
                                   "sum_salary": 0.0}
        summary[department]["number_of_employees"] += 1
        summary[department]["sum_salary"] += salary
        if summary[department]["min_salary"] > salary:
            summary[department]["min_salary"] = salary
        if summary[department]["max_salary"] < salary:
            summary[department]["max_salary"] = salary

    for values in summary.values():
        values["avg_salary"] = values.pop("sum_salary")
        values["avg_salary"] = values["avg_salary"] / values["number_of_employees"]
    return summary


def print_departmental_summary(summary):
    for department, values in summary.items():
        employees = values["number_of_employees"]
        min_sal = values["min_salary"]
        max_sal = values["max_salary"]
        avg_sal = values["avg_salary"]
        print(
            f"{department}: сотрудников — {employees}, "
            f"мин. зарплата — {min_sal:.2f}, "
            f"макс. зарплата — {max_sal:.2f}, "
            f"средняя зарплата — {avg_sal:.2f}"
        )


def save_departmental_summary_to_csv(summary_data, filename):
    with open(filename, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=";")

        writer.writerow([
            "Департамент",
            "Количество сотрудников",
            "Минимальная зарплата",
            "Максимальная зарплата",
            "Средняя зарплата"
        ])

        for department, values in summary_data.items():
            writer.writerow([
                department,
                values["number_of_employees"],
                values["min_salary"],
                values["max_salary"],
                values["avg_salary"]
            ])


def report(number, input_file=INPUT_FILE, output_file=OUTPUT_FILE):
    if type(number) is not int:
        raise TypeError()

    data = read_csv_file(input_file)

    if number == 1:
        hierarchy = hierarchy_report(data)
        print_hierarchy(hierarchy)
    elif number == 2:
        summary = departmental_summary(data)
        print_departmental_summary(summary)
    elif number == 3:
        summary = departmental_summary(data)
        save_departmental_summary_to_csv(summary, output_file)
        print(f"Отчёт сохранён в файл {output_file}")
    else:
        print("Неизвестная команда")


if __name__ == "__main__":
    choice = input(
        "Выберите вариант отчёта:\n"
        "1 — Иерархия для каждого департамента\n"
        "2 — Сводка по департаментам\n"
        "3 — Сохранить сводку по департаментам в CSV\n"
    )
    if choice.isdigit():
        report(int(choice))
    else:
        print("Ошибка: нужно ввести целое число от 1 до 3.")
