from pathlib import Path
import re
from types import SimpleNamespace

import agate
import pytest
from jinja2 import Environment

from dbt.adapters.tidb.column import TiDBColumn
from dbt.adapters.tidb.impl import TiDBAdapter
from dbt.adapters.tidb.relation import TiDBRelation
from dbt.exceptions import DbtRuntimeError

MACROS = Path(__file__).parents[2] / "dbt/include/tidb/macros"
adapter = object.__new__(TiDBAdapter)


def render_macro(filename, name, *args, rows=()):
    statements = []

    def statement(name, caller, **kwargs):
        statements.append((name, caller()))
        return ""

    env = Environment(extensions=["jinja2.ext.do"])
    module = env.from_string((MACROS / filename).read_text()).make_module(
        {
            "adapter": adapter,
            "statement": statement,
            "load_result": lambda _: SimpleNamespace(table=rows),
            "return": lambda value: "",
            "sql_convert_columns_in_relation": lambda value: [],
            "config": {"get": lambda *args: None},
        }
    )
    return getattr(module, name)(*args), statements


def test_identifier_quoting_all_entry_points():
    name = "a`b"
    relation = TiDBRelation.create(schema=name, identifier=name)
    assert adapter.quote(name) == "`a``b`"
    assert adapter.quote(None) == "`None`"
    assert TiDBColumn(name, "int").quoted == "`a``b`"
    assert relation.render() == "`a``b`.`a``b`"


def test_metadata_queries_quote_identifiers_and_literals():
    relation = TiDBRelation.create(
        schema="s'\\`",
        identifier="t`name",
        type="table",
        quote_policy={"schema": False, "identifier": False},
    )
    _, statements = render_macro(
        "adapters.sql", "tidb__get_columns_in_relation", relation
    )
    assert "show columns from `s'\\```.`t``name`" in statements[0][1]
    sql, _ = render_macro("apply_grants.sql", "default__get_show_grant_sql", relation)
    assert adapter.sql_string_literal(relation.schema) in sql
    assert adapter.sql_string_literal(relation.identifier) in sql
    assert "s'\\`" not in sql
    assert sql.count("`Host` as host") == 4
    _, statements = render_macro(
        "adapters.sql", "tidb__list_relations_without_caching", relation
    )
    assert adapter.sql_string_literal(relation.schema) in statements[0][1]


def test_create_table_validates_type_and_quotes_column():
    relation = TiDBRelation.create(schema="db`x", identifier="target", type="table")
    _, statements = render_macro(
        "adapters.sql",
        "tidb__create_table_as",
        False,
        relation,
        "select 1",
        rows=[("a`b", "varchar(20)", "YES")],
    )
    assert "`a``b`" in dict(statements)["xxx"]
    assert "`db``x`.`__dbt_stage_" in dict(statements)["get_columns_in_relation"]
    with pytest.raises(DbtRuntimeError):
        render_macro(
            "adapters.sql",
            "tidb__create_table_as",
            False,
            relation,
            "select 1",
            rows=[("col", "int); DROP TABLE users; --", "YES")],
        )


def test_staging_view_is_unique_per_materialization_and_used_consistently():
    relation = TiDBRelation.create(schema="db", identifier="target", type="table")
    names = set()
    for _ in range(20):
        _, statements = render_macro(
            "adapters.sql",
            "tidb__create_table_as",
            False,
            relation,
            "select 1",
            rows=[("col", "int", "YES")],
        )
        sql = dict(statements)
        name = re.search(r"__dbt_stage_[0-9a-f]{32}", sql["create_view_as"]).group()
        for step in ("get_columns_in_relation", "drop_view"):
            assert f"`db`.`{name}`" in sql[step]
        assert "select 1" in sql["copy_data_from_view_to_table"]
        assert name not in sql["copy_data_from_view_to_table"]
        names.add(name)
    assert len(names) == 20


@pytest.mark.parametrize(
    "value",
    [
        "int(11)",
        "bigint unsigned",
        "decimal(10,2)",
        "varchar(255)",
        "timestamp(6)",
        "enum('a','b')",
        "set('a''b','c')",
        "json",
    ],
)
def test_valid_column_types(value):
    assert adapter.column_type_sql(value) == value


@pytest.mark.parametrize(
    "value",
    [
        "int; DROP TABLE x",
        "int /*x*/",
        "enum('a\\', 'b'); DROP TABLE x; --')",
        "varchar(10) default 1",
    ],
)
def test_rejects_untrusted_type_sql(value):
    with pytest.raises(DbtRuntimeError):
        adapter.column_type_sql(value)


def test_drop_type_and_grantee_are_safe():
    relation = TiDBRelation.create(schema="db", identifier="x`y", type="table")
    for macro in ("tidb__get_grant_sql", "tidb__get_revoke_sql"):
        sql, _ = render_macro(
            "apply_grants.sql", macro, relation, "select", ["bad`user"]
        )
        assert "`db`.`x``y`" in sql
        assert "`bad``user`" in sql
    with pytest.raises(DbtRuntimeError):
        adapter.relation_type_sql("table; DROP TABLE x")
    with pytest.raises(DbtRuntimeError):
        render_macro(
            "apply_grants.sql",
            "tidb__get_revoke_sql",
            relation,
            "select; DROP TABLE x",
            ["user"],
        )


