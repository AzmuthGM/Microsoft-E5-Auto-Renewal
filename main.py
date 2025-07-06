import asyncio
import httpx
import logging
import random
from config import Config

TIME_DELAY = Config.TIME_DELAY

class HTTPClient:
    token_endpoint = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
    graph_endpoints = [
        'https://graph.microsoft.com/v1.0/me/drive/root',
        'https://graph.microsoft.com/v1.0/me/messages',
        'https://graph.microsoft.com/v1.0/me/events',
    ]
    instance = httpx.AsyncClient()

    @classmethod
    async def acquire_access_token(cls):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'client_id': Config.CLIENT_ID,
            'client_secret': Config.CLIENT_SECRET,
            'grant_type': 'refresh_token',
            'refresh_token': Config.REFRESH_TOKEN,
            'redirect_uri': Config.REDIRECT_URI
        }
        response = await cls.instance.post(cls.token_endpoint, headers=headers, data=data)
        try:
            result = response.json()
        except Exception:
            result = {"error": "Invalid JSON", "text": await response.aread()}

        if "access_token" not in result:
            print("[ERROR] Token response error:")
            print(result)
        return result.get("access_token")

    @classmethod
    async def call_endpoints(cls, access_token: str):
        random.shuffle(cls.graph_endpoints)
        headers = {
            'Authorization': access_token,
            'Content-Type': 'application/json'
        }
        for endpoint in cls.graph_endpoints:
            await asyncio.sleep(TIME_DELAY)
            try:
                await cls.instance.get(endpoint, headers=headers)
                print(f"[OK] Accessed: {endpoint}")
            except Exception as e:
                print(f"[WARN] Failed: {endpoint} - {e}")


async def main():
    print("[Start] Starting activity simulation...")
    token = await HTTPClient.acquire_access_token()
    if token:
        await HTTPClient.call_endpoints(token)
    else:
        print("[FAIL] Failed to acquire access token. Check credentials.")


if __name__ == "__main__":
    asyncio.run(main())
