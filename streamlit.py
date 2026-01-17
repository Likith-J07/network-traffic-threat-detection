import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# ===== APP CONFIG =====
st.set_page_config(page_title="Real-Time Network Traffic Monitor", layout="wide")

# ===== CUSTOM CSS =====
st.markdown("""
    <style>
        body, .stApp {
            background: linear-gradient(135deg, #fbe9e7, #fce4ec) !important;
            font-family: 'Inter', 'Segoe UI', sans-serif;
            color: #1b2a49 !important;
        }
        div[data-testid="stVerticalBlock"] > div {
            background: white;
            border-radius: 20px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.1);
            margin-bottom: 25px;
            padding: 25px 28px;
        }
        .section-title {
            color: #d81b60;
            font-weight: 800;
            font-size: 1.6rem;
            border-bottom: 2px solid #d81b60;
            margin-bottom: 15px;
        }
        .stTextInput>div>input, .stNumberInput input {
            background: #fff0f6 !important;
            border-radius: 12px !important;
            border: 2px solid #f48fb1 !important;
            padding: 12px 14px;
            font-size: 1.05rem;
            color: #1b2a49 !important;
        }
        .stButton>button {
            background: linear-gradient(90deg, #ec407a, #d81b60);
            color: white;
            font-weight: 700;
            font-size: 1.2rem;
            padding: 12px 0;
            border-radius: 25px;
            box-shadow: 0 4px 15px rgba(216,27,96,0.4);
            width: 100%;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #c2185b, #ad1457);
        }
        .stDataFrame table {
            color: #1b2a49;
            font-size: 1rem;
        }
        .login-main {
            min-height: 95vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #f8bbd0, #fce4ec);
        }
        .login-card {
            background: white;
            padding: 50px 55px;
            border-radius: 28px;
            box-shadow: 0 18px 50px rgba(233,30,99,0.25);
            max-width: 430px;
            text-align: center;
            border: 2px solid #ec407a;
            position: relative;
            overflow: hidden;
        }
        .login-card:before {
            content: "";
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle at center, rgba(236,64,122,0.1) 0%, transparent 70%);
            z-index: 0;
        }
        .login-icon {
            font-size: 4rem;
            color: #d81b60;
            margin-bottom: 20px;
            z-index: 1;
            position: relative;
        }
        .login-title {
            font-size: 2.2rem;
            font-weight: 900;
            color: #ad1457;
            margin-bottom: 12px;
            z-index: 1;
            position: relative;
        }
        .login-subtext {
            font-size: 1.1rem;
            color: #6a1b9a;
            margin-bottom: 30px;
            z-index: 1;
            position: relative;
        }
        .stError {
            font-size: 1.1rem;
            font-weight: 600;
            color: #f44336 !important;
        }
    </style>
""", unsafe_allow_html=True)

# ========= LOGIN PAGE ==========
def login_page():
    st.markdown("""
        <div class="login-main">
            <div class="login-card">
                <div class="login-icon">🛡️</div>
                <div class="login-title">Secure Network Monitor</div>
                <div class="login-subtext">AI-powered real-time protection</div>
    """, unsafe_allow_html=True)

    username = st.text_input("Username", key="username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", key="password", placeholder="Enter your password")
    login_btn = st.button("Sign In", key="loginbutton")

    st.markdown("</div></div>", unsafe_allow_html=True)

    if login_btn:
        if username == "admin" and password == "admin123":
            st.session_state["logged_in"] = True
            if hasattr(st, 'experimental_rerun'):
                st.experimental_rerun()
            else:
                st.markdown("<script>window.location.reload();</script>", unsafe_allow_html=True)
        else:
            st.error("❌ Incorrect username or password.")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login_page()
    st.stop()

# ========= DASHBOARD ==========
st.markdown("""
    <div style="background-color:#fce4ec; border-radius: 15px; padding: 25px 30px; margin-bottom:20px;">
        <h2 style="color:#6d0d36; margin-bottom: 0;">📡 Real-Time <span style="color:#6d0d36;">Network Traffic Monitor</span></h2>
        <p style="color:#6d0d36; font-size: 1.15rem;">Live AI-powered dashboard — manual prediction, export & visualization</p>
    </div>
""", unsafe_allow_html=True)

# ------- Manual Prediction -------
with st.container():
    st.markdown('<div class="section-title">📝 Manual Prediction Input</div>', unsafe_allow_html=True)
    with st.form("manual_form"):
        cols = st.columns(6)
        protocol = cols[0].selectbox("Protocol", ["TCP", "UDP", "ICMP"])
        packet_size = cols[1].number_input("Packet Size", min_value=1, value=100)
        flow_duration = cols[2].number_input("Flow Duration", min_value=0.0, format="%.6f", value=0.1)
        flags = cols[3].selectbox("Flags", ["-", "SYN", "FIN", "ACK", "PSH"])
        src_ip = cols[4].text_input("Source IP Address", placeholder="Enter Src IP")
        dst_ip = cols[5].text_input("Destination IP Address", placeholder="Enter Dst IP")
        submit_btn = st.form_submit_button("Get Prediction")
        if submit_btn:
            data = {
                "Protocol": protocol,
                "Packet_Size": packet_size,
                "Flow_Duration": flow_duration,
                "Flags": flags,
                "Src_IP": src_ip,
                "Dst_IP": dst_ip,
            }
            try:
                resp = requests.post("http://127.0.0.1:5000/predict", json=data)
                if resp.status_code == 200:
                    res = resp.json()
                    st.success(f"Prediction: {res.get('prediction','N/A')}\nSource IP: {src_ip}\nDestination IP: {dst_ip}")
                else:
                    st.error("❌ Flask backend not responding.")
            except Exception as e:
                st.error(f"Error: {e}")

# ========= Charts (Medium Blue, Red, Yellow) ==========
def plot_bar(df):
    counts = df['prediction'].value_counts().reset_index()
    counts.columns = ['Label', 'Count']

    color_palette = ["#1E90FF", "#FF4C4C", "#FFD700"]  # Blue, Red, Yellow

    fig = px.bar(
        counts, x='Label', y='Count', color='Label',
        text='Count',
        color_discrete_sequence=color_palette,
        title="Prediction Distribution"
    )
    fig.update_traces(marker_line_color="#222", marker_line_width=1.5, textfont_size=16)
    fig.update_layout(
        width=700, height=400,
        margin=dict(l=10, r=10, t=40, b=20),
        plot_bgcolor="#fefefe",
        paper_bgcolor="#fefefe",
        showlegend=False
    )
    return fig

def plot_pie(df):
    pie_data = df['prediction'].value_counts().reset_index()
    pie_data.columns = ['Label', 'Count']

    color_palette = ["#1E90FF", "#FF4C4C", "#FFD700"]  # Blue, Red, Yellow

    fig = px.pie(
        pie_data, names='Label', values='Count',
        color_discrete_sequence=color_palette,
        hole=0.35, title="Prediction Breakdown"
    )
    fig.update_traces(
        textinfo='percent+label',
        textfont_size=15,
        marker=dict(line=dict(color='white', width=2))
    )
    fig.update_layout(
        width=700, height=400,
        margin=dict(l=10, r=10, t=40, b=20),
        plot_bgcolor="#fefefe",
        paper_bgcolor="#fefefe",
        showlegend=True
    )
    return fig

# ========= Prediction Table + Charts ==========
st.markdown('<h3 style="color:#ad1457; font-weight:800; margin-bottom:10px;">📋 Prediction Results</h3>', unsafe_allow_html=True)

table_container = st.container()
bar_chart_container = st.container()
pie_chart_container = st.container()

with table_container:
    download_btn_placeholder = st.empty()
    prediction_table = st.empty()

with bar_chart_container:
    bar_chart_placeholder = st.empty()

with pie_chart_container:
    pie_chart_placeholder = st.empty()

# Auto-refresh every 3 sec
count = st_autorefresh(interval=3000, limit=None, key="refresh")

try:
    response = requests.get("http://127.0.0.1:5000/history")
    if response.status_code == 200:
        data = response.json()
        if data:
            df = pd.DataFrame(data)
            df = df[::-1]  # Latest first

            if not df.empty and any(df['prediction'].isin(["DDoS", "PortScan"])):
                st.warning("⚠️ Suspicious network activity detected!", icon="🚨")

            download_btn_placeholder.download_button(
                label="⬇️ Download Predictions (CSV)",
                data=df.to_csv(index=False).encode(),
                file_name="predictions.csv",
                mime="text/csv",
                key=f"download_csv_{count}"
            )

            prediction_table.dataframe(df, height=300, use_container_width=True, hide_index=True)

            bar_chart_placeholder.plotly_chart(plot_bar(df), use_container_width=True)
            pie_chart_placeholder.plotly_chart(plot_pie(df), use_container_width=True)

        else:
            prediction_table.info("⚠️ No prediction data yet. Waiting for traffic simulation...", icon="ℹ️")
    else:
        prediction_table.error("❌ Flask backend not responding.", icon="🚫")
except Exception as e:
    prediction_table.error(f"🚫 Error connecting to Flask backend: {e}")
