import re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ഇവിടെ ചാനൽ ഐഡികൾ അല്ലെങ്കിൽ യൂസർനെയിമുകൾ നൽകുക
CHANNELS = [-1002015288592]     # ഫയലുകൾ പരിശോധിക്കേണ്ട ചാനൽ ഐഡി
AUTH_CHANNEL = -1002110922261   # പോസ്റ്റും ഫോട്ടോയും അയക്കേണ്ട ചാനൽ ഐഡി

# സീരിയൽ മാപ്പിംഗ് ഡാറ്റ
SERIALS_MAPPING = {
    "kanmashi": "Kanmashi",
    "karnan": "Karnan",
    "valyettan": "Valyettan",
    "pranayavilasam": "Pranayavilasam",
    "durga": "Durga",
    "chembarathy": "Chembarathy",
    "saregamapa": "SaReGaMaPa",
    "saregamapa_lil_champs": "SaReGaMaPa Lil Champs",
    "kudumbasametham": "Kudumbasametham",
    "meghasandhesham": "Meghasandhesham",
    "seethayanam": "Seethayanam",
    "krishnagadha": "Krishnagadha",
    "meghasandesam": "Meghasandesam",
    "aval_arundhati": "Aval Arundhati",
    "akale": "Akale",
    "snehapoorvam_shyama": "Snehapoorvam Shyama",
    "mangalyam": "Mangalyam",
    "manathe_kottaram": "Manathe Kottaram",
    "ashwathi_nakshatram": "Ashwathi Nakshatram",
    "kudumbashree_sharada": "Kudumbashree Sharada",
    "bigg_boss": "Bigg Boss",
    "taste_time": "Taste Time",
    "sindhu_bhairavi": "Sindhu Bhairavi",
    "comedy_cooks": "Comedy Cooks",
    "ivar_vivahitharayal": "Ivar Vivahitharayal",
    "oru_kochu_swapnam": "Oru Kochu Swapnam",
    "advocate_anjali": "Advocate Anjali",
    "kattathe_kilikoodu": "Kattathe Kilikoodu",
    "ee_puzhayum_kadannu": "Ee Puzhayum Kadannu",
    "sindoorapottu": "Sindoorapottu",
    "star_singer": "Star Singer",
    "teacheramma": "Teacheramma",
    "mazha_thorum_munpe": "Mazha Thorum Munpe",
    "pavithram": "Pavithram",
    "ishtam_mathram": "Ishtam Mathram",
    "santhwanam": "Santhwanam",
    "snehakkoottu": "Snehakkoottu",
    "mounaragam": "Mounaragam",
    "patharamattu": "Patharamattu",
    "amma_manassu": "Amma Manassu",
    "chempaneer_poovu": "Chempaneer Poovu",
    "dharmma_yoddhavu_garudan": "Dharmma Yoddhavu Garudan",
    "othiri_othiri_swapnangal": "Othiri Othiri Swapnangal",
    "ottashikharam": "Ottashikharam",
    "archana_chechi_llb": "Archana Chechi LLB",
    "super_kanmani": "Super Kanmani",
    "marimayam": "Marimayam",
    "oru_chiri_iru_chiri_bumper_chiri": "Oru Chiri Iru Chiri Bumper Chiri",
    "the_great_family_challenge": "The Great Family Challenge",
    "roopavathi": "Roopavathi",
    "thenmavin_kombath": "Thenmavin Kombath",
    "punnaram": "Punnaram",
    "anju_sundarikal": "Anju Sundarikal",
    "amme_mookambike": "Amme Mookambike",
    "peythozhiyathe": "Peythozhiyathe",
    "chattambipparu": "Chattambipparu",
    "hridayam": "Hridayam",
    "kanyadaanam": "Kanyadaanam",
    "swayamavarapanthal": "Swayamavarapanthal",
    "mangalyam_thanthunanena": "Mangalyam Thanthunanena"
}

