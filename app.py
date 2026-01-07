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
            sh = gc.open("Qarar Leads")
            worksheet = sh.sheet1
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            worksheet.append_row([name, email, current_time])
            return True
        else:
            return False
    except Exception as e:
        return False

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
    
    # أزرار تواصل HTML
    st.markdown("""
    <div style='display: flex; flex-direction: column; gap: 10px;'>
        <a href='https://www.linkedin.com/in/reham-morsy-45b61a192/' target='_blank'>
            <button style='width: 100%; background-color: #0077B5; color: white; border: none; padding: 10px; border-radius: 5px; cursor: pointer;'>
                LinkedIn 🔗
            </button>
        </a>
        <a href='mailto:rehammorsy2012@gmail.com'>
            <button style='width: 100%; background-color: #333; color: white; border: none; padding: 10px; border-radius: 5px; cursor: pointer;'>
                 Email Me 📧
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)
    st.caption("© 2024 Dr. Reham Morsy")

# ---------------------------------------------------------
# 4. المحتوى
# ---------------------------------------------------------

# تهيئة الجلسة
if 'email_submitted' not in st.session_state:
    st.session_state.email_submitted = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = "Guest"

# --- الصفحة الرئيسية ---
if mode == "🏠 الصفحة الرئيسية":
    c1, c2 = st.columns(2)
    with c1:
        st.title("حوّل بياناتك إلى قرارات 🚀")
        st.markdown("### منصة قرار لتحليل الأعمال")
        st.info("👈 ابدأ من القائمة الجانبية.")
    with c2:
        st.image("https://images.unsplash.com/photo-1460925895917-afdab827c52f", caption="Dashboard")

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
                df = pd.read_excel(uploaded_file)
            
            st.success("✅ تم قراءة الملف!")
            
            # البوابة
            if not st.session_state.email_submitted:
                st.markdown("---")
                col_gate1, col_gate2 = st.columns([2, 1])
                with col_gate1:
                    st.warning("🔒 **التقرير محمي:** يرجى التسجيل للمتابعة.")
                    with st.form("gate_form"):
                        name = st.text_input("الاسم:")
                        email = st.text_input("البريد الإلكتروني:")
                        if st.form_submit_button("🔓 فتح التقرير"):
                            if "@" in email:
                                st.session_state.email_submitted = True
                                st.session_state.user_name = name
                                save_to_google_sheets(name, email)
                                st.balloons()
                                st.rerun()
                            else:
                                st.error("إيميل غير صحيح")
            else:
                # العرض
                st.info(f"مرحباً {st.session_state.user_name}")
                num_cols = df.select_dtypes(include=['number']).columns
                cat_cols = df.select_dtypes(include=['object']).columns
                
                if len(num_cols) > 0:
                    st.metric("الإجمالي", f"{df[num_cols[0]].sum():,.0f}")
                    if len(cat_cols) > 0:
                        st.plotly_chart(px.bar(df, x=cat_cols[0], y=num_cols[0]), use_container_width=True)
                    else:
                        st.dataframe(df)
                else:
                    st.dataframe(df)

        except Exception as e:
            st.error("الملف غير مدعوم")
