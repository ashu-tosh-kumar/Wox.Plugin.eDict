"""
    encoding=utf8
    author: ashutosh

    Note: The dictionary.json file used in this project is sourced
            from https://github.com/matthewreagan/WebstersEnglishDictionary
            that in turn depends upon https://www.gutenberg.org/ebooks/29765
"""

from json import load
from spell import SpellCorrect
from wox import Wox, WoxAPI


class EDict(Wox):
    """Easy Dictionay Class used by Wox"""

    def _add_result(self, definitions, results, key, max_results, correction_flag):
        """Adds first two definitions to the result sent to Wox"""
        for definition in definitions.split(';')[:max_results]:
            if definition[0].isdigit():
                definition = definition[3:]
            try:
                definition = definition[:definition.index('.')]
            except ValueError:
                pass
            try:
                definition.strip()[0].upper()+definition.strip()[1:]
            except IndexError:
                pass
            result = {"Title": definition, 'SubTitle': None,
                      "IcoPath": "Images\\edict.ico"}
            if correction_flag:
                result['SubTitle'] = f'Showing results for "{key}" (auto-corrected)'
            else:
                result['SubTitle'] = f'Showing results for "{key}"'
            results.append(result)

    def query(self, key):
        """Overides Wox query function to capture user input"""
        with open('dictionary_compact_with_words.json', 'r') as edict_file:
            self.edict = load(edict_file)
        words = self.edict['cb2b20da-9168-4e8e-8e8f-9b54e7d42214']
        spell_correct = SpellCorrect(words)
        results = []
        try:
            definitions = self.edict[key.strip()]
            self._add_result(definitions, results, key, 4, False)
        except KeyError:
            try:
                corrected_key = spell_correct.correction(key)
                definitions = self.edict[corrected_key]
                self._add_result(definitions, results, corrected_key, 4, True)
            except KeyError:
                pass
        return results


if __name__ == "__main__":
    EDict()
