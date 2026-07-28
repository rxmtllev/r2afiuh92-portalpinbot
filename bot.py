import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
import json
import os

BOT_TOKEN = "8337116890:AAGETZWBZVVNnUtQFIHAtZ_h8lxHu6cuuG4"
ADMIN_ID = 5866652107
CHANNEL_ID = -1003791438142

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

def get_internal_user_id(telegram_id):
    filename = 'users.json'
    if not os.path.exists(filename):
        data = {"users": {}, "next_id": 1000}
    else:
        with open(filename, 'r') as f:
            data = json.load(f)
            
    tg_id_str = str(telegram_id)
    if tg_id_str not in data["users"]:
        data["users"][tg_id_str] = data["next_id"]
        data["next_id"] += 1
        with open(filename, 'w') as f:
            json.dump(data, f)
            
    return data["users"][tg_id_str]

# func.php dagi inlinekey funksiyasining analogi
def inlinekey(text, cb_data, icon_id="0", style="default", url=None):
    if url:
        btn = InlineKeyboardButton(text=text, url=url)  # type: ignore
    else:
        btn = InlineKeyboardButton(text=text, callback_data=cb_data)  # type: ignore
        
    # Rasmiy Telegram API da tugma rangi yo'q bo'lsa-da, 
    # ba'zi maxsus mijozlar (client) o'qishi uchun xuddi PHP dagi kabi JSON ga qo'shamiz:
    orig_to_dict = btn.to_dict
    def custom_to_dict():
        d = orig_to_dict()
        d['icon_custom_emoji_id'] = icon_id
        d['style'] = style
        return d
    
    btn.to_dict = custom_to_dict
    return btn


@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = InlineKeyboardMarkup()
    
    # 1-qator
    markup.row(
        inlinekey("Xisob toldirish", "xisob_toldirish", "5443127283898405358", "default"), 
        inlinekey("Xisobim", "xisobim", "4972482444025398275", "default")
    )
    # 2-qator
    markup.row(
        inlinekey("Gram (ton) olish", "gram_olish", "5280908091410389246", "primary"), 
        inlinekey("Gram (ton) sotish", "gram_sotish", "5240228673738527951", "primary")
    )
    # 3-qator
    markup.row(
        inlinekey("Stars olish", "stars_olish", "5951810621887484519", "success"), 
        inlinekey("Stars sotish", "stars_sotish", "6014655953457123498", "success")
    )
    # 4-qator
    markup.row(
        inlinekey("Gift olish", "gift_olish", "6021710505960281699", "success"), 
        inlinekey("NFT gift sotish", "nft_sotish", "5150158575271674966", "success")
    )
    # 5-qator
    markup.row(
        inlinekey("USDT olish", "usdt_olish", "5287231198098117669", "success"), 
        inlinekey("USDT sotish", "usdt_sotish", "6014655953457123498", "success")
    )
    # 6-qator
    markup.row(
        inlinekey("Premium olish", "premium_olish", "6298821774423361023", "success"), 
        inlinekey("Kanal,gr sotish", "kanal_sotish", "5316847419965579451", "success")
    )
    # 7-qator
    markup.row(
        inlinekey("Pubg uc olish", "pubg_olish", "5397808249279909223", "danger"), 
        inlinekey("SMM xizmatlari", "smm_xizmatlari", "5460689598445273231", "danger")
    )
    # 8-qator
    markup.row(
        inlinekey("Statistika", "stat", "5231200819986047254", "default"), 
        inlinekey("Admin", None, "5444965061749644170", "default", url="https://t.me/raxmatullayevic")
    )
    
    user = message.from_user
    username_text = f"@{user.username}" if user.username else user.first_name
    
    # Yangi foydalanuvchiga 1000 dan boshlanuvchi ID beramiz
    internal_id = get_internal_user_id(user.id)
    
    caption_text = f"""<tg-emoji emoji-id="5458603043203327669">👋</tg-emoji> Xush kelibsiz, {username_text}

<tg-emoji emoji-id="5456140674028019486">⚡️</tg-emoji> Qulay interfeys
<tg-emoji emoji-id="5456140674028019486">⚡️</tg-emoji> Qulay to'lov
<tg-emoji emoji-id="5456140674028019486">⚡️</tg-emoji> To'liq avtomatlashtirilgan xizmat

User ID: {internal_id}

Pastdagi tugmani bosing va hoziroq boshlang <tg-emoji emoji-id="5406745015365943482">⬇️</tg-emoji>"""
    
    # Rasmni yuborish (rasm fayli kod turgan papkada 'logo.jpg' nomida bo'lishi kerak)
    try:
        with open('logo.jpg', 'rb') as photo:
            bot.send_photo(
                chat_id=message.chat.id,
                photo=photo,
                caption=caption_text,
                reply_markup=markup
            )
    except FileNotFoundError:
        # Agar rasm topilmasa, oddiy xabar yuboradi
        bot.send_message(
            chat_id=message.chat.id,
            text=caption_text + "\n\n<i>(Rasm topilmadi, iltimos papkaga 'logo.jpg' faylini tashlang)</i>",
            reply_markup=markup
        )

@bot.message_handler(commands=['sendphoto'])
def sendphoto_handler(message):
    markup = InlineKeyboardMarkup()
    markup.add(inlinekey("🏠", "1"))
    
    bot.send_photo(
        chat_id=message.chat.id,
        photo="https://t.me/photoaibeck/10",
        caption="<b>Salom</b>",
        reply_markup=markup
    )

@bot.message_handler(commands=['da'])
def da_handler(message):
    markup = InlineKeyboardMarkup()
    markup.add(inlinekey("🏠", "ans"))
    
    bot.send_message(
        chat_id=CHANNEL_ID,
        text="<b>Salom</b>",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "1":
        # Foydalanuvchini kanaldagi holatini tekshiramiz
        try:
            member = bot.get_chat_member(CHANNEL_ID, call.from_user.id)
            status = member.status
            
            if status in ['creator', 'administrator', 'member']:
                bot.answer_callback_query(call.id, text="Salom ey", show_alert=True)
            else:
                bot.answer_callback_query(
                    call.id, 
                    text="❌ Xato\n\nKerakli ma'lumotni olish uchun avval kanalga obuna bo‘ling", 
                    show_alert=True
                )
        except telebot.apihelper.ApiTelegramException:
            # Agar botning kanalda adminlik huquqi bo'lmasa xato beradi
            bot.answer_callback_query(call.id, text="Bot kanalda admin emas!", show_alert=True)

if __name__ == '__main__':
    # Menyu tugmasini sozlash (Menu Commands)
    bot.set_my_commands([
        BotCommand("start", "Botni yangilash")
    ])
    
    # PHP'dan (webhook) o'tganimiz uchun eski webhook'ni o'chirib tashlaymiz
    bot.remove_webhook()
    bot.polling(none_stop=True)
