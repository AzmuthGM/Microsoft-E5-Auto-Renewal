import asyncio
import httpx
import logging
import random
from config import Config
from utils.notify import send_telegram
from datetime import datetime

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

        # Gửi request lấy token
        response = await cls.instance.post(cls.token_endpoint, headers=headers, data=data)

        # Thử parse JSON kết quả
        try:
            # httpx.Response.json() là sync, không await
            result = response.json()
        except Exception:
            # Nếu parse JSON lỗi, đọc raw bytes
            body_bytes = await response.aread()
            body_text = body_bytes.decode(errors="ignore")
            result = {
                "error": "Invalid JSON",
                "text": body_text
            }

        # Kiểm tra kết quả
        if "access_token" not in result:
            print("[ERROR] Token response error:")
            print(f"[DEBUG] Status: {response.status_code}")
            print(f"[DEBUG] Response: {result}")
            send_telegram(f"❌ Không lấy được token. Phản hồi từ server:\n{result}")
            return None

        # Trả về access token
        return result.get("access_token")

    @classmethod
    async def call_endpoints(cls, access_token: str):
        random.shuffle(cls.graph_endpoints)
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        for endpoint in cls.graph_endpoints:
            await asyncio.sleep(TIME_DELAY)
            try:
                response = await cls.instance.get(endpoint, headers=headers)
                print(f"[OK] Accessed: {endpoint} ({response.status_code})")
            except Exception as e:
                print(f"[WARN] Failed: {endpoint} - {e}")

        # Gửi thông báo Telegram sau khi hoàn tất vòng lặp
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        send_telegram(f"✅ Gia hạn E5 thành công lúc {now}. Tài khoản vẫn đang hoạt động.")

async def main():
    print("[Start] Starting activity simulation...")
    token = await HTTPClient.acquire_access_token()
    if token:
        await HTTPClient.call_endpoints(token)
    else:
        print("[FAIL] Failed to acquire access token. Check credentials.")
        send_telegram("❌ Không lấy được access token. Có thể sai REFRESH_TOKEN hoặc CLIENT_SECRET.")

if __name__ == "__main__":
    asyncio.run(main())
