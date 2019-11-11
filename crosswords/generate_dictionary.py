import codecs
import tempfile
import unidecode
import urllib.request
import zipfile

from pathlib import Path


DICTIONARY_FILE = 'crosswords/francais.txt'
DICTIONARY_URL = 'http://gwicks.net/textlists/francais.zip'


def deduplicate_list(word_list):
    return list(set(word_list))


dictionary_zip_path, _ = urllib.request.urlretrieve(DICTIONARY_URL)

temporary_directory = tempfile.TemporaryDirectory()
with zipfile.ZipFile(dictionary_zip_path, 'r') as dictionary_zip:
    dictionary_zip.extractall(temporary_directory.name)

Path(DICTIONARY_FILE).touch()
words = list(map(
    unidecode.unidecode,
    codecs.open(temporary_directory.name + '/francais.txt', 'r', encoding='ISO-8859-1').read().split('\n')
))

words = deduplicate_list(words)
words = sorted(words)

with open(DICTIONARY_FILE, 'w') as dictionary_file:
    dictionary_file.write(
        ''.join(list(map(lambda w: w + '\n', words)))
    )
