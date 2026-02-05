import streamlit as st
from datetime import datetime, date, time
import sqlite3
import pandas as pd
import time as st_time

# ================= 1. إعدادات الوقت وقاعدة البيانات =================
NOW = datetime.now()
TODAY = NOW.date()

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

# ================= 2. إعداد الصفحة والستايل =================
st.set_page_config(
    page_title="عيادة الدكتورة ياسمين عبد الرحمن",
    page_icon="⚕️", 
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');

/* إخفاء العناصر العلوية المزعجة */
header[data-testid="stHeader"] {visibility: hidden;}
.stDeployButton {display:none;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* الخلفية العامة */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    font-family: 'Cairo', sans-serif;
    color: #f1f5f9;
}

/* هيدر الصفحة الرئيسي */
.main-hero {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(56, 189, 248, 0.3);
    border-radius: 30px;
    padding: 40px;
    margin-bottom: 30px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    backdrop-filter: blur(10px);
    box-shadow: 0 15px 35px rgba(0,0,0,0.3);
}

.hero-text h1 {
    font-size: 45px !important;
    color: #fbbf24 !important;
    font-weight: 900 !important;
    margin-bottom: 5px;
}

/* الصورة الدائرية (لوز اللوز) */
.profile-pic {
    width: 200px;
    height: 200px;
    border-radius: 50% !important;
    border: 5px solid #38bdf8;
    object-fit: cover;
    box-shadow: 0 0 25px rgba(56, 189, 248, 0.4);
}

/* كروت الخدمات */
.service-card {
    background: rgba(255, 255, 255, 0.05);
    border-right: 5px solid #38bdf8;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
}

/* القائمة الجانبية */
[data-testid="stSidebar"] {
    background-color: #020617 !important;
}
</style>
""", unsafe_allow_html=True)

# ================= 3. الهيدر (واجهة العيادة) =================
st.markdown(f"""
<div class="main-hero">
    <div class="hero-text" style="text-align: right;">
        <h1>عيادة الدكتورة ياسمين عبد الرحمن</h1>
        <p style="color: #38bdf8; font-size: 24px; font-weight: bold;">أخصائي الباطنة والسكر والقدم السكري</p>
        <p style="color: #94a3b8;">📍 سرس الليان - كوبرى المرور | 📞 01111077824</p>
    </div>
    <img src="https://img.freepik.com/free-photo/female-doctor-hospital-with-stethoscope_23-2148827701.jpg" class="profile-pic">
</div>
""", unsafe_allow_html=True)

# ================= 4. القائمة الجانبية (التحكم الكامل) =================
st.sidebar.markdown("<h2 style='text-align:center; color:#fbbf24;'>لوحة التحكم ⚕️</h2>", unsafe_allow_html=True)
menu = st.sidebar.radio(
    "انتقل إلى:",
    ["🏠 الصفحة الرئيسية", "📅 حجز موعد جديد", "📋 كشف الحجوزات", "💡 نصائح طبية"],
    key="nav"
)
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='text-align:center; color:#94a3b8;'>
    <b>🕒 مواعيد العمل</b><br>
    يومياً: 4:00 م - 9:00 م<br>
    الجمعة إجازة
</div>
""", unsafe_allow_html=True)

# ================= 5. تنفيذ الصفحات =================

# --- الصفحة الرئيسية ---
if menu == "🏠 الصفحة الرئيسية":
    st.markdown("<h2 style='text-align:right;'>خدماتنا الرائدة 🌟</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='service-card'><h3 style='color:#38bdf8;'>💉 باطنة عامة</h3><p>تشخيص ومتابعة كافة أمراض الباطنة بأحدث الأجهزة.</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='service-card'><h3 style='color:#38bdf8;'>🩸 رعاية السكر</h3><p>تنظيم مستويات السكر ووضع برامج غذائية متكاملة.</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='service-card'><h3 style='color:#38bdf8;'>🦶 القدم السكري</h3><p>عناية خاصة وفحص دوري لحماية القدم من المضاعفات.</p></div>", unsafe_allow_html=True)

# --- صفحة الحجز (بكل تكاتها) ---
elif menu == "📅 حجز موعد جديد":
    st.markdown("<h2 style='text-align:center;'>تسجيل بيانات الحجز 📝</h2>", unsafe_allow_html=True)
    with st.form("booking_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        name = col1.text_input("اسم المريض بالكامل")
        phone = col2.text_input("رقم الهاتف للتواصل")
        
        service = st.selectbox("نوع الخدمة المطلوبة", ["كشف باطنة", "متابعة سكر", "فحص قدم سكري", "استشارة سريعة"])
        
        col3, col4 = st.columns(2)
        res_date = col3.date_input("تاريخ الحجز", min_value=TODAY)
        res_time = col4.time_input("الوقت المفضل")
        
        submitted = st.form_submit_button("تأكيد الحجز ومسابقة الزمن 🚀")
        
        if submitted:
            if name and phone:
                c.execute("INSERT INTO bookings (name, phone, service, date, time) VALUES (?,?,?,?,?)",
                          (name, phone, service, str(res_date), str(res_time)))
                conn.commit()
                
                # إضافة شريط التقدم اللي كان موجود
                progress_bar = st.progress(0)
                for i in range(100):
                    st_time.sleep(0.01)
                    progress_bar.progress(i + 1)
                
                st.success(f"تم الحجز بنجاح يا {name}! ننتظرك في الموعد.")
                st.balloons()
            else:
                st.error("من فضلك املأ الاسم ورقم التليفون أولاً!")

# --- صفحة الإدارة ---
elif menu == "📋 كشف الحجوزات":
    st.markdown("<h2 style='text-align:center;'>سجل الحجوزات 🔐</h2>", unsafe_allow_html=True)
    password = st.text_input("كلمة مرور الإدارة", type="password")
    if password == "admin123":
        df = pd.read_sql("SELECT name, phone, service, date, time FROM bookings ORDER BY date DESC", conn)
        st.dataframe(df, use_container_width=True)
    elif password:
        st.error("كلمة المرور غير صحيحة!")

# --- صفحة النصائح ---
elif menu == "💡 نصائح طبية":
    st.success("🍏 نصيحة اليوم: المشي لمدة 30 دقيقة يومياً يقلل من مخاطر مضاعفات السكر بنسبة 40%.")
    st.info("💧 اشرب ما لا يقل عن 8 أكواب ماء يومياً للحفاظ على سلامة الكلى.")

# ================= 6. الفوتر =================
st.markdown(f"""
<div style='text-align:center; padding:30px; color:#64748b; border-top:1px solid rgba(255,255,255,0.05); margin-top:50px;'>
    تم التطوير بكل حب بواسطة <b>البشمهندس مصطفى الفيشاوي</b> ⚡ 2026
</div>
""", unsafe_allow_html=True)