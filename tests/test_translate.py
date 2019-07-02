import pytest
import os
import sys
import requests
from src.translate import GoogleTranslate

test_file_path_token = "./test_token.json"
test_file_input = "./test_input.json"

test_user_input_input_eng = "Hi"
test_user_input_input_heb = "היי"

""" ====================================
        Test utils
"""


@pytest.fixture()
def input_from_str_he(request):
    input_from_str(request, "היי")


@pytest.fixture()
def input_from_str_en(request):
    input_from_str(request, "Hi")


def input_from_str(request, user_input):
    orig_stdin = sys.stdin

    with open(test_file_input, 'w') as input_file_to_write:
        input_file_to_write.write(user_input)

    input_file_to_read = open(test_file_input, "r")
    sys.stdin = input_file_to_read

    def return_stdin():
        sys.stdin = orig_stdin
        input_file_to_read.close()
        os.remove(test_file_input)
    request.addfinalizer(return_stdin)


@pytest.fixture
def test_file_token(request):
    def delete_test_token_file():
        os.remove(test_file_path_token)
    request.addfinalizer(delete_test_token_file)


""" ====================================
        basic tests
"""


def test_success_no_assert():
    tranl_object = GoogleTranslate()
    tranl_object.translate("hello", "he")


def test_success_with_assert():
    tranl_object = GoogleTranslate()
    assert tranl_object.translate("hello", "he") == "שלום"


""" ====================================
        2 directions, hebrew --> english, english --> hebrew
"""


def test_translate_no_opt_params_en_to_heb():
    tranl_object = GoogleTranslate()
    assert tranl_object.translate("hello", "he", "en") == "שלום"


def test_translate_no_opt_params_heb_to_eng():
    tranl_object = GoogleTranslate()
    assert tranl_object.translate("שלום", "en", "he") == "Hello"


""" ====================================
        Source and target tests
"""


def test_translate_auto_detect_en_to_heb():
    tranl_object = GoogleTranslate()
    assert tranl_object.translate("hello", "he") == "שלום"


def test_translate_auto_detect_heb_to_eng():
    tranl_object = GoogleTranslate()
    assert tranl_object.translate("שלום", "en") == "Hello"


def test_translate_source_explicit_en_to_heb():
    tranl_object = GoogleTranslate()
    assert tranl_object.translate("hello", "he", "en") == "שלום"


def test_translate_source_explicit_heb_to_eng():
    tranl_object = GoogleTranslate()
    assert tranl_object.translate("שלום", "en", "he") == "Hello"


def test_invalid_source():
    tranl_object = GoogleTranslate()
    with pytest.raises(requests.exceptions.HTTPError, match="400 Client Error: Bad Request"):
        tranl_object.translate("Hello", "en", "invalid_source")


def test_invalid_target():
    tranl_object = GoogleTranslate()
    with pytest.raises(requests.exceptions.HTTPError, match="400 Client Error: Bad Request"):
        tranl_object.translate("Hello", "invalid_target")


""" ====================================
        Format tests
"""


def test_translate_format_text_en_to_heb():
    tranl_object = GoogleTranslate()
    assert tranl_object.translate("hello", "he", None, "text") == "שלום"


def test_translate_format_text_heb_to_eng():
    tranl_object = GoogleTranslate()
    assert tranl_object.translate("שלום", "en", None, "text") == "Hello"


def test_translate_format_html_en_to_heb():
    tranl_object = GoogleTranslate()
    assert tranl_object.translate("hello", "he", None, "html") == "שלום"


def test_translate_format_html_heb_to_eng():
    tranl_object = GoogleTranslate()
    assert tranl_object.translate("שלום", "en", None, "html") == "Hello"


def test_invalid_format():
    tranl_object = GoogleTranslate()
    with pytest.raises(requests.exceptions.HTTPError, match="400 Client Error: Bad Request"):
        tranl_object.translate("Hello", "he", "en", "invalid_format")


""" ====================================
        Different ways of getting the string to translate tests 
"""


def test_empty_string():
    tranl_object = GoogleTranslate()
    assert tranl_object.translate("", "he", "en") == ""


def test_translate_string_given():
    tranl_object = GoogleTranslate()
    assert tranl_object.translate("hello", "he") == "שלום"


def test_user_input_eng(input_from_str_en):
    tranl_object = GoogleTranslate()
    # input is in variable "test_user_input_input" at the beginning of file
    assert tranl_object._tmp_translate_from_user("he") == "היי"


@pytest.mark.skip(reason="hebrew reading rom input fails on encoding")
def test_user_input_heb(input_from_str_he):
    tranl_object = GoogleTranslate()
    # input is in variable "test_user_input_input" at the beginning of file
    assert tranl_object._tmp_translate_from_user("en") == "Hi"


""" ====================================
        Invalid/expired token file, token and URL tests 
"""


def test_invalid_token_file():
    with pytest.raises(FileNotFoundError, match="token"):
        GoogleTranslate("../resources/token_invalid.txt")


def test_invalid_token(test_file_token):
    with open(test_file_path_token, "w") as token_file:
        token_file.write("InvalidToken")

    tranl_object = GoogleTranslate(test_file_path_token)
    with pytest.raises(requests.exceptions.HTTPError, match=r"401"):
        tranl_object.translate("Hello", "he")


def test_token_file_multiple_lines(test_file_token):
    with open(test_file_path_token, "w") as token_file:
        token_file.write("InvalidToken\n")
        token_file.write("InvalidToken2")

    with pytest.raises(ValueError, match=r"There are more than 1 lines in token file"):
        GoogleTranslate(test_file_path_token)


def test_invalid_url():
    tranl_object = GoogleTranslate(GoogleTranslate.token_file_path, GoogleTranslate.translate_url + "_")
    with pytest.raises(requests.exceptions.HTTPError, match="404 Client Error: Not Found for url"):
        tranl_object.translate("Hello", "he", "en", "text")
