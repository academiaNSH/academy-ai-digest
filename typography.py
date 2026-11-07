# -*- coding: utf-8 -*-
"""Типографика для русского текста.

Главная задача — убрать висячие предлоги и союзы в конце строки, которые
особенно заметны на телефоне. Для этого после коротких слов ставится
неразрывный пробел: «в\u00A0классе» переносится целиком.

Правила простые и работают на любом тексте:
- короткие предлоги и союзы не отрываются от следующего слова;
- тире не начинает строку;
- число не отрывается от единицы измерения («30\u00A0секунд»);
- сокращения «т. д.», «т. п.», «2026 г.» не разрываются.
"""

import re

NBSP = "\u00A0"

SHORT_WORDS = (
    "в", "во", "на", "и", "а", "но", "с", "со", "к", "ко", "по", "у", "о", "об",
    "обо", "за", "из", "изо", "от", "ото", "до", "не", "ни", "же", "ли", "бы",
    "что", "как", "при", "для", "над", "под", "про", "без", "через", "между",
    "или", "либо", "то", "так", "вот", "даже", "уже", "ещё", "еще", "где",
    "когда", "если", "чем", "тем", "это", "этот", "эта", "эти", "его", "её",
    "ее", "их", "мы", "вы", "он", "она", "они", "оно", "нам", "вам", "вас",
    "нас", "мне", "меня", "себя", "около", "после", "перед", "среди", "кроме",
    "ради", "сквозь", "согласно",
)

UNITS = (
    "сек", "секунд", "секунды", "мин", "минут", "минуты", "час", "часа",
    "часов", "класс", "класса", "классе", "шаг", "шага", "шагов", "материал",
    "материала", "карточка", "карточки", "слайд", "слайда",
)

_words = "|".join(sorted((re.escape(word) for word in SHORT_WORDS), key=len, reverse=True))
_units = "|".join(UNITS)

RE_SHORT = re.compile(r"(?<![\w-])(%s)[ ]+" % _words, re.IGNORECASE)
RE_UNIT = re.compile(r"(\d)[ ]+(?=(?:%s)\b)" % _units, re.IGNORECASE)
RE_DASH = re.compile(r"[ \t]+—[ \t]*")
RE_ABBR = re.compile(r"\bт\.[ ]+([дпе])\.")
RE_YEAR = re.compile(r"(\d)[ ]+г\.")


def typograph(text):
    """Расставляет неразрывные пробелы в обычном тексте."""
    if not text:
        return text

    text = RE_DASH.sub(NBSP + "—" + NBSP, text)
    text = RE_SHORT.sub(lambda match: match.group(1) + NBSP, text)
    text = RE_UNIT.sub(lambda match: match.group(1) + NBSP, text)
    text = RE_ABBR.sub(lambda match: "т." + NBSP + match.group(1) + ".", text)
    text = RE_YEAR.sub(lambda match: match.group(1) + NBSP + "г.", text)
    return re.sub(r"[ ]{2,}", " ", text)


TAG_RE = re.compile(
    r"(<!--.*?-->|<script\b.*?</script\s*>|<style\b.*?</style\s*>|<[^>]+>)",
    re.DOTALL | re.IGNORECASE,
)


def typograph_html(html):
    """Обрабатывает только текст между тегами, не трогая разметку и скрипты."""
    parts = TAG_RE.split(html)
    for index in range(0, len(parts), 2):
        parts[index] = typograph(parts[index])
    return "".join(parts)
