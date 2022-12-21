import pytest

from main import EDict


@pytest.fixture
def edict_client():
    edict_client = EDict()

    yield edict_client


class TestIntegration:
    @pytest.mark.parametrize(
        "key, expected_value",
        [
            ("hello", [{"Title": "See Halloo", "IcoPath": "icons\\edict.ico", "SubTitle": "Showing results for 'hello'"}]),
            ("helllo", [{"Title": "See Halloo", "IcoPath": "icons\\edict.ico", "SubTitle": "Showing results for 'hello' (auto-corrected)"}]),
            ("", []),
        ],
        ids=["no-spelling-mistake-in-key", "spelling-mistake-in-key", "empty-key"],
    )
    def test_integration(self, edict_client, key, expected_value):
        actual_value = edict_client.query(key)

        assert expected_value == actual_value
