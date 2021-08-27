from typing import Any, Optional, Union

from aiohttp import ClientSession

from .http import HTTPClient
from .objects import Result


class Client:
    """Main class. Everything you need for your cloud-db database.

    Attributes
    ----------
    key: str
        Your database token.
    session: ClientSession
        Optional session to create the request with. Easier for closing i guess.
    auto_retry: bool
        Set to True if the wrapper should retry when the API throws a cooldown.
    """
    __slots__ = ("_request",)

    def __init__(
            self,
            key: str,
            *,
            session: ClientSession = None,
            auto_retry: bool = False
    ) -> None:
        self._request: HTTPClient = HTTPClient(key, auto_retry = auto_retry, session = session)

    async def get(self, name: str, /, *, only_value: bool = False) -> Union[Optional[Result], Optional[Any]]:
        """Returns the `Result()` associated with the key (name). If `only_value` is False (Default)

        Parameters
        -----------
        name: str
            The key to get the value of.
        only_value: bool
            Whether to directly return the value instead of a Result object. Defaults to False.

        Raises
        --------
        OnCooldown
            You are on a cooldown.

        Returns
        --------
        Union[Any, Result]
            Result object or the key value if `only_value` is True.
        """
        result = await self._request.get(name)
        if only_value:
            return result.get("value")

        return Result(result)

    async def delete(self, name: str, /) -> bool:
        """Delete all data associated with the key (name).

        Parameters
        -----------
        name: str
            Name of the key to delete.

        Raises
        --------
        NotFound
            A key with that name does not exist.
        OnCooldown
            You are on a cooldown.

        Returns
        --------
        bool
            Boolean value of whether the delete was successful.
        """
        result = await self._request.delete(name)
        return result.get('success', False)

    async def all(self) -> Result:
        """Returns all data in the database associated with the token.

        Returns
        --------
        Result
            An instance of Result( with an attribute called `data`.
        """
        result = await self._request.all()
        return Result(result)

    async def set(self, name: str, value: Any, /, *, return_data: bool = False) -> Union[bool, Result]:
        """Set a key with value in the database.

        Parameters
        -----------
        name: str
            The key name.
        value: Any
            The value.
        return_data: bool
            Whether to return a full Result object instead of boolean. Defaults to False.

        Raises
        --------
        OnCooldown
            You are on a cooldown.

        Returns
        --------
         Union[bool, Result]
            Boolean value of whether the addition was successful or a Result object if `return_data` is True.
        """
        result = await self._request.set(name, value)
        if return_data is True:
            add_result = dict(result)
            add_result.update(name = name, value = value)
            return Result(add_result)

        return result.get('success', False)

    async def add(self, name: str, value: int, /) -> Result:
        """Add x amount to a key's integer value.

        .. note::

            The value of the input AND key must be an integer else this will fail.

        Parameters
        -----------
        name: str
            The key name.
        value: Any
            The amount to add.

        Raises
        --------
        BadRequest
            The input or the key value is not an integer.
        OnCooldown
            You are on a cooldown.

        Returns
        --------
        Result
            Result object with an attribute called `number` to get the new value.
        """
        if not isinstance(value, int):
            raise TypeError("value must be a valid integer.")

        result = await self._request.add(name, value)
        return Result(result)

    async def subtract(self, name: Any, value: int, /):
        """Substract x amount from a key's integer value.

        .. note::

            The value of the input AND key must be an integer else this will fail.

        Parameters
        -----------
        name: str
            The key.
        value: Any
            The amount to subtract.

        Raises
        --------
        BadRequest
            The input or the key value is not an integer.
        OnCooldown
            You are on a cooldown.

        Returns
        --------
        Result
            Result object with an attribute called `number` to get the new value.
        """
        if not isinstance(value, int):
            raise TypeError("value must be a valid integer.")

        result = await self._request.subtract(name, value)
        return Result(result)

    async def close(self) -> None:
        await self._request.close()
