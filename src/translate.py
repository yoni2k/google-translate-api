import requests
import traceback

"""
Possible future features:
- Add feature of printing languages supported for translation using https://translation.googleapis.com/language/translate/v2/languages API
- Add feature of giving flexibility which language to translate to besides Hebrew and English
- Support API key in a more user-friendly way: find a way to get a longer term API key, or get it programmatically
- Make work from Windows command line for Hebrew - encoding issues
- Maybe: make a demo and put a link on Github
"""

"""
Start documentation:
1. Go to the following link and authorize to get API key for using translation services:
https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=https%3A%2F%2Fdevelopers.google.com%2Foauthplayground&prompt=consent&response_type=code&client_id=407408718192.apps.googleusercontent.com&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcloud-platform+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcloud-translation&access_type=offline
2. Press on "Exchange authorization code for tokens"
3. Copy the Access token into ./resources/token.txt
The token is good for one hour and needs to be refreshed.
"""

# Change to True to allow detailed debug
debug = False
# debug = True


class GoogleTranslate:
    """
            Translate text from 1 language to another using Google translate API
            Relies on:
                - valid not expired Google token in resources/token.txt of any Google account
                    and scope https://www.googleapis.com/auth/cloud-translation
    """

    translate_url = "https://translation.googleapis.com/language/translate/v2"
    token_file_path = "../resources/token.txt"

    def _set_token(self, token_file_path):
        """ Returns token to be used when connection to Google API """
        with open(token_file_path, "r") as tokenFile:
            file_lines = tokenFile.readlines()

        if len(file_lines) > 1:
            raise ValueError('There are more than 1 lines in token file')
        self.token = file_lines[0].strip('\n')

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

        if debug:
            print("DEBUG: querystring: " + str(querystring))
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
        :param source: language code (ISO-639-1) of text given to translate, example: "en" for English, "he" for Hebrew
            If None is given, Google translated API will autodetect the language
        :param format_type: "text"/"html" - how the translated text should be returned in the Json,
            easier to put as text or embed in html.
            If not given, will not be sent to Google translate, and HTML will be chosen by default by Google translate.
        :return: parsed translated text
        """
        assert text_to_translate is not None
        assert target
        response = self._send_request(text_to_translate, target, source, format_type)
        if not response.ok:
            response.raise_for_status()
        if debug:
            print("DEBUG: response: " + str(response) + str(response.json()))
        return self._parse_translate_response(response.json())

    def __init__(self, token_file_path=token_file_path, url=translate_url):
        """ Init function that reads the token """
        self.translate_url = url
        self._set_token(token_file_path)

    def translate_input_from_user(self):
        """ Asks user for needs to be done (translate what language to what), get input string from user,
            perform the translation and prints it to standard output """

        option, *_ = input(""" 
Welcome to Google translate API playground by Yoni Krichevsky
Options:
1. Translate from English to Hebrew
2. Translate from Hebrew to English
3. Translate from any language (auto-detect) to Hebrew
4. Translate from any language (auto-detect) to English
5. Exit 
=====================> Please enter your choice: """).split()

        if option == "1":
            print("Chosen: 1. Translate from English to Hebrew")
            source = "en"
            target = "he"
            text_to_translate = input("Enter text to translate: ")
        elif option == "2":
            print("Chosen: 2. Translate from Hebrew to English")
            source = "he"
            target = "en"
            text_to_translate = input("Enter text to translate: ")
        elif option == "3":
            print("Chosen: 3. Translate from any language (auto-detect) to Hebrew")
            source = None
            target = "he"
            text_to_translate = input("Enter text to translate: ")
        elif option == "4":
            print("Chosen: 4. Translate from any language (auto-detect) to English")
            source = None
            target = "en"
            text_to_translate = input("Enter text to translate: ")
        elif option == "5":
            print("Chosen: 5. Exit")
            return
        else:
            print("Invalid option: " + option)
            return

        translation = self.translate(text_to_translate, target, source, "text")
        print("Translation: \"" + text_to_translate + "\": \"" + translation.encode("utf-8").decode("utf-8") + "\"")
        # TODO not great that on one hand outputs the result, and on the other hand returns it
        return translation


def main():
    try:
        GoogleTranslate().translate_input_from_user()
    except Exception:
        print(traceback.print_exc())


main()
