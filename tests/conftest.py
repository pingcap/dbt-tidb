import pytest
import os

# Import the fuctional fixtures as a plugin
# Note: fixtures with session scope need to be local

pytest_plugins = ["dbt.tests.fixtures.project"]

# The profile dictionary, used to write out profiles.yml
# dbt will supply a unique schema per test, so we do not specify 'schema' here
@pytest.fixture(scope="class")
def dbt_profile_target():
    return {
        "type": "tidb",
        "threads": 1,
        "host": os.getenv("TIDB_TEST_HOST", "127.0.0.1"),
        "user": os.getenv("TIDB_TEST_USER", "root"),
        "password": os.getenv("TIDB_TEST_PASSWORD", ""),
        "port": os.getenv("TIDB_TEST_PORT", 4000),
    }
