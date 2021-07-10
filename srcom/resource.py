class Resource:

    endpoint = None

    def __init__(self, data, http):
        self._http = http
        self.id = data.get('id')
        self.link = data['weblink']
        self._links = data.get('links')

    def __eq__(self, other):
        return self.id == other.id

    @classmethod
    async def from_id(cls, id, http):
        resp = await http.get(f'{cls.endpoint}/{id}')
        return cls(resp['data'], http)