@pytest.mark.parametrize("action,preposition", [("grant", "to"), ("revoke", "from")])
@pytest.mark.parametrize("privilege", ["SELECT", "Insert", "uPdAtE", "delete"])
def test_grants_accept_only_supported_privileges(action, preposition, privilege):
    relation = TiDBRelation.create(
        schema="db`name",
        identifier="table`name",
        quote_policy={"schema": False, "identifier": False},
    )
    sql, _ = render_macro(
        "apply_grants.sql",
        f"tidb__get_{action}_sql",
        relation,
        privilege,
        ["user1", "user2"],
    )
    assert sql == (
        f"{action} {privilege.lower()} on `db``name`.`table``name` "
        f"{preposition} `user1`@'%', `user2`@'%'"
    )
    _, statements = render_macro("apply_grants.sql", "tidb__call_dcl_statements", [sql])
    assert len(statements) == 1
    assert statements[0][1].strip() == sql


@pytest.mark.parametrize("action", ["grant", "revoke"])
@pytest.mark.parametrize(
    "privilege",
    [
        "ALL PRIVILEGES",
        "ALL PRIVILEGES ON *.*",
        "SUPER",
        "GRANT OPTION",
        "SELECT ON *.* TO 'x'@'%' IDENTIFIED BY 'p' WITH GRANT OPTION --",
        "select; DROP USER root",
        "select, insert",
        "select/*comment*/",
        "select\nON *.*",
        " select",
        "select ",
        "",
        None,
        1,
        ["select"],
    ],
)
def test_grants_reject_untrusted_privileges_before_execution(action, privilege):
    relation = TiDBRelation.create(schema="db", identifier="target")
    with pytest.raises(DbtRuntimeError, match="Unsupported grant privilege"):
        render_macro(
            "apply_grants.sql",
            f"tidb__get_{action}_sql",
            relation,
            privilege,
            ["user"],
        )


@pytest.mark.parametrize("action,preposition", [("grant", "to"), ("revoke", "from")])
@pytest.mark.parametrize(
    "grantee,quoted",
    [
        ('bad"user', '`bad"user`'),
        ("bad'user", "`bad'user`"),
        ("bad`user", "`bad``user`"),
        ("bad\\user", "`bad\\user`"),
        ('x" WITH GRANT OPTION --', '`x" WITH GRANT OPTION --`'),
        (
            "x` WITH GRANT OPTION; DROP USER root; --",
            "`x`` WITH GRANT OPTION; DROP USER root; --`",
        ),
        ("x`@`%", "`x``@``%`"),
    ],
)
def test_grantee_payloads_remain_one_quoted_account(
    action, preposition, grantee, quoted
):
    relation = TiDBRelation.create(schema="db", identifier="target")
    sql, _ = render_macro(
        "apply_grants.sql",
        f"tidb__get_{action}_sql",
        relation,
        "select",
        [grantee, "reader"],
    )
    assert sql == (
        f"{action} select on `db`.`target` {preposition} " f"{quoted}@'%', `reader`@'%'"
    )


@pytest.mark.parametrize("action", ["grant", "revoke"])
@pytest.mark.parametrize("grantee", ["", " ", "\t\n", None, False, 0, 1, [], {}])
def test_grants_reject_invalid_grantees(action, grantee):
    relation = TiDBRelation.create(schema="db", identifier="target")
    with pytest.raises(DbtRuntimeError, match="Invalid grant grantee"):
        render_macro(
            "apply_grants.sql",
            f"tidb__get_{action}_sql",
            relation,
            "select",
            ["reader", grantee],
        )


def grants_table(rows):
    return agate.Table(
        rows,
        ["privilege_type", "grantee", "host"],
        [agate.Text(), agate.Text(), agate.Text()],
    )


def test_grant_discovery_preserves_supported_accounts():
    assert adapter.standardize_grants_dict(grants_table([])) == {}
    assert adapter.standardize_grants_dict(
        grants_table(
            [
                ("select", "reader", "%"),
                ("select", "other`reader", "%"),
                ("insert", "writer", "%"),
                ("update", "writer", "%"),
                ("delete", "writer", "%"),
            ]
        )
    ) == {
        "select": ["reader", "other`reader"],
        "insert": ["writer"],
        "update": ["writer"],
        "delete": ["writer"],
    }


@pytest.mark.parametrize("host", ["10.0.0.1", "localhost", "10.%", "", None])
def test_grant_discovery_rejects_host_scoped_accounts(host):
    # A same-name wildcard account must not hide the host-scoped account.
    with pytest.raises(DbtRuntimeError, match="Cannot reconcile grants for account"):
        adapter.standardize_grants_dict(
            grants_table([("select", "reader", "%"), ("select", "reader", host)])
        )


@pytest.mark.parametrize("grantee", ["", " ", None])
def test_grant_discovery_rejects_anonymous_accounts(grantee):
    with pytest.raises(DbtRuntimeError, match="Invalid grant grantee"):
        adapter.standardize_grants_dict(grants_table([("select", grantee, "%")]))
