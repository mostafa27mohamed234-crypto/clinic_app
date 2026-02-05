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

# ================= الستايل الطبي الأصلي + إخفاء العلامات =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Play&display=swap');

/* ✅ إخفاء الفورك وعلامة جيت هاب والديبوي فقط */
header[data-testid="stHeader"] {visibility: hidden;}
.stDeployButton {display:none;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* الخلفية الطبية الأصلية */
.stApp {
    background: linear-gradient(135deg, #1A2A3A, #0A1520); 
    font-family: 'Cairo', sans-serif;
    color: #E0E0E0;
    background-attachment: fixed;
}

/* الهيدر الرئيسي */
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
}

/* صورة الطبيبة الدائرية */
.doctor-hero-photo {
    width: 180px;
    height: 180px;
    border-radius: 50% !important;
    object-fit: cover;
    border: 5px solid #00BFFF;
    box-shadow: 0 0 25px rgba(0, 191, 255, 0.5);
}

.doctor-name-main {
    font-size: 45px;
    font-weight: bold;
    color: #FFD700;
    text-shadow: 0 0 20px rgba(255, 215, 0, 0.6);
}

/* تصميم القائمة الجانبية (الأزرار اللي طلبتها) */
section[data-testid="stSidebar"] {
    background: #0A1520 !important;
    border-right: 1px solid rgba(0, 191, 255, 0.2);
}

/* تصميم الأزرار */
.stButton > button {
    background: linear-gradient(45deg, #00BFFF, #007FFF) !important;
    color: white !important;
    font-weight: bold !important;
    border-radius: 10px !important;
    height: 50px !important;
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
    <div class='doctor-hero-info' style='text-align:right;'>
        <div class='doctor-name-main'>عيادة الدكتورة ياسمين عبد الرحمن</div>
        <div style='color:#00BFFF; font-size:25px;'>أخصائي الباطنة والسكر والقدم السكري</div>
        <div style='margin-top:10px;'>📍 سرس الليان - كوبرى المرور | 📞 01111077824</div>
    </div>
    <img src="https://img.freepik.com/free-photo/female-doctor-hospital-with-stethoscope_23-2148827701.jpg" class='doctor-hero-photo'>
</div>
""", unsafe_allow_html=True)

# ================= القائمة الجانبية (الأزرار المطلوبة) =================
st.sidebar.markdown("<h3 style='color:#FFD700; text-align:center;'>القائمة الرئيسية ⚕️</h3>", unsafe_allow_html=True)
menu = st.sidebar.radio("اختر الوجهة:", ["🏠 الصفحة الرئيسية", "📅 حجز موعد جديد", "📋 لوحة الحجوزات", "💡 نصائح العيادة"])
st.sidebar.markdown("---")
st.sidebar.info("🕒 مواعيد العمل:\n\nيومياً من الساعة 4:00 عصراً حتى 9:00 مساءً\n(ما عدا يوم الجمعة إجازة).")

# ================= الأقسام =================

# 1. الصفحة الرئيسية
if menu == "🏠 الصفحة الرئيسية":
    st.markdown("<h2 style='text-align:center;'>مرحباً بكم في عيادتنا 🌟</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div style='background:rgba(0,191,255,0.05); padding:20px; border-radius:15px; border-left: 3px solid #00BFFF;'><h4>💉 استشارات باطنة</h4><p>تشخيص دقيق لأمراض الجهاز الهضمي والقلب والكلى.</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div style='background:rgba(0,191,255,0.05); padding:20px; border-radius:15px; border-left: 3px solid #00BFFF;'><h4>🩸 متابعة السكر</h4><p>متابعة مستمرة لمرضى السكر بأحدث البروتوكولات.</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div style='background:rgba(0,191,255,0.05); padding:20px; border-radius:15px; border-left: 3px solid #00BFFF;'><h4>🦶 القدم السكري</h4><p>فحص وقائي شامل لمرضى السكر للحماية من المضاعفات.</p></div>", unsafe_allow_html=True)

# 2. خانة الحجز
elif menu == "📅 حجز موعد جديد":
    st.markdown("<h2 style='text-align:center;'>تأكيد حجز موعد 📅</h2>", unsafe_allow_html=True)
    with st.form("medical_booking"):
        col1, col2 = st.columns(2)
        name = col1.text_input("اسم المريض", placeholder="الاسم بالكامل")
        phone = col2.text_input("رقم الموبايل", placeholder="01xxxxxxxxx")
        service = st.selectbox("نوع الكشف", ["كشف باطنة", "متابعة سكر", "فحص قدم سكري", "استشارة"])
        col3, col4 = st.columns(2)
        date_selected = col3.date_input("اختر التاريخ", min_value=TODAY)
        time_selected = col4.time_input("اختر الوقت")
        
        submit_button = st.form_submit_button("تأكيد الحجز الآن 🌟")

        if submit_button:
            if not name or not phone:
                st.error("⚠️ برجاء إدخال الاسم ورقم الهاتف.")
            else:
                c.execute("INSERT INTO bookings (name, phone, service, date, time) VALUES (?, ?, ?, ?, ?)",
                          (name, phone, service, str(date_selected), str(time_selected)))
                conn.commit()
                # شريط التقدم (البروجرس بار)
                progress_bar = st.progress(0)
                for percent_complete in range(100):
                    st_time.sleep(0.01)
                    progress_bar.progress(percent_complete + 1)
                st.success(f"✅ تم تسجيل الحجز بنجاح يا {name}")
                st.balloons()

# 3. عرض الحجوزات (للمسؤول)
elif menu == "📋 لوحة الحجوزات":
    st.markdown("<h2 style='text-align:center;'>سجل الحجوزات اليومية 📋</h2>", unsafe_allow_html=True)
    pwd = st.text_input("أدخل كلمة المرور للمشاهدة", type="password")
    if pwd == "admin123":
        df = pd.read_sql("SELECT name as 'الاسم', phone as 'الهاتف', service as 'الخدمة', date as 'التاريخ', time as 'الوقت' FROM bookings", conn)
        st.table(df)
    elif pwd:
        st.error("❌ كلمة المرور غير صحيحة")

# 4. النصائح
elif menu == "💡 نصائح العيادة":
    st.info("💡 نصيحة اليوم: شرب كميات كافية من الماء يحسن من كفاءة الدورة الدموية بشكل كبير.")

# ================= الفوتر =================
st.markdown(f"""
<div class='footer-signature'>تم التطوير بواسطة <b>البشمهندس مصطفى الفيشاوي</b> ⚡ 2026</div>
""", unsafe_allow_html=True)