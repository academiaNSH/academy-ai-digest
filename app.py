# -*- coding: utf-8 -*-
"""Нейродайджест — сайт с подборкой материалов про ИИ для новичков.

Запуск:
    pip install flask
    python app.py

После запуска открой в браузере http://127.0.0.1:5000
"""

from flask import Flask, jsonify, render_template, request

from materials import CATEGORIES, MATERIALS
from issues import ISSUES

app = Flask(__name__)


# Быстрый доступ к материалу по ссылке вида /material/chto-takoe-neyroset
MATERIALS_BY_ID = {item["id"]: item for item in MATERIALS}

# Подписчики хранятся в памяти: для учебного проекта этого достаточно.
# При перезапуске сервера список обнулится — позже его можно заменить на базу данных.
SUBSCRIBERS = []
BASE_SUBSCRIBERS = 1247


@app.route("/")
def index():
    """Главная страница: герой-блок, карточки материалов и форма подписки."""
    return render_template(
        "index.html",
        materials=MATERIALS,
        categories=CATEGORIES,
        subscribers_count=format_count(BASE_SUBSCRIBERS + len(SUBSCRIBERS)),
        issues=list(ISSUES.values()),
    )


@app.route("/material/<material_id>")
def material(material_id):
    """Отдельная страница материала."""
    item = MATERIALS_BY_ID.get(material_id)
    if item is None:
        return render_template("404.html"), 404

    others = [m for m in MATERIALS if m["id"] != material_id][:3]
    return render_template("material.html", item=item, others=others)


@app.route("/vypusk/<int:number>")
def vypusk(number):
    """Отдельная страница тематического выпуска (например, выпуск 2)."""
    issue = ISSUES.get(number)
    if issue is None:
        return render_template("404.html"), 404
    return render_template("vypusk.html", issue=issue)


@app.route("/subscribe", methods=["POST"])
def subscribe():
    """Приём email из формы. Отвечаем JSON — его показывает JavaScript."""
    data = request.get_json(silent=True) or request.form
    email = (data.get("email") or "").strip()

    if not is_valid_email(email):
        return jsonify(ok=False, message="Похоже, в адресе ошибка. Проверь и попробуй снова."), 400

    if email.lower() in [item.lower() for item in SUBSCRIBERS]:
        return jsonify(ok=True, message="Этот адрес уже в списке — дайджест приходит раз в месяц.")

    SUBSCRIBERS.append(email)
    return jsonify(ok=True, message="Готово! Первый выпуск придёт в начале следующего месяца.")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


def is_valid_email(email):
    """Простая проверка адреса без регулярных выражений — чтобы было понятно новичку."""
    if len(email) < 5 or email.count("@") != 1:
        return False
    login, domain = email.split("@")
    return bool(login) and "." in domain and not domain.startswith(".") and not domain.endswith(".")


def format_count(number):
    """1247 -> '1 247' — так число читается легче."""
    return f"{number:,}".replace(",", " ")


if __name__ == "__main__":
    app.run(debug=True)
