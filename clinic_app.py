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

# ================= ADVANCED CSS (ULTIMATE UI) =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');

/* Hide Streamlit Elements */
header[data-testid="stHeader"] {visibility: hidden;}
.stDeployButton {display:none;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Global Styles */
.stApp {
    background: radial-gradient(circle at top right, #1e293b, #0f172a);
    font-family: 'Poppins', sans-serif;
    color: #f8fafc;
}

/* Hero Section */
.hero-container {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(15px);
    border-radius: 30px;
    padding: 50px;
    margin-bottom: 40px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}

.hero-content h1 {
    font-size: 50px !important;
    font-weight: 800 !important;
    background: linear-gradient(to right, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}

.hero-content p {
    font-size: 20px;
    color: #94a3b8;
}

.doctor-image {
    width: 220px;
    height: 220px;
    border-radius: 50%;
    border: 4px solid #38bdf8;
    object-fit: cover;
    box-shadow: 0 0 30px rgba(56, 189, 248, 0.4);
}

/* Glass Cards */
.glass-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 30px;
    text-align: center;
    transition: all 0.4s ease;
}

.glass-card:hover {
    background: rgba(56, 189, 248, 0.1);
    transform: translateY(-10px);
    border-color: #38bdf8;
}

/* Form Styles */
div[data-testid="stForm"] {
    background: rgba(255, 255, 255, 0.05) !important;
    border-radius: 25px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    padding: 40px !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(90deg, #0ea5e9, #6366f1) !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 15px 30px !important;
    border-radius: 15px !important;
    border: none !important;
    width: 100% !important;
    transition: 0.3s !important;
}

.stButton > button:hover {
    box-shadow: 0 10px 20px rgba(14, 165, 233, 0.4) !important;
    transform: scale(1.02) !important;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background-color: #0f172a !important;
    border-right: 1px solid rgba(255, 255, 255, 0.1);
}
</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR NAVIGATION =================
st.sidebar.markdown("<h2 style='text-align:center; color:#38bdf8;'>Control Panel</h2>", unsafe_allow_html=True)
menu = st.sidebar.radio(
    "Go to:",
    ["🏠 Home", "📅 Book Appointment", "📋 View Bookings", "💡 Health Tips"],
    key="nav_menu"
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='color:#94a3b8; padding:10px;'>
    <b>🕒 Working Hours:</b><br>
    Daily: 4:00 PM - 9:00 PM<br>
    Friday: Closed
</div>
""", unsafe_allow_html=True)

# ================= HOME SECTION =================
if menu == "🏠 Home":
    st.markdown(f"""
    <div class="hero-container">
        <div class="hero-content">
            <h1>Dr. Yasmine Abdelrahman</h1>
            <p>Internal Medicine & Diabetes Specialist</p>
            <p style="font-size:16px;">📍 Sirs Al-Layan - Traffic Bridge | 📞 01111077824</p>
        </div>
        <img src="https://img.freepik.com/free-photo/doctor-offering-medical-teleconsultation_23-2149329007.jpg" class="doctor-image">
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='text-align:center; margin-bottom:40px;'>Our Specialties</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("<div class='glass-card'><h3>🩺</h3><h3>Internal Medicine</h3><p>Accurate diagnosis for gastrointestinal and kidney diseases.</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='glass-card'><h3>🩸</h3><h3>Diabetes Care</h3><p>Comprehensive monitoring and personalized nutrition plans.</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='glass-card'><h3>🦶</h3><h3>Diabetic Foot</h3><p>Professional screening and prevention of complications.</p></div>", unsafe_allow_html=True)

# ================= BOOKING SECTION =================
elif menu == "📅 Book Appointment":
    st.markdown("<h1 style='text-align:center;'>Reserve Your Visit</h1>", unsafe_allow_html=True)
    
    with st.form("booking_form"):
        col1, col2 = st.columns(2)
        name = col1.text_input("Full Name", placeholder="Enter your name")
        phone = col2.text_input("Phone Number", placeholder="01xxxxxxxxx")
        
        service = st.selectbox("Service Type", ["General Checkup", "Diabetes Follow-up", "Diabetic Foot Exam", "Consultation"])
        
        col3, col4 = st.columns(2)
        b_date = col3.date_input("Date", min_value=date.today())
        b_time = col4.time_input("Preferred Time")
        
        submitted = st.form_submit_button("Confirm Booking ✅")
        
        if submitted:
            if name and phone:
                # Working hours check
                if time(16, 0) <= b_time <= time(21, 0):
                    c.execute("INSERT INTO bookings (name, phone, service, date, time) VALUES (?,?,?,?,?)",
                              (name, phone, service, str(b_date), str(b_time)))
                    conn.commit()
                    st.success(f"Success! Your appointment is scheduled for {b_date}")
                    st.balloons()
                else:
                    st.error("Please select a time between 4:00 PM and 9:00 PM.")
            else:
                st.warning("Please fill in all required fields.")

# ================= ADMIN VIEW =================
elif menu == "📋 View Bookings":
    st.markdown("<h1 style='text-align:center;'>Admin Dashboard</h1>", unsafe_allow_html=True)
    password = st.text_input("Enter Admin Password", type="password")
    
    if password == "admin123":
        df = pd.read_sql("SELECT name, phone, service, date, time FROM bookings ORDER BY date", conn)
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No bookings found.")
    elif password:
        st.error("Access Denied!")

# ================= TIPS SECTION =================
elif menu == "💡 Health Tips":
    st.markdown("<h1 style='text-align:center;'>Daily Wellness</h1>", unsafe_allow_html=True)
    st.info("💧 Hydration is key: Drink at least 3 liters of water daily.")
    st.success("🍏 Balanced Diet: Include more fiber and greens in your meals.")

# ================= FOOTER =================
st.markdown(f"""
<div style='text-align:center; padding:40px; color:#64748b; font-size:14px; border-top:1px solid rgba(255,255,255,0.05); margin-top:50px;'>
    Developed by <b>Eng. Mostafa El-Fishawy</b> ⚡ 2024<br>
    All Rights Reserved - Dr. Yasmine Clinic
</div>
""", unsafe_allow_html=True)