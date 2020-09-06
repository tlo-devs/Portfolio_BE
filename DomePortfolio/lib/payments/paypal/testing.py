from typing import ClassVar


class AttrDict(dict):
    __slots__ = []
    __doc__ = ""

    def __getattr__(self, item):
        return super(AttrDict, self).__getitem__(item)


class MockPayPalResponse:
    purchase_units_schema: ClassVar[tuple] = (
        "reference_id",
    )
    payer_schema: ClassVar[tuple] = (
        "payer_id",
        "email_address",
    )

    def __init__(self,
                 purchase_units: dict,
                 payer: dict,
                 status_code: int = 200) -> None:
        # Make sure that both dicts fit the required schema
        if not self._enforce_schema(
            self.purchase_units_schema, purchase_units
        ) or not self._enforce_schema(
            self.payer_schema, payer
        ):
            raise ValueError("Schema did not match")

        self.result = AttrDict(
            purchase_units=AttrDict(purchase_units),
            payer=AttrDict(payer),
        )
        self.status_code = status_code

    @classmethod
    def _enforce_schema(cls, schema: tuple, obj: dict) -> bool:
        if not len(schema) == len(obj.keys()):
            return False
        try:
            for key in schema:
                obj.__getitem__(key)
        except KeyError:
            return False
        return True


__all__ = ["MockPayPalResponse"]
