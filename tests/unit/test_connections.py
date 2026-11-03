from types import SimpleNamespace
from unittest.mock import patch

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
    assert not any(key.startswith("ssl_") for key in kwargs)


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
