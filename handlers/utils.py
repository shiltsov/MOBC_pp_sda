import re
import logging
import joblib

from pymystem3 import Mystem

vectorizer = [
    joblib.load("models/cv-ngram-13.bin"),
    joblib.load("models/tfidf-ngram-23.bin"),
]
clf = [
    joblib.load("models/lr-cv-ngram-13.bin"),
    joblib.load("models/lr-tfidf-ngram-23.bin"),
]

mystem_analyzer = Mystem()

label2name = {
    0: "А.Пушкин",
    1: "Д.Мамин-Сибиряк",
    2: "И.Тургенев",
    3: "А.Чехов",
    4: "Н.Гоголь",
    5: "И.Бунин",
    6: "А.Куприн",
    7: "А.Платонов",
    8: "В.Гаршин",
    9: "Ф.Достоевский",
}

writers = {
    "А.Пушкин": (
        "0.jpg",
        "<b>Алекса́ндр Серге́евич Пу́шкин</b> — русский поэт, драматург и прозаик, заложивший основы русского реалистического направления, литературный критик и теоретик литературы, историк, публицист, журналист. Один из самых авторитетных литературных деятелей первой трети XIX века",
    ),
    "Д.Мамин-Сибиряк": (
        "1.jpg",
        "<b>Дми́трий Нарки́сович Ма́мин-Сибиря́к</b> — русский писатель-прозаик и драматург",
    ),
    "И.Тургенев": (
        "2.jpg",
        "<b>Ива́н Серге́евич Турге́нев</b> — русский писатель-реалист, поэт, публицист, драматург, прозаик и переводчик. Один из классиков русской литературы, внёсших наиболее значительный вклад в её развитие во второй половине XIX века.",
    ),
    "А.Чехов": (
        "3.jpg",
        "<b>Анто́н Па́влович Че́хов</b> — русский писатель, прозаик, драматург, публицист, врач, общественный деятель в сфере благотворительности. Классик мировой литературы. Почётный академик Императорской академии наук по разряду изящной словесности.",
    ),
    "Н.Гоголь": (
        "4.jpg",
        "<b>Никола́й Васи́льевич Го́голь</b> — русский прозаик, драматург, критик, публицист, признанный одним из классиков русской литературы. Происходил из старинного малороссийского дворянского рода Гоголей-Яновских",
    ),
    "И.Бунин": (
        "5.jpg",
        "<b>Ива́н Алексе́евич Бу́нин</b> — русский писатель, поэт и переводчик, лауреат Нобелевской премии по литературе 1933 года. Будучи представителем обедневшей дворянской семьи, Бунин рано начал самостоятельную жизнь; в юношеские годы работал в газетах, канцеляриях, много странствовал",
    ),
    "А.Куприн": (
        "6.jpg",
        "<b>Алекса́ндр Ива́нович Купри́н</b> — русский писатель, переводчик",
    ),
    "А.Платонов": (
        "7.jpg",
        "<b>Андре́й Плато́нович Плато́нов</b> — русский советский писатель, поэт, публицист, драматург, сценарист, журналист, военный корреспондент и инженер. Участник Великой Отечественной войны",
    ),
    "В.Гаршин": (
        "8.jpg",
        "<b>Все́волод Миха́йлович Га́ршин</b> — русский писатель, поэт, художественный критик",
    ),
    "Ф.Достоевский": (
        "9.jpg",
        "<b>Фёдор Миха́йлович Достое́вский</b> — русский писатель, мыслитель, философ и публицист. Член-корреспондент Петербургской академии наук с 1877 года. Классик мировой литературы, по данным ЮНЕСКО, один из самых читаемых писателей в мире",
    ),
}


def clean_sentence(sentence):
    sentence = re.sub(r"[^а-яА-ЯёЁ \-\"!'(),.:;?]", "", sentence)
    return sentence


def make_punkt(sentence):
    repl = [
        (".", " POINT "),
        (",", " COMMA "),
        ("?", " QST "),
        ("!", " EXCL "),
        (":", " COLON "),
        (";", " SEMICOL "),
        (",", " DASH "),
    ]
    for p, r in repl:
        sentence = sentence.replace(p, r)
    sentence = re.sub(
        r"\s?-\s|\s-\s?", " DASH ", sentence
    )  # не трогать тире в слове (как-то)
    return sentence


def make_grams(sentence):
    morph = mystem_analyzer.analyze(sentence)

    ret = []
    for lex in morph:
        if lex["text"] in ["POINT", "COMMA", "QST", "EXCL", "COLON", "SEMICOL", "DASH"]:
            ret.append(lex["text"])
            continue

        try:
            if "analysis" in lex.keys() and "gr" in lex["analysis"][0].keys():
                ret.append(lex["analysis"][0]["gr"])
        except KeyError:
            logging.warning('wrong lex:', lex)
            continue
    return " ".join(ret)


def prepare_text(Text_corp):
    res = []
    for text in Text_corp:
        text = clean_sentence(text)
        text = make_punkt(text)
        text = make_grams(text)
        res.append(text)
    return res


def infer_one(text, model=0):
    X_infer = prepare_text([text])
    X_infer = vectorizer[model].transform(X_infer)
    predict_proba = clf[model].predict_proba(X_infer)
    logging.info("\n" + str(text) + "\n")
    logging.info(predict_proba)

    # выдадим список авторов и уверенностей по убыванию уверенности
    return sorted(
        zip(label2name.values(), predict_proba[0]), key=lambda x: x[1], reverse=True
    )


if __name__ == "__main__":
    print(infer_one("""успешный успех!"""))
