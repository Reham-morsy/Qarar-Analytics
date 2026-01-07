import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from datetime import datetime

# ---------------------------------------------------------
# 1. إعدادات الصفحة والتصميم (UI/UX)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Qarar | قرار",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تخصيص المظهر (CSS)
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    /* تحسين شكل الحقول */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 1px solid #ddd;
    }
    /* تحسين الأزرار */
    .stButton > button {
        border-radius: 10px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. نظام الربط وقاعدة البيانات (Backend)
# ---------------------------------------------------------
def save_to_google_sheets(name, email):
    try:
        # الاتصال بجوجل باستخدام المفاتيح السرية
        gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
        sh = gc.open("Qarar Leads") # اسم الملف
        worksheet = sh.sheet1
        
        # تسجيل البيانات والوقت
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        worksheet.append_row([name, email, current_time])
        return True
    except Exception as e:
        # في حالة الخطأ، لا نوقف التطبيق، فقط نطبع الخطأ في الخلفية
        print(f"Database Error: {e}")
        return False

# ---------------------------------------------------------
# 3. القائمة الجانبية (Sidebar & Navigation)
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3094/3094851.png", width=80)
    st.markdown("### 📊 منصة قرار")
    st.caption("حوّل بياناتك إلى قرارات ذكية")
    
    st.markdown("---")
    
    # قائمة التنقل
    mode = st.radio("القائمة:", 
                    ["🏠 الصفحة الرئيسية", "⚡ تجربة النظام (Demo)", "📂 رفع وتحليل ملفي"], 
                    index=0)
    
    st.markdown("---")
    
    # قسم التواصل الاحترافي
    st.header("📞 تواصل معنا")
    st.info("لطلب استشارة خاصة أو بناء نظام مخصص:")
    
    # أزرار تواصل HTML
    st.markdown("""
    <div style='display: flex; flex-direction: column; gap: 10px;'>
        <a href='https://www.linkedin.com/in/reham-morsy-45b61a192/' target='_blank' style='text-decoration: none;'>
            <button style='width: 100%; background-color: #0077B5; color: white; border: none; padding: 10px; border-radius: 5px; cursor: pointer; font-weight: bold;'>
                LinkedIn 🔗
            </button>
        </a>
        <a href='mailto:rehammorsy2012@gmail.com' style='text-decoration: none;'>
            <button style='width: 100%; background-color: #333; color: white; border: none; padding: 10px; border-radius: 5px; cursor: pointer; font-weight: bold;'>
                 Email Me 📧
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("© 2024 Dr. Reham Morsy")

# ---------------------------------------------------------
# 4. محتوى الصفحات (Page Content)
# ---------------------------------------------------------

# تهيئة متغيرات الجلسة
if 'email_submitted' not in st.session_state:
    st.session_state.email_submitted = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = "Guest"

# --- الصفحة 1: الرئيسية (Landing Page) ---
if
