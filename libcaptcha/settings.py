import os

CAPTCHA_FONT_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), 'fonts/Vera.ttf'))
CAPTCHA_FONT_SIZE = 22
CAPTCHA_LETTER_ROTATION = (-35, 35)
CAPTCHA_BACKGROUND_COLOR = '#ffffff'
CAPTCHA_FOREGROUND_COLOR = '#001100'
CAPTCHA_CHALLENGE_FUNCT = 'helpers.random_char_challenge'
CAPTCHA_NOISE_FUNCTIONS = ('helpers.noise_arcs', 'helpers.noise_dots',)
CAPTCHA_FILTER_FUNCTIONS = ('helpers.post_smooth',)
CAPTCHA_WORDS_DICTIONARY = '/usr/share/dict/words'
CAPTCHA_PUNCTUATION = '''_"',.;:-'''
CAPTCHA_FLITE_PATH = None
CAPTCHA_TIMEOUT = 5  # Minutes
CAPTCHA_LENGTH = 4
CAPTCHA_IMAGE_BEFORE_FIELD = True
CAPTCHA_DICTIONARY_MIN_LENGTH = 0
CAPTCHA_DICTIONARY_MAX_LENGTH = 99
if CAPTCHA_IMAGE_BEFORE_FIELD:
    CAPTCHA_OUTPUT_FORMAT = '%(image)s %(hidden_field)s %(text_field)s'
else:
    CAPTCHA_OUTPUT_FORMAT = '%(hidden_field)s %(text_field)s %(image)s'


# Failsafe
if CAPTCHA_DICTIONARY_MIN_LENGTH > CAPTCHA_DICTIONARY_MAX_LENGTH:
    CAPTCHA_DICTIONARY_MIN_LENGTH, CAPTCHA_DICTIONARY_MAX_LENGTH = CAPTCHA_DICTIONARY_MAX_LENGTH, CAPTCHA_DICTIONARY_MIN_LENGTH


def _callable_from_string(string_or_callable):
    if callable(string_or_callable):
        return string_or_callable
    else:
        return getattr(__import__('.'.join(string_or_callable.split('.')[:-1]), {}, {}, ['']), string_or_callable.split('.')[-1])


def get_challenge():
    return _callable_from_string(CAPTCHA_CHALLENGE_FUNCT)


def noise_functions():
    if CAPTCHA_NOISE_FUNCTIONS:
        return map(_callable_from_string, CAPTCHA_NOISE_FUNCTIONS)
    return []


def filter_functions():
    if CAPTCHA_FILTER_FUNCTIONS:
        return map(_callable_from_string, CAPTCHA_FILTER_FUNCTIONS)
    return []
