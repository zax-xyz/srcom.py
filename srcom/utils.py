def get_uri(rel, links):
    return next(link["uri"] for link in links if link["rel"] == rel)


async def get_link(obj, rel, params=None):
    uri = get_uri(rel, obj._links)
    return await obj._http._get(uri, params)


async def get_data(obj, rel, params=None):
    return (await get_link(obj, rel, params))["data"]


def safeget(dct, keys, default=None):
    # derived from https://stackoverflow.com/a/25833661/14053758
    for key in keys:
        try:
            dct = dct[key]
        except (KeyError, TypeError):
            return default
    return dct
