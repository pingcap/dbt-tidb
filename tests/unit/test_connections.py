from types import SimpleNamespace
from unittest.mock import patch

import pytest
from hologram import ValidationError

from dbt.adapters.tidb.connections import TiDBConnectionManager, TiDBCredentials


def connect_with_profile(profile):
    credentials = TiDBCredentials.from_dict(profile)
    connection = SimpleNamespace(state="init", credentials=credentials)
    with patch.object(TiDBConnectionManager, "retry_connection") as retry, patch(
        "dbt.adapters.tidb.connections.mysql.connector.connect"
    ) as connect:
        retry.side_effect = lambda connection, connect, **kwargs: connect()
        TiDBConnectionManager.open(connection)
        return connect.call_args.kwargs


def test_connection_disables_local_infile_by_default():
    kwargs = connect_with_profile({"server": "localhost", "schema": "test"})
    assert kwargs["allow_local_infile"] is False
    assert kwargs["ssl_verify_cert"] is True
    assert kwargs["ssl_verify_identity"] is True


def test_connection_passes_tls_profile_options():
    tls = {
        "ssl_ca": "/ca.pem",
        "ssl_cert": "/client.pem",
        "ssl_key": "/client-key.pem",
        "ssl_verify_cert": True,
        "ssl_verify_identity": True,
    }
    kwargs = connect_with_profile({"server": "db.example.com", "schema": "test", **tls})
    assert all(kwargs[key] == value for key, value in tls.items())
    assert kwargs["allow_local_infile"] is False


def test_verification_can_be_explicitly_disabled_for_local_tests():
    kwargs = connect_with_profile(
        {
            "server": "localhost",
            "schema": "test",
            "ssl_verify_cert": False,
            "ssl_verify_identity": False,
        }
    )
    assert kwargs["ssl_verify_cert"] is False
    assert kwargs["ssl_verify_identity"] is False


@pytest.mark.parametrize("option", ["ssl_verify_cert", "ssl_verify_identity"])
def test_null_cannot_bypass_verification_defaults(option):
    with pytest.raises(ValidationError, match="not of type 'boolean'"):
        TiDBCredentials.validate(
            {"server": "localhost", "schema": "test", option: None}
        )
