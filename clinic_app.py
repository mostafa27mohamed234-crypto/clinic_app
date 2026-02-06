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

# ================= الستايل الطبي الخرافي (Ultimate Medical UI) =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Play&display=swap');

/* الخلفية الطبية المتدرجة */
.stApp {
    background: linear-gradient(135deg, #1A2A3A, #0A1520); /* تدرج أزرق داكن */
    font-family: 'Cairo', sans-serif;
    color: #E0E0E0; /* لون نص فاتح وواضح */
    background-attachment: fixed;
}

/* تأثير جزيئات طبية خفيفة في الخلفية */
.stApp::before {
    content: "";
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    background: url('https://www.transparenttextures.com/patterns/micro-carbon.png'); /* نسيج خفيف */
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
    border: 2px solid #00BFFF; /* أزرق سماوي */
    box-shadow: 0 10px 40px rgba(0, 191, 255, 0.3);
    display: flex;
    align-items: center;
    justify-content: space-around;
    flex-wrap: wrap;
    position: relative;
    overflow: hidden;
}

.doctor-hero-header::before { /* تأثير ضوئي خفيف */
    content: "";
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle, rgba(0, 191, 255, 0.1) 0%, transparent 70%);
    animation: rotateLight 10s linear infinite;
}

@keyframes rotateLight {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
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
    color: #FFD700; /* ذهبي */
    text-shadow: 0 0 20px rgba(255, 215, 0, 0.6);
    line-height: 1.2;
}

.doctor-specialty {
    font-size: 30px;
    color: #00BFFF; /* أزرق سماوي */
    margin-top: 5px;
}

.doctor-contact-details {
    font-size: 20px;
    color: #E0E0E0;
    margin-top: 15px;
}

/* الكروت (البطاقات) بتأثير 3D */
div[data-testid="stForm"], .st-emotion-cache-12w0qpk, .st-emotion-cache-1d0b11n { 
    background: rgba(255, 255, 255, 0.07) !important;
    backdrop-filter: blur(18px) !important;
    border-radius: 20px !important;
    border: 1px solid rgba(0, 191, 255, 0.2) !important;
    box-shadow: 0 12px 30px rgba(0,0,0,0.5), 0 0 0 4px rgba(0, 191, 255, 0.05) !important;
    transition: all 0.3s ease-in-out;
}

div[data-testid="stForm"]:hover, .st-emotion-cache-12w0qpk:hover {
    box-shadow: 0 15px 40px rgba(0,0,0,0.6), 0 0 0 5px rgba(0, 191, 255, 0.1) !important;
    transform: translateY(-3px);
}

/* عناوين الأقسام */
h1, h2, h3, h4 {
    color: #FFD700; 
    font-weight: bold;
    text-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
}

