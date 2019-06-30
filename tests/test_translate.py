from src import translate


def test_translate():
    assert translate.translate("hello", "text", "en", "he") == "שלום"
