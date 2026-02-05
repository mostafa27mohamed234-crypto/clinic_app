import streamlit as st
from datetime import datetime, date, time
import sqlite3
import pandas as pd
import time as st_time # لتجنب تضارب الاسم مع datetime.time

# ================= الوقت الحقيقي =================
NOW = datetime.now()
TODAY = NOW.date()

# ================= قاعدة البيانات =================
conn = sqlite3.connect("clinic_bookings.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    service TEXT,
    date TEXT,
    time TEXT
)
""")
conn.commit()

# ================= إعداد الصفحة =================
st.set_page_config(
    page_title="عيادة الدكتورة ياسمين عبد الرحمن",
    page_icon="⚕️", 
    layout="wide"
)

# ================= الستايل الطبي الخرافي (مع إخفاء الفورك وعلامة جيت هاب) =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Play&display=swap');

/* --- كود إخفاء الفورك وعلامة جيت هاب والديبوي --- */
header[data-testid="stHeader"] {visibility: hidden;}
.stDeployButton {display:none;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
/* ------------------------------------------- */

/* الخلفية الطبية المتدرجة */
.stApp {
    background: linear-gradient(135deg, #1A2A3A, #0A1520); 
    font-family: 'Cairo', sans-serif;
    color: #E0E0E0;
    background-attachment: fixed;
}

.stApp::before {
    content: "";
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    background: url('https://www.transparenttextures.com/patterns/micro-carbon.png');
    opacity: 0.1;
    z-index: -1;
}

/* الهيدر الرئيسي - لوحة معلومات الأطباء */
.doctor-hero-header {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(15px);
    border-radius: 25px;
    padding: 30px;
    margin-bottom: 40px;
    border: 2px solid #00BFFF;
    box-shadow: 0 10px 40px rgba(0, 191, 255, 0.3);
    display: flex;
    align-items: center;
    justify-content: space-around;
    flex-wrap: wrap;
    position: relative;
    overflow: hidden;
}

.doctor-hero-info {
    text-align: right;
    flex-grow: 1;
    padding-right: 20px;
}

.doctor-hero-photo {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    object-fit: cover;
    border: 5px solid #00BFFF;
    box-shadow: 0 0 20px rgba(0, 191, 255, 0.5);
}

.doctor-name-main {
    font-family: 'Play', sans-serif;
    font-size: 55px;
    font-weight: bold;
    color: #FFD700;
    text-shadow: 0 0 20px rgba(255, 215, 0, 0.6);
    line-height: 1.2;
}

.doctor-specialty {
    font-size: 30px;
    color: #00BFFF;
    margin-top: 5px;
}

.doctor-contact-details {
    font-size: 20px;
    color: #E0E0E0;
    margin-top: 15px;
}

div[data-testid="stForm"], .st-emotion-cache-12w0qpk {
    background: rgba(255, 255, 255, 0.07) !important;
    backdrop-filter: blur(18px) !important;
    border-radius: 20px !important;
    border: 1px solid rgba(0, 191, 255, 0.2) !important;
    box-shadow: 0 12px 30px rgba(0,0,0,0.5) !important;
}

h1, h2, h3, h4 { color: #FFD700; font-weight: bold; }

.stButton > button {
    background: linear-gradient(45deg, #00BFFF, #007FFF) !important;
    color: white !important;
    border-radius: 10px !important;
    font-weight: bold !important;
    height: 50px !important;
    width: 100% !important;
}

.footer-signature {
    text-align: center;
    padding: 25px;
    margin-top: 50px;
    border-top: 1px solid rgba(0, 191, 255, 0.2);
    color: #999999;
}
.footer-signature b { color: #00BFFF; }
</style>
""", unsafe_allow_html=True)

# ================= الهيدر الرئيسي =================
st.markdown(f"""
<div class='doctor-hero-header'>
    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR_x1p7jP6s_bS0S4D5dY3D7Y_oJ0Q2_M7x7Q&s" class='doctor-hero-photo' alt='Doctor Yasmine Photo'>
    <div class='doctor-hero-info'>
        <div class='doctor-name-main'>عيادة الدكتورة ياسمين عبد الرحمن</div>
        <div class='doctor-specialty'>أخصائي الباطنة والسكر والقدم السكري</div>
        <div class='doctor-contact-details'>📍 سرس الليان - كوبرى المرور | 📞 01111077824</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ================= القائمة الجانبية =================
st.sidebar.markdown("<h3 style='color:#FFD700; text-align:center;'>لوحة التحكم ⚕️</h3>", unsafe_allow_html=True)
menu = st.sidebar.radio("اختر القسم", ["🏠 الرئيسية", "📅 حجز موعد", "📋 عرض الحجوزات", "💡 نصائح صحية"], index=0)
st.sidebar.info("🕒 مواعيد العمل:\n\nيومياً من الساعة 4:00 عصراً حتى 9:00 مساءً\n(ما عدا يوم الجمعة إجازة).")

# ================= المحتوى الرئيسي =================

if menu == "🏠 الرئيسية":
    st.markdown("<h2 style='text-align:center;'>خدماتنا المميزة 🌟</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div style='background:rgba(0,191,255,0.05); padding:20px; border-radius:15px; border-left: 3px solid #00BFFF;'><h4 style='color:#00BFFF;'>💉 استشارات باطنة</h4><p>نقدم تشخيصاً دقيقاً وعلاجاً فعالاً لأمراض الجهاز الهضمي والقلب والكلى.</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div style='background:rgba(0,191,255,0.05); padding:20px; border-radius:15px; border-left: 3px solid #00BFFF;'><h4 style='color:#00BFFF;'>🩸 متابعة حالات السكر</h4><p>برامج متكاملة لمتابعة مستويات السكر وضع خطط علاجية وتغذوية.</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div style='background:rgba(0,191,255,0.05); padding:20px; border-radius:15px; border-left: 3px solid #00BFFF;'><h4 style='color:#00BFFF;'>🦶 فحص القدم السكري</h4><p>فحص شامل للقدم السكري للوقاية من المضاعفات وتوفير الرعاية.</p></div>", unsafe_allow_html=True)

elif menu == "📅 حجز موعد":
    st.markdown("<h2 style='text-align:center;'>احجز موعدك الآن بكل سهولة 📅</h2>", unsafe_allow_html=True)
    with st.form("medical_booking"):
        col1, col2 = st.columns(2)
        name = col1.text_input("الاسم بالكامل", placeholder="الاسم ثلاثي")
        phone = col2.text_input("رقم الهاتف (للتواصل)", placeholder="مثال: 01xxxxxxxxx")
        service = st.selectbox("اختر نوع الخدمة / الكشف", ["كشف باطنة عام", "متابعة سكر", "فحص قدم سكري", "استشارة"])
        col3, col4 = st.columns(2)
        date_selected = col3.date_input("تاريخ الحضور", min_value=TODAY)
        time_selected = col4.time_input("الوقت المفضل")
        submit_button = st.form_submit_button("تأكيد الحجز 🌟")

        if submit_button:
            if not name.strip() or not phone.strip():
                st.error("⚠️ من فضلك، املأ جميع الحقول المطلوبة.")
            elif not (st_time.time(16, 0) <= time_selected <= st_time.time(21, 0)):
                st.error("❌ مواعيد الحجز من 4 عصراً حتى 9 مساءً فقط.")
            else:
                c.execute("INSERT INTO bookings (name, phone, service, date, time) VALUES (?, ?, ?, ?, ?)",
                          (name.strip(), phone.strip(), service, str(date_selected), str(time_selected)))
                conn.commit()
                progress_text = "جاري تأكيد الحجز..."
                my_bar = st.progress(0, text=progress_text)
                for p in range(100):
                    st_time.sleep(0.01)
                    my_bar.progress(p + 1, text=progress_text)
                st.success(f"✅ تم تأكيد حجزك يا: {name} بنجاح!")
                st.balloons()

elif menu == "📋 عرض الحجوزات":
    st.markdown("<h2 style='text-align:center;'>لوحة إدارة الحجوزات 🔐</h2>", unsafe_allow_html=True)
    pwd = st.text_input("كلمة سر المسؤول", type="password")
    if pwd == "admin123":
        data = pd.read_sql("SELECT name, phone, service, date, time FROM bookings", conn)
        st.dataframe(data, use_container_width=True)

elif menu == "💡 نصائح صحية":
    st.markdown("<h2 style='text-align:center;'>نصائح صحية 🩺</h2>", unsafe_allow_html=True)
    st.success("💎 شرب 8 أكواب ماء يومياً يحسن وظائف الجسم.")
    st.info("🍏 التغذية السليمة تدعم جهاز المناعة.")

# ================= الفوتر =================
st.markdown(f"""
<div class='footer-signature'>تم التطوير بواسطة <b>البشمهندس مصطفى الفيشاوي</b> ⚡ 2024</div>
""", unsafe_allow_html=True)