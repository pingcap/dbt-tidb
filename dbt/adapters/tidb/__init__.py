from dbt.adapters.tidb.connections import TiDBConnectionManager  # noqa
from dbt.adapters.tidb.connections import TiDBCredentials
from dbt.adapters.tidb.relation import TiDBRelation  # noqa
from dbt.adapters.tidb.column import TiDBColumn  # noqa
from dbt.adapters.tidb.impl import TiDBAdapter

from dbt.adapters.base import AdapterPlugin
from dbt.include import tidb


Plugin = AdapterPlugin(
    adapter=TiDBAdapter,
    credentials=TiDBCredentials,
    include_path=tidb.PACKAGE_PATH)
