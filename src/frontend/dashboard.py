import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import datetime

API = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Grievance System", layout="wide")

# -------- SESSION --------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

# -------- LOGIN --------
if not st.session_state.logged_in:
    st.title("🔐 Login Panel")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "" or password == "":
            st.warning("Enter credentials")
        else:
            try:
                res = requests.post(
                    f"{API}/login",
                    json={"username": username, "password": password},
                    timeout=5
                ).json()

                if res["status"] == "success":
                    st.session_state.logged_in = True
                    st.session_state.role = res["role"]
                    st.success("Login successful")
                    st.rerun()
                else:
                    st.error("Invalid credentials")

            except Exception as e:
                st.error("❌ Backend not running")
                st.text(str(e))

    st.stop()

# -------- HEADER --------
st.title("🧠 AI Grievance Dashboard")

st.sidebar.success(f"Logged in as: {st.session_state.role}")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# -------- INPUT --------
st.subheader("📝 Submit Complaint")

text = st.text_area("Enter complaint")

if st.button("🔍 Analyze"):
    if text.strip() == "":
        st.warning("Enter complaint first")
    else:
        try:
            res = requests.post(
                f"{API}/analyze",
                json={"text": text},
                timeout=5
            ).json()

            c1, c2, c3 = st.columns(3)
            c1.metric("Category", res["category"])
            c2.metric("Sentiment", res["sentiment"])
            c3.metric("Priority", res["priority"])

        except Exception as e:
            st.error("❌ Backend error")
            st.text(str(e))

st.markdown("---")

# -------- DASHBOARD --------
st.subheader("📊 Dashboard")

# 🔄 Refresh Button
if st.button("🔄 Refresh"):
    st.rerun()

try:
    response = requests.get(f"{API}/complaints", timeout=5)

    if response.status_code != 200:
        st.error("API Error")
        st.stop()

    data = response.json()

    if not data:
        st.warning("No complaints yet")
        st.stop()

    df = pd.DataFrame(data, columns=[
        "ID","Text","Category","Priority","Sentiment","Status"
    ])

    # ⏰ Last Updated
    st.markdown(
        f"<p style='color:gray;'>⏰ Last updated: {datetime.datetime.now().strftime('%H:%M:%S')}</p>",
        unsafe_allow_html=True
    )

    # -------- KPI --------
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total", len(df))
    c2.metric("High", len(df[df["Priority"]=="High"]))
    c3.metric("Departments", df["Category"].nunique())
    c4.metric("Pending", len(df[df["Status"]=="Pending"]))

    st.dataframe(df, width="stretch")

    # -------- CHARTS --------
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(px.pie(df, names="Category"), width="stretch")

    with col2:
        st.plotly_chart(px.pie(df, names="Priority"), width="stretch")

except Exception as e:
    st.error("❌ Backend not reachable")
    st.text(str(e))
    st.stop()

# -------- ADMIN PANEL --------
if st.session_state.role == "admin":
    st.markdown("### 🛠 Admin Panel")

    cid = st.number_input("Complaint ID", step=1)
    status = st.selectbox("Status", ["Pending","Resolved"])

    if st.button("Update Status"):
        try:
            requests.put(
                f"{API}/update/{cid}",
                params={"status": status},
                timeout=5
            )
            st.success("✅ Updated")
            st.rerun()
        except:
            st.error("❌ Update failed")