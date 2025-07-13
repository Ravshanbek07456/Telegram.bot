from pyrogram import Client, filters
import re

api_id = 22177060
api_hash = "85ad236b9c5d60ff7d523042a3512207"
bot_token = "7772718934:AAFgN7KTGDBruHd3FfrI3vRvGsX89xGzKcY"

app = Client("smart_cleaner_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Ko‘k yozuv bormi — tekshiruvchi funksiya
def has_blue_text(text):
    return bool(re.search(r'@\w+|t\.me/\S+', text))

# Ko‘k yozuvni matndan olib tashlaydi
def clean_text(text):
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'https?://t\.me/\S+', '', text)
    return text.strip()

@app.on_message(filters.channel)
async def handle_post(client, message):
    try:
        text = message.text or message.caption

        if text and has_blue_text(text):
            cleaned = clean_text(text)

            # Post turi: rasm, video, fayl, matn — tekshiradi
            if message.photo:
                await client.delete_messages(message.chat.id, message.id)
                await client.send_photo(message.chat.id, message.photo.file_id, caption=cleaned)
            elif message.video:
                await client.delete_messages(message.chat.id, message.id)
                await client.send_video(message.chat.id, message.video.file_id, caption=cleaned)
            elif message.document:
                await client.delete_messages(message.chat.id, message.id)
                await client.send_document(message.chat.id, message.document.file_id, caption=cleaned)
            elif message.text:
                await client.delete_messages(message.chat.id, message.id)
                await client.send_message(message.chat.id, cleaned)
            else:
                print("ℹ️ Qo‘llab-quvvatlanmaydigan post turi.")
        else:
            print("✅ Toza post yoki hech qanday ko‘k yozuv yo‘q.")

    except Exception as e:
        print(f"❌ Xatolik: {e}")

app.run()