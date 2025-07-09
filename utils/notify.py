import requests
import os

def send_telegram(message: str):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("❗ Thiếu TELEGRAM_TOKEN hoặc TELEGRAM_CHAT_ID.")
        return

    # ✅ Giới hạn độ dài message để tránh lỗi Telegram
    if len(message) > 4000:
        message = message[:4000] + "\n\n⚠️ [Truncated]"

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print("⚠️ Gửi tin nhắn Telegram thất bại:", response.text)
        else:
            print("✅ Đã gửi thông báo Telegram.")
    except Exception as e:
        print(f"❌ Lỗi khi gửi Telegram: {e}")
