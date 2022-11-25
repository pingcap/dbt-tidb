import pytest

from dbt.tests.util import (
    run_dbt,
    check_relations_equal,
    rm_file,
    write_file
    )
from dbt.tests.adapter.concurrency.test_concurrency import (
    BaseConcurrency,
    seeds__update_csv
    )

class TestConcurrencyTiDB(BaseConcurrency):
    def test_conncurrency_tidb(self, project):
        run_dbt(["seed", "--select", "seed"])
        results = run_dbt(["run"], expect_pass=False)
        assert len(results) == 7
        check_relations_equal(project.adapter, ["SEED", "VIEW_MODEL", "DEP", "TABLE_A", "TABLE_B"])

        rm_file(project.project_root, "seeds", "seed.csv")
        write_file(seeds__update_csv, project.project_root + '/seeds', "seed.csv")
        results = run_dbt(["run"], expect_pass=False)
        assert len(results) == 7
        check_relations_equal(project.adapter, ["SEED", "VIEW_MODEL", "DEP", "TABLE_A", "TABLE_B"])
