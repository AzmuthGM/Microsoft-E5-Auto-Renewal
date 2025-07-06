from httpx import AsyncClient as httpx_client
from asyncio import sleep as async_sleep
from random import shuffle
from config import *

class HTTPClient:
    instance = httpx_client()
    token_endpoint = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
    graph_endpoints = [
        'https://graph.microsoft.com/v1.0/me/drive/root',
        'https://graph.microsoft.com/v1.0/me/drive',
        'https://graph.microsoft.com/v1.0/drive/root',
        'https://graph.microsoft.com/v1.0/users',
        'https://graph.microsoft.com/v1.0/me/messages',
        'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules',
        'https://graph.microsoft.com/v1.0/me/drive/root/children',
        'https://api.powerbi.com/v1.0/myorg/apps',
        'https://graph.microsoft.com/v1.0/me/mailFolders',
        'https://graph.microsoft.com/v1.0/me/outlook/masterCategories',
        'https://graph.microsoft.com/v1.0/applications?$count=true',
        'https://graph.microsoft.com/v1.0/me/?$select=displayName,skills',
        'https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages/delta',
        'https://graph.microsoft.com/beta/me/outlook/masterCategories',
        'https://graph.microsoft.com/beta/me/messages?$select=internetMessageHeaders&$top=1',
        'https://graph.microsoft.com/v1.0/sites/root/lists',
        'https://graph.microsoft.com/v1.0/sites/root',
        'https://graph.microsoft.com/v1.0/sites/root/drives'
    ]

    @classmethod
    async def acquire_access_token(
        cls,
        refresh_token: str = None,
        client_id: str = None,
        client_secret: str = None
    ):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token or REFRESH_TOKEN,
            'client_id': client_id or CLIENT_ID,
            'client_secret': client_secret or CLIENT_SECRET,
            'redirect_uri': 'http://localhost:53682/'
        }

        response = await cls.instance.post(cls.token_endpoint, headers=headers, data=data)
        return response.json().get('access_token')

    @classmethod
    async def call_endpoints(cls, access_token: str):
        shuffle(cls.graph_endpoints)
        headers = {
            'Authorization': access_token,
            'Content-Type': 'application/json'
        }

        for endpoint in cls.graph_endpoints:
            await async_sleep(TIME_DELAY)
            try:
                await cls.instance.get(endpoint, headers=headers)
                print(f"✅ Accessed: {endpoint}")
            except Exception as e:
                print(f"⚠️ Failed: {endpoint} - {e}")

# ---------- Entry Point for GitHub Actions ----------

import asyncio

async def run_task_once():
    print("🚀 Starting activity simulation...")
    token = await HTTPClient.acquire_access_token()
    if not token:
        print("❌ Failed to acquire access token. Check credentials.")
        return
    await HTTPClient.call_endpoints(token)
    print("✅ Activity simulation completed!")

if __name__ == '__main__':
    asyncio.run(run_task_once())
