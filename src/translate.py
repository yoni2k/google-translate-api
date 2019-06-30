"""
TODOs:
- Put in Github
- Move to temporary google account
- Check how to work with longer tokens
- UTs
- Flexibility in choosing which language to translate from
- Flexibility in choosing which language to translate to
- Learning what language it is automatically
- Make a movie out of it
- Put the movie on Github and send to others
"""

import requests
import json
import traceback


class GoogleTranslate:

    translate_url = "https://translation.googleapis.com/language/translate/v2"

    class SettingNames:
        name_token_file_path = 'token_file_path'
        name_string_to_translate_source_file = 'string_to_translate_source_file'
        name_translate_string_source = 'translate_string_source'

        mand_settings_list = (  name_token_file_path,
                                name_translate_string_source)

        source_types = ("file", "user_input")

    def get_token(self):
        """ Returns token to be used when connection to Google API """
        with open(self.settings[self.SettingNames.name_token_file_path], "r") as tokenFile:
            file_lines = tokenFile.readlines()

        if len(file_lines) > 1:
            raise ValueError('There are more than 1 lines in token file')
        return file_lines[0].strip('\n')

    def get_str_to_translate(self):
        """ Returns string that should be translated """
        # TODO do I need this function at all? Like this?
        if self.settings[self.SettingNames.name_translate_string_source] == "user_input":
            return input('Enter word to translate from English to Hebrew: ')
        elif self.settings[self.SettingNames.name_translate_string_source] == "file":
            return self.settings[self.SettingNames.name_string_to_translate_source_file]
        else:
            raise ValueError("Invalid source type: " + self.SettingNames.name_translate_string_source)

    def send_request(self, text_to_translate, format_type, source, target):
        # TODO write explanation
        querystring = {"q":        text_to_translate,
                       "format":   format_type,
                       "source":   source,
                       "target":   target}

        headers = {'Authorization':    f'Bearer {self.token}',
                   'Host':             "translation.googleapis.com"}

        return requests.request("GET", self.translate_url, headers=headers, params=querystring)

    @staticmethod
    def parse_translate_response(resp_json):
        # TODO write explanation
        if resp_json.get('data'):
            return resp_json['data']['translations'][0]['translatedText']
        elif resp_json.get('error'):
            raise ValueError("ERROR: " + resp_json['error'])
        else:
            raise ValueError('ERROR: unknown parsing error of the response: ' + resp_json)

    def translate(self, text_to_translate, format_type, source, target):
        # TODO write explanation
        response = self.send_request(text_to_translate, format_type, source, target)
        return self.parse_translate_response(response.json())

    def check_all_settings_exist(self):
        for setting_name in self.SettingNames.mand_settings_list:
            self.settings[setting_name]

        if not self.settings[self.SettingNames.name_translate_string_source] in self.SettingNames.source_types:
            raise ValueError("Invalid source type: " + self.SettingNames.string_to_translate_source_type)

        if (str(self.settings[self.SettingNames.name_translate_string_source])) == "file":
            self.settings[self.SettingNames.name_string_to_translate_source_file]

    def __init__(self, settings_file_path):
        # TODO write explanation
        with open(settings_file_path, "r") as settings_file:
            self.settings = json.load(settings_file)
        self.check_all_settings_exist()
        self.token = self.get_token()


def main():
    try:
        tranl_object = GoogleTranslate("../resources/settings.json")

        # TODO is this how we want to get it?
        text_to_translate = tranl_object.get_str_to_translate()

        translation = tranl_object.translate(text_to_translate, "text", "en", "he")
        print("Translating \"" + text_to_translate + "\": \"" + translation + "\"")
    except Exception as e:
        print(traceback.print_exc())


main()
