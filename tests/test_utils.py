import pytest

from handlers.utils import (
    clean_sentence,
    make_punkt,
    make_grams,
    prepare_text,
    infer_one,
)


def test_clean_sentence():
    assert clean_sentence("Яблоки na snegu !") == "Яблоки   !"
    assert clean_sentence("Ёклмн, xyz:~!") == "Ёклмн, :!"


def test_make_punkt():
    assert (
        make_punkt("Вот видишь: лето, ОСЕНЬ! '!?'")
        == "Вот видишь COLON  лето COMMA  ОСЕНЬ EXCL  ' EXCL  QST '"
    )
    assert make_punkt("Ёклмн, xyz:~!") == "Ёклмн COMMA  xyz COLON ~ EXCL "


def test_make_grams():
    assert (
        make_grams("мама; мыла раму")
        == "S,жен,од=им,ед V,несов,пе=прош,ед,изъяв,жен S,жен,неод=вин,ед"
    )
    assert (
        make_grams("успешный успех!")
        == "A=(вин,ед,полн,муж,неод|им,ед,полн,муж) S,муж,неод=(вин,ед|им,ед)"
    )


def test_prepare_text():
    assert prepare_text(["карандаш."]) == ["S,муж,неод=(вин,ед|им,ед) POINT"]
    assert prepare_text(["успешный успех!", "после?"]) == [
        "A=(вин,ед,полн,муж,неод|им,ед,полн,муж) S,муж,неод=(вин,ед|им,ед) EXCL",
        "ADV= QST",
    ]


def test_infer_one():
    assert infer_one("карандаш.") == [
        ("А.Чехов", 0.22629146704570768),
        ("А.Платонов", 0.14694909343770282),
        ("Д.Мамин-Сибиряк", 0.12716072355566999),
        ("В.Гаршин", 0.1201160299561439),
        ("А.Куприн", 0.10095365259508952),
        ("А.Пушкин", 0.06889427311216254),
        ("И.Бунин", 0.0627789217420879),
        ("Н.Гоголь", 0.053364446576640315),
        ("И.Тургенев", 0.04773725833569127),
        ("Ф.Достоевский", 0.04575413364310402),
    ]
    assert infer_one("успешный успех!") == [
        ("А.Чехов", 0.2299396933747943),
        ("И.Бунин", 0.1616885550481674),
        ("А.Платонов", 0.14667316858237012),
        ("Н.Гоголь", 0.10082455802845604),
        ("А.Куприн", 0.09728042240275225),
        ("И.Тургенев", 0.06386016726450419),
        ("Д.Мамин-Сибиряк", 0.05993011617876628),
        ("Ф.Достоевский", 0.05262543189595764),
        ("В.Гаршин", 0.04555240250402153),
        ("А.Пушкин", 0.04162548472021019),
    ]
