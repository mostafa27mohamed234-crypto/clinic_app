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

# ================= إعداد الصفحة =================
st.set_page_config(
    page_title="عيادة الدكتورة ياسمين عبد الرحمن",
    page_icon="🩺",
    layout="wide"
)

# ================= الستايل الطبي الخرافي (Ultra-Modern) =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');

/* الخلفية والنبض المتحرك */
.stApp {
    background: #0a0e17;
    background-image: 
        radial-gradient(circle at 20% 30%, rgba(0, 206, 209, 0.05) 0%, transparent 50%),
        radial-gradient(circle at 80% 70%, rgba(106, 90, 205, 0.05) 0%, transparent 50%);
    font-family: 'Cairo', sans-serif;
    color: #ffffff;
}

/* تأثير خط نبض القلب الخلفي */
.stApp::after {
    content: "";
    position: fixed;
    top: 50%; left: 0; width: 100%; height: 2px;
    background: linear-gradient(90deg, transparent, #00CED1, transparent);
    opacity: 0.1;
    animation: pulse 4s linear infinite;
    z-index: -1;
}

@keyframes pulse {
    0% { transform: scaleX(0); opacity: 0; }
    50% { opacity: 0.2; }
    100% { transform: scaleX(1); opacity: 0; }
}

/* الهيدر الطبي الفخم */
.medical-header {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(15px);
    border: 1px solid rgba(0, 206, 209, 0.3);
    border-radius: 30px;
    padding: 40px;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0 0 40px rgba(0, 206, 209, 0.1);
}

.doctor-name {
    font-size: 50px;
    font-weight: 700;
    color: #FFD700;
    text-shadow: 0 0 25px rgba(255, 215, 0, 0.4);
    margin-bottom: 10px;
}

.doctor-spec {
    font-size: 26px;
    color: #00CED1;
    letter-spacing: 1px;
}

.contact-info {
    margin-top: 20px;
    padding: 10px;
    background: rgba(0, 206, 209, 0.1);
    border-radius: 50px;
    display: inline-block;
    color: #ffffff;
    font-weight: bold;
}

/* الكروت (البطاقات الزجاجية) */
div[data-testid="stForm"], .st-emotion-cache-12w0qpk {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(20px) !important;
    border-radius: 25px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5) !important;
}

/* مداخل البيانات */
.stTextInput input, .stSelectbox div {
    background-color: rgba(255, 255, 255, 0.05) !important;
    color: white !important;
    border: 1px solid rgba(0, 206, 209, 0.2) !important;
    border-radius: 12px !important;
}

/* الأزرار الطبية */
.stButton > button {
    background: linear-gradient(45deg, #00CED1, #6A5ACD) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: bold !important;
    height: 50px !important;
    width: 100% !important;
    transition: 0.4s !important;
    font-size: 20px !important;
}

.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(0, 206, 209, 0.5);
}

