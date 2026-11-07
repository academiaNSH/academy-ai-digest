# -*- coding: utf-8 -*-
"""Сборка статической версии сайта для GitHub Pages.

Flask-версия остаётся основной, а здесь те же шаблоны рендерятся в обычные
HTML-файлы: GitHub Pages умеет отдавать только статику, без Python.

Запуск:
    python build_static.py

Результат — папка docs/, её и публикует GitHub Pages.
"""

import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from materials import CATEGORIES, MATERIALS
from issues import ISSUES

ROOT = Path(__file__).parent
TEMPLATES = ROOT / "templates"
STATIC = ROOT / "static"
OUT = ROOT / "docs"

BASE_SUBSCRIBERS = 1247


def format_count(number):
    """1247 -> '1 247' — так же, как на серверной версии."""
    return f"{number:,}".replace(",", " ")


def url_for(endpoint, **values):
    """Повторяет Flask url_for, но возвращает пути к статическим файлам.

    Все страницы лежат в одной папке, поэтому ссылки относительные
    и работают и на GitHub Pages, и при открытии docs/index.html с диска.
    """
    if endpoint == "static":
        return f"static/{values['filename']}"
    if endpoint == "index":
        return "index.html"
    if endpoint == "material":
        return f"material-{values['material_id']}.html"
    if endpoint == "vypusk":
        return f"vypusk-{values['number']}.html"
    if endpoint == "subscribe":
        return "#subscribe"
    raise ValueError(f"Неизвестный маршрут: {endpoint}")


def render(env, template_name, **context):
    """Рендерит шаблон с нашим url_for и пометкой статической версии."""
    template = env.get_template(template_name)
    return template.render(url_for=url_for, static_version=True, **context)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "static").mkdir(parents=True)

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        autoescape=select_autoescape(["html"]),
    )

    pages = {
        "index.html": render(
            env,
            "index.html",
            materials=MATERIALS,
            categories=CATEGORIES,
            subscribers_count=format_count(BASE_SUBSCRIBERS),
            issues=list(ISSUES.values()),
        ),
        "404.html": render(env, "404.html"),
    }

    for item in MATERIALS:
        others = [m for m in MATERIALS if m["id"] != item["id"]][:3]
        pages[f"material-{item['id']}.html"] = render(
            env, "material.html", item=item, others=others
        )

    for number, issue in ISSUES.items():
        pages[f"vypusk-{number}.html"] = render(env, "vypusk.html", issue=issue)

    for name, html in pages.items():
        (OUT / name).write_text(html, encoding="utf-8")

    shutil.copytree(STATIC, OUT / "static", dirs_exist_ok=True)

    # Без этого файла GitHub Pages прогоняет сайт через Jekyll — нам это не нужно.
    (OUT / ".nojekyll").touch()

    print(f"Готово: {len(pages)} страниц в {OUT}")


if __name__ == "__main__":
    main()
