import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

class TelegramBot:
    BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
    MAX_LENGTH = 4096

    def send_message(self, text: str) -> bool:
        print("\n📤 Sending to Telegram...\n")

        chunks = self._split_message(text)
        success = True

        for i, chunk in enumerate(chunks):
            print(f"\n🔁 Sending chunk {i+1}/{len(chunks)}...\n")
            print("Payload:\n", chunk[:500], "...\n" if len(chunk) > 500 else chunk)  # preview

            try:
                resp = requests.post(
                    f"{self.BASE_URL}/sendMessage",
                    json={
                        "chat_id": TELEGRAM_CHAT_ID,
                        "text": chunk,
                        "disable_web_page_preview": False,
                    },
                    timeout=20
                )
                if resp.status_code != 200:
                    print(f"❌ Failed to send chunk {i+1}. Error: {resp.status_code}")
                    print(resp.text)
                    success = False
                else:
                    print(f"✅ Chunk {i+1} sent!")
            except Exception as e:
                print(f"❌ Telegram error on chunk {i+1}: {e}")
                success = False

        return success

    def _split_message(self, message):
        if len(message) <= self.MAX_LENGTH:
            return [message]

        # Try to split by paragraphs first
        paragraphs = message.split('\n\n')
        chunks = []
        current = ""

        for para in paragraphs:
            if len(current) + len(para) + 2 <= self.MAX_LENGTH:
                current += para + "\n\n"
            else:
                chunks.append(current.strip())
                current = para + "\n\n"

        if current:
            chunks.append(current.strip())

        return chunks