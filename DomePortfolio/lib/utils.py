from uuid import UUID


def uuid4_is_valid(uuid: str) -> bool:
    try:
        val = UUID(uuid, version=4)
    except ValueError:
        return False
    return val.hex == uuid


__all__ = ["uuid4_is_valid"]
