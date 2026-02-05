import streamlit as st
from datetime import datetime, date, time
import sqlite3
import pandas as pd

# ================= DATABASE =================
conn = sqlite3.connect("clinic_bookings.db", check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS bookings (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, service TEXT, date TEXT, time TEXT)")
conn.commit()

# ================= CONFIG =================
st.set_page_config(page_title="Dr. Yasmine Clinic", page_icon="⚕️", layout="wide")

# ================= SESSION STATE (FOR NAVIGATION) =================
if 'page' not in st.session_state:
    st.session_state.page = "🏠 Home"

def change_page(page_name):
    st.session_state.page = page_name

# ================= CSS (THE LUXURY GLOW) =================
st.markdown("""
<style>
header[data-testid="stHeader"] {visibility: hidden;}
.stDeployButton {display:none;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stApp { background: #020617; font-family: 'Poppins', sans-serif; color: white; }

/* صورة الطبيبة الدائرية */
.doctor-container {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
}
.doctor-circle {
    width: 250px;
    height: 250px;
    border-radius: 50% !important; /* دايرة مثالية */
    object-fit: cover;
    border: 5px solid #38bdf8;
    box-shadow: 0 0 30px rgba(56, 189, 248, 0.6);
}

.hero-section { text-align: center; padding: 40px; }
.hero-section h1 { font-size: 60px; color: #38bdf8; font-weight: 800; }

/* تصميم زرار الحجز العملاق */
.stButton > button {
    background: linear-gradient(90deg, #38bdf8, #6366f1) !important;
    color: white !important;
    font-size: 24px !important;
    font-weight: bold !important;
    border-radius: 50px !important;
    padding: 15px 50px !important;
    border: none !important;
    display: block;
    margin: 0 auto;
}
</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
st.sidebar.title("🏥 Clinic Menu")
choice = st.sidebar.radio("Navigate", ["🏠 Home", "📅 Booking", "📋 Admin", "💡 Tips"], index=0 if st.session_state.page == "🏠 Home" else 1)

# Sync sidebar with session state
if choice != st.session_state.page:
    st.session_state.page = choice

# ================= HOME PAGE =================
if st.session_state.page == "🏠 Home":
    st.markdown('<div class="hero-section">', unsafe_allow_html=True)
    
    # الصورة الدائرية
    st.markdown("""
    <div class="doctor-container">
        <img src="https://img.freepik.com/free-photo/pleased-young-female-doctor-wearing-medical-gown-with-stethoscope-around-neck-standing-with-folded-arms-isolated-white-background_141793-58707.jpg" class="doctor-circle">
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1>Dr. Yasmine Abdelrahman</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:24px; color:#94a3b8;'>Internal Medicine & Diabetes Expert</p>", unsafe_allow_html=True)
    
    # زرار الحجز اللي بيفتح الصفحة
    st.write("---")
    if st.button("🚀 BOOK YOUR APPOINTMENT NOW"):
        st.session_state.page = "📅 Booking"
        st.rerun()
    st.write("---")

# ================= BOOKING PAGE =================
elif st.session_state.page == "📅 Booking":
    st.markdown("<h1 style='text-align:center; color:#38bdf8;'>📅 Appointment Form</h1>", unsafe_allow_html=True)
    with st.form("booking_form"):
        name = st.text_input("Patient Full Name")
        phone = st.text_input("Mobile Number")
        service = st.selectbox("Service", ["General Medicine", "Diabetes Follow-up", "Foot Care"])
        b_date = st.date_input("Visit Date")
        b_time = st.time_input("Visit Time")
        
        if st.form_submit_button("Confirm Booking ✅"):
            if name and phone:
                c.execute("INSERT INTO bookings (name, phone, service, date, time) VALUES (?,?,?,?,?)",
                          (name, phone, service, str(b_date), str(b_time)))
                conn.commit()
                st.success("🎉 Appointment Registered Successfully!")
                st.balloons()
            else:
                st.error("Missing Data!")

# ================= ADMIN =================
elif st.session_state.page == "📋 Admin":
    pwd = st.text_input("Admin Password", type="password")
    if pwd == "admin123":
        df = pd.read_sql("SELECT * FROM bookings", conn)
        st.dataframe(df, use_container_width=True)

# ================= TIPS =================
elif st.session_state.page == "💡 Tips":
    st.info("Stay Healthy: Drink 3L of water and walk 30 mins a day!")

# ================= FOOTER =================
st.markdown(f"""
<div style='text-align:center; padding:30px; color:#64748b; margin-top:50px;'>
    Developed by <b>Eng. Mostafa El-Fishawy</b> ⚡ 2026
</div>
""", unsafe_allow_html=True)