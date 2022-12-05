import pytest

from dbt.tests.util import run_dbt, check_relations_equal
from dbt.tests.adapter.ephemeral.test_ephemeral import BaseEphemeralMulti


class TestEphemeralMultiTiDB(BaseEphemeralMulti):
    def test_ephemeral_multi_snowflake(self, project):
        run_dbt(["seed"])
        results = run_dbt(["run"])
        assert len(results) == 3
        check_relations_equal(project.adapter, ["seed", "dependent"])
        # TiDB does not support double dependent
        # check_relations_equal(project.adapter, ["seed", "double_dependent"])
        check_relations_equal(project.adapter, ["seed", "super_dependent"])
