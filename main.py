import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
from datetime import datetime
from flask import Flask, request

TOKEN = "8952729513:AAGP1kxZmZEWD6L2vkQ4_EzNL2vOtJsyQPQ"
OWNER_ID = 6530901319
bot = telebot.TeleBot(TOKEN, threaded=False)

app = Flask(__name__)

DIGITS_DATA = {
    "buy_1kwet": "🎯 လူကြီးမင်း ဝယ်ယူထားသော [တစ်ကွက်ကောင်း] - ( 25 ) အပိုင်ရိုက်ပါဗျာ။",
    "buy_4lone": "📊 လူကြီးမင်း ဝယ်ယူထားသော [၄လုံးအခွေ] - ( 1, 3, 5, 7 ) အပိုင်ပတ်ပါဗျာ။",
    "buy_bk": "💥 လူကြီးမင်း ဝယ်ယူထားသော [BK] - ( 07, 70, 08, 80 ) အဆင်ပြေပါစေဗျာ။",
    "buy_pat": "🎯 လူကြီးမင်း ဝယ်ယူထားသော [ပတ်သီး] - ( 9 ) ထိပ်စီးပတ်ပါဗျာ။"
}
PRICES = {"buy_1kwet": "15,000 ကျပ်", "buy_4lone": "10,000 ကျပ်", "buy_bk": "10,000 ကျပ်", "buy_pat": "10,000 ကျပ်"}
user_selections, pending_payments = {}, {}

def get_main_menu():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("🎰 ကံစမ်းမဲနှင့် ဂိမ်းများ", callback_data="menu_games"), InlineKeyboardButton("📊 တွက်နည်းနှင့် ဗဟုသုတ", callback_data="menu_knowledge"))
    markup.row(InlineKeyboardButton("🎯 မွေးဂဏန်း ဝယ်ရန်", callback_data="menu_buy_digits"), InlineKeyboardButton("🛠️ အထွေထွေ Tools", callback_data="menu_tools"))
    return markup

def get_digits_menu():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("🌟 တစ်ကွက်ကောင်း (15,000 ကျပ်)", callback_data="buy_1kwet"))
    markup.row(InlineKeyboardButton("🔄 4လုံးအခွေ (10,000 ကျပ်)", callback_data="buy_4lone"))
    markup.row(InlineKeyboardButton("💥 BK (10,000 ကျပ်)", callback_data="buy_bk"))
    markup.row(InlineKeyboardButton("🎯 ပတ်သီး (10,000 ကျပ်)", callback_data="buy_pat"))
    markup.row(InlineKeyboardButton("🔙 ပင်မမီနူးသို့", callback_data="back_to_main"))
    return markup

def get_bank_menu():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("📱 KBZ Pay နံပါတ်ရယူရန်", callback_data="pay_kpay"), InlineKeyboardButton("💵 Wave Pay နံပါတ်ရယူရန်", callback_data="pay_wave"))
    markup.row(InlineKeyboardButton("🔙 နောက်သို့", callback_data="menu_buy_digits"))
    return markup

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "👋 မင်္ဂလာပါဗျာ SawYanNaing Bot မှ ကြိုဆိုပါတယ်။\n\n👇 အောက်က ခလုတ်များကို နှိပ်၍ အသုံးပြုနိုင်ပါပြီ။", reply_markup=get_main_menu())

