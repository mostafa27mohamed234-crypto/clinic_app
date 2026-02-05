import streamlit as st
from datetime import datetime, date, time
import sqlite3
import pandas as pd
import time as st_time

# ================= DATABASE SETUP =================
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

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Dr. Yasmine Clinic",
    page_icon="⚕️",
    layout="wide"
)

# ================= LUXURY UI STYLING =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');

/* Hide Streamlit Default Elements */
header[data-testid="stHeader"] {visibility: hidden;}
.stDeployButton {display:none;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Background & Global Font */
.stApp {
    background: #0f172a;
    font-family: 'Poppins', sans-serif;
    color: #f8fafc;
}

/* Luxury Hero Section */
.hero-box {
    background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.01) 100%);
    border: 1px solid rgba(56, 189, 248, 0.3);
    border-radius: 40px;
    padding: 50px;
    margin-bottom: 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    backdrop-filter: blur(20px);
}

.doctor-img {
    width: 250px;
    height: 250px;
    border-radius: 50%;
    border: 5px solid #38bdf8;
    object-fit: cover;
    box-shadow: 0 0 40px rgba(56, 189, 248, 0.4);
}

.hero-text h1 {
    font-size: 55px !important;
    font-weight: 800 !important;
    color: #38bdf8 !important;
    margin-bottom: 5px;
}

.hero-text p {
    font-size: 22px;
    color: #94a3b8;
}

/* Interaction Cards */
.nav-card {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 20px;
    padding: 30px;
    text-align: center;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: 0.3s;
}
.nav-card:hover {
    transform: translateY(-10px);
    border-color: #38bdf8;
    background: rgba(56, 189, 248, 0.1);
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background-color: #020617 !important;
}

/* Button Styling */
.stButton > button {
    background: #38bdf8 !important;
    color: #020617 !important;
    font-weight: bold !important;
    border-radius: 12px !important;
    height: 50px !important;
}
</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/387/387561.png", width=100)
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Navigate to:", ["🏠 Home", "📅 Booking", "📋 Admin Panel", "💡 Health Tips"])

# ================= HOME PAGE =================
if menu == "🏠 Home":
    # Hero Section with Female Doctor Image
    st.markdown(f"""
    <div class="hero-box">
        <div class="hero-text">
            <h1>Dr. Yasmine Abdelrahman</h1>
            <p>Internal Medicine & Diabetes Specialist</p>
            <div style="margin-top:20px; font-size:16px;">
                📍 Sirs Al-Layan - Traffic Bridge<br>
                📞 Contact: 01111077824
            </div>
        </div>
        <img src="https://img.freepik.com/free-photo/pleased-young-female-doctor-wearing-medical-gown-with-stethoscope-around-neck-standing-with-folded-arms-isolated-white-background_141793-58707.jpg" class="doctor-img">
    </div>
    """, unsafe_allow_html=True)

    # Quick Access Grid
    st.markdown("<h2 style='text-align:center;'>Welcome to Our Clinic</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("<div class='nav-card'><h3>💉</h3><h4>General Medicine</h4><p>High-quality diagnostic services.</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='nav-card'><h3>🩸</h3><h4>Diabetes Follow-up</h4><p>Stay healthy with regular checks.</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='nav-card'><h3>🦶</h3><h4>Diabetic Foot</h4><p>Professional prevention & care.</p></div>", unsafe_allow_html=True)

# ================= BOOKING PAGE =================
elif menu == "📅 Booking":
    st.markdown("<h1 style='text-align:center;'>Schedule an Appointment</h1>", unsafe_allow_html=True)
    with st.form("booking_form"):
        name = st.text_input("Full Name")
        phone = st.text_input("Phone Number")
        service = st.selectbox("Service", ["Checkup", "Diabetes Care", "Consultation"])
        b_date = st.date_input("Select Date", min_value=date.today())
        b_time = st.time_input("Select Time")
        
        if st.form_submit_button("Confirm Booking"):
            if name and phone:
                c.execute("INSERT INTO bookings (name, phone, service, date, time) VALUES (?,?,?,?,?)",
                          (name, phone, service, str(b_date), str(b_time)))
                conn.commit()
                st.success("Appointment confirmed! See you soon.")
                st.balloons()
            else:
                st.error("Please fill all fields.")

# ================= ADMIN PANEL =================
elif menu == "📋 Admin Panel":
    st.markdown("<h1>Admin Access</h1>", unsafe_allow_html=True)
    pwd = st.text_input("Password", type="password")
    if pwd == "admin123":
        df = pd.read_sql("SELECT * FROM bookings", conn)
        st.dataframe(df, use_container_width=True)

# ================= TIPS =================
elif menu == "💡 Health Tips":
    st.info("💡 Keep your blood sugar stable by walking 30 minutes daily.")

# ================= FOOTER =================
st.markdown(f"""
<div style='text-align:center; padding:30px; color:#64748b; border-top:1px solid rgba(255,255,255,0.1); margin-top:50px;'>
    Developed by <b>Eng. Mostafa El-Fishawy</b> ⚡ 2024
</div>
""", unsafe_allow_html=True)