import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from datetime import datetime
import os

# --- 1. الإعدادات ---
st.set_page_config(
    page_title="Qarar | قرار",
    page_icon="💎",
    layout="wide"
)

# --- 2. التصميم CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
html, body, [class*="css"] { font-family: 'Cairo', sans-serif; }

.service-box {
    background-color: white; padding: 20px;
    border-radius: 15px; text-align: center;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    border-top: 5px solid #2E86C1;
    height: 200px; margin-bottom: 20px;
}
.hero-box {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    padding: 30px; border-radius: 20px;
    margin-bottom: 30px; text-align: right; direction: rtl;
}
.footer {
    position: fixed; left: 0; bottom: 0; width: 100%;
    background-color: #f1f1f1; color: #555; 
    text-align: center; padding: 10px; z-index: 100;
    font-size: 13px; border-top: 1px solid #ddd;
}
</style>
""", unsafe_allow_html=True)

# --- 3. دالة الحفظ ---
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

# --- 4. القائمة الجانبية ---
with st.sidebar:
    # عرض اللوجو
    if os.path.exists("logo.png"):
        st.image("logo.png", use_column_width=True)
    else:
        st.image("https://cdn-icons-png.flaticon.com/512/3094/3094851.png", width=80)
    
    st.markdown("<h2 style='text-align: center; color: #2E86C1;'>منصة قرار</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    nav = st.radio("القائمة:", ["🏠 الرئيسية", "⚡ ديمو", "📂 التحليل"])
    st.markdown("---")
    st.markdown("[LinkedIn 🔗](https://www.linkedin.com/in/reham-morsy-45b61a192/)")
    st.caption("© 2026 Dr. Reham Morsy")

if 'auth' not in st.session_state: st.session_state.auth = False
if 'user' not in st.session_state: st.session_state.user = "Guest"

# --- 5. المحتوى ---

# ==========================
# 🏠 الصفحة الرئيسية
# ==========================
if nav == "🏠 الرئيسية":
    
    with st.container():
        st.markdown('<div class="hero-box">', unsafe_allow_html=True)
        c1, c2 = st.columns([1, 3])
        
        with c1:
            # محاولة عرض الصورة (آمنة جداً)
            img_shown = False
            if os.path.exists("profile.png"):
                try:
                    st.image("profile.png", width=180)
                    img_shown = True
                except:
                    pass
            
            if not img_shown:
                st.image("https://cdn-icons-png.flaticon.com/512/949/949635.png", width=180)

        with c2:
            st.markdown("## د. ريهام مرسي")
            st.markdown("#### شريكك الاستراتيجي في تحليل الأعمال")
            st.write("أساعد الشركات على تحويل البيانات إلى قرارات مربحة.")
        st.markdown('</div>', unsafe_allow_html=True)
