import telebot
import requests
import firebase_admin
from firebase_admin import credentials, db  # استخدم firestore إذا كنت تعمل مع Firestore

# ✅ 1️⃣ تهيئة الاتصال بـ Firebase باستخدام ملف المفاتيح
cred = credentials.Certificate(r"C:\Users\LENOVO\Desktop\frapp\serviceAccountKey.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://mychessgame-7811e-default-rtdb.europe-west1.firebasedatabase.app/'  # تأكد من استخدام قاعدة بيانات Realtime Database
})

# ✅ 2️⃣ إعداد بوت تيليجرام
BOT_TOKEN = "7996338110:AAGKkgFy1qpUQG4E9A4ZJrgc0aon4cx8JpI"
bot = telebot.TeleBot(BOT_TOKEN)

# ✅ 3️⃣ رابط API المستضاف على Vercel
VERCEL_URL = "https://tamerver.vercel.app/update-score"

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.username or f"User_{user_id}"  # ✅ التأكد من أن لديه اسم مستخدم

    # ✅ 4️⃣ اتصال بـ Firebase (إضافة أو تعديل البيانات)
    ref = db.reference(f'users/{username}')
    user_data = ref.get()

    if user_data is None:
        user_data = {"username": username, "points": 5}  # ✅ أول مرة يحصل على 5 نقاط
        ref.set(user_data)
    else:
        user_data["points"] = user_data.get("points", 0)  # ✅ إذا كان موجودًا، نأخذ نقاطه الحالية

    # ✅ 5️⃣ إرسال البيانات إلى Vercel
    try:
        response = requests.post(VERCEL_URL, json=user_data)
        if response.status_code == 200:
            bot.reply_to(message, f"مرحبًا {username}! لديك {user_data['points']} نقطة.")
            print("✅ تم إرسال البيانات بنجاح إلى Vercel!")
        else:
            print(f"⚠️ خطأ في الإرسال: {response.status_code}, الرد: {response.text}")
            bot.reply_to(message, "⚠️ حدث خطأ أثناء إرسال البيانات للخادم.")
    except requests.exceptions.RequestException as e:
        print(f"❌ خطأ أثناء إرسال البيانات: {e}")
        bot.reply_to(message, "❌ حدث خطأ أثناء إرسال البيانات للخادم.")

# ✅ 6️⃣ تشغيل البوت
bot.polling(none_stop=True)
