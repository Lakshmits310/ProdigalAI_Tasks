from bots.telegram import TelegramBot

msg = "*Bold Title* with some _italic text_ and a [link](https://example.com)"
TelegramBot().send_message(msg)
