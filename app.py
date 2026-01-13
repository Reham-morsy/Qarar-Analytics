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

# تنسيق CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .service-card {
        background-color: #f8f9fa; padding: 20px; border-radius: 10px;
        border-left: 5px solid #2E86C1; text-align: center; margin-bottom: 10px;
    }
    .footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: #f1f1f1; color: #555; text-align: center; padding: 10px; z-index: 100;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. دالة جوجل شيت ---
def save_to_google_sheets(name, email):
    try:
        if "gcp_service_account" in st.secrets:
            gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
            sh = gc.open("QararLeads")
            worksheet = sh.sheet1
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            worksheet.append_row([name, email, current_time])
            return True, "تم الحفظ"
        return False, "No Secrets"
    except Exception as e:
        return False, str(e)

# --- 3. القائمة الجانبية ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3094/3094851.png", width=80)
    st.title("منصة قرار")
    st.markdown("---")
    mode = st.radio("القائمة:", ["🏠 الصفحة الرئيسية", "⚡ تجربة النظام (Demo)", "📂 رفع وتحليل ملفي"])
    st.markdown("---")
    st.header("📞 تواصل معنا")
    st.markdown("[LinkedIn 🔗](https://www.linkedin.com/in/reham-morsy-45b61a192/)")
    st.caption("© 2026 Dr. Reham Morsy")

# تجهيز المتغيرات
if 'email_submitted' not in st.session_state: st.session_state.email_submitted = False
if 'user_name' not in st.session_state: st.session_state.user_name = "Guest"

# --- 4. المحتوى الرئيسي ---

# === الصفحة الرئيسية ===
if mode == "🏠 الصفحة الرئيسية":
    st.markdown("<h1 style='text-align: center; color: #2E86C1;'>منصة قرار 🎯</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>عندما تتحدث الأرقام.. نصنع نحن القرار</h3>", unsafe_allow_html=True)
    st.write("---")
    
    c1, c2 = st.columns([1, 2.5])
    with c1:
        if os.path.exists("profile.png"): 
            st.image("profile.png", width=200)
        else: 
            st.image("https://cdn-icons-png.flaticon.com/512/4140/4140048.png", width=180)
        st.caption("د. ريهام مرسي")
    
    with c2:
        st.markdown("""
        ### مرحباً، أنا د. ريهام مرسي 👋
        **شريكك الاستراتيجي في تحليل الأعمال والمالية**
        
        أؤمن أن خلف كل رقم في شركتك قصة. دوري ليس مجرد حساب الأرقام، 
        بل ترجمتها إلى لغة يفهمها صناع القرار.
        """)
    
    st.write("---")
    st.subheader("🛠️ خدماتنا")
    s1, s2, s3 = st.columns(3)
    s1.markdown('<div class="service-card"><h3>📊 تحليل مالي</h3><p>داشبورد تفاعلية.</p></div>', unsafe_allow_html=True)
    s2.markdown('<div class="service-card"><h3>💡 دراسات جدوى</h3><p>حساب ROI بدقة.</p></div>', unsafe_allow_html=True)
    s3.markdown('<div class="service-card"><h3>📉 خفض التكاليف</h3><p>رفع كفاءة التشغيل.</p></div>
