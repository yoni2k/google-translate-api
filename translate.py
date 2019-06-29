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
        with open('./token.txt', "r") as tokenFile:
            file_lines = tokenFile.readlines()
    except Exception as e:
        print("ERROR: Unable to read from token file: " + str(e))
        exit(1)

    if len(file_lines) > 1:
        print('ERROR: There are more than 1 lines in token file')
        exit(1)
    return file_lines[0].strip('\n')


def get_str_to_translate():
    """ Returns string that should be translated """
    try:
        with open('./to-translate.txt', "r") as translateFile:
            translate_lines = translateFile.readlines()
    except Exception as e:
        print("ERROR: Unable to read from file with string to translate: " + str(e))
        exit(1)

    if len(translate_lines) > 1:
        print('ERROR: There are more than 1 lines in translate file')
        exit(1)
    return translate_lines[0].strip('\n')


def send_request(req_token):
    querystring = {
        "q":        toTranslate,
        "format":   "text",
        "source":   "en",
        "target":   "he"
        }

    headers = {
        'Authorization':    f'Bearer {req_token}',
        'Host':             "translation.googleapis.com"
        }

    try:
        return requests.request("GET", url, headers=headers, params=querystring)
    except Exception as e:
        print("ERROR: Got exception when sending data to Google:\n" + str(e))
        exit(1)


def print_response(resp_json):
    if resp_json.get('data'):
        print(f'\"{toTranslate}\" translates to \"' + resp_json['data']['translations'][0]['translatedText'] + '\"')
    elif resp_json.get('error'):
        print(resp_json)
    else:
        print('ERROR: unknown parsing error of the response')


token = get_token()
toTranslate = get_str_to_translate()
toTranslate = input('Enter word to translate from English to Hebrew: ')
response = send_request(token)
print_response(response.json())

