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
                - settings file in resources/settings.json
                - valid not expired Google token in resources/token.txt of any Google account
                    and scope https://www.googleapis.com/auth/cloud-translation
    """

    translate_url = "https://translation.googleapis.com/language/translate/v2"
    last_translated = ""

    class SettingNames:
        name_token_file_path = 'token_file_path'
        name_string_to_translate_source_file = 'string_to_translate_source_file'
        name_translate_string_source = 'translate_string_source'

        mand_settings_list = (name_token_file_path,
                              name_translate_string_source)

        source_types = ("file", "user_input")

    def _get_token(self):
        """ Returns token to be used when connection to Google API """
        with open(self.settings[self.SettingNames.name_token_file_path], "r") as tokenFile:
            file_lines = tokenFile.readlines()

        if len(file_lines) > 1:
            raise ValueError('There are more than 1 lines in token file')
        return file_lines[0].strip('\n')

    def _get_str_to_translate(self):
        """ Returns string that should be translated, depends on "translate_string_source" setting """
        if self.settings[self.SettingNames.name_translate_string_source] == "user_input":
            return input('Enter word to translate from English to Hebrew: ')
        elif self.settings[self.SettingNames.name_translate_string_source] == "file":
            return self.settings[self.SettingNames.name_string_to_translate_source_file]
        else:
            raise ValueError("Invalid source type: " + self.SettingNames.name_translate_string_source)

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

    def translate(self, text_to_translate=None, target=None, source=None, format_type=None):
        """
        Translate text from 1 language to another using Google translate API
        :param text_to_translate: Text to translate could be taken from 3 sources:
            - given in this parameter to translate method, if this parameter is not None
            - taken from settings file, if "translate_string_source" setting = "file" and this param is None
            - taken from user input, if "translate_string_source" setting = "user_input" and this param is None
        :param target: language code (ISO-639-1) to translate the text to, for example "en" for English, "he" for Hebrew
        :param source: language code (ISO-639-1) of text given to translate, for example "en" for English, "he" for Hebrew
        :param format_type: "text"/"html" - how the translated text should be returned in the Json,
            easier to put as text or embed in html.
            If not given, will not be sent to Google translate, and HTML will be chosen by default by Google translate.
        :return: parsed translated text
        """
        if text_to_translate is None:
            text_to_translate = self._get_str_to_translate()
        self.last_translated = text_to_translate  # for printing / debugging
        response = self._send_request(text_to_translate, target, source, format_type)
        print("response: " + str(response))
        print("response.txt: " + str(response.text))
        if not response.ok:
            response.raise_for_status()
        return self._parse_translate_response(response.json())

    def check_all_settings_exist(self):
        for setting_name in self.SettingNames.mand_settings_list:
            self.settings[setting_name]

        if not self.settings[self.SettingNames.name_translate_string_source] in self.SettingNames.source_types:
            raise ValueError("Invalid source type: " + self.SettingNames.name_translate_string_source)

        if (str(self.settings[self.SettingNames.name_translate_string_source])) == "file":
            self.settings[self.SettingNames.name_string_to_translate_source_file]

    def __init__(self, settings_file_path, url=translate_url):
        """ Init function that reads and validates the settings and token """
        self.translate_url = url
        with open(settings_file_path, "r") as settings_file:
            self.settings = json.load(settings_file)
        self.check_all_settings_exist()
        self.token = self._get_token()


def main():
    try:
        tranl_object = GoogleTranslate("../resources/settings.json")
        translation = tranl_object.translate(None, "he", "en", "text")
        print("Translation: \"" + tranl_object.last_translated + "\": \"" + translation + "\"")
    except Exception:
        print(traceback.print_exc())


main()