/* الفوتر (توقيع المهندس) */
.footer-note {
    text-align: center;
    color: rgba(255,255,255,0.3);
    margin-top: 50px;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ================= الهيدر الرئيسي =================
st.markdown(f"""
<div class='medical-header'>
    <div class='doctor-name'>🩺 عيادة الدكتورة ياسمين عبد الرحمن</div>
    <div class='doctor-spec'>أخصائي الباطنة والسكر والقدم السكري</div>
    <div class='contact-info'>📍 سرس الليان - كوبرى المرور | 📞 01111077824</div>
</div>
""", unsafe_allow_html=True)

# ================= القائمة الجانبية =================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2785/2785482.png", width=100)
st.sidebar.markdown("---")
menu = st.sidebar.radio("القائمة الرئيسية", ["🏠 الصفحة الرئيسية", "📅 حجز موعد جديد", "📋 كشف الحجوزات"], index=0)

# ================= الرئيسية =================
if menu == "🏠 الصفحة الرئيسية":
    col_l, col_r = st.columns([2, 1])
    with col_l:
        st.markdown(f"""
        <div style='background:rgba(0,206,209,0.05); padding:30px; border-radius:20px; border-left: 5px solid #00CED1;'>
            <h2 style='color:#00CED1;'>مرحباً بكم في عيادتنا 🌿</h2>
            <p style='font-size:18px;'>نحن ملتزمون بتوفير أدق الفحوصات الطبية لمتابعة حالات الباطنة والسكر بأحدث الوسائل العلمية.</p>
            <ul style='list-style-type: "💉 ";'>
                <li>متابعة دورية لحالات السكر.</li>
                <li>فحص القدم السكري.</li>
                <li>استشارات الباطنة العامة.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col_r:
        st.info("🕒 مواعيد العمل:\n\nيومياً من الساعة 4:00 عصراً حتى 9:00 مساءً عدا الجمعة.")

# ================= حجز موعد =================
elif menu == "📅 حجز موعد جديد":
    st.markdown("<h3 style='color:#FFD700;'>📝 استمارة الحجز الإلكتروني</h3>", unsafe_allow_html=True)
    
    with st.form("medical_booking"):
        c1, c2 = st.columns(2)
        name = c1.text_input("اسم المريض بالكامل")
        phone = c2.text_input("رقم الموبايل للتواصل")
        
        service = st.selectbox("نوع الكشف المطلوب", 
                             ["كشف باطنة جديد", "متابعة سكر دورية", "فحص قدم سكري", "استشارة سريعة"])

        c3, c4 = st.columns(2)
        date_selected = c3.date_input("تاريخ الحضور", min_value=TODAY)
        time_selected = c4.time_input("الوقت المفضل")

        if st.form_submit_button("إرسال طلب الحجز 💉"):
            if not name.strip() or not phone.strip():
                st.warning("⚠️ يرجى ملء الاسم ورقم الهاتف")
            elif not (time(16, 0) <= time_selected <= time(21, 0)):
                st.error("❌ عذراً، الحجز متاح فقط من 4 عصراً إلى 9 مساءً")
            else:
                # التحقق من تكرار الموعد
                c.execute("SELECT 1 FROM bookings WHERE date = ? AND time = ?", (str(date_selected), str(time_selected)))
                if c.fetchone():
                    st.error("⚠️ هذا الموعد محجوز مسبقاً، يرجى اختيار وقت آخر")
                else:
                    c.execute("INSERT INTO bookings (name, phone, service, date, time) VALUES (?, ?, ?, ?, ?)",
                              (name.strip(), phone.strip(), service, str(date_selected), str(time_selected)))
                    conn.commit()
                    st.balloons()
                    st.success(f"✅ تم تسجيل حجزك يا {name} بنجاح!")

# ================= عرض الحجوزات =================
elif menu == "📋 كشف الحجوزات":
    st.markdown("<h3 style='color:#00CED1;'>🔐 إدارة العيادة</h3>", unsafe_allow_html=True)
    pwd = st.text_input("كلمة سر المسؤول", type="password")
    
    if pwd == "admin123":
        data = pd.read_sql("SELECT name as 'الاسم', phone as 'الهاتف', service as 'الخدمة', date as 'التاريخ', time as 'الوقت' FROM bookings ORDER BY date DESC, time DESC", conn)
        if not data.empty:
            st.dataframe(data, use_container_width=True)
            # زر لتحميل البيانات اكسل
            csv = data.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 تحميل كشف الحجوزات Excel", csv, "bookings.csv", "text/csv")
        else:
            st.info("لا توجد حجوزات مسجلة حالياً.")

# ================= الفوتر =================
st.markdown(f"""
<div class='footer-note'>
    تم التطوير بواسطة البشمهندس مصطفى الفيشاوي ⚡ 2024<br>
    جميع الحقوق محفوظة لعيادة الدكتورة ياسمين عبد الرحمن
</div>
""", unsafe_allow_html=True)