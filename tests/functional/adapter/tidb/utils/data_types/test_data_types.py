import pytest

from dbt.tests.adapter.utils.data_types.test_type_int import BaseTypeInt
from dbt.tests.adapter.utils.data_types.test_type_bigint import BaseTypeBigInt
from dbt.tests.adapter.utils.data_types.test_type_boolean import BaseTypeBoolean
from dbt.tests.adapter.utils.data_types.test_type_numeric import BaseTypeNumeric
from dbt.tests.adapter.utils.data_types.test_type_string import BaseTypeString
from dbt.tests.adapter.utils.data_types.test_type_float import BaseTypeFloat
from dbt.tests.adapter.utils.data_types.test_type_timestamp import BaseTypeTimestamp


@pytest.mark.skip(reason="TiDB does not support cast as int")
class TestTypeIntTiDB(BaseTypeInt):
    pass


@pytest.mark.skip(reason="TiDB does not support cast as bigint")
class TestTypeBigIntTiDB(BaseTypeBigInt):
    pass


@pytest.mark.skip(reason="TiDB does not support cast as boolean")
class TestTypeBooleanTiDB(BaseTypeBoolean):
    pass


@pytest.mark.skip(reason="TiDB does not support numeric type")
class TestTypeNumericTiDb(BaseTypeNumeric):
    pass


@pytest.mark.skip(reason="TiDB does not support cast as text")
class TestTypeStringTiDB(BaseTypeString):
    pass


class TestTypeFloatTiDB(BaseTypeFloat):
    pass


@pytest.mark.skip(reason="TiDB does not support cast as timestamp")
class TestTypeTimestampTiDB(BaseTypeTimestamp):
    pass
