def tidb_expected_references_catalog(
    project,
    role,
    id_type,
    text_type,
    time_type,
    view_type,
    table_type,
    model_stats,
    bigint_type=None,
    seed_stats=None,
    case=None,
    case_columns=False,
    view_summary_stats=None,
):
  if case is None:

    def case(x):
      return x

  col_case = case if case_columns else lambda x: x

  if seed_stats is None:
    seed_stats = model_stats

  if view_summary_stats is None:
    view_summary_stats = model_stats

  model_database = project.database
  my_schema_name = case(project.test_schema)

  summary_columns = {
    "first_name": {
      "type": text_type,
      "index": 0,
      "name": "first_name",
      "comment": None,
    },
    "ct": {
      "type": bigint_type,
      "index": 1,
      "name": "ct",
      "comment": None,
    },
  }

  seed_columns = {
    "id": {
      "type": id_type,
      "index": 0,
      "name": col_case("id"),
      "comment": None,
    },
    "first_name": {
      "type": text_type,
      "index": 1,
      "name": col_case("first_name"),
      "comment": None,
    },
    "email": {
      "type": text_type,
      "index": 2,
      "name": col_case("email"),
      "comment": None,
    },
    "ip_address": {
      "type": text_type,
      "index": 3,
      "name": col_case("ip_address"),
      "comment": None,
    },
    "updated_at": {
      "type": time_type,
      "index": 4,
      "name": col_case("updated_at"),
      "comment": None,
    },
  }
  return {
    "nodes": {
      "seed.test.seed": {
        "unique_id": "seed.test.seed",
        "metadata": {
          "schema": my_schema_name,
          "database": project.database,
          "name": case("seed"),
          "type": table_type,
          "comment": None,
          "owner": role,
        },
        "stats": seed_stats,
        "columns": seed_columns,
      },
      "model.test.ephemeral_summary": {
        "unique_id": "model.test.ephemeral_summary",
        "metadata": {
          "schema": my_schema_name,
          "database": model_database,
          "name": case("ephemeral_summary"),
          "type": table_type,
          "comment": None,
          "owner": role,
        },
        "stats": model_stats,
        "columns": summary_columns,
      },
      "model.test.view_summary": {
        "unique_id": "model.test.view_summary",
        "metadata": {
          "type": view_type,
          "schema": my_schema_name,
          "database": model_database,
          "name": case("view_summary"),
          "comment": None,
          "owner": role,
        },
        "stats": view_summary_stats,
        "columns": summary_columns,
      },
    },
    "sources": {
      "source.test.my_source.my_table": {
        "unique_id": "source.test.my_source.my_table",
        "metadata": {
          "schema": my_schema_name,
          "database": project.database,
          "name": case("seed"),
          "type": table_type,
          "comment": None,
          "owner": role,
        },
        "stats": seed_stats,
        "columns": seed_columns,
      },
    },
  }