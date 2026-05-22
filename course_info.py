import csv
import os
from html import escape

from flask import Flask, request

app = Flask(__name__)
app.json.ensure_ascii = False

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
FILES = {
    "hw-01": "hw_01.csv",
    "hw-02": "hw_02.csv",
}

def read_table(file_name: str) -> list[dict[str, str]]:
    rows = []
    path = os.path.join(ROOT_DIR, file_name)
    with open(path, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["name"] != "":
                rows.append(row)
    return rows

def load_tables() -> dict[str, list[dict[str, str]]]:
    tables = {}
    for hw_name in FILES:
        tables[hw_name] = read_table(FILES[hw_name])
    return tables

TABLES = load_tables()

def get_score(row: dict[str, str]) -> float:
    if row["score"] == "":
        return 0.0
    return float(row["score"])

def make_mean(numbers: list[float]) -> float | None:
    if len(numbers) == 0:
        return None
    return round(sum(numbers) / len(numbers), 2)

def get_scores(hw_name: str, group_id: str = "") -> list[float] | None:
    if hw_name not in TABLES:
        return None
    scores = []
    for row in TABLES[hw_name]:
        if group_id == "" or row["group_id"] == group_id:
            scores.append(get_score(row))
    return scores

def score_to_mark(score: float) -> int:
    if score >= 50:
        return 5
    if score >= 30:
        return 4
    if score >= 1:
        return 3
    return 2

def error(message: str) -> tuple[dict[str, str], int]:
    return {"статус": "ошибка", "сообщение": message}, 400

@app.route("/names")
def names() -> dict[str, list[str]]:
    names_list = []
    for hw_name in TABLES:
        for row in TABLES[hw_name]:
            if row["name"] not in names_list:
                names_list.append(row["name"])
    return {"имена": names_list}

@app.route("/<hw_name>/mean_score")
def mean_score_for_hw(hw_name: str) -> dict[str, float] | tuple[dict[str, str], int]:
    scores = get_scores(hw_name)
    if scores is None:
        return error("нет такой домашки")
    result = make_mean(scores)
    if result is None:
        return error("пустая таблица")
    return {"средний балл": result}

@app.route("/<hw_name>/<group_id>/mean_score")
def mean_score_for_group(hw_name: str, group_id: str) -> dict[str, float] | tuple[dict[str, str], int]:
    scores = get_scores(hw_name, group_id)
    if scores is None:
        return error("нет такой домашки")
    result = make_mean(scores)
    if result is None:
        return error("нет такой группы")
    return {"средний балл": result}

@app.route("/mean_score")
@app.route("/mean_score/")
def mean_score_from_args() -> dict[str, float] | tuple[dict[str, str], int]:
    hw_name = request.args.get("hw_name", "")
    group_id = request.args.get("group_id", "")
    if hw_name == "" or group_id == "":
        return error("нужны hw_name и group_id")
    scores = get_scores(hw_name, group_id)
    if scores is None:
        return error("нет такой домашки")
    result = make_mean(scores)
    if result is None:
        return error("нет такой группы")
    return {"средний балл": result}

@app.route("/mark")
@app.route("/mark/")
def mark() -> dict[str, int | float] | tuple[dict[str, str], int]:
    student_name = request.args.get("student_name")
    group_id = request.args.get("group_id")
    if student_name is None and group_id is None:
        return error("нужно student_name или group_id")
    if student_name is not None and group_id is not None:
        return error("нужен только один параметр")
    if student_name is not None:
        for row in TABLES["hw-02"]:
            if row["name"] == student_name:
                return {"оценка": score_to_mark(get_score(row))}
        return error("нет такого студента")
    marks = []
    for row in TABLES["hw-02"]:
        if row["group_id"] == group_id:
            marks.append(score_to_mark(get_score(row)))
    result = make_mean(marks)
    if result is None:
        return error("нет такой группы")
    return {"средняя оценка": result}

@app.route("/course_table")
@app.route("/course_table/")
def course_table() -> str | tuple[dict[str, str], int]:
    hw_name = request.args.get("hw_name", "")
    group_id = request.args.get("group_id", "")
    if hw_name == "":
        return error("нужен hw_name")
    if hw_name not in TABLES:
        return error("нет такой домашки")
    html = ["<table border='1'>"]
    html.append("<tr><th>ФИ</th><th>Группа</th><th>Ссылка на MR</th><th>Баллы</th></tr>")
    count = 0
    for row in TABLES[hw_name]:
        if group_id == "" or row["group_id"] == group_id:
            count += 1
            html.append("<tr>")
            html.append("<td>" + escape(row["name"]) + "</td>")
            html.append("<td>" + escape(row["group_id"]) + "</td>")
            html.append("<td>" + escape(row["mr"]) + "</td>")
            html.append("<td>" + escape(row["score"]) + "</td>")
            html.append("</tr>")
    if count == 0:
        return error("нет такой группы")
    html.append("</table>")
    return "\n".join(html)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=1337)
