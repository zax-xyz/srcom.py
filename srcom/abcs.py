from . import client as srcom_client


class Resource:

    endpoint = None

    def __init__(self, data, http):
        self._http = http
        self.id = data.get("id")
        self.link = data.get("weblink")
        self._links = data.get("links")

    def __eq__(self, other):
        return self.id == other.id

    @classmethod
    async def from_id(cls, id, client=None):
        if client is None:
            client = srcom_client.Client()

        resp = await client.http.get(f"{cls.endpoint}/{id}")
        return cls(resp["data"], client.http)
