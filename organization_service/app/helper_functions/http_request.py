import httpx

from requests import exceptions


async def send_request(url, method, params={}, data={}):
    try:
        async with httpx.AsyncClient() as client:
            if method == "post":
                response = await client.post(url=url, json=data, params=params, timeout=8)
            elif method == "get":
                response = await client.get(url=url, params=params, timeout=8)
            elif method == "delete":
                response = await client.delete(url=url, params=params, timeout=8)
    except exceptions.ConnectionError as e:
        raise e
    except Exception as e:
        raise e
    return response.json()
