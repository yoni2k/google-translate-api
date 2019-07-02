"""
TODO:
- Go over this API documentation in Google
- Flexibility in choosing which language to translate from
- Flexibility in choosing which language to translate to
- Learning what language it is automatically
- Go over other close to it APIs in Google
- Completely redo user input
- Check how to work with longer tokens
- Make a movie out of it
- Put the movie on Github and send to others
"""

import requests
import json
import traceback


class GoogleTranslate:
    """
            Translate text from 1 language to another using Google translate API
            Relies on:
                - valid not expired Google token in resources/token.txt of any Google account
                    and scope https://www.googleapis.com/auth/cloud-translation
    """

    translate_url = "https://translation.googleapis.com/language/translate/v2"
    token_file_path = "../resources/token.txt"
    last_translated = ""

    def _get_token(self, token_file_path):
        """ Returns token to be used when connection to Google API """
        with open(token_file_path, "r") as tokenFile:
            file_lines = tokenFile.readlines()

        if len(file_lines) > 1:
            raise ValueError('There are more than 1 lines in token file')
        return file_lines[0].strip('\n')

    def _send_request(self, text_to_translate, target, source=None, format_type=None):
        """ Sends request to Google translate API after insertion of given parameters """
        querystring = {"q":        text_to_translate,
                       "target":   target}

        if source:
            querystring["source"] = source

        if format_type:
            querystring["format"] = format_type

        headers = {'Authorization':    f'Bearer {self.token}',
                   'Host':             "translation.googleapis.com"}

        print("querystring: " + str(querystring))
        return requests.request("GET", self.translate_url, headers=headers, params=querystring)

    @staticmethod
    def _parse_translate_response(resp_json):
        """ Parses the translated text out of the response received from Google API"""
        if resp_json.get('data'):
            return resp_json['data']['translations'][0]['translatedText']
        elif resp_json.get('error'):
            raise ValueError("ERROR: " + str(resp_json['error']))
        else:
            raise ValueError('ERROR: unknown parsing error of the response: ' + resp_json)

    def translate(self, text_to_translate, target, source=None, format_type=None):
        """
        Translate text from 1 language to another using Google translate API
        :param text_to_translate: Text to translate to the target language
        :param target: language code (ISO-639-1) to translate the text to, for example "en" for English, "he" for Hebrew
        :param source: language code (ISO-639-1) of text given to translate, for example "en" for English, "he" for Hebrew
            If None is given, Google translated API will autodetect the language
        :param format_type: "text"/"html" - how the translated text should be returned in the Json,
            easier to put as text or embed in html.
            If not given, will not be sent to Google translate, and HTML will be chosen by default by Google translate.
        :return: parsed translated text
        """
        assert text_to_translate is not None
        assert target
        self.last_translated = text_to_translate  # for printing / debugging
        response = self._send_request(text_to_translate, target, source, format_type)
        print("response: " + str(response))
        print("response.txt: " + str(response.text))
        if not response.ok:
            response.raise_for_status()
        return self._parse_translate_response(response.json())

    def _tmp_translate_from_user(self, target, source=None, format_type=None):
        #TODO decide what to do with this fuction, if leaving - rename and add docs
        text_to_translate = input('Enter word to translate from English to Hebrew: ')
        return self.translate(text_to_translate, target, source, format_type)

    def __init__(self, token_file_path=token_file_path, url=translate_url):
        """ Init function that reads the token """
        self.translate_url = url
        self.token = self._get_token(token_file_path)


def main():
    try:
        # TODO if there any point in having a constructor, and a separate line?
        tranl_object = GoogleTranslate()
        translation = tranl_object._tmp_translate_from_user(None, "he", "en", "text")
        print("Translation: \"" + tranl_object.last_translated + "\": \"" + translation + "\"")
    except Exception:
        print(traceback.print_exc())


main()
