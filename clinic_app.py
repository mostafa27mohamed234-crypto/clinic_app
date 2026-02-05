import streamlit as st
from datetime import datetime, date, time
import sqlite3
import pandas as pd
import time as st_time 

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

# ================= الستايل الطبي (تم إضافة كود الإخفاء هنا) =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Play&display=swap');

/* --- كود إخفاء الفورك والقائمة وعلامة جيت هاب --- */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display:none;}
[data-testid="stStatusWidget"] {visibility: hidden;}
button[title="View source code"] {display: none;}
/* ------------------------------------------- */

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

div[data-testid="stForm"], .st-emotion-cache-12w0qpk {
    background: rgba(255, 255, 255, 0.07) !important;
    backdrop-filter: blur(18px) !important;
    border-radius: 20px !important;
    border: 1px solid rgba(0, 191, 255, 0.2) !important;
    padding: 20px !important;
}

.stButton > button {
    background: linear-gradient(45deg, #00BFFF, #007FFF) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: bold !important;
    height: 50px !important;
    width: 100% !important;
    font-size: 18px !important;
}

.footer-signature {
    text-align: center;
    padding: 25px;
    margin-top: 50px;
    border-top: 1px solid rgba(0, 191, 255, 0.2);
    color: #999999;
}
</style>
""", unsafe_allow_html=True)

# ================= الهيدر الرئيسي =================
st.markdown(f"""
<div class='doctor-hero-header'>
    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR_x1p7jP6s_bS0S4D5dY3D7Y_oJ0Q2_M7x7Q&s" class='doctor-hero-photo'>
    <div class='doctor-hero-info'>
        <div class='doctor-name-main'>عيادة الدكتورة ياسمين عبد الرحمن</div>
        <div class='doctor-specialty'>أخصائي الباطنة والسكر والقدم السكري</div>
        <div style='color:#E0E0E0; margin-top:15px; font-size:20px;'>📍 سرس الليان - كوبرى المرور | 📞 01111077824</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ================= القائمة الجانبية =================
st.sidebar.markdown("<h3 style='color:#FFD700; text-align:center;'>لوحة التحكم ⚕️</h3>", unsafe_allow_html=True)
menu = st.sidebar.radio("اختر القسم", ["🏠 الرئيسية", "📅 حجز موعد", "📋 عرض الحجوزات", "💡 نصائح صحية"])

# ================= المحتوى =================
if menu == "🏠 الرئيسية":
    st.markdown("<h2 style='text-align:center;'>خدماتنا المميزة 🌟</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1: st.info("💉 استشارات باطنة")
    with col2: st.info("🩸 متابعة حالات السكر")
    with col3: st.info("🦶 فحص القدم السكري")

elif menu == "📅 حجز موعد":
    st.markdown("<h2 style='text-align:center;'>احجز موعدك الآن بكل سهولة 📅</h2>", unsafe_allow_html=True)
    with st.form("medical_booking"):
        col1, col2 = st.columns(2)
        name = col1.text_input("الاسم بالكامل")
        phone = col2.text_input("رقم الهاتف")
        service = st.selectbox("الخدمة", ["كشف باطنة عام", "متابعة سكر", "فحص قدم سكري", "استشارة"])
        d_selected = st.date_input("التاريخ", min_value=TODAY)
        t_selected = st.time_input("الوقت")
        if st.form_submit_button("تأكيد الحجز 🌟"):
            if name and phone:
                c.execute("INSERT INTO bookings (name, phone, service, date, time) VALUES (?, ?, ?, ?, ?)",
                          (name, phone, service, str(d_selected), str(t_selected)))
                conn.commit()
                st.success("✅ تم الحجز بنجاح!")
            else: st.error("اكمل البيانات")

elif menu == "📋 عرض الحجوزات":
    pwd = st.text_input("كلمة السر", type="password")
    if pwd == "admin123":
        data = pd.read_sql("SELECT name, phone, service, date, time FROM bookings", conn)
        st.dataframe(data, use_container_width=True)

elif menu == "💡 نصائح صحية":
    st.success("💧 شرب الماء بكثرة يحافظ على نشاط الكلى.")

# ================= الفوتر =================
st.markdown(f"""
<div class='footer-signature'>
    تم التطوير بواسطة <b>البشمهندس مصطفى الفيشاوي</b> ⚡ 2024
</div>
""", unsafe_allow_html=True)