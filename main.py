"""
    encoding=utf8
    author: ashutosh

    MIT License

    Copyright (c) 2020 Ashutosh

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

    Notes:
        - The dictionary_compact_with_words.json file used in this project is modified
        form of dictionary_compact.json file sourced from
        https://github.com/matthewreagan/WebstersEnglishDictionary that in turn depends
        upon Project Gutenberg's Webster's Unabridged English Dictionary
        https://www.gutenberg.org/ebooks/29765.
        - The spell.py file used in this project is sourced from  Peter Norvig's website
        norvig.com http://norvig.com/spell-correct.html. The file is modified for the
        current use case.
        - Wox documentation on how to create a plugin:
        http://doc.wox.one/en/plugin/python_plugin.html
"""

from json import load
from typing import Dict, List
from zipfile import ZipFile

from lib.src.pyperclip import copy
from spell import SpellCorrect

# Wox already contains a python env with `wox` library pre-installed
from wox import Wox

ICON_PATH = "icons\\edict.ico"
DICTIONARY_ZIP_FILE = "dictionary_compact_with_words.zip"
DICTIONARY_JSON_FILE = "dictionary_compact_with_words.json"
MAXIMUM_RESULTS = 4


class EDict(Wox):
    """Easy Dictionary Class used by Wox"""

    def __init__(self, *args, **kwargs) -> None:
        """Initializer for `EDict` class"""
        with ZipFile(DICTIONARY_ZIP_FILE, "r") as zip_file:
            with zip_file.open(DICTIONARY_JSON_FILE) as edict_file:
                self._edict = load(edict_file)

        # Key "cb2b20da-9168-4e8e-8e8f-9b54e7d42214" gives a list of all words
        words = self._edict["cb2b20da-9168-4e8e-8e8f-9b54e7d42214"]
        self._spell_correct = SpellCorrect(words)

        super().__init__(*args, **kwargs)

    def _format_result(self, definitions: str, key: str, max_results: int, correction_flag: bool) -> List[Dict[str, str]]:
        """Adds `max_results` number of definitions from `definitions` formatted for Wox

        Args:
            definitions (str): String containing all definitions separated by ";"
            key (str): Word for which definitions are passed
            max_results (int): Maximum number of results to be returned
            correction_flag (bool): Whether the key is corrected

        Returns:
            List[Dict[str, str]]: Returns list of results where each result is a
            dictionary containing `Title`, `SubTitle` and `IcoPath`
        """
        results: List[Dict[str, str]] = []
        for definition in definitions.split(";")[:max_results]:
            if definition[0].isdigit():
                definition = definition[3:]

            try:
                definition = definition[: definition.index(".")]
            except ValueError:
                pass

            try:
                definition.strip()[0].upper() + definition.strip()[1:]
            except IndexError:
                pass

            # Creating result
            result = {
                "Title": definition,
                "IcoPath": ICON_PATH,
                "SubTitle": "Press Enter to Copy",
                "JsonRPCAction": {"method": "copy_to_clipboard", "parameters": [definition], "dontHideAfterAction": False},
            }

            # Showing whether the key has been auto-corrected or not
            if correction_flag:
                result["SubTitle"] = f"Showing results for '{key}' (auto-corrected)"
            else:
                result["SubTitle"] = f"Showing results for '{key}'"

            results.append(result)

        return results

    # A function named query is necessary, we will automatically invoke this function
    # when user query this plugin
    def query(self, key: str) -> List[Dict[str, str]]:
        """Overrides Wox query function to capture user input

        Args:
            key (str): User search input

        Returns:
            List[Dict[str, str]]: Returns list of results where each result is a
            dictionary.
        """
        results: List[Dict[str, str]] = []
        key = key.strip().lower()

        if not key:
            # Avoid looking for empty key
            return results

        try:
            # Look for the given key
            definitions = self._edict[key]
            results = self._format_result(definitions, key, MAXIMUM_RESULTS, False)
        except KeyError:
            # Try correcting the key and looking again with the corrected key
            try:
                corrected_key = self._spell_correct.correction(key)
                definitions = self._edict[corrected_key]
                results = self._format_result(definitions, corrected_key, MAXIMUM_RESULTS, True)
            except KeyError:
                # Word doesn't exist in our dictionary
                pass

        return results

    def copy_to_clipboard(self, data: str) -> None:
        """Copies data to Windows clipboard using `pyperclip.copy` command

        Args:
            data (str): Data that needs to be copied to clipboard
        """
        # No viable and safe option as of now
        copy(data)
        # WoxAPI.hide_app()


# Following statement is necessary by Wox
if __name__ == "__main__":
    EDict()
