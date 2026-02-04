import streamlit as st
from datetime import datetime, date as dt_date, time as dt_time
import sqlite3
import pandas as pd

# ---------------- إعداد قاعدة البيانات ----------------
conn = sqlite3.connect("clinic_bookings.db", check_same_thread=False)
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    service TEXT,
    date TEXT,
    time TEXT
)
''')
conn.commit()

# ---------------- إعداد الصفحة ----------------
st.set_page_config(page_title="عيادة الدكتورة ياسمين عبدالرحمن", layout="wide")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(to bottom, #1E1E2F, #2C2C44);
    color: white;
    font-family: 'Arial', sans-serif;
}
.header {
    color: #FFD700;
    font-size:50px;
    font-weight:bold;
    text-align:center;
    text-shadow: 2px 2px 4px #000000;
    margin-bottom:10px;
}
.subheader {
    color: #00CED1;
    font-size:28px;
    font-weight:bold;
    text-align:center;
    margin-bottom:10px;
}
.info-text {
    color: #FFFFFF;
    font-size:18px;
    text-align:center;
    margin-bottom:30px;
}
.box {
    background: linear-gradient(135deg, #6A5ACD, #00CED1);
    border-radius: 25px;
    padding: 50px;
    margin: 20px auto;
    max-width: 700px;
    font-size:32px;
    font-weight:bold;
    color: #FFFFFF;
    text-align:center;
    box-shadow: 5px 5px 20px #000000;
}
.service-table {
    background: #1E1E2F;
    border-radius: 15px;
    padding: 10px;
    margin: 10px auto;
    max-width: 900px;
    color: #FFFFFF;
}
th {
    background-color: #6A5ACD;
    color: white;
    padding: 8px;
    text-align: center;
}
td {
    text-align: center;
    padding: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- الهيدر ----------------
st.markdown("<div class='header'>🩺 عيادة الدكتورة ياسمين عبدالرحمن</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>أخصائي الباطنة والسكر</div>", unsafe_allow_html=True)
st.markdown("<div class='info-text'>📍 الموقع: سرس الليان - كوبرى المرور<br>📞 رقم التواصل: 01111077824</div>", unsafe_allow_html=True)

# ---------------- التنقل ----------------
menu = st.sidebar.selectbox("القائمة", ["الرئيسية", "حجز موعد", "عرض الحجوزات"])

# ---------------- الرئيسية ----------------
if menu == "الرئيسية":
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='box'>مرحبا بك في عيادتنا 💚</div>", unsafe_allow_html=True)
        st.markdown("<div class='box'>احجز الآن لتحصل على أفضل رعاية صحية!</div>", unsafe_allow_html=True)
    with col2:
        st.image("https://images.unsplash.com/photo-1588776814546-5b67dbbf0b03?auto=format&fit=crop&w=700&q=80", use_column_width=True)

# ---------------- حجز موعد ----------------
elif menu == "حجز موعد":
    st.header("📅 حجز موعد")
    name = st.text_input("الاسم", key="name_clean")
    phone = st.text_input("رقم الهاتف", key="phone_clean")
    service = st.selectbox("الخدمة", ["استشارة باطنة", "متابعة سكر", "تحاليل وفحوصات"])
    date_selected = st.date_input("التاريخ", dt_date.today())
    time_selected = st.time_input("الوقت")

    if st.button("حجز الآن"):
        if not name or not phone:
            st.error("من فضلك اكمل البيانات")
        elif not (dt_time(16,0) <= time_selected <= dt_time(21,0)):
            st.error("الحجز من 4 العصر لـ 9 مساءً")
        else:
            c.execute("SELECT * FROM bookings WHERE date=? AND time=?", (str(date_selected), str(time_selected)))
            if c.fetchone():
                st.error("المعاد ده محجوز")
            else:
                c.execute("INSERT INTO bookings (name, phone, service, date, time) VALUES (?,?,?,?,?)",
                          (name, phone, service, str(date_selected), str(time_selected)))
                conn.commit()
                st.success("✅ تم الحجز بنجاح")

# ---------------- عرض الحجوزات ----------------
elif menu == "عرض الحجوزات":
    password = st.text_input("كلمة المرور", type="password", key="pass_clean")
    if password == "admin123":
        c.execute("SELECT * FROM bookings ORDER BY date, time")
        rows = c.fetchall()
        if rows:
            df = pd.DataFrame(rows, columns=["ID","الاسم","الهاتف","الخدمة","التاريخ","الوقت"])
            df = df.drop(columns=["ID"])
            st.markdown("<div class='service-table'>"+df.to_html(index=False, escape=False)+"</div>", unsafe_allow_html=True)
        else:
            st.info("لا توجد حجوزات حتى الآن")
