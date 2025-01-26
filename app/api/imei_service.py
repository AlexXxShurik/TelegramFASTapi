import os

import httpx
from dotenv import load_dotenv

load_dotenv()
LIVE_API_TOKEN = os.getenv("LIVE_API_TOKEN")


async def check_imei_from_api(imei: str):
    url = 'https://api.imeicheck.net/v1/checks'

    headers = {
        'Authorization': 'Bearer ' + LIVE_API_TOKEN,
        'Content-Type': 'application/json'
    }

    body = {
        "deviceId": imei,
        "serviceId": 1
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=body, headers=headers)

    return response