# Get File Links Dictionary (Allutvbot ആക്കി മാറ്റിയ ലിങ്കുകൾ)
GET_FILE_LINKS_DICT = {
    "kanmashi": "https://telegram.me/Allutvbot?start=getfile-Kanmashi",
    "karnan": "https://telegram.me/Allutvbot?start=getfile-Karnan",
    "valyettan": "https://telegram.me/Allutvbot?start=getfile-Valyettan",
    "pranayavilasam": "https://telegram.me/Allutvbot?start=getfile-Pranayavilasam",
    "durga": "https://telegram.me/Allutvbot?start=getfile-Durga",
    "chembarathy": "https://telegram.me/Allutvbot?start=getfile-Chembarathy",
    "saregamapa": "https://telegram.me/Allutvbot?start=getfile-SaReGaMaPa",
    "saregamapa_lil_champs": "https://telegram.me/Allutvbot?start=getfile-SaReGaMaPa-Lil-Champs",
    "kudumbasametham": "https://telegram.me/Allutvbot?start=getfile-Kudumbasametham",
    "meghasandhesham": "https://telegram.me/Allutvbot?start=getfile-Meghasandhesham",
    "seethayanam": "https://telegram.me/Allutvbot?start=getfile-Seethayanam",
    "krishnagadha": "https://telegram.me/Allutvbot?start=getfile-Krishnagadha",
    "meghasandesam": "https://telegram.me/Allutvbot?start=getfile-Meghasandesam",
    "aval_arundhati": "https://telegram.me/Allutvbot?start=getfile-Aval-Arundhati",
    "akale": "https://telegram.me/Allutvbot?start=getfile-Akale",
    "snehapoorvam_shyama": "https://telegram.me/Allutvbot?start=getfile-Snehapoorvam-Shyama",
    "mangalyam": "https://telegram.me/Allutvbot?start=getfile-Mangalyam",
    "manathe_kottaram": "https://telegram.me/Allutvbot?start=getfile-Manathe-Kottaram",
    "ashwathi_nakshatram": "https://telegram.me/Allutvbot?start=getfile-Ashwathi-Nakshatram",
    "kudumbashree_sharada": "https://telegram.me/Allutvbot?start=getfile-Kudumbashree-Sharada",
    "bigg_boss": "https://telegram.me/Allutvbot?start=getfile-Bigg-Boss",
    "taste_time": "https://telegram.me/Allutvbot?start=getfile-Taste-Time",
    "sindhu_bhairavi": "https://telegram.me/Allutvbot?start=getfile-Sindhu-Bhairavi",
    "comedy_cooks": "https://telegram.me/Allutvbot?start=getfile-Comedy-Cooks",
    "ivar_vivahitharayal": "https://telegram.me/Allutvbot?start=getfile-Ivar-Vivahitharayal",
    "oru_kochu_swapnam": "https://telegram.me/Allutvbot?start=getfile-Oru-Kochu-Swapnam",
    "advocate_anjali": "https://telegram.me/Allutvbot?start=getfile-Advocate-Anjali",
    "kattathe_kilikoodu": "https://telegram.me/Allutvbot?start=getfile-Kattathe-Kilikoodu",
    "ee_puzhayum_kadannu": "https://telegram.me/Allutvbot?start=getfile-Ee-Puzhayum-Kadannu",
    "sindoorapottu": "https://telegram.me/Allutvbot?start=getfile-Sindoorapottu",
    "star_singer": "https://telegram.me/Allutvbot?start=getfile-Star-Singer",
    "teacheramma": "https://telegram.me/Allutvbot?start=getfile-Teacheramma",
    "mazha_thorum_munpe": "https://telegram.me/Allutvbot?start=getfile-Mazha-Thorum-Munpe",
    "pavithram": "https://telegram.me/Allutvbot?start=getfile-Pavithram",
    "ishtam_mathram": "https://telegram.me/Allutvbot?start=getfile-Ishtam-Mathram",
    "santhwanam": "https://telegram.me/Allutvbot?start=getfile-Santhwanam",
    "snehakkoottu": "https://telegram.me/Allutvbot?start=getfile-Snehakkoottu",
    "mounaragam": "https://telegram.me/Allutvbot?start=getfile-Mounaragam",
    "patharamattu": "https://telegram.me/Allutvbot?start=getfile-Patharamattu",
    "amma_manassu": "https://telegram.me/Allutvbot?start=getfile-Amma-Manassu",
    "chempaneer_poovu": "https://telegram.me/Allutvbot?start=getfile-Chempaneer-Poovu",
    "dharmma_yoddhavu_garudan": "https://telegram.me/Allutvbot?start=getfile-Dharmma-Yoddhavu-Garudan",
    "othiri_othiri_swapnangal": "https://telegram.me/Allutvbot?start=getfile-Othiri-Othiri-Swapnangal",
    "ottashikharam": "https://telegram.me/Allutvbot?start=getfile-Ottashikharam",
    "archana_chechi_llb": "https://telegram.me/Allutvbot?start=getfile-Archana-Chechi-LLB",
    "super_kanmani": "https://telegram.me/Allutvbot?start=getfile-Super-Kanmani",
    "marimayam": "https://telegram.me/Allutvbot?start=getfile-Marimayam",
    "oru_chiri_iru_chiri_bumper_chiri": "https://telegram.me/Allutvbot?start=getfile-Oru-Chiri-Iru-Chiri-Bumper-Chiri",
    "the_great_family_challenge": "https://telegram.me/Allutvbot?start=getfile-The-Great-Family-Challenge",
    "roopavathi": "https://telegram.me/Allutvbot/roopavathi",
    "thenmavin_kombath": "https://telegram.me/Allutvbot?start=getfile-Thenmavin-Kombath",
    "punnaram": "https://telegram.me/Allutvbot?start=getfile-Punnaram",
    "anju_sundarikal": "https://telegram.me/Allutvbot?start=getfile-Anju-Sundarikal",
    "amme_mookambike": "https://telegram.me/Allutvbot?start=getfile-Amme-Mookambike",
    "peythozhiyathe": "https://telegram.me/Allutvbot?start=getfile-Peythozhiyathe",
    "chattambipparu": "https://telegram.me/Allutvbot?start=getfile-Chattambipparu",
    "hridayam": "https://telegram.me/Allutvbot?start=getfile-Hridayam",
    "kanyadaanam": "https://telegram.me/Allutvbot?start=getfile-Kanyadaanam",
    "swayamavarapanthal": "https://telegram.me/Allutvbot?start=getfile-Swayamavarapanthal",
    "mangalyam_thanthunanena": "https://telegram.me/Allutvbot?start=getfile-Mangalyam-Thanthunanena"
}

