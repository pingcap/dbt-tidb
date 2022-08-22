import os

import pytest

from dbt.tests.adapter.basic.test_base import BaseSimpleMaterializations
from dbt.tests.adapter.basic.test_singular_tests import BaseSingularTests
from dbt.tests.adapter.basic.test_singular_tests_ephemeral import (
    BaseSingularTestsEphemeral,
)
from dbt.tests.adapter.basic.test_empty import BaseEmpty
from dbt.tests.adapter.basic.test_ephemeral import BaseEphemeral
from dbt.tests.adapter.basic.test_incremental import BaseIncremental
from dbt.tests.adapter.basic.test_generic_tests import BaseGenericTests
from dbt.tests.adapter.basic.test_snapshot_check_cols import BaseSnapshotCheckCols
from dbt.tests.adapter.basic.test_snapshot_timestamp import BaseSnapshotTimestamp
from dbt.tests.adapter.basic.test_adapter_methods import BaseAdapterMethod
from dbt.tests.util import run_dbt, check_relations_equal
from dbt.tests.adapter.basic.expected_catalog import no_stats, base_expected_catalog
from dbt.tests.adapter.basic.test_docs_generate import BaseDocsGenerate
from dbt.tests.adapter.basic.test_validate_connection import BaseValidateConnection
from dbt.tests.adapter.incremental.test_incremental_unique_id import (
    BaseIncrementalUniqueKey,
)


class TestEmptyMyAdapter(BaseEmpty):
    pass


class TestSimpleMaterializationsMyAdapter(BaseSimpleMaterializations):
    pass


@pytest.mark.skip(reason="TiDB 4.0 ~ 5.0 does not support CTE")
class TestEphemeralMyAdapter(BaseEphemeral):
    pass


@pytest.mark.skip(
    reason="TiDB 4.0 ~ 5.2 does not support creating a temporary table or view"
)
class TestIncrementalMyAdapter(BaseIncremental):
    pass


@pytest.mark.skip(
    reason="TiDB 4.0 ~ 5.2 does not support creating a temporary table or view"
)
class TestSnapshotCheckColsMyAdapter(BaseSnapshotCheckCols):
    pass


@pytest.mark.skip(
    reason="TiDB 4.0 ~ 5.2 does not support creating a temporary table or view"
)
class TestSnapshotTimestampMyAdapter(BaseSnapshotTimestamp):
    pass


@pytest.mark.skip(reason="TiDB 4.0 ~ 5.0 does not support CTE")
class TestSingularTestsEphemeral(BaseSingularTestsEphemeral):
    pass


class TestSingularTestsMyAdapter(BaseSingularTests):
    pass


class TestGenericTestsMyAdapter(BaseGenericTests):
    pass


class TestBaseAdapterMethod(BaseAdapterMethod):
    def test_adapter_methods(self, project, equal_tables):
        result = run_dbt()
        assert len(result) == 3
        check_relations_equal(project.adapter, equal_tables)


class TestValidateConnection(BaseValidateConnection):
    pass


class TestDocsGenerate(BaseDocsGenerate):
    @pytest.fixture(scope="class")
    def expected_catalog(self, project):
        return base_expected_catalog(
            project,
            role=None,
            id_type="int(11)",
            text_type="text",
            time_type="timestamp",
            view_type="view",
            table_type="table",
            model_stats=no_stats(),
        )


@pytest.mark.skip(
    reason="TiDB 4.0 ~ 5.2 does not support creating a temporary table or view."
)
class TestIncrementalUniqueKey(BaseIncrementalUniqueKey):
    pass
