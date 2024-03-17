import pytest

from main import EDict


@pytest.fixture
def edict_client():
    edict_client = EDict()

    yield edict_client


class TestIntegration:
    @pytest.mark.parametrize(
        "key",
        [
            ("hello"),
            ("helllo"),
            (""),
        ],
        ids=["no-spelling-mistake-in-key", "spelling-mistake-in-key", "empty-key"],
    )
    def test_integration(self, edict_client, key, snapshot):
        actual_value = edict_client.query(key)

        assert snapshot == actual_value