/* الأزرار الطبية العصرية */
.stButton > button {
    background: linear-gradient(45deg, #00BFFF, #007FFF) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: bold !important;
    height: 50px !important;
    width: 100% !important;
    transition: all 0.3s ease !important;
    font-size: 18px !important;
    box-shadow: 0 5px 15px rgba(0, 191, 255, 0.4);
}

.footer-signature {
    text-align: center;
    padding: 25px;
    margin-top: 50px;
    border-top: 1px solid rgba(0, 191, 255, 0.2);
    color: #999999;
    font-size: 15px;
}
.footer-signature b {
    color: #00BFFF;
}
</style>
""", unsafe_allow_html=True)

# ================= الهيدر الرئيسي - لوحة معلومات الأطباء =================
st.markdown(f"""
<div class='doctor-hero-header'>
    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR_x1p7jP6s_bS0S4D5dY3D7Y_oJ0Q2_M7x7Q&s" class='doctor-hero-photo' alt='Doctor Yasmine Photo'>
    <div class='doctor-hero-info'>
        <div class='doctor-name-main'>عيادة الدكتورة ياسمين عبد الرحمن</div>
        <div class='doctor-specialty'>أخصائي الباطنة والسكر والجهاز الهضمي</div>
        <div class='doctor-contact-details'>📍 سرس الليان - كوبرى المرور | 📞 01111077824</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ================= القائمة الجانبية =================
st.sidebar.markdown("<h3 style='color:#FFD700; text-align:center;'>لوحة التحكم ⚕️</h3>", unsafe_allow_html=True)
menu = st.sidebar.radio("اختر القسم", 
                        ["🏠 الرئيسية", "📅 حجز موعد", "📋 عرض الحجوزات", "💡 نصائح صحية"], 
                        index=0, key="main_menu")
st.sidebar.markdown("---")
st.sidebar.info("🕒 مواعيد العمل:\n\nيومياً من الساعة 5:00 مساءً حتى 9:00 مساءً\n(ما عدا يوم الجمعة إجازة).")


# ================= المحتوى الرئيسي =================

# 🏠 الرئيسية
if menu == "🏠 الرئيسية":
    st.markdown("<h2 style='text-align:center;'>خدماتنا المميزة 🌟</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div style='background:rgba(0,191,255,0.05); padding:20px; border-radius:15px; border-left: 3px solid #00BFFF;'>
            <h4 style='color:#00BFFF;'>💉 استشارات باطنة</h4>
            <p>نقدم تشخيصاً دقيقاً وعلاجاً فعالاً لأمراض القلب، الكلى، والغدد الصماء.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style='background:rgba(0,191,255,0.05); padding:20px; border-radius:15px; border-left: 3px solid #00BFFF;'>
            <h4 style='color:#00BFFF;'>🩸 متابعة حالات السكر</h4>
            <p>برامج متكاملة لمتابعة مستويات السكر، وضع خطط علاجية وتغذوية للحفاظ على صحتكم.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div style='background:rgba(0,191,255,0.05); padding:20px; border-radius:15px; border-left: 3px solid #00BFFF;'>
            <h4 style='color:#00BFFF;'>🧪 أمراض الجهاز الهضمي</h4>
            <p>تشخيص وعلاج اضطرابات القولون، المعدة، والمرارة وتوفير الرعاية اللازمة.</p>
        </div>
        """, unsafe_allow_html=True)

# 📅 حجز موعد
elif menu == "📅 حجز موعد":
    st.markdown("<h2 style='text-align:center;'>احجز موعدك الآن بكل سهولة 📅</h2>", unsafe_allow_html=True)
    
    with st.form("medical_booking"):
        col1, col2 = st.columns(2)
        name = col1.text_input("الاسم بالكامل", placeholder="الاسم ثلاثي")
        phone = col2.text_input("رقم الهاتف (للتواصل)", placeholder="مثال: 01xxxxxxxxx")
        
        service = st.selectbox("اختر نوع الخدمة / الكشف", 
                               ["كشف باطنة عام", "متابعة سكر", "كشف جهاز هضمي", "استشارة"],
                               index=0, key="service_select")

        col3, col4 = st.columns(2)
        date_selected = col3.date_input("تاريخ الحضور", min_value=TODAY, key="date_input")
        time_selected = col4.time_input("الوقت المفضل", key="time_input")

        submit_button = st.form_submit_button("تأكيد الحجز 🌟")

        if submit_button:
            if not name.strip() or not phone.strip():
                st.error("⚠️ من فضلك، املأ جميع الحقول المطلوبة (الاسم ورقم الهاتف).")
            # التعديل: المواعيد من 5 مساءً (17) لـ 9 مساءً (21)
            elif not (st_time.time(17, 0) <= time_selected <= st_time.time(21, 0)):
                st.error("❌ عذراً، مواعيد الحجز المتاحة من 5 مساءً حتى 9 مساءً فقط.")
            else:
                c.execute("SELECT 1 FROM bookings WHERE date = ? AND time = ?", (str(date_selected), str(time_selected)))
                if c.fetchone():
                    st.warning("⚠️ هذا الموعد محجوز بالفعل. يرجى اختيار وقت آخر.")
                else:
                    progress_text = "جاري تأكيد الحجز..."
                    booking_progress = st.progress(0, text=progress_text)
                    for percent_complete in range(100):
                        st_time.sleep(0.01) 
                        booking_progress.progress(percent_complete + 1, text=progress_text)
                    
                    c.execute("INSERT INTO bookings (name, phone, service, date, time) VALUES (?, ?, ?, ?, ?)",
                              (name.strip(), phone.strip(), service, str(date_selected), str(time_selected)))
                    conn.commit()
                    booking_progress.empty() 
                    st.success(f"✅ تم تأكيد حجزك يا: {name} بنجاح! ننتظركم في الموعد.")
                    st.balloons() 

# 📋 عرض الحجوزات (للمسؤول)
elif menu == "📋 عرض الحجوزات":
    st.markdown("<h2 style='text-align:center;'>لوحة إدارة الحجوزات 🔐</h2>", unsafe_allow_html=True)
    pwd = st.text_input("كلمة سر المسؤول", type="password", key="admin_pwd_view")
    
    if pwd == "admin123":
        st.markdown("<h3 style='color:#00BFFF;'>قائمة بجميع الحجوزات:</h3>", unsafe_allow_html=True)
        data = pd.read_sql("SELECT name as 'اسم المريض', phone as 'رقم الهاتف', service as 'الخدمة', date as 'التاريخ', time as 'الوقت' FROM bookings ORDER BY date DESC, time DESC", conn)
        
        if not data.empty:
            st.dataframe(data, use_container_width=True)
            csv = data.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                "📥 تحميل كشف الحجوزات (Excel)",
                csv,
                "Clinic_Bookings.csv",
                "text/csv;charset=utf-8",
                key="download_bookings_csv"
            )
            
            st.markdown("---")
            st.markdown("<h3 style='color:#FFD700;'>خيارات إضافية:</h3>", unsafe_allow_html=True)
            if st.button("🗑️ مسح كل الحجوزات القديمة", key="clear_all_bookings_btn"):
                c.execute("DELETE FROM bookings WHERE date < ?", (str(TODAY),))
                conn.commit()
                st.success("✅ تم مسح الحجوزات المنتهية بنجاح.")
                st.rerun() 
        else:
            st.info("لا توجد حجوزات مسجلة حالياً.")
    elif pwd: 
        st.error("❌ كلمة المرور غير صحيحة.")

# 💡 نصائح صحية
elif menu == "💡 نصائح صحية":
    st.markdown("<h2 style='text-align:center;'>نصائح صحية من عيادة الدكتورة ياسمين 🩺</h2>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='background:rgba(255,255,255,0.05); padding:25px; border-radius:20px; margin-bottom:20px; border-left: 4px solid #FFD700;'>
        <h3 style='color:#FFD700;'>💎 حافظ على صحتك</h3>
        <p>شرب كميات كافية من الماء يومياً يساعد على تحسين وظائف الجهاز الهضمي ويقلل من الحموضة.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style='background:rgba(255,255,255,0.05); padding:25px; border-radius:20px; margin-bottom:20px; border-left: 4px solid #00BFFF;'>
        <h3 style='color:#00BFFF;'>🍏 التغذية السليمة</h3>
        <p>تناول الألياف المتوفرة في الخضروات والفواكه يعزز صحة القولون ويمنع اضطرابات المعدة.</p>
    </div>
    """, unsafe_allow_html=True)


# ================= الفوتر (توقيع المهندس) =================
st.markdown(f"""
<div class='footer-signature'>
    تم التطوير بواسطة <b>البشمهندس مصطفى الفيشاوي</b> ⚡ 2024<br>
    جميع الحقوق محفوظة لعيادة الدكتورة ياسمين عبد الرحمن
</div>
""", unsafe_allow_html=True)