from typing import Any, Dict, List, Optional, Union


class Data:
    __slots__ = ("name", "value")

    def __init__(self, data: Dict[str, Any]):
        self.name: str = data.get("name")
        self.value: Optional[Any] = data.get("value")

    def __str__(self) -> str:
        return str(self.value) if self.value else ''

    def __repr__(self) -> str:
        return f'Data(name={self.name}, value={self.value})'


class Result:
    __slots__ = ("__raw_data", "success", "message", "number")

    def __init__(self, data: Dict[str, Union[Any, Data]]):
        self.__raw_data = data

        self.success: bool = data.get("success", False)
        self.message: str = data.get("message")
        self.number: Optional[int] = data.get("number")

    @property
    def data(self) -> Union[Data, List[Data], None]:
        if self.__raw_data.get("name") or self.__raw_data.get("value"):
            return_data: Dict[str, Any] = {
                "name": self.__raw_data.get("name"),
                "value": self.__raw_data.get("value")
            }
            result: Data = Data(return_data)
        elif self.__raw_data.get("data"):
            result: List[Data] = [Data(field) for field in self.__raw_data.get("data")]
        else:
            return None

        return result

    def __repr__(self) -> str:
        return f"Result(success={self.success}, message={self.message}, data={self.data!r}, number={self.number})"