@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    chat_id, msg_id = call.message.chat.id, call.message.message_id
    if call.data == "back_to_main":
        bot.edit_message_text("👇 အောက်က မီနူးခလုတ်များကို နှိပ်၍ အသုံးပြုနိုင်ပါပြီဗျာ။", chat_id, msg_id, reply_markup=get_main_menu())
    elif call.data == "menu_games":
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton("🎰 Lucky Wheel", callback_data="game_wheel"), InlineKeyboardButton("🔮 ဗေဒင်", callback_data="game_fortune"))
        markup.row(InlineKeyboardButton("🔙 ပင်မမီနူးသို့", callback_data="back_to_main"))
        bot.edit_message_text("🎰 **ကံစမ်းမဲနှင့် ဖျော်ဖြေရေးစနစ်များ**", chat_id, msg_id, reply_markup=markup)
    elif call.data == "menu_knowledge":
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton("📖 Formula Book", callback_data="know_formula"), InlineKeyboardButton("📅 2D Calendar Text", callback_data="know_calendar"))
        markup.row(InlineKeyboardButton("🔙 ပင်မမီနူးသို့", callback_data="back_to_main"))
        bot.edit_message_text("📊 **၂ဒီ တွက်နည်းနှင့် ဗဟုသုတစနစ်များ**", chat_id, msg_id, reply_markup=markup)
    elif call.data == "menu_tools":
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton("⏱️ Time & Date", callback_data="tool_time"), InlineKeyboardButton("💰 Price List", callback_data="tool_price"))
        markup.row(InlineKeyboardButton("🔙 ပင်မမီနူးသို့", callback_data="back_to_main"))
        bot.edit_message_text("🛠️ **အထွေထွေနှင့် စနစ်ထိန်းချုပ်ရေး**", chat_id, msg_id, reply_markup=markup)
    elif call.data == "tool_price":
        bot.send_message(chat_id, "💰 **SawYanNaing မွေးကွက်စျေးနှုန်းများ**\n\n🌟 တစ်ကွက်ကောင်း - `15,000 ကျပ်`\n🔄 အခြားအကွက်များ - `10,000 ကျပ်`။")
    elif call.data == "menu_buy_digits":
        bot.edit_message_text("🎯 **မိမိဝယ်ယူလိုသော မွေးဂဏန်းအမျိုးအစားကို ရွေးချယ်ပေးပါခင်ဗျာ။** 👇", chat_id, msg_id, reply_markup=get_digits_menu())
    elif call.data in ["buy_1kwet", "buy_4lone", "buy_bk", "buy_pat"]:
        user_selections[chat_id] = call.data
        bot.edit_message_text("💰 **ငွေလွှဲအသုံးပြုမည့် မိုဘိုင်းဘဏ်စနစ်ကို ရွေးချယ်ပေးပါခင်ဗျာ။** 👇", chat_id, msg_id, reply_markup=get_bank_menu())
    elif call.data in ["pay_kpay", "pay_wave"]:
        st = user_selections.get(chat_id, "buy_1kwet"); pr = PRICES.get(st, "10,000 ကျပ်"); tn = st.replace('buy_', '').upper()
        num = "09697514209" if call.data == "pay_kpay" else "09686563395"
        name = "Aung Win Oo" if call.data == "pay_kpay" else "Shwe Zin Tun"
        bank = "KBZ Pay" if call.data == "pay_kpay" else "Wave Pay"
        bot.send_message(chat_id, f"📱 **{bank} ဖြင့် ငွေလွှဲရန် အချက်အလက်**\n\n📊 အမျိုးအစား - **{tn}**\n💰 ပမာဏ - **{pr}**\n\n🔹 နံပါတ် - `{num}` (Copy နှိပ်ပါ)\n🔹 အမည် - {name}\n\n⚠️ **ငွေလွှဲပြီးပါက ပြေစာ (Screenshot) ဓာတ်ပုံအား ပို့ပေးပါဗျာ။**")
    elif call.data.startswith("approve_"):
        target_chat_id = int(call.data.split("_"))
        if target_chat_id in pending_payments:
            selected_type = pending_payments[target_chat_id]
            bot.send_message(target_chat_id, f"✅ **လူကြီးမင်း၏ ငွေလွှဲပြေစာကို အက်ဒမင်မှ အတည်ပြုပေးလိုက်ပါပြီဗျာ။**\n\n{DIGITS_DATA[selected_type]}", reply_markup=get_main_menu())
            bot.edit_message_text(f"✅ User ID: `{target_chat_id}` ကို မွေးကွက် ထုတ်ပေးလိုက်ပါပြီ ဆရာကြီး။", chat_id, msg_id)
            try: del pending_payments[target_chat_id]
            except: pass
        else: bot.edit_message_text("❌ ဒီပြေစာက သက်တမ်းကုန်သွားပါပြီ။", chat_id, msg_id)
    elif call.data == "game_wheel": bot.send_message(chat_id, f"🎰 **Lucky Wheel:** [{random.randint(0, 99):02d}]")
    elif call.data == "game_fortune": bot.send_message(chat_id, "🔮 **၂ဒီ ဗေဒင်:** ဒီနေ့ အကွက်ရှယ် တိုးမယ့်နေ့ပါဗျာ။")
    elif call.data == "know_formula": bot.send_message(chat_id, "📖 **Formula Book:** ထိပ်ပိတ်မြှောက်ခြင်း စနစ်တွက်နည်း")
    elif call.data == "know_calendar": bot.send_message(chat_id, "📅 **2D Calendar:** တနင်္လာ - 2/7 ဘရိတ်")
    elif call.data == "tool_time": bot.send_message(chat_id, f"⏱️ **နာရီနှင့် ရက်စွဲ:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

@bot.message_handler(content_types=['photo'])
def handle_payment_screenshot(message):
    chat_id = message.chat.id
    if chat_id not in user_selections:
        bot.reply_to(message, "⚠️ `🎯 မွေးဂဏန်း ဝယ်ရန်` မှတစ်ဆင့် အမျိုးအစား အရင်ရွေးချယ်ပေးပါဗျာ။")
        return
    st = user_selections[chat_id]; pending_payments[chat_id] = st; price = PRICES.get(st, "10,000 ကျပ်")
    bot.reply_to(message, "⏳ ပြေစာကို အက်ဒမင်ထံသို့ စစ်ဆေးရန် ပို့ဆောင်ပေးလိုက်ပါပြီ။ ခေတ္တစောင့်ပေးပါခင်ဗျာ။")
    admin_markup = InlineKeyboardMarkup()
    admin_markup.row(InlineKeyboardButton("✅ အတည်ပြုရန်", callback_data=f"approve_{chat_id}"))
    try: bot.send_photo(OWNER_ID, photo=message.photo[-1].file_id, caption=f"🔔 **ငွေလွှဲပြေစာအသစ် ရောက်လာပါသည်**\n\n👤 ဝယ်ယူသူ: {message.from_user.first_name}\n🆔 ID: `{chat_id}`\n📊 အမျိုးအစား: {st.replace('buy_', '').upper()}\n💰 စျေးနှုန်း: {price}", reply_markup=admin_markup)
    except Exception as e: print(f"Error: {e}")

@bot.message_handler(func=lambda message: True)
def text_handler(message):
    if message.text.strip().lower() in ["hi", "hello", "ဟိုင်း"]: bot.reply_to(message, "Hello ဗျာ! SawYanNaing Bot မှ ကြိုဆိုပါတယ်။", reply_markup=get_main_menu())

# Vercel အတွက် Webhook လမ်းကြောင်းဆောက်ခြင်း
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    # ညီလေး၏ Vercel Link ကို အောက်ပါလင့်ခ်နေရာတွင် နောက်ဆုံးအဆင့်ကျမှ ထည့်ပါမည်
    # bot.set_webhook(url='https://YOUR_VERCEL_URL/' + TOKEN)
    return "Bot is alive!", 200
        
