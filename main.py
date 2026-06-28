import os
from flask import Flask, request, abort
import telebot

# သင့်ရဲ့ Bot Token ကို ကုဒ်ထဲမှာ တိုက်ရိုက် ထည့်သွင်းထားပါတယ်
BOT_TOKEN = "8952729513:AAFnmakiB8i-K_g4_niUFJPKQZb9fYksKj4"
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

app = Flask(__name__)

# ၁။ Telegram Webhook အတွက် လမ်းကြောင်း (Route)
@app.route('/' + BOT_TOKEN, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', 200
    else:
        abort(403)

# ၂။ Browser ကနေ ပုံမှန် ဝင်ကြည့်ရင် ပြမည့် လမ်းကြောင်း
@app.route('/', methods=['GET'])
def index():
    return "Bot Engine is Running perfectly...", 200

# ၃။ /start ဟု ပို့လာပါက Reply Markup Buttons များ ပြသပေးမည့် Handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # စာသားအောက်တွင် တွဲပြမည့် Inline Keyboard Buttons များ တည်ဆောက်ခြင်း
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    
    btn1 = telebot.types.InlineKeyboardButton("📊 2D Live Result", callback_data="2d_live")
    btn2 = telebot.types.InlineKeyboardButton("ထွက်ဂဏန်းမှတ်တမ်း", callback_data="2d_history")
    btn3 = telebot.types.InlineKeyboardButton("📞 Admin ဆက်သွယ်ရန်", callback_data="contact_admin")
    
    # ခလုတ်များကို နေရာချခြင်း (ပထမတန်းမှာ ၂ ခု၊ ဒုတိယတန်းမှာ ၁ ခု)
    markup.add(btn1, btn2)
    markup.add(btn3)
    
    welcome_text = "👋 မင်္ဂလာပါ! 2D Business Bot မှ ကြိုဆိုပါတယ်။\n\nအောက်ပါ Menu ခလုတ်များကို နှိပ်ပြီး အသုံးပြုနိုင်ပါတယ်ခင်ဗျာ။"
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

# ၄။ User က ခလုတ်တစ်ခုခု နှိပ်လိုက်သည့်အခါ အလုပ်လုပ်မည့် Callback Query Handler
@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    if call.data == "2d_live":
        # ဤနေရာတွင် နောက်ပိုင်း၌ Live API ချိတ်ဆက်ပြီး ဂဏန်းထုတ်ပေးရမည်
        bot.answer_callback_query(call.id, "Live API မှ အချက်အလက်များ ဆွဲယူနေဆဲဖြစ်သည်...")
        bot.send_message(call.message.chat.id, "📊 ယနေ့ထွက်ဂဏန်းများ (စမ်းသပ်ချက်):\n• 12:01 PM -> **45**\n• 04:30 PM -> **89**", parse_mode="Markdown")
        
    elif call.data == "2d_history":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "📅 ပြီးခဲ့သည့် အပတ်က ထွက်ဂဏန်းများကို ပြသပေးပါမည်။")
        
    elif call.data == "contact_admin":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "📞 အကူအညီအတွက် @AdminUsername (သို့) ဖုန်း ဝ၉-xxxxxxxxx ကို ဆက်သွယ်နိုင်ပါသည်။")

# ၅။ ကျန်ရှိသည့် မည်သည့် စာသားမဆို ပို့လာပါက အလိုအလျောက် ပြန်ဖြေပေးမည့် စနစ်
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"သင်ပြောလိုက်တာက: {message.text}\n\nအဓိက အသုံးပြုရန်အတွက် /start ကို နှိပ်ပါဗျာ။")

# Vercel Serverless Server ပေါ်တွင် အလုပ်လုပ်ရန် သတ်မှတ်ချက်
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
    
