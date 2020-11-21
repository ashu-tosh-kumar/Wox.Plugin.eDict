"""
    encoding=utf8
    author: ashutosh

    Note: The dictionary.json file used in this project is sourced
            from https://github.com/matthewreagan/WebstersEnglishDictionary
            that in turn depends upon https://www.gutenberg.org/ebooks/29765
"""

from json import load
from wox import Wox, WoxAPI


class EDict(Wox):
    """Easy Dictionay Class used by Wox"""

    def _add_result(self, results, key, max_results):
        """Adds first two definitions to the result sent to Wox"""
        for _definition in self._definitions.split(';')[:max_results]:
            if _definition[0].isdigit():
                _definition = _definition[3:]
            try:
                _definition = _definition[:_definition.index('.')]
            except ValueError:
                pass
            results.append(
                {"Title": _definition.strip(), "IcoPath": "Images\\edict.ico"})

    def query(self, key):
        """Overides Wox query function to capture user input"""
        with open('dictionary_compact.json', 'r') as edict_file:
            self.edict = load(edict_file)
        results = []
        try:
            self._definitions = self.edict[key.strip()]
            self._add_result(results, key, 4)
        except KeyError:
            pass
        return results


if __name__ == "__main__":
    EDict()
