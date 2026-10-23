import csv

all_data = []
with open("Corp_Summary.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=';')
    all_data = list(reader)


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

    for el, values in summary.items():
        summary[el]["avg_salary"] = summary[el].pop("sum_salary")
        summary[el]["avg_salary"] = summary[el]["avg_salary"] / summary[el]["number_of_employees"]
    return summary


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


def report(number):
    if type(number) is not int:
        raise TypeError()
    if number == 1:
        result = hierarchy_report(all_data)
        return result
    elif number == 2:
        result = departmental_summary(all_data)
        return result
    elif number == 3:
        save_departmental_summary_to_csv(
            departmental_summary(all_data),
            "departmental_summary.csv"
        )
    else:
        print("Неизвестная команда")
