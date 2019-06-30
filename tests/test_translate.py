import pytest
from src.translate import GoogleTranslate



def test_translate_string_given():
    tranl_object = GoogleTranslate("../resources/settings.json")
    assert tranl_object.translate("hello", "text", "en", "he") == "שלום"

def test_translate_string_from_file():
    tranl_object = GoogleTranslate("../resources/settings.json")
    assert tranl_object.translate(None, "text", "en", "he") == "שלום עולם"

def test_translate_hebrew_to_english():
    tranl_object = GoogleTranslate("../resources/settings.json")
    assert tranl_object.translate("שלום", "text", "he", "en") == "Hello"

"""
src_token_location = '../resources/token.txt'
dest_token_location = src_token_location + '1'


@pytest.fixture(name='rename_token_file_back', scope='module')
def rename_token_file_back(request):
    print("Yoni in rename_token_file_back")

    def finalizer():
        print("Yoni in finalizer")
        os.rename(dest_token_location, src_token_location)
        basic_test()

    request.addfinalizer(finalizer)


@pytest.mark.usefixtures("rename_token_file_back")
def test_token_file_not_found():
    print("Yoni test_token_file_not_found called")
    # make sure things work before file change
    basic_test()

    # setup - rename file
    os.rename(src_token_location, dest_token_location)
    # test
    with pytest.raises(Exception) as e:
        print("Yoni got up to here")
"""



