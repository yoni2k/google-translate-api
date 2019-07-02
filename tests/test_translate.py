import pytest
import json
import os
import sys
import requests
from src.translate import GoogleTranslate

test_file_path_settings = "./test_settings.json"
test_file_path_token = "./test_token.json"
test_file_input = "./test_input.json"

test_user_input_input = "Hi"


@pytest.fixture()
def input_from_str(request):
    orig_stdin = sys.stdin

    with open(test_file_input, 'w') as input_file_to_write:
        input_file_to_write.write(test_user_input_input)

    input_file_to_read = open(test_file_input, "r")
    sys.stdin = input_file_to_read

    def return_stdin():
        sys.stdin = orig_stdin
        input_file_to_read.close()
        os.remove(test_file_input)
    request.addfinalizer(return_stdin)


@pytest.fixture
def test_file_settings(request):
    def delete_test_settings_file():
        os.remove(test_file_path_settings)
    request.addfinalizer(delete_test_settings_file)


@pytest.fixture
def test_file_token(request):
    def delete_test_token_file():
        os.remove(test_file_path_token)
    request.addfinalizer(delete_test_token_file)


def create_test_settings_file_from_dic(dic):
    with open(test_file_path_settings, 'w') as settings_file:
        json.dump(dic, settings_file)


def create_test_settings_file(token_file_path, translate_string_source, string_to_translate_source_file):
    dic = {}
    if token_file_path:
        dic[GoogleTranslate.SettingNames.name_token_file_path] = token_file_path
    if translate_string_source:
        dic[GoogleTranslate.SettingNames.name_translate_string_source] = translate_string_source
    if string_to_translate_source_file:
        dic[GoogleTranslate.SettingNames.name_string_to_translate_source_file] = string_to_translate_source_file

    create_test_settings_file_from_dic(dic)


def test_success_no_assert():
    tranl_object = GoogleTranslate("../resources/settings.json")
    tranl_object.translate("hello", "he", "en", "text")


def test_translate_string_given():
    tranl_object = GoogleTranslate("../resources/settings.json")
    assert tranl_object.translate("hello", "he", "en", "text") == "שלום"


def test_translate_string_from_file():
    tranl_object = GoogleTranslate("../resources/settings.json")
    assert tranl_object.translate(None, "he", "en", "text") == "שלום עולם"


def test_translate_hebrew_to_english():
    tranl_object = GoogleTranslate("../resources/settings.json")
    assert tranl_object.translate("שלום", "en", "he", "text") == "Hello"


def test_undefined_settings_path():
    with pytest.raises(FileNotFoundError, match="settings"):
        GoogleTranslate("../resources/settings_invalid.json")


def test_invalid_token_file(test_file_settings):
    create_test_settings_file("../resources/token_invalid.txt", "file", "Hi")
    with pytest.raises(FileNotFoundError, match="token"):
        GoogleTranslate(test_file_path_settings)


def test_invalid_string_source(test_file_settings):
    create_test_settings_file("../resources/token.txt", "invalid_source", "Hi")
    with pytest.raises(ValueError, match=GoogleTranslate.SettingNames.name_translate_string_source):
        GoogleTranslate(test_file_path_settings)


def test_missing_string_in_settings(test_file_settings):
    create_test_settings_file("../resources/token.txt", "file", None)
    with pytest.raises(KeyError, match=GoogleTranslate.SettingNames.name_string_to_translate_source_file):
        GoogleTranslate(test_file_path_settings)


def test_missing_user_input_test_giving_string_no_string_in_file(test_file_settings):
    create_test_settings_file("../resources/token.txt", "user_input", None)
    tranl_object = GoogleTranslate(test_file_path_settings)
    assert tranl_object.translate("hello", "he", "en", "text") == "שלום"


def test_missing_user_input_test_giving_string_with_string_in_file(test_file_settings):
    create_test_settings_file("../resources/token.txt", "user_input", "Hi")
    tranl_object = GoogleTranslate(test_file_path_settings)
    assert tranl_object.translate("hello", "he", "en", "text") == "שלום"


def test_invalid_token(test_file_token):
    create_test_settings_file(test_file_path_token, "file", "Hi")
    with open(test_file_path_token, "w") as token_file:
        token_file.write("InvalidToken")

    tranl_object = GoogleTranslate(test_file_path_settings)
    with pytest.raises(requests.exceptions.HTTPError, match=r"401"):
        tranl_object.translate("Hello", "he", "en", "text")


def test_token_file_multiple_lines(test_file_token, test_file_settings):
    create_test_settings_file(test_file_path_token, "file", "Hi")
    with open(test_file_path_token, "w") as token_file:
        token_file.write("InvalidToken\n")
        token_file.write("InvalidToken2")

    with pytest.raises(ValueError, match=r"There are more than 1 lines in token file"):
        GoogleTranslate(test_file_path_settings)


def test_user_input(test_file_settings, input_from_str):
    create_test_settings_file("../resources/token.txt", "user_input", None)
    tranl_object = GoogleTranslate(test_file_path_settings)
    # input is in variable "test_user_input_input" at the beginning of file
    assert tranl_object.translate(None, "he", "en", "text") == "היי"


def test_invalid_url():
    tranl_object = GoogleTranslate("../resources/settings.json", GoogleTranslate.translate_url + "_")
    with pytest.raises(requests.exceptions.HTTPError, match="404 Client Error: Not Found for url"):
        tranl_object.translate("Hello", "he", "en", "text")


def test_empty_string():
    tranl_object = GoogleTranslate("../resources/settings.json")
    tranl_object.translate("", "he", "en", "text") == ""


def test_invalid_format():
    tranl_object = GoogleTranslate("../resources/settings.json")
    with pytest.raises(requests.exceptions.HTTPError, match="400 Client Error: Bad Request"):
        tranl_object.translate("Hello", "he", "en", "invalid_format")


def test_html_format():
    tranl_object = GoogleTranslate("../resources/settings.json")
    assert tranl_object.translate("Hello", "he", "en", "html") == "שלום"


def test_invalid_source():
    tranl_object = GoogleTranslate("../resources/settings.json")
    with pytest.raises(requests.exceptions.HTTPError, match="400 Client Error: Bad Request"):
        tranl_object.translate("Hello", "he", "invalid_source", "text")


def test_invalid_source():
    tranl_object = GoogleTranslate("../resources/settings.json")
    with pytest.raises(requests.exceptions.HTTPError, match="400 Client Error: Bad Request"):
        tranl_object.translate("Hello", "invalid_target", "en", "html")


def test_hebrew_auto_detect():
    pass
