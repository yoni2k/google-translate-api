# What google-translate-api does
Text translation:
 - from English to Hebrew
 - from Hebrew to English
 - from any language to Hebrew
 - from any language to English  

# My purpose
In order to practice the following technical areas:
 - Using REST APIs
 - HTTP communication - headers, parameters, authentication etc.
 - Python programming
    - Design of small Python module with multiple ways to be used
    - Design of testable Python class
    - Writing, reading and parsing files
    - JSON parsing and writing
    - Working with `requests` for HTTP communication
    - Exception handling and raising
    - User input and parsing 
    - PyTest testing - including fixtures and finalizers, redirecting stdin 
 - Encodings (UTF-8, Windows Character maps)

# How it works
By calling Google Cloud Translate REST API
`https://translation.googleapis.com/language/translate/v2`

See details here: https://cloud.google.com/translate/docs/reference/rest/v2/translate

# Authentication / security
In order to call Google Cloud Translate API, a token / API key is needed based on OAuth 2.0 authentication.  In order not to commit the keys, and since the token expires every hour, see "First time and every hour" setup

# Setup
## Prerequisites on the machine
1. Python
2. Pip (if wasn't installed as part of the Python installation)
To check if was installed:
`pip3 --version` or `pip --version`
3. Git
4. _On Windows:_ PyCharm IDE or any program that allows to run python programs with UTF-8 encoding if want to overcome the limitation in Limitations below. _On Linux_ should work as is.

## Setup - first time
1. Clone this Repository
2. From the local directory of the repository, run:
    `pip install -r "requirements.txt"` or `pip3 install -r "requirements.txt"`

## Setup - first time and every hour
 See Authentication / Security above.
Replace this whole file with token / API string authorize using one of your Google accounts
    to get short expiration API key for using Google translation services by:
1. In a browser, go to the following link: https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=https%3A%2F%2Fdevelopers.google.com%2Foauthplayground&prompt=consent&response_type=code&client_id=407408718192.apps.googleusercontent.com&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcloud-platform+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcloud-translation&access_type=offline
2. In the browser, Choose the Google account, [enter password if necessary]
3. In the browser, press "Allow" to allow for a short-term translation services from this account
4. In the browser, when redirected back to Google Cloud OAuth 2.0 Playground, Press on "Exchange authorization code for tokens"
5. In the browser, in Google Cloud OAuth 2.0 Playground, go to "Step 2 Exchange authorization code for tokens"
6. In the browser, copy "Access token" into `./resources/token.txt` and completely replace the file content with the raw token
_Note: The token is good for one hour and needs to be refreshed every hour by following the process above._
 
# API
## By calling GoogleTranslate class of google-translate-api programmatically in Python
### GoogleTranslate() constructor
    def GoogleTranslate(token_file_path=token_file_path, url=translate_url):
    """ Reads the token and can override Google Cloud translate URL
    :param token_file_path: optional - path of the file with Google API key / token,
        by default taken from "../resources/token.txt"
    :param url: optional - Google Cloud Translate URL - was added mostly for testing purposes """
### translate() API
    def translate(self, text_to_translate, target, source=None, format_type=None):
    """ Translate text from 1 language to another using Google translate API
    :param text_to_translate: Text to translate to the target language
    :param target: language code (ISO-639-1) to translate the text to, for example "en" for English, "he" for Hebrew
    :param source: language code (ISO-639-1) of text given to translate, example: "en" for English, "he" for Hebrew
        If None is given, Google translate API will autodetect the language
    :param format_type: "text"/"html" - how the translated text should be returned in the JSON,
        easier to put as text or embed in html.
        If not given, will not be sent to Google translate, and html will be chosen by default by Google translate.
    :return: parsed translated text """

### Examples of usage
#### Basic
    GoogleTranslate().translate("hello", "he") == "שלום"
#### Using all parameters
    GoogleTranslate().translate("שלום", "en", None, "text") == "Hello"
    

## By user input
 _See known limitations about running it from Windows command line_
 - Run the module:
    `python src/translate.py`
 - Follow the instructions given in Standard Output
 - The translation will be presented on the screen
 
### Options: 
1. Translate from English to Hebrew
2. Translate from Hebrew to English
3. Translate from any language (auto-detect) to Hebrew
4. Translate from any language (auto-detect) to English
5. Exit 

### Example of usage
    Welcome to Google translate API playground by Yoni Krichevsky
    Options:
    1. Translate from English to Hebrew
    2. Translate from Hebrew to English
    3. Translate from any language (auto-detect) to Hebrew
    4. Translate from any language (auto-detect) to English
    5. Exit 
    =====================> Please enter your choice: 1
    Chosen: 1. Translate from English to Hebrew
    Enter text to translate: Hello World!
    Translation: "Hello World!": "שלום עולם!"

# Known limitations
1. Due to encoding issues in Windows, doesn't work well with languages that require unicode encoding (like Hebrew).  Works well when ran from PyCharm, or with languages that don't require unicode. See list of possible future features below.

# Unit tests
There are extensive unit tests that test different use cases and variations of using the module with PyTest: 
 - Programmatic and User input use cases
 - From English to Hebrew and from Hebrew to English translations
 - With giving explicit source language, or let translate to _auto-detect_
 - Invalid parameters testing
 - Testing user input with invalid options given
See more tests and details in `tests/test_translate.py`

# Possible future features
 - Add feature of returning / printing languages supported for translation using `https://translation.googleapis.com/language/translate/v2/languages` API
 - Add feature of giving flexibility which language to translate to besides Hebrew and English
 - Support API key in a more user-friendly way: find a way to get a longer term API key, or get it programmatically without user intervention 
 - Resolve Windows command line encoding issues to allow translation from/to languages that require unicode (Hebrew)
 - Make a demo of using the module and put a link on Github
