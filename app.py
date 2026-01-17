import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from datetime import datetime
import os

# --- 1. Settings ---
st.set_page_config(
    page_title="Qarar Analytics",
    page_icon="💎",
    layout="wide"
)

# --- 2. CSS (English LTR Styling) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }

/* Main Colors */
h1, h2, h3 { color: #27AE60; }

/* Buttons */
div.stButton > button {
    background-color: #27AE60; color: white; border: none;
    border-radius: 8px; padding: 8px 20px; font-weight: bold;
    width: 100%; transition: 0.3s;
}
div.stButton > button:hover {
    background-color: #219150; border-color: #219150; color: white;
}

/* Service Cards */
.service-card {
    background-color: #f9f9f9; padding: 20px;
    border-radius: 10px; text-align: center;
    border-top: 4px solid #27AE60;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    margin-bottom: 10px;
    height: 180px;
}

/* Footer */
.footer {
    position: fixed; left: 0; bottom: 0; width: 100%;
    background-color: #f1f1f1; color: #555; 
    text-align: center; padding: 8px; z-index: 100;
    font-size: 12px; border-top: 1px solid #ddd;
}
</style>
""", unsafe_allow_html=True)

# --- 3. Save Function (Backend) ---
def save_data(n, e):
    try:
        if "gcp_service_account" in st.secrets:
            creds = st.secrets["gcp_service_account"]
            gc = gspread.service_account_from_dict(creds)
            sh = gc.open("QararLeads")
            wks = sh.sheet1
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            wks.append_row([n, e, now])
            return True
        return False
    except:
        return False

# --- 4. Sidebar ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_column_width=True)
    else:
        st.header("💎 Qarar")
    
    st.markdown("<h3 style='text-align: center; color: #27AE60;'>Qarar Analytics</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Navigation
    if 'page' not in st.session_state: st.session_state.page = "🏠 Home"
    def set_page(p): st.session_state.page = p
    
    if 'auth' not in st.session_state: st.session_state.auth = False
    if 'user' not in st.session_state: st.session_state.user = "Guest"
    
    # Menu Buttons
    if st.button("🏠 Home", use_container_width=True): set_page("🏠 Home")
    if st.button("⚡ Demo", use_container_width=True): set_page("⚡ Demo")
    if st.button("📂 Analysis", use_container_width=True): set_page("📂 Analysis")
    
    st.markdown("---")
    if st.session_state.auth:
        st.caption(f"👤 {st.session_state.user}")
        if st.button("Logout"):
            st.session_state.auth = False
            st.session_state.user = "Guest"
            st.rerun()
            
    st.markdown("[LinkedIn 🔗](https://www.linkedin.com/in/reham-morsy-45b61a192/)")
    st.caption("© 2026 Dr. Reham Morsy")

# --- 5. Content ---

# === HOME PAGE ===
if st.session_state.page == "🏠 Home":
    
    c1, c2 = st.columns([1, 2])
    
    # --- Left Column: Login ---
    with c1:
        st.write("")
        st.write("")
        if not st.session_state.auth:
            with st.container(border=True):
                st.markdown("#### 🔐 Login to Start")
                st.caption("Get full access for free")
                with st.form("login_form"):
                    name_in = st.text_input("Name", placeholder="Your Full Name")
                    email_in = st.text_input("Email", placeholder="example@mail.com")
                    btn = st.form_submit_button("🚀 Get Started")
                    
                    if btn:
                        if "@" in email_in and len(name_in) > 2:
                            save_data(name_in, email_in)
                            st.session_state.auth = True
                            st.session_state.user = name_in
                            st.rerun()
                        else:
                            st.error("Invalid details")
        else:
            with st.container(border=True):
                st.success(f"Welcome back, {st.session_state.user} 🌟")
                if st.button("📂 Go to Analysis"):
                    set_page("📂 Analysis")
                    st.rerun()

    # --- Right Column: Intro ---
    with c2:
        r1, r2 = st.columns([1, 3])
        with r1:
            if os.path.exists("profile.png"):
                st.image("profile.png", width=140)
            else:
                st.image("https://cdn-icons-png.flaticon.com/512/949/949635.png", width=140)
        with r2:
            st.markdown("## Dr. Reham Morsi")
            st.markdown("**Your Strategic Business Partner**")
            st.write("Transforming complex data into profitable decisions.")

        st.markdown("---")
        st.markdown("#### 🚀 Our Services")
        
        # HTML Cards for Services (English)
        html_s1 = """
        <div class="service-card">
            <h3>📊</h3>
            <b>Financial Analysis</b><br>
            <small>Instant Interactive Dashboards</small>
        </div>
        """
        html_s2 = """
        <div class="service-card">
            <h3>💡</h3>
            <b>Feasibility Studies</b><br>
            <small>Accurate Risk Assessment</small>
        </div>
        """
        html_s3 = """
        <div class="service-card">
            <h3>📈</h3>
            <b>Growth Consulting</b><br>
            <small>Efficiency & Optimization</small>
        </div>
        """
        
        sc1, sc2, sc3 = st.columns(3)
        with sc1: st.markdown(html_s1, unsafe_allow_html=True)
        with sc2: st.markdown(html_s2, unsafe_allow_html=True)
        with sc3: st.markdown(html_s3, unsafe_allow_html=True)

    st.write("---")
    
    # --- Experience Section ---
    st.markdown("### 🎓 Education & Experience")
    e1, e2, e3, e4 = st.columns(4)
    
    with e1:
        st.success("🏗️ **2013**")
        st.caption("B.A. Business Admin")
    
    with e2:
        st.info("📈 **2017**")
        st.caption("M.Sc. Finance")
        
    with e3:
        st.warning("🏛️ **Academic**")
        st.caption("Lecturer & Researcher")
        
    with e4:
        st.error("💼 **2020**")
        st.caption("Corporate Consultant")

    st.markdown('<div class="footer">© 2026 Qarar Analytics. All Rights Reserved.</div>', unsafe_allow_html=True)

# === DEMO PAGE ===
elif st.session_state.page == "⚡ Demo":
    st.header("⚡ Live Demo")
    data = {'Branch': ['Riyadh', 'Jeddah']*5, 'Sales': [45000, 32000]*5}
    fig = px.bar(
        pd.DataFrame(data), 
        x='Branch', 
        y='Sales', 
        color_discrete_sequence=['#27AE60']
    )
    st.plotly_chart(fig)

# === ANALYSIS PAGE ===
elif st.session_state.page == "📂 Analysis":
    if not st.session_state.auth:
        st.warning("🔒 Please login first")
        if st.button("🔙 Go Back"):
            set_page("🏠 Home")
            st.rerun()
    else:
        st.header("📂 Private Data Analysis")
        up_file = st.file_uploader(
            "Upload Excel/CSV File", 
            type=['xlsx', 'csv']
        )
        
        if up_file:
            try:
                if up_file.name.endswith('.csv'):
                    df = pd.read_csv(up_file)
                else:
                    df = pd.read_excel(up_file)
                st.success("✅ File Loaded Successfully")
                
                nums = df.select_dtypes(include=['number']).columns
                if len(nums) > 0:
                    st.subheader("💰 Profitability Calculator")
                    c1, c2 = st.columns(2)
                    v1 = c1.selectbox("Select Revenue Column:", nums, index=0)
                    
                    idx = 1 if len(nums) > 1 else 0
                    v2 = c2.selectbox("Select Cost Column:", nums, index=idx)
                    
                    rev = df[v1].sum()
                    cost = df[v2].sum()
                    prof = rev - cost
                    
                    k1, k2, k3 = st.columns(3)
                    k1.metric("Total Revenue", f"{rev:,.0f}")
                    k2.metric("Total Cost", f"{cost:,.0f}")
                    k3.metric("Net Profit", f"{prof:,.0f}")
                    
                    fig = px.bar(
                        df, 
                        x=df.columns[0], 
                        y=v1, 
                        color_discrete_sequence=['#27AE60']
                    )
                    st.plotly_chart(fig)
                else:
                    st.dataframe(df)
            except:
                st.error("Error reading file. Please check format.")
