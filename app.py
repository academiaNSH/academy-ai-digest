# -*- coding: utf-8 -*-
"""Нейродайджест — сайт с подборкой материалов про ИИ для новичков.

Запуск:
    pip install flask
    python app.py

После запуска открой в браузере http://127.0.0.1:5000
"""

from flask import Flask, render_template

from materials import CATEGORIES, MATERIALS
from issues import ISSUES
from typography import typograph_html

app = Flask(__name__)


@app.after_request
def apply_typography(response):
    """Расставляет неразрывные пробелы в готовом HTML перед отправкой."""
    if response.mimetype == "text/html":
        response.set_data(typograph_html(response.get_data(as_text=True)))
    return response


# Быстрый доступ к материалу по ссылке вида /material/chto-takoe-neyroset
MATERIALS_BY_ID = {item["id"]: item for item in MATERIALS}

# Порядок материалов: «Читать дальше» ведёт к следующим по списку.
MATERIAL_ORDER = {item["id"]: index for index, item in enumerate(MATERIALS)}


@app.route("/")
def index():
    """Главная страница: герой-блок и карточки материалов."""
    return render_template(
        "index.html",
        materials=MATERIALS,
        categories=CATEGORIES,
        issues=list(ISSUES.values()),
    )


@app.route("/material/<material_id>")
def material(material_id):
    """Отдельная страница материала."""
    item = MATERIALS_BY_ID.get(material_id)
    if item is None:
        return render_template("404.html"), 404

    start = MATERIAL_ORDER[material_id]
    others = [MATERIALS[(start + step) % len(MATERIALS)] for step in (1, 2, 3)]
    return render_template("material.html", item=item, others=others)


@app.route("/vypusk/<int:number>")
def vypusk(number):
    """Отдельная страница тематического выпуска (например, выпуск 2)."""
    issue = ISSUES.get(number)
    if issue is None:
        return render_template("404.html"), 404
    return render_template("vypusk.html", issue=issue)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
