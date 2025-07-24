import asyncio
import httpx
import logging
import random
from config import Config
from utils.notify import send_telegram
from datetime import datetime

# Cấu hình logging: ghi log mức INFO, hiển thị thời gian và mức cảnh báo
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

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
        # Gửi yêu cầu lấy token
        response = await cls.instance.post(cls.token_endpoint, headers=headers, data=data)
        try:
            result = response.json()
        except Exception:
            # Nếu JSON lỗi, đọc body thô
            body_bytes = await response.aread()
            body_text = body_bytes.decode(errors="ignore")
            result = {"error": "Invalid JSON", "text": body_text}
        # Kiểm tra kết quả
        if "access_token" not in result:
            logger.error("Token response error")
            logger.debug(f"Status: {response.status_code}")
            logger.debug(f"Response: {result}")
            # Thông báo Telegram khi lỗi token
            await send_telegram(f"❌ Không lấy được token. Phản hồi từ server:\n{result}")
            return None
        return result.get("access_token")

    @classmethod
    async def call_endpoints(cls, access_token: str):
        # Xáo trộn và gọi từng endpoint
        random.shuffle(cls.graph_endpoints)
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        results = []
        for endpoint in cls.graph_endpoints:
            await asyncio.sleep(TIME_DELAY)
            try:
                response = await cls.instance.get(endpoint, headers=headers)
                logger.info(f"[OK] Accessed {endpoint} (status={response.status_code})")
                # Ghi lại kết quả thành công
                results.append(f"✅ {endpoint.split('/v1.0/')[-1]}: {response.status_code}")
            except Exception as e:
                logger.warning(f"[WARN] Failed {endpoint}: {e}")
                # Ghi lại kết quả lỗi
                results.append(f"❗ {endpoint.split('/v1.0/')[-1]}: {e}")
        # Sau khi hoàn tất, gửi một tin nhắn Telegram tổng hợp
        summary = "\n".join(results)
        await send_telegram(f"Tổng hợp hoạt động E5:\n{summary}")

async def main():
    logger.info("[Start] Starting activity simulation...")
    token = await HTTPClient.acquire_access_token()
    if token:
        await HTTPClient.call_endpoints(token)
    else:
        logger.error("[FAIL] Failed to acquire access token. Check credentials.")
        await send_telegram("❌ Không lấy được access token. Có thể sai REFRESH_TOKEN hoặc CLIENT_SECRET.")

if __name__ == "__main__":
    asyncio.run(main())
