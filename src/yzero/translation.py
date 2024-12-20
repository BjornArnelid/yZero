import json


class Translations:
    def __init__(self, location):
        self.location = location
        self.dictionary = None
        self.load_dictionary()

    def load_dictionary(self):
        with open(self.location, 'r') as dictionary_file:
            self.dictionary = json.load(dictionary_file)

    def get_string(self, key):
        return self.dictionary[key] if key in self.dictionary else key

    def has_string(self, key):
        return key in self.dictionary

    def add_sub_dictionary(self, sub_dictionary):
        self.dictionary.update(sub_dictionary)


translations = None
default_translations = Translations('resources/english.json')


def set_dictionary(location):
    global translations
    translations = Translations(location)


def get_string(key):
    global translations
    if translations is None:
        translations = Translations('resources/english.json')

    if key in translations.dictionary:
        return translations.get_string(key)
    return default_translations.get_string(key)