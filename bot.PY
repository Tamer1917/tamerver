import telebot
import requests
import firebase_admin
from firebase_admin import credentials, db

# 🔹 تهيئة الاتصال بـ Firebase باستخدام ملف المفاتيح

cred = credentials.Certificate(r"C:\Users\LENOVO\Desktop\frapp\serviceAccountKey.json")


firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://mychessgame-7811e-default-rtdb.europe-west1.firebasedatabase.app/'
})

# 🔹 إعداد بوت تيليجرام
BOT_TOKEN = "7996338110:AAGKkgFy1qpUQG4E9A4ZJrgc0aon4cx8JpI"
bot = telebot.TeleBot(BOT_TOKEN)

# 🔹 رابط صفحة HTML المستضافة على Vercel (تأكد من أن لديك API Endpoint جاهز لاستقبال البيانات)
VERCEL_URL = "https://fernew1.vercel.app/update-score"

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.username or f"User_{user_id}"  # في حال لم يكن لديه اسم مستخدم

    # اتصال بـ Firebase (إضافة أو تعديل البيانات)
    ref = db.reference(f'users/{username}')
    user_data = ref.get()

    if user_data is None:
        # 🔹 المستخدم غير مسجل، نضيفه إلى قاعدة البيانات مع 5 نقاط
        user_data = {"username": username, "points": 5}
        ref.set(user_data)
    else:
        # 🔹 إذا كان مسجلاً مسبقًا، نحصل على البيانات الحالية
        user_data["points"] = user_data.get("points", 0)

    # 🔹 إرسال البيانات إلى الخادم (Vercel)
    try:
        response = requests.post(VERCEL_URL, json=user_data)
        response.raise_for_status()  # رفع استثناء إذا كان هناك خطأ في الرد
        bot.reply_to(message, f"مرحبًا {username}! لديك {user_data['points']} نقطة.")
        print("تم إرسال البيانات بنجاح")
    except requests.exceptions.RequestException as e:
        print(f"⚠️ حدث خطأ أثناء إرسال البيانات: {e}")
        bot.reply_to(message, "حدث خطأ أثناء إرسال البيانات للخادم.")

# 🔹 تشغيل البوت
bot.polling(none_stop=True)