# ഓട്ടോ പോസ്റ്റ് ഫോർമാറ്റർ കോഡ്
@Client.on_message(filters.chat(CHANNELS) & (filters.document | filters.video))
async def auto_post_formatter(client, message):
    try:
        # ഫയലിന്റെ ഒറിജിനൽ പേര് സുരക്ഷിതമായി എടുക്കുന്നു
        if message.document:
            file_name_raw = message.document.file_name
        elif message.video:
            file_name_raw = message.video.file_name or "Media File"
        else:
            return

        # ഫയൽ നാമത്തിലുള്ള എക്സ്റ്റൻഷൻ നീക്കം ചെയ്യുന്നു
        file_name_clean_ext = re.sub(r'\.(mkv|mp4|avi|mov)$', '', file_name_raw, flags=re.IGNORECASE)
        raw_lower = file_name_clean_ext.lower()
        
        matched_key = None
        matched_display_name = "Malayalam Serial"

        # SERIALS_MAPPING-മായി ഫയൽ പേര് ഒത്തുനോക്കുന്നു
        for key, display_name in SERIALS_MAPPING.items():
            key_words = key.split('_')
            if all(word in raw_lower for word in key_words):
                matched_key = key
                matched_display_name = display_name
                break

        # മാപ്പിംഗിൽ കിട്ടിയില്ലെങ്കിൽ സാധാരണ രീതിയിൽ ക്ലീൻ ചെയ്യുന്നു
        if not matched_key:
            clean_name = re.sub(r's\d+|season\s*\d+|e\d+|episode\s*\d+|\d{3,4}p|WEB|HDRip|H\.264|AAC', '', file_name_clean_ext, flags=re.IGNORECASE).strip()
            clean_name = clean_name.replace('.', ' ').replace('_', ' ').strip()
            matched_display_name = clean_name if clean_name else "Malayalam Serial"
            matched_key = re.sub(r'[^a-zA-Z0-9]', '_', matched_display_name).lower()

        # Season കണ്ടെത്താൻ
        season_match = re.search(r'(?:s|season\s*)(\d+)', file_name_raw, re.IGNORECASE)
        season = season_match.group(1).zfill(2) if season_match else "01"

        # Episode കണ്ടെത്താൻ
        episode_match = re.search(r'(?:e|episode\s*|\bep\s*)(\d+)', file_name_raw, re.IGNORECASE)
        episode_num = episode_match.group(1) if episode_match else "1"

        # Quality കണ്ടെത്താൻ
        quality_match = re.search(r'(\d{3,4}p)', file_name_raw, re.IGNORECASE)
        quality = quality_match.group(1) if quality_match else "720p"

        # ക്യാപ്ഷൻ ഫോർമാറ്റ്
        caption = (
            f"📁 **File Name :** {matched_display_name}\n"
            f"🎞️ **Season :** {season}\n"
            f"📌 **Episode :** {episode_num}\n"
            f"🎬 **Quality :** {quality}"
        )

        # GET_FILE_LINKS_DICT-ൽ നിന്ന് link എടുക്കുന്നു
        bot_link = GET_FILE_LINKS_DICT.get(matched_key, f"https://telegram.me/Allutvbot?start=getfile-{matched_display_name.replace(' ', '-')}")

        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("📥 Get File", url=bot_link)]]
        )

        BANNER_PHOTO = "https://ibb.co/cS5zrTGD"

        # അപ്ഡേറ്റ് ചാനലിലേക്ക് ഫോട്ടോയും ക്യാപ്ഷനും അയക്കുന്നു
        await client.send_photo(
            chat_id=AUTH_CHANNEL,
            photo=BANNER_PHOTO,
            caption=caption,
            reply_markup=reply_markup
        )

    except Exception as e:
        print(f"Auto-Formatter Error: {e}")
