from pathlib import Path
import sqlite3

import pytest
from jinja2 import Environment

from dbt.adapters.tidb.impl import TiDBAdapter

HELPERS = (
    Path(__file__).parents[2]
    / "dbt/include/tidb/macros/materializations/incremental/helpers.sql"
)


def render_delete(macro, unique_key):
    adapter = object.__new__(TiDBAdapter)
    module = (
        Environment(extensions=["jinja2.ext.do"])
        .from_string(HELPERS.read_text())
        .make_module(
            {
                "adapter": adapter,
                "get_quoted_csv": lambda names: ", ".join(
                    adapter.quote(name) for name in names
                ),
            }
        )
    )
    sql = getattr(module, macro)("target", "source", unique_key, [])
    return sql.split(";", 1)[0].strip()


@pytest.mark.parametrize(
    "macro", ["incremental_delete", "tidb__get_delete_insert_merge_sql"]
)
@pytest.mark.parametrize(
    "unique_key,target,source,survivors",
    [
        # Component values all occur in the batch, but the historical tuples do not.
        (
            ["k1", "k2"],
            [("a", 1), ("b", 2), ("c", 3)],
            [("a", 2), ("b", 1), ("c", 3)],
            [("a", 1), ("b", 2)],
        ),
        (("k1", "k2"), [("a", 1), ("b", 2)], [], [("a", 1), ("b", 2)]),
        # NULL retains SQL equality semantics: NULL keys do not match each other.
        (
            ["k1", "k2"],
            [("a", None), (None, 1), ("b", 2)],
            [("a", None), (None, 1), ("b", 2)],
            [("a", None), (None, 1)],
        ),
        (["k1"], [("a", 1), ("b", 2)], [("a", 3)], [("b", 2)]),
        ("k1", [("a", 1), ("b", 2)], [("a", 3)], [("b", 2)]),
        (None, [("a", 1), ("b", 2)], [("a", 3)], [("a", 1), ("b", 2)]),
    ],
)
def test_delete_matches_complete_keys(macro, unique_key, target, source, survivors):
    with sqlite3.connect(":memory:") as db:
        db.execute("create table target (k1 text, k2 integer)")
        db.execute("create table source (k1 text, k2 integer)")
        db.executemany("insert into target values (?, ?)", target)
        db.executemany("insert into source values (?, ?)", source)
        sql = render_delete(macro, unique_key)
        if unique_key:
            db.execute(sql)
        assert db.execute("select * from target").fetchall() == survivors
        db.execute("insert into target select * from source")
        assert db.execute("select * from target").fetchall() == survivors + source
