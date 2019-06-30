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

url = "https://translation.googleapis.com/language/translate/v2"


def get_token():
    """ Returns token to be used when connection to Google API """
    try:
        with open('../token.txt', "r") as tokenFile:
            file_lines = tokenFile.readlines()
    except Exception:
        print("ERROR: Unable to read from token file: ")
        raise

    if len(file_lines) > 1:
        raise ValueError('There are more than 1 lines in token file')
    return file_lines[0].strip('\n')


def get_str_to_translate():
    """ Returns string that should be translated """
    try:
        with open('../to-translate.txt', "r") as translateFile:
            translate_lines = translateFile.readlines()
    except Exception:
        print("ERROR: Unable to read from file with string to translate: ")
        raise

    if len(translate_lines) > 1:
        ValueError('There are more than 1 lines in translate file')
    return translate_lines[0].strip('\n')


def send_request(req_token, text_to_translate, format_type, source, target):
    querystring = {"q":        text_to_translate,
                   "format":   format_type,
                   "source":   source,
                   "target":   target}

    headers = {'Authorization':    f'Bearer {req_token}',
               'Host':             "translation.googleapis.com"}

    try:
        return requests.request("GET", url, headers=headers, params=querystring)
    except Exception:
        print("ERROR: Got exception when sending data to Google:\n")
        raise


def get_translation(resp_json):
    if resp_json.get('data'):
        return resp_json['data']['translations'][0]['translatedText']
    elif resp_json.get('error'):
        return "ERROR: " + resp_json['error']
    else:
        return 'ERROR: unknown parsing error of the response: ' + resp_json


def translate(text_to_translate, format_type, source, target):
    token = get_token()
    response = send_request(token, text_to_translate, format_type, source, target)
    return get_translation(response.json())


def main():
    try:
        text_to_translate = get_str_to_translate()
        # to_translate = input('Enter word to translate from English to Hebrew: ')
        translation = translate(text_to_translate, "text", "en", "he")
        print("Translating \"" + text_to_translate + "\": \"" + translation + "\"")
    except Exception as e:
        print("ERROR while translating: " + str(e))


main()
