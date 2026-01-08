import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from datetime import datetime

# ---------------------------------------------------------
# 1. إعدادات الصفحة
# ---------------------------------------------------------
st.set_page_config(
    page_title="Qarar | قرار",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS للتجميل
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 1px solid #ddd;
    }
    .stButton > button {
        border-radius: 10px;
        width: 100%;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. دالة الربط (Backend)
# ---------------------------------------------------------
def save_to_google_sheets(name, email):
    try:
        if "gcp_service_account" in st.secrets:
            gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
            # اسم الملف مطابق لما أنشأتِه في جوجل درايف
            sh = gc.open("QararLeads")
            worksheet = sh.sheet1
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            worksheet.append_row([name, email, current_time])
            return True, "تم الحفظ"
        else:
            return False, "المفاتيح غير موجودة"
    except Exception as e:
        return False, str(e)

# ---------------------------------------------------------
# 3. القائمة الجانبية
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3094/3094851.png", width=80)
    st.title("منصة قرار")
    st.markdown("---")
    
    mode = st.radio("القائمة:", 
                    ["🏠 الصفحة الرئيسية", "⚡ تجربة النظام (Demo)", "📂 رفع وتحليل ملفي"], 
                    index=0)
    
    st.markdown("---")
    st.header("📞 تواصل معنا")
    st.markdown("[LinkedIn 🔗](https://www.linkedin.com/in/reham-morsy-45b61a192/)")
    st.caption("© 2024 Dr. Reham Morsy")

# ---------------------------------------------------------
# 4. المحتوى
# ---------------------------------------------------------

if 'email_submitted' not in st.session_state:
    st.session_state.email_submitted = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = "Guest"

# --- الصفحة الرئيسية ---
if mode == "🏠 الصفحة الرئيسية":
    c1, c2 = st.columns(2)
    with c1:
        st.title("حوّل بياناتك إلى أرباح 🚀")
        st.markdown("### منصة قرار لتحليل الأعمال")
        st.info("👈 ابدأ من القائمة الجانبية.")
    with c2:
        st.image("https://images.unsplash.com/photo-1460925895917-afdab827c52f")

# --- الديمو ---
elif mode == "⚡ تجربة النظام (Demo)":
    st.title("⚡ تجربة حية")
    data = {'المدينة': ['الرياض', 'جدة']*10, 'المبيعات': [5000, 3000]*10}
    st.plotly_chart(px.bar(pd.DataFrame(data), x='المدينة', y='المبيعات'), use_container_width=True)

# --- رفع الملف (المنتج الأساسي) ---
elif mode == "📂 رفع وتحليل ملفي":
    st.title("📂 تحليل البيانات الخاص")
    uploaded_file = st.file_uploader("ارفع ملف Excel/CSV", type=['xlsx', 'csv'])
    
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd
