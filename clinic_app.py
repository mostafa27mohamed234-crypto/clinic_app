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

# ================= الستايل الطبي المطور (الروقان) =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');

/* ✅ إخفاء الفورك وعلامة جيت هاب */
header[data-testid="stHeader"] {visibility: hidden;}
.stDeployButton {display:none;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* الخلفية */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    font-family: 'Cairo', sans-serif;
    color: #f1f5f9;
}

/* الهيدر المطور */
.hero-card {
    background: rgba(255, 255, 255, 0.05);
    border: 2px solid #38bdf8;
    border-radius: 30px;
    padding: 40px;
    margin-bottom: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 30px;
    box-shadow: 0 20px 50px rgba(0, 191, 255, 0.15);
    backdrop-filter: blur(10px);
}

.doctor-img {
    width: 200px;
    height: 200px;
    border-radius: 50%;
    border: 6px solid #38bdf8;
    object-fit: cover;
    box-shadow: 0 0 30px rgba(56, 189, 248, 0.5);
}

.hero-text {
    text-align: right;
}

.hero-text h1 {
    font-size: 45px !important;
    font-weight: 900 !important;
    color: #fbbf24 !important;
    margin-bottom: 10px;
    text-shadow: 2px 2px 10px rgba(0,0,0,0.5);
}

/* الكروت الجانبية */
.service-box {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(56, 189, 248, 0.2);
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    transition: 0.3s;
}

.service-box:hover {
    border-color: #38bdf8;
    transform: translateY(-5px);
    background: rgba(56, 189, 248, 0.05);
}

/* الأزرار */
.stButton > button {
    background: linear-gradient(90deg, #38bdf8, #0ea5e9) !important;
    color: white !important;
    border-radius: 12px !important;
    height: 55px !important;
    font-size: 20px !important;
    border: none !important;
}

/* القائمة الجانبية */
section[data-testid="stSidebar"] {
    background: #0f172a !important;
}
</style>
""", unsafe_allow_html=True)

# ================= الهيدر الرئيسي بصورة الدكتورة =================
st.markdown(f"""
<div class="hero-card">
    <div class="hero-text">
        <h1>عيادة الدكتورة ياسمين عبد الرحمن</h1>
        <h2 style="color:#38bdf8; font-size:28px;">أخصائي الباطنة والسكر والقدم السكري</h2>
        <p style="font-size:18px; color:#cbd5e1;">📍 سرس الليان - كوبرى المرور | 📞 01111077824</p>
    </div>
    <img src="https://img.freepik.com/free-photo/female-doctor-hospital-with-stethoscope_23-2148827701.jpg" class="doctor-img">
</div>
""", unsafe_allow_html=True)

# ================= القائمة الجانبية =================
st.sidebar.markdown("<h2 style='text-align:center; color:#fbbf24;'>لوحة التحكم ⚕️</h2>", unsafe_allow_html=True)
menu = st.sidebar.radio("اختر القسم", ["🏠 الرئيسية", "📅 حجز موعد", "📋 عرض الحجوزات", "💡 نصائح صحية"])
st.sidebar.markdown("---")
st.sidebar.info("🕒 مواعيد العمل:\n\nيومياً من الساعة 4:00 عصراً حتى 9:00 مساءً\n(ما عدا يوم الجمعة إجازة).")

# ================= الأقسام =================

if menu == "🏠 الرئيسية":
    st.markdown("<h2 style='text-align:center; margin-bottom:30px;'>خدماتنا المميزة 🌟</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='service-box'><h3>💉</h3><h4>استشارات باطنة</h4><p>تشخيص دقيق لأمراض الجهاز الهضمي والقلب والكلى.</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='service-box'><h3>🩸</h3><h4>متابعة السكر</h4><p>برامج متكاملة لمتابعة السكر ووضع خطط علاجية.</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='service-box'><h3>🦶</h3><h4>القدم السكري</h4><p>فحص شامل للوقاية من المضاعفات وتوفير الرعاية.</p></div>", unsafe_allow_html=True)

elif menu == "📅 حجز موعد":
    st.markdown("<h2 style='text-align:center;'>احجز موعدك الآن 📅</h2>", unsafe_allow_html=True)
    with st.form("booking_form"):
        col1, col2 = st.columns(2)
        name = col1.text_input("الاسم بالكامل")
        phone = col2.text_input("رقم الهاتف")
        service = st.selectbox("نوع الخدمة", ["كشف باطنة عام", "متابعة سكر", "فحص قدم سكري", "استشارة"])
        col3, col4 = st.columns(2)
        d_sel = col3.date_input("التاريخ", min_value=TODAY)
        t_sel = col4.time_input("الوقت المفضل")
        if st.form_submit_button("تأكيد الحجز الآن ✅"):
            if name and phone:
                if st_time.time(16, 0) <= t_sel <= st_time.time(21, 0):
                    c.execute("INSERT INTO bookings (name, phone, service, date, time) VALUES (?, ?, ?, ?, ?)", (name, phone, service, str(d_sel), str(t_sel)))
                    conn.commit()
                    st.success("🎉 تم تأكيد الحجز بنجاح!")
                    st.balloons()
                else: st.error("المواعيد من 4 عصراً لـ 9 مساءً.")
            else: st.error("برجاء إدخال البيانات.")

elif menu == "📋 عرض الحجوزات":
    pwd = st.text_input("كلمة سر المسؤول", type="password")
    if pwd == "admin123":
        df = pd.read_sql("SELECT name, phone, service, date, time FROM bookings", conn)
        st.dataframe(df, use_container_width=True)

elif menu == "💡 نصائح صحية":
    st.info("🍏 نصيحة اليوم: شرب الماء بانتظام يحسن من أداء وظائف الكلى.")

# ================= الفوتر =================
st.markdown(f"""
<div style='text-align:center; padding:30px; border-top:1px solid rgba(255,255,255,0.1); color:#94a3b8;'>
    تم التطوير بواسطة <b>البشمهندس مصطفى الفيشاوي</b> ⚡ 2024
</div>
""", unsafe_allow_html=True)