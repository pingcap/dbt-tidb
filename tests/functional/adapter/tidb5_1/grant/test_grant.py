import pytest

from dbt.tests.adapter.grants.test_model_grants import BaseModelGrants
from dbt.tests.adapter.grants.test_incremental_grants import BaseIncrementalGrants
from dbt.tests.adapter.grants.test_invalid_grants import BaseInvalidGrants
from dbt.tests.adapter.grants.test_seed_grants import BaseSeedGrants
from dbt.tests.adapter.grants.test_snapshot_grants import BaseSnapshotGrants


# need to export DBT_TEST_USER_1,DBT_TEST_USER_2,DBT_TEST_USER_3
class TestModelGrantsTiDB(BaseModelGrants):
    pass


@pytest.mark.skip(
    reason="TiDB 4.0 ~ 5.2 does not support creating a temporary table or view."
)
class TestIncrementalGrantsTiDB(BaseIncrementalGrants):
    pass


class TestSeedGrantsTiDB(BaseSeedGrants):
    pass


@pytest.mark.skip(
    reason="TiDB 4.0 ~ 5.2 does not support creating a temporary table or view."
)
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
        return "Illegal privilege level specified for"
