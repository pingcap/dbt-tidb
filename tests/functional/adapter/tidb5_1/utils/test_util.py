import pytest
from dbt.tests.adapter.utils.test_any_value import BaseAnyValue
from dbt.tests.adapter.utils.test_bool_or import BaseBoolOr
from dbt.tests.adapter.utils.test_cast_bool_to_text import BaseCastBoolToText
from dbt.tests.adapter.utils.test_concat import BaseConcat
from dbt.tests.adapter.utils.test_dateadd import BaseDateAdd
from dbt.tests.adapter.utils.test_datediff import BaseDateDiff
from dbt.tests.adapter.utils.test_date_trunc import BaseDateTrunc
from dbt.tests.adapter.utils.test_escape_single_quotes import (
    BaseEscapeSingleQuotesQuote,
)
from dbt.tests.adapter.utils.test_except import BaseExcept
from dbt.tests.adapter.utils.test_hash import BaseHash
from dbt.tests.adapter.utils.test_intersect import BaseIntersect
from dbt.tests.adapter.utils.test_last_day import BaseLastDay
from dbt.tests.adapter.utils.test_length import BaseLength
from dbt.tests.adapter.utils.test_position import BasePosition
from dbt.tests.adapter.utils.test_replace import BaseReplace
from dbt.tests.adapter.utils.test_right import BaseRight
from dbt.tests.adapter.utils.test_safe_cast import BaseSafeCast
from dbt.tests.adapter.utils.test_split_part import BaseSplitPart
from dbt.tests.adapter.utils.test_string_literal import BaseStringLiteral
from dbt.tests.adapter.utils.test_listagg import BaseListagg
from tests.functional.adapter.tidb5_1.utils.fixture_bool_or import (
    models__test_bool_or_sql,
    models__test_bool_or_yml,
)
from tests.functional.adapter.tidb5_1.utils.fixture_dateadd import (
    models__test_dateadd_yml,
    models__test_dateadd_sql,
)
from tests.functional.adapter.tidb5_1.utils.fixture_datediff import (
    seeds__data_datediff_csv,
    models__test_datediff_sql,
    models__test_datediff_yml,
)
from tests.functional.adapter.tidb5_1.utils.fixture_datetrunc import (
    models__test_date_trunc_sql,
    models__test_date_trunc_yml,
)
from tests.functional.adapter.tidb5_1.utils.fixture_safe_cast import (
    models__test_safe_cast_yml,
    models__test_safe_cast_sql,
)
from tests.functional.adapter.tidb5_1.utils.fixture_split_part import (
    models__test_split_part_yml,
    models__test_split_part_sql,
)


class TestAnyValue(BaseAnyValue):
    pass


class TestBoolOr(BaseBoolOr):
    @pytest.fixture(scope="class")
    def models(self):
        return {
            "test_bool_or.yml": models__test_bool_or_yml,
            "test_bool_or.sql": self.interpolate_macro_namespace(
                models__test_bool_or_sql, "bool_or"
            ),
        }


class TestCastBoolToText(BaseCastBoolToText):
    pass


class TestConcat(BaseConcat):
    pass


class TestDateAdd(BaseDateAdd):
    @pytest.fixture(scope="class")
    def models(self):
        return {
            "test_dateadd.yml": models__test_dateadd_yml,
            "test_dateadd.sql": self.interpolate_macro_namespace(
                models__test_dateadd_sql, "dateadd"
            ),
        }


class TestDateDiff(BaseDateDiff):
    @pytest.fixture(scope="class")
    def seeds(self):
        return {"data_datediff.csv": seeds__data_datediff_csv}

    @pytest.fixture(scope="class")
    def models(self):
        return {
            "test_datediff.yml": models__test_datediff_yml,
            "test_datediff.sql": self.interpolate_macro_namespace(
                models__test_datediff_sql, "datediff"
            ),
        }


class TestDateTrunc(BaseDateTrunc):
    @pytest.fixture(scope="class")
    def models(self):
        return {
            "test_date_trunc.yml": models__test_date_trunc_yml,
            "test_date_trunc.sql": self.interpolate_macro_namespace(
                models__test_date_trunc_sql, "date_trunc"
            ),
        }


class TestEscapeSingleQuotes(BaseEscapeSingleQuotesQuote):
    pass


class TestExcept(BaseExcept):
    pass


class TestHash(BaseHash):
    pass


class TestIntersect(BaseIntersect):
    pass


class TestLastDay(BaseLastDay):
    pass


class TestLength(BaseLength):
    pass


@pytest.mark.skip(reason="unsupport")
class TestListagg(BaseListagg):
    pass


class TestPosition(BasePosition):
    pass


class TestReplace(BaseReplace):
    pass


class TestRight(BaseRight):
    pass


class TestSafeCast(BaseSafeCast):
    @pytest.fixture(scope="class")
    def models(self):
        return {
            "test_safe_cast.yml": models__test_safe_cast_yml,
            "test_safe_cast.sql": self.interpolate_macro_namespace(
                self.interpolate_macro_namespace(
                    models__test_safe_cast_sql, "safe_cast"
                ),
                "type_string",
            ),
        }


class TestSplitPart(BaseSplitPart):
    @pytest.fixture(scope="class")
    def models(self):
        return {
            "test_split_part.yml": models__test_split_part_yml,
            "test_split_part.sql": self.interpolate_macro_namespace(
                models__test_split_part_sql, "split_part"
            ),
        }


class TestStringLiteral(BaseStringLiteral):
    pass
