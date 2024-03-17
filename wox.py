"""Dummy Wox class only for local development
"""

import json


class Wox:
    """Dummy `Wox` class only for local development and to avoid build failure because of
    unvailability of actual `Wox` class
    """

    pass


class WoxAPI:
    """Dummy `WoxAPI` class only for local development and to avoid build failure because of
    unvailability of actual `WoxAPI` class
    """

    @classmethod
    def hide_app(cls):
        """
        hide wox
        """
        print(json.dumps({"method": "Wox.HideApp", "parameters": []}))
