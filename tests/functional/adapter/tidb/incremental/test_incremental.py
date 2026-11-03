import pytest
from dbt.tests.util import run_dbt

from dbt.tests.adapter.incremental.test_incremental_unique_id import (
    BaseIncrementalUniqueKey,
)


class TestIncrementalUniqueKeyTiDB(BaseIncrementalUniqueKey):
    pass


class TestCompositeIncrementalKeyTiDB:
    @pytest.fixture(scope="class")
    def models(self):
        return {
            "composite.sql": """
                {{ config(materialized='incremental', unique_key=['k1', 'k2']) }}
                {% if is_incremental() %}
                    select 'a' as k1, 2 as k2, 'new' as payload
                    union all select 'b', 1, 'new'
                    union all select 'c', 3, 'new'
                {% else %}
                    select 'a' as k1, 1 as k2, 'old' as payload
                    union all select 'b', 2, 'old'
                    union all select 'c', 3, 'old'
                {% endif %}
            """,
        }

    def test_preserves_unmatched_tuples(self, project):
        assert len(run_dbt(["run"])) == 1
        expected = [
            ("a", 1, "old"),
            ("a", 2, "new"),
            ("b", 1, "new"),
            ("b", 2, "old"),
            ("c", 3, "new"),
        ]
        # Repeat the batch to check replacement without accumulating duplicates.
        for _ in range(2):
            assert len(run_dbt(["run"])) == 1
            rows = project.run_sql(
                f"select k1, k2, payload from {project.test_schema}.composite "
                "order by k1, k2",
                fetch="all",
            )
            assert [tuple(row) for row in rows] == expected
