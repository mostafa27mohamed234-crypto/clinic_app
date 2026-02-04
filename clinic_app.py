import streamlit as st
from datetime import date as dt_date, time as dt_time
import sqlite3
import pandas as pd

# ================= التاريخ الحالي =================
TODAY = dt_date.today()

# ================= قاعدة البيانات =================
conn = sqlite3.connect("clinic_bookings.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    service TEXT,
    date TEXT,
    time TEXT
)
""")
conn.commit()

# ================= إعداد الصفحة =================
st.set_page_config(
    page_title="عيادة الدكتورة ياسمين عبدالرحمن",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(to bottom, #1E1E2F, #2C2C44);
    color: white;
    font-family: Arial;
}
.header {
    color: #FFD700;
    font-size:48px;
    font-weight:bold;
    text-align:center;
}
.subheader {
    color: #00CED1;
    font-size:26px;
    text-align:center;
}
.info {
    text-align:center;
    font-size:18px;
    margin-bottom:30px;
}
.box {
    background: linear-gradient(135deg, #6A5ACD, #00CED1);
    border-radius:20px;
    padding:40px;
    margin:20px auto;
    max-width:700px;
    font-size:28px;
    text-align:center;
}
.table-box {
    background:#1E1E2F;
    padding:15px;
    border-radius:15px;
}
</style>
""", unsafe_allow_html=True)

# ================= الهيدر =================
st.markdown("<div class='header'>🩺 عيادة الدكتورة ياسمين عبدالرحمن</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>أخصائي الباطنة والسكر</div>", unsafe_allow_html=True)
st.markdown("<div class='info'>📍 سرس الليان - كوبرى المرور<br>📞 01111077824</div>", unsafe_allow_html=True)

# ================= القائمة =================
menu = st.sidebar.selectbox(
    "القائمة",
    ["الرئيسية", "حجز موعد", "عرض الحجوزات"]
)

# ================= الرئيسية =================
if menu == "الرئيسية":
    st.markdown(
        "<div class='box'>أهلاً بيك 🌿<br>احجز الآن لتحصل على أفضل رعاية صحية</div>",
        unsafe_allow_html=True
    )

# ================= حجز موعد =================
elif menu == "حجز موعد":
    st.header("📅 حجز موعد جديد")

    name = st.text_input("الاسم")
    phone = st.text_input("رقم الهاتف")
    service = st.selectbox(
        "الخدمة",
        ["استشارة باطنة", "متابعة سكر", "تحاليل وفحوصات"]
    )

    date_selected = st.date_input(
        "التاريخ",
        value=TODAY,
        min_value=TODAY
    )

    time_selected = st.time_input("الوقت")

    if st.button("حجز الآن"):

        # 🔒 قفل نهائي للأيام الماضية
        if date_selected < TODAY:
            st.error("❌ لا يمكن الحجز في أيام ماضية")
            st.stop()

        if not name.strip() or not phone.strip():
            st.error("❌ من فضلك اكمل جميع البيانات")

        elif not (dt_time(16, 0) <= time_selected <= dt_time(21, 0)):
            st.error("❌ الحجز من 4 العصر حتى 9 مساءً")

        else:
            c.execute(
                "SELECT 1 FROM bookings WHERE date=? AND time=?",
                (str(date_selected), str(time_selected))
            )

            if c.fetchone():
                st.error("❌ هذا الموعد محجوز بالفعل")
            else:
                c.execute(
                    "INSERT INTO bookings (name, phone, service, date, time) VALUES (?,?,?,?,?)",
                    (name, phone, service, str(date_selected), str(time_selected))
                )
                conn.commit()
                st.success("✅ تم حجز الموعد بنجاح")

# ================= عرض الحجوزات =================
elif menu == "عرض الحجوزات":
    password = st.text_input("كلمة المرور", type="password")

    if password == "admin123":
        c.execute(
            "SELECT name, phone, service, date, time FROM bookings ORDER BY date, time"
        )
        rows = c.fetchall()

        if rows:
            df = pd.DataFrame(
                rows,
                columns=["الاسم", "الهاتف", "الخدمة", "التاريخ", "الوقت"]
            )
            st.markdown(
                "<div class='table-box'>" +
                df.to_html(index=False) +
                "</div>",
                unsafe_allow_html=True
            )
        else:
            st.info("لا توجد حجوزات حتى الآن")
