from aiohttp import ClientSession, TCPConnector
from core.settings import CONNECTION_LIMIT


class CustomClientSession(ClientSession):
    _connector = TCPConnector(limit_per_host=CONNECTION_LIMIT)
