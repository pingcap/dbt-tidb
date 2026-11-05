import pytest
from uuid import uuid4

from dbt.tests.util import run_dbt, run_dbt_and_capture, write_file
from dbt.tests.adapter.grants.test_model_grants import BaseModelGrants
from dbt.tests.adapter.grants.test_incremental_grants import BaseIncrementalGrants
from dbt.tests.adapter.grants.test_invalid_grants import BaseInvalidGrants
from dbt.tests.adapter.grants.test_seed_grants import BaseSeedGrants
from dbt.tests.adapter.grants.test_snapshot_grants import BaseSnapshotGrants
from tests.functional.adapter.tidb.grant.fixture_snapshots import (
    my_snapshot_sql,
    snapshot_schema_yml,
)


# need to export DBT_TEST_USER_1,DBT_TEST_USER_2,DBT_TEST_USER_3
class TestModelGrantsTiDB(BaseModelGrants):
    pass


class TestIncrementalGrantsTiDB(BaseIncrementalGrants):
    pass


class TestSeedGrantsTiDB(BaseSeedGrants):
    pass


class TestSnapshotGrantsTiDB(BaseSnapshotGrants):
    @pytest.fixture(scope="class")
    def snapshots(self):
        return {
            "my_snapshot.sql": my_snapshot_sql,
            "schema.yml": self.interpolate_name_overrides(snapshot_schema_yml),
        }


class TestInvalidGrantsTiDB(BaseInvalidGrants):
    def grantee_does_not_exist_error(self):
        return "You are not allowed to create a user with GRANT"

    def privilege_does_not_exist_error(self):
        return "Unsupported grant privilege"


class TestGrantAccountValidation:
    @pytest.fixture(scope="class")
    def models(self):
        return {
            "grant_target.sql": "{{ config(materialized='incremental') }} select 1 as id",
        }

    def test_blank_grantee(self, project):
        write_file(
            "{{ config(materialized='incremental', grants={'select': ['']}) }} "
            "select 1 as id",
            project.project_root,
            "models",
            "grant_target.sql",
        )
        _, output = run_dbt_and_capture(["run"], expect_pass=False)
        assert "Invalid grant grantee" in output
        assert (
            project.run_sql(
                "select count(*) from mysql.tables_priv "
                f"where DB = '{project.test_schema}' and Table_name = 'grant_target'",
                fetch="one",
            )[0]
            == 0
        )

    @pytest.mark.parametrize("remove_grants", [False, True])
    def test_host_scoped_grants_stop_reconciliation(self, project, remove_grants):
        write_file(
            "{{ config(materialized='incremental', grants={'select': ['user1']}) }} "
            "select 1 as id",
            project.project_root,
            "models",
            "grant_target.sql",
        )
        run_dbt(["run"])
        user = "dbt_grants_" + uuid4().hex[:8]
        account = f"'{user}'@'10.0.0.1'"
        project.run_sql(f"CREATE USER {account}")
        try:
            project.run_sql(
                f"GRANT SELECT ON `{project.test_schema}`.`grant_target` TO {account}"
            )
            if remove_grants:
                write_file(
                    "{{ config(materialized='incremental', grants={'select': []}) }} "
                    "select 1 as id",
                    project.project_root,
                    "models",
                    "grant_target.sql",
                )
            _, output = run_dbt_and_capture(["run"], expect_pass=False)
            assert "Cannot reconcile grants for account" in output
            # Validation must stop the entire DCL batch, including valid revokes.
            assert (
                project.run_sql(
                    "select count(*) from mysql.tables_priv "
                    f"where DB = '{project.test_schema}' and Table_name = 'grant_target' "
                    f"and User in ('user1', '{user}') and Table_priv like '%Select%'",
                    fetch="one",
                )[0]
                == 2
            )
        finally:
            project.run_sql(f"DROP USER {account}")
