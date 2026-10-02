import re
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# 1. നിങ്ങളുടെ ഡാറ്റാബേസ് ചാനൽ ഐഡിയും അപ്ഡേറ്റ് ചാനൽ ഐഡിയും ഇവിടെ നൽകുക
CHANNELS = -1004363261958         # ഡാറ്റാബേസ് ചാനൽ ഐഡി
UPDATE_CHANNEL_ID = -1009876543210 # അപ്ഡേറ്റ് ചാനൽ ഐഡി

def parse_media_info(file_name):
    season = "01"
    episode = "Unknown"
    quality = "720p"
    
    clean_filename = re.sub(r'\.(mkv|mp4|avi|mov)$', '', file_name, flags=re.IGNORECASE)
    
    s_match = re.search(r'(?:s|season\s*)(\d+)', clean_filename, re.IGNORECASE)
    if s_match:
        season = s_match.group(1).zfill(2)
        
    ep_match = re.search(r'(?:ep|episode|\b)?\s*(\d+(?:\s*-\s*\d+)?)', clean_filename, re.IGNORECASE)
    if ep_match:
        episode = ep_match.group(1).replace(" ", "")
        
    q_match = re.search(r'(\d{3,4}p)', clean_filename, re.IGNORECASE)
    if q_match:
        quality = q_match.group(1)
        
    show_name = re.sub(r'\[.*?\]|\{.*?\}|\(.*?\)|720p|1080p|480p|s\d+|season\s*\d+|ep\s*\d+', '', clean_filename, flags=re.IGNORECASE).strip()
    show_name = " ".join(show_name.split())
    
    if not show_name:
        show_name = "Malayalam Serials"
        
    return show_name, season, episode, quality

# 2. ഡാറ്റാബേസ് ചാനലിൽ ഫയൽ വരുമ്പോൾ ഓട്ടോമാറ്റിക്കായി അപ്ഡേറ്റ് ചാനലിലേക്ക് പോസ്റ്റ് ചെയ്യുന്ന ഭാഗം
@Client.on_message(filters.chat(CHANNELS) & (filters.document | filters.video))
async def auto_update_handler(client: Client, message: Message):
    try:
        media = message.document or message.video
        if not media:
            return
            
        file_name = getattr(media, "file_name", None)
        if not file_name:
            file_name = message.caption if message.caption else "Unknown File"
            
        show_name, season, episode, quality = parse_media_info(file_name)
        
        caption_text = (
            f"<b>Malayalam Serials</b>\n\n"
            f"📁 <b>File Name :</b> {show_name}\n"
            f"🎞 <b>Season :</b> {season}\n"
            f"📌 <b>Episode :</b> {episode}\n"
            f"🎬 <b>Quality :</b> {quality}"
        )
        
        bot_username = (await client.get_me()).username
        
        # ഓരോ ഫയലിനും യൂണീക്ക് ആയി കിട്ടുന്ന മെസ്സേജ് ഐഡി വെച്ച് ലിങ്ക് ഉണ്ടാക്കുന്നു
        msg_id = message.id
        
        # ഗെറ്റ് ഫയൽ ബട്ടൺ
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📥 Get File", url=f"https://t.me/{bot_username}?start=file_{msg_id}")]
        ])
        
        await client.send_message(
            chat_id=UPDATE_CHANNEL_ID,
            text=caption_text,
            reply_markup=keyboard
        )
        
    except Exception as e:
        print(f"Auto Update Error: {e}")

# 3. അപ്ഡേറ്റ് ചാനലിലെ ബട്ടൺ ക്ലിക്ക് ചെയ്ത് വരുമ്പോൾ ഡാറ്റാബേസ് ചാനലിൽ നിന്ന് ഫയൽ എടുത്ത് യൂസർക്ക് അയച്ചു കൊടുക്കുന്ന ഭാഗം
@Client.on_message(filters.command("start") & filters.private)
async def send_file_via_link(client: Client, message: Message):
    try:
        if len(message.command) > 1:
            parameter = message.command[1]
            
            # 'file_' എന്ന് തുടങ്ങുന്ന ലിങ്ക് ആണെങ്കിൽ വർക്ക് ചെയ്യും
            if parameter.startswith("file_"):
                msg_id_str = parameter.replace("file_", "")
                if msg_id_str.isdigit():
                    msg_id = int(msg_id_str)
                    
                    # ഡാറ്റാബേസ് ചാനലിൽ നിന്ന് ആ മെസ്സേജ് (ഫയൽ) കോപ്പി ചെയ്ത് യൂസർക്ക് അയക്കുന്നു
                    await client.copy_message(
                        chat_id=message.chat.id,
                        from_chat_id=CHANNELS,
                        message_id=msg_id
                    )
                    return
                    
        # സാധാരണ സ്റ്റാർട്ട് മെസ്സേജ്
        await message.reply_text(
            "ഹലോ! അപ്ഡേറ്റ് ചാനലിൽ നൽകിയിരിക്കുന്ന 'Get File' ബട്ടൺ വഴി നിങ്ങൾക്ക് ആവശ്യമായ ഫയലുകൾ ഡൗൺലോഡ് ചെയ്യാവുന്നതാണ്."
        )
        
    except Exception as e:
        await message.reply_text("ക്ഷമിക്കണം, ഈ ഫയൽ കണ്ടെത്താൻ കഴിഞ്ഞില്ല അല്ലെങ്കിൽ ലിങ്ക് എക്സ്പയർ ആയിട്ടുണ്ട്.")
        print(f"Send File Link Error: {e}")
