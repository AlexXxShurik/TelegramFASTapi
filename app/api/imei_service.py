import httpx

async def check_imei_from_api(imei: str, token: str):
    url = 'https://api.imeicheck.net/v1/checks'

    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

    body = {
        "deviceId": imei,
        "serviceId": 1
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=body, headers=headers)

    return response
