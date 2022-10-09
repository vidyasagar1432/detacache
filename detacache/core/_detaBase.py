import typing
import aiohttp
import requests


class DetaBase:
    def __init__(self,projectKey: str ,baseName: str , projectId: str = None):
        if not "_" in projectKey:
            raise ValueError("Bad project key provided")

        if not projectId:
            projectId = projectKey.split("_")[0]
        
        self._headers = {
                "Content-type": "application/json",
                "X-API-Key": projectKey,
            }
        self._baseUrl = f'https://database.deta.sh/v1/{projectId}/{baseName}'

    def put(self, data: dict) -> dict:
        raise NotImplementedError

    def get(self, key: str) -> dict:
        raise NotImplementedError

class SyncBase(DetaBase):
    def __init__(self, projectKey: str, baseName: str, projectId: str = None):
        super().__init__(projectKey, baseName, projectId)

    def put(self, data: typing.Union[dict, list, str, int, bool],key: str = None) -> dict:
        if key:
            data["key"] = key
        with requests.Session() as _session:
            with _session.put(f"{self._baseUrl}/items", json={"items": [data]},headers=self._headers) as resp:
                return resp.json()["processed"]["items"][0]

    def get(self, key: str) -> dict:
        with requests.Session() as _session:
            with _session.get(f"{self._baseUrl}/items/{key}",headers=self._headers) as resp:
                _res = resp.json()
                return _res if len(_res) > 1 else None

class AsyncBase(DetaBase):
    def __init__(self, projectKey: str, baseName: str, projectId: str = None):
        super().__init__(projectKey, baseName, projectId)

    async def put(self, data: typing.Union[dict, list, str, int, bool],key: str = None)-> dict:
        if key:
            data["key"] = key
        async with aiohttp.ClientSession(headers=self._headers) as _session:
            async with _session.put(f"{self._baseUrl}/items", json={"items": [data]}) as resp:
                _res =  await resp.json()
                return _res["processed"]["items"][0]

    async def get(self, key: str)-> dict:
        async with aiohttp.ClientSession(headers=self._headers) as _session:
            async with _session.get(f"{self._baseUrl}/items/{key}") as resp:
                _res = await resp.json()
                return _res if len(_res) > 1 else None