import pytest

from dbt.tests.adapter.basic.test_base import BaseSimpleMaterializations
from dbt.tests.adapter.basic.test_singular_tests import BaseSingularTests
from dbt.tests.adapter.basic.test_singular_tests_ephemeral import BaseSingularTestsEphemeral
from dbt.tests.adapter.basic.test_empty import BaseEmpty
from dbt.tests.adapter.basic.test_ephemeral import BaseEphemeral
from dbt.tests.adapter.basic.test_incremental import BaseIncremental
from dbt.tests.adapter.basic.test_generic_tests import BaseGenericTests
from dbt.tests.adapter.basic.test_snapshot_check_cols import BaseSnapshotCheckCols
from dbt.tests.adapter.basic.test_snapshot_timestamp import BaseSnapshotTimestamp
from dbt.tests.adapter.basic.test_adapter_methods import BaseAdapterMethod
from dbt.tests.util import run_dbt, check_relations_equal
from dbt.tests.adapter.basic.expected_catalog import no_stats
from dbt.tests.adapter.basic.test_docs_generate import BaseDocsGenReferences,BaseDocsGenerate
from dbt.tests.adapter.basic.test_validate_connection import BaseValidateConnection

from test.functional.adapter.basic.tidb_expected_catalog import tidb_expected_references_catalog

@pytest.fixture(scope="class")
def dbt_profile_target():
  return {
    'type': 'tidb',
    'threads': 1,
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'port': 4001,
  }


class TestEmptyMyAdapter(BaseEmpty):
  pass


class TestSimpleMaterializationsMyAdapter(BaseSimpleMaterializations):
  pass


class TestEphemeralMyAdapter(BaseEphemeral):
  pass

@pytest.mark.skip(reason="unsupport")
class TestIncrementalMyAdapter(BaseIncremental):
  pass

@pytest.mark.skip(reason="unsupport")
class TestSnapshotCheckColsMyAdapter(BaseSnapshotCheckCols):
  pass

@pytest.mark.skip(reason="unsupport")
class TestSnapshotTimestampMyAdapter(BaseSnapshotTimestamp):
  pass


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


@pytest.mark.skip(reason="need to fix")
class TestDocsGenerate(BaseDocsGenerate):
  pass


@pytest.mark.skip(reason="need to fix")
class TestDocsGenReferences(BaseDocsGenReferences):
  @pytest.fixture(scope="class")
  def expected_catalog(self, project, profile_user):
    return tidb_expected_references_catalog(
      project,
      role=None,
      id_type="int(11)",
      text_type="text",
      time_type="timestamp",
      bigint_type="bigint(21)",
      view_type="view",
      table_type="table",
      model_stats=no_stats(),
    )