from asyncio import sleep
from typing import Any, Optional, Union

from aiohttp import ClientSession

from .errors import OnCooldown
from .http import HTTPClient
from .objects import Result


class Client:
    """Main class. Everything you need for the cloud-db database.

    Attributes
    ----------
    key: str
        Your database token.
    session: ClientSession
        Optional session to create the request with. Easier for closing i guess.
    auto_retry: bool
        Set this to True if the lib should retry when the API throws a cooldown.
        This basically sleeps for 1 second and then tries again.
    """
    __slots__ = ("_request", "__auto_retry_value")

    def __init__(self, key: str, *, session: ClientSession = None, auto_retry: bool = False) -> None:
        self.__auto_retry_value: bool = auto_retry
        self._request: HTTPClient = HTTPClient(key, auto_retry = auto_retry, session = session)

    async def get(
            self,
            name: str,
            /,
            only_value: bool = False,
    ) -> Union[Optional[Result], Optional[Any]]:
        """Returns the `Result()` associated with the key (name). If `only_value` is False (Default)

        Parameters
        -----------
        name: str
            The key to get the value of.
        only_value: bool
            Whether to directly return the value instead of a `Result()`. Defaults to False.
        Raises
        --------
        OnCooldown
            You are on a cooldown.

        Returns
        --------
        Optional[Result]
            Instance of `Result()` if the only_value is set to False.
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
            The key to delete.

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
        return True if result.get('success', False) is True else False

    async def all(self) -> Result:
        """Returns all data in the database associated with the token.

        Returns
        --------
        Result
            An instance of `Result()` with a `data` attribute.
        """
        result = await self._request.all()
        return Result(result)

    async def set(self, name: str, value: Any, /, *, return_data: bool = False) -> Union[bool, Result]:
        """Set a key with value in the database.

        This normally would return a boolean whether the addition was successful
        but can return the added data when `return_data` is True.

        Parameters
        -----------
        name: str
            The key.
        value: Any
            The value.
        return_data: bool
            Whether to return the added data instead of a bool.
            This creates an extra request by calling the `get` method. Defaults to False.

        Raises
        --------
        OnCooldown
            You are on a cooldown.

        Returns
        --------
         Union[bool, Result]
            Boolean value of whether the addition was successful or
            an instance of `Result()` if `return_data` is set to True
        """
        result = await self._request.set(name, value)
        if return_data:
            if self.__auto_retry_value is True:
                return await self.get(name)
            else:
                try:
                    await sleep(1)
                    result = await self.get(name)
                except OnCooldown:  # try again.
                    result = await self.get(name)

                return result

        return True if result.get('success', False) is True else False

    async def add(self, name: str, value: int, /) -> Result:
        """Add x amount to a key with integer value.

        .. note::

            The value of the input AND key must be an integer else this will fail.

        Parameters
        -----------
        name: str
            The key.
        value: Any
            The value.

        Raises
        --------
        BadRequest
            The input or the key value is not an integer.

        OnCooldown
            You are on a cooldown.

        Returns
        --------
        Result
            An instance of `Result()` which has a special attribute called `number` to get the new value of the key.
        """
        if not isinstance(value, int):
            raise TypeError("value must be a valid integer.")

        result = await self._request.add(name, value)
        return Result(result)

    async def subtract(self, name: Any, value: int, /):
        """Substract x amount from a key with integer value.

        .. note::

            The value of the input AND key must be an integer else this will fail.

        Parameters
        -----------
        name: str
            The key.
        value: Any
            The value.

        Raises
        --------
        BadRequest
            The input or the key value is not an integer.

        OnCooldown
            You are on a cooldown.

        Returns
        --------
        Result
            An instance of `Result()` which has a special attribute called `number` to get the new value of the key.
        """
        if not isinstance(value, int):
            raise TypeError("value must be a valid integer.")

        result = await self._request.subtract(name, value)
        return Result(result)

    async def close(self) -> None:
        await self._request.close()
