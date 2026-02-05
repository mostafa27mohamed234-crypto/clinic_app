import streamlit as st
from datetime import datetime, date, time
import sqlite3
import pandas as pd

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

# ================= الصفحة =================
st.set_page_config(
    page_title="عيادة الدكتورة ياسمين عبدالرحمن",
    layout="wide"
)

# ================= الستايل الخرافي المدمج =================
st.markdown("""
<style>
/* الخلفية الطبية المتطورة */
.stApp {
    background: radial-gradient(circle at center, #1e2a4a 0%, #0a0e1a 100%);
    background-image: url('https://www.transparenttextures.com/patterns/stardust.png');
    color: white;
    font-family: 'Cairo', sans-serif;
}

/* تأثير القلب المتوهج في الخلفية (اختياري عبر CSS) */
.stApp::before {
    content: "";
    position: fixed;
    top: 50%; left: 50%;
    width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(0, 206, 209, 0.1) 0%, rgba(0,0,0,0) 70%);
    transform: translate(-50%, -50%);
    z-index: -1;
}

/* تصميم الهيدر (المربع العلوي) */
.header-container {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border-radius: 30px;
    padding: 30px;
    border: 1px solid rgba(255, 215, 0, 0.3);
    text-align: center;
    margin-bottom: 40px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}

.header-text {
    color: #FFD700;
    font-size: 45px;
    font-weight: bold;
    text-shadow: 0 0 20px rgba(255, 215, 0, 0.4);
}

.subheader-text {
    color: #00CED1;
    font-size: 24px;
    margin-top: 10px;
}

/* تصميم الكروت (الفورم) */
div[data-testid="stForm"], .box {
    background: rgba(255, 255, 255, 0.07) !important;
    backdrop-filter: blur(15px);
    border-radius: 25px !important;
    padding: 35px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    box-shadow: 0 15px 35px rgba(0,0,0,0.4) !important;
}

/* الأزرار */
.stButton > button {
    background: linear-gradient(90deg, #00CED1 0%, #6A5ACD 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 15px !important;
    font-weight: bold !important;
    padding: 10px 25px !important;
    transition: 0.3s !important;
}

.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px #00CED1;
}

/* الجداول */
.table-box {
    background: rgba(0, 0, 0, 0.3);
    padding: 20px;
    border-radius: 20px;
    border: 1px solid #00CED1;
}

/* القائمة الجانبية */
section[data-testid="stSidebar"] {
    background-color: #0a0e1a !important;
}
</style>
""", unsafe_allow_html=True)

# ================= الهيدر =================
st.markdown(f"""
<div class='header-container'>
    <div class='header-text'>🩺 عيادة الدكتورة ياسمين عبدالرحمن</div>
    <div class='subheader-text'>أخصائي الباطنة والسكر</div>
    <div style='color: #ccc; margin-top:15px;'>📍 سرس الليان - كوبرى المرور | 📞 01111077824</div>
</div>
""", unsafe_allow_html=True)

# ================= القائمة =================
st.sidebar.markdown("### 🏥 لوحة التحكم")
menu = st.sidebar.selectbox("انتقل إلى:", ["الرئيسية", "حجز موعد", "عرض الحجوزات"])

# ================= الرئيسية =================
if menu == "الرئيسية":
    st.markdown(
        "<div class='box' style='text-align:center; font-size:30px;'>"
        "أهلاً بكم في نظام الحجز الذكي 🌿<br>"
        "<span style='font-size:20px; color:#00CED1;'>نحن هنا لتقديم أفضل رعاية صحية لكم</span>"
        "</div>",
        unsafe_allow_html=True
    )

# ================= حجز موعد =================
elif menu == "حجز موعد":
    st.markdown("### 📅 تسجيل بيانات الحجز")
    
    with st.form("booking_form"):
        col1, col2 = st.columns(2)
        name = col1.text_input("الاسم الثلاثي")
        phone = col2.text_input("رقم الهاتف")
        
        service = st.selectbox("نوع الكشف / الخدمة", ["استشارة باطنة", "متابعة سكر", "تحاليل وفحوصات"])

        col3, col4 = st.columns(2)
        date_selected = col3.date_input("اختر التاريخ", value=TODAY, min_value=TODAY)
        time_selected = col4.time_input("اختر الوقت")

        submit = st.form_submit_button("تأكيد الحجز الآن ✨")

        if submit:
            real_today = datetime.now().date()
            if date_selected < real_today:
                st.error("❌ لا يمكن الحجز في أيام ماضية")
            elif not name.strip() or not phone.strip():
                st.error("❌ من فضلك اكمل جميع البيانات")
            elif not (time(16, 0) <= time_selected <= time(21, 0)):
                st.error("❌ مواعيد العيادة من 4 عصراً حتى 9 مساءً")
            else:
                c.execute("SELECT 1 FROM bookings WHERE date = ? AND time = ?", (str(date_selected), str(time_selected)))
                if c.fetchone():
                    st.error("❌ هذا الموعد محجوز بالفعل، اختر وقتاً آخر")
                else:
                    c.execute("INSERT INTO bookings (name, phone, service, date, time) VALUES (?, ?, ?, ?, ?)",
                              (name.strip(), phone.strip(), service, str(date_selected), str(time_selected)))
                    conn.commit()
                    st.success("✅ تم حجز الموعد بنجاح.. نتمنى لكم الشفاء العاجل")

# ================= عرض الحجوزات =================
elif menu == "عرض الحجوزات":
    st.markdown("### 🔐 منطقة المسؤول")
    password = st.text_input("ادخل كلمة المرور للعرض", type="password")

    if password == "admin123":
        c.execute("SELECT name, phone, service, date, time FROM bookings ORDER BY date, time")
        rows = c.fetchall()

        if rows:
            df = pd.DataFrame(rows, columns=["الاسم", "الهاتف", "الخدمة", "التاريخ", "الوقت"])
            st.markdown("<div class='table-box'>", unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("لا توجد حجوزات مسجلة حالياً")