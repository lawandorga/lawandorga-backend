import abc

from core.folders.domain.types import StrDict


class Box(bytes):
    def __init__(self):
        super().__init__()

    def __new__(cls, **kwargs):

        value: bytes

        if issubclass(cls, OpenBox):
            value = kwargs["data"]
        elif issubclass(cls, LockedBox):
            value = kwargs["enc_data"]
        else:
            raise TypeError("The cls '{}' is of the wrong class.".format(cls))

        return super().__new__(cls, value)

    def __eq__(self, other):
        if type(other) == type(self):
            return hash(other) == hash(self)
        return NotImplemented

    @property
    @abc.abstractmethod
    def value(self) -> bytes:
        pass


class LockedBox(Box):
    @staticmethod
    def create_from_dict(d: StrDict) -> "LockedBox":
        assert (
            "enc_data" in d
            and "key_origin" in d
            and isinstance(d["enc_data"], str)
            and isinstance(d["key_origin"], str)
        )

        enc_data = d["enc_data"].encode("ISO-8859-1")
        key_origin: str = d["key_origin"]

        return LockedBox(enc_data=enc_data, key_origin=key_origin)

    def __init__(self, enc_data: bytes, key_origin: str):
        self.__enc_data = enc_data
        self.__key_origin = key_origin
        super().__init__()

    def __repr__(self):
        return "LockedBox({}, '{}')".format(self.__enc_data, self.__key_origin)

    def __dict__(self) -> StrDict:  # type: ignore
        return {
            "enc_data": self.__enc_data.decode("ISO-8859-1"),
            "key_origin": self.__key_origin,
        }

    def __hash__(self):
        return hash("{}{}".format(self.__enc_data, self.__key_origin))

    @property
    def key_origin(self) -> str:
        return self.__key_origin

    @property
    def value(self) -> bytes:
        return self.__enc_data


class OpenBox(Box):
    @staticmethod
    def create_from_dict(d: StrDict) -> "OpenBox":
        assert "data" in d and isinstance(d["data"], str)

        data = d["data"].encode("utf-8")

        return OpenBox(data=data)

    def __init__(self, data: bytes):
        self.__data = data
        super().__init__()

    def __repr__(self):
        return "OpenBox({})".format(self.__data)

    def __dict__(self) -> StrDict:  # type: ignore
        return {"data": self.__data.decode("utf-8")}

    def __hash__(self):
        return hash("openbox{}".format(self.__data))

    @property
    def value(self) -> bytes:
        return self.__data
