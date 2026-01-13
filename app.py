import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from datetime import datetime
import os

# --- 1. إعدادات الصفحة ---
st.set_page_config(
    page_title="Qarar | قرار",
    page_icon="💎",
    layout="wide"
)

# --- 2. التصميم CSS (النسخة الاحترافية) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
html, body, [class*="css"] { font-family: 'Cairo', sans-serif; }

/* تنسيق الهيرو سكشن */
.hero-box {
    background: linear-gradient(135deg, #f6f8f9 0%, #e5ebee 100%);
    padding: 40px; border-radius: 20px;
    margin-bottom: 30px; text-align: right; direction: rtl;
    border-right: 6px solid #2E86C1;
}

/* تنسيق كروت الخدمات */
.service-box {
    background-color: white; padding: 20px;
    border-radius: 15px; text-align: center;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    border-bottom: 4px solid #2E86C1;
    height: 180px; margin-bottom: 10px;
}

/* الفوتر */
.footer-text {
    text-align: center; color: #888; font-size: 12px;
    margin-top: 50px; border-top: 1px solid #eee; padding-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# --- 3. دالة الحفظ (Google Sheets) ---
def save_data(n, e):
    try:
        if "gcp_service_account" in st.secrets:
            # الاتصال بجوجل
            creds = st.secrets["gcp_service_account"]
            gc = gspread.service_account_from_dict(creds)
            sh = gc.open("QararLeads")
            # تسجيل البيانات
            wks = sh.sheet1
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            wks.append_row([n, e, now])
            return True
        return False
    except:
        return False

# --- 4. القائمة الجانبية ---
with st.sidebar:
    try:
        st.image("https://cdn-icons-png.flaticon.com/512/3094/3094851.png", width=80)
    except:
        st.write("💎")
        
    st.title("منصة قرار")
    st.markdown("---")
    
    # قائمة التنقل
    nav = st.radio(
        "القائمة:", 
        ["🏠 الرئيسية", "⚡ ديمو", "📂 التحليل"]
    )
    
    st.markdown("---")
    st.markdown("**تواصل معنا:**")
    st.markdown("[LinkedIn Profile 🔗](https://www.linkedin.com/in/reham-morsy-45b61a192/)")
    st.caption("© 2026 Dr. Reham Morsy")

# تهيئة الجلسة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'user' not in st.session_state: st.session_state.user = "Guest"

# --- 5. المحتوى الرئيسي ---

# ==========================
# 🏠 الصفحة الرئيسية (كاملة)
# ==========================
if nav == "🏠 الرئيسية":
    
    # 1. الهيرو سكشن (الافتتاحية الفخمة)
    with st.container():
        st.markdown('<div class="hero-box">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # كود الصورة الذكي (يحاول الحقيقية ثم البديلة)
            real_img = "profile.png"
            fake_img = "https://cdn-icons-png.flaticon.com/512/949/949635.png"
            
            if os.path.exists(real_img):
                try:
                    st.image(real_img, width=180)
                except:
                    st.image(fake_img, width=180)
            else:
                st.image(fake_img, width=180)
                
        with col2:
            st.markdown("## د. ريهام مرسي")
            st.markdown("#### شريكك الاستراتيجي في تحليل الأعمال")
            st.write("""
            أساعد الشركات ورواد الأعمال على تحويل البيانات الجامدة 
            إلى قرارات استراتيجية مربحة.
            خبرة تجمع بين الدقة الأكاديمية والواقع العملي.
            """)
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("") # مسافة

    # 2. قسم
