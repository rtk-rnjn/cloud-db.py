import json
from asyncio import sleep
from typing import Any, ClassVar, Coroutine, Dict, Literal, TypeVar, Union

from aiohttp import ClientResponse, ClientSession

from .errors import BadRequest, HTTPException, NotFound, OnCooldown

HC = TypeVar('HC', bound = 'HTTPClient')
Method = Literal["GET", "DELETE", "POST", "PATCH"]
Endpoint = Literal["all", "set", "get", "delete", "add", "subtract"]


async def json_or_text(response: ClientResponse) -> Union[Dict[str, Any], str]:
    text = await response.text(encoding = 'utf-8')
    JSON_CONTENT_TYPE: str = 'application/json'
    if response.headers.get('content-type', '') == JSON_CONTENT_TYPE or response.content_type == JSON_CONTENT_TYPE:
        return json.loads(text)

    return text


class HTTPClient:
    __slots__ = ("_key", "_session", "_auto_retry")
    BASE: ClassVar[str] = "https://cloud-db.ml/"

    def __init__(self, key: str, /, *, auto_retry: bool = False, session: ClientSession = None) -> None:
        self._key = key
        self._auto_retry = auto_retry
        self._session = session

    # Aiohttp client sessions must be created in async functions
    async def _create_session(self) -> None:
        self._session = ClientSession()

    async def request(
            self: HC,
            endpoint: Endpoint,
            method: Method = "GET",
            *,
            name: str = None,
            value: Any = None
    ) -> Dict[str, Any]:
        if self._session is None:
            await self._create_session()

        extras: Dict[str, Any] = {}
        if value:
            extras['json'] = {"value": value}

        header = {"Authorization": str(self._key)}
        url = f"{self.BASE}/{endpoint}"
        if name is not None:
            url += f"?name={name}"

        async with self._session.request(method, url, headers = header, **extras) as res:
            data = await json_or_text(res)

            if res.status == 200:
                return await res.json()

            # Raise a special exception for cooldown.
            if res.status == 403 or isinstance(data, dict) and "Cooldown" in data["message"]:
                if self._auto_retry:
                    await sleep(1)  # wait 1 second and try again.
                    return await self.request(endpoint, method, name = name, value = value)

                raise OnCooldown(data["message"])

            if res.status == 404:
                raise NotFound(data)
            elif res.status == 400:
                if isinstance(data, dict) and data["message"] == "The Data is not a Number":
                    msg = f"The value of \"{name}\" is not a number"
                else:
                    msg = data
                raise BadRequest(msg)
            else:
                raise HTTPException(res.status, data)

    def get(self, name: str):
        return self.request("get", "GET", name = str(name))

    def delete(self, name: str):
        return self.request("delete", "DELETE", name = str(name))

    def all(self):
        return self.request("all")

    def set(self, name: str, value: Any):
        return self.request("set", "POST", name = str(name), value = value)

    def add(self, name: str, value: int):
        return self.request("add", "PATCH", name = str(name), value = value)

    def subtract(self, name: Any, value: int):
        return self.request("subtract", "PATCH", name = str(name), value = value)

    async def close(self) -> None:
        if self._session:
            if not self._session.closed:
                await self._session.close()
