   importstreamlit as st
import pandas as pd
import plotly.express as px
import gspread
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(page_title="Qarar | قرار", page_icon="💎", layout="wide", initial_sidebar_state="expanded")

# CSS
st.markdown("""<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} .stDeployButton {display:none;} .stTextInput > div > div > input {border-radius: 10px;}</style>""", unsafe_allow_html=True)

# --- دالة الربط (معدلة لتكشف الأخطاء) ---
def save_to_google_sheets(name, email):
    try:
        # محاولة الاتصال
        gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
        sh = gc.open("Qarar Leads") # اسم الملف
        worksheet = sh.sheet1
        
        # محاولة الحفظ
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        worksheet.append_row([name, email, current_time])
        return True, "تم الحفظ بنجاح"
        
    except Exception as e:
        # هنا سنظهر الخطأ على الشاشة
        return False, str(e)

# --- القائمة الجانبية ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3094/3094851.png", width=80)
    st.title("منصة قرار")
    st.markdown("---")
    mode = st.radio("القائمة:", ["🏠 الرئيسية", "⚡ ديمو (Demo)", "📂 رفع وتحليل ملف"], index=0)
    st.markdown("---")
    st.caption("Debug Mode Active 🔧")

# --- الصفحات ---
if mode == "🏠 الرئيسية":
    st.title("حوّل فوضى الأرقام.. إلى قرارات 🚀")
    st.warning("👈 اختر (رفع وتحليل ملف) لتجربة الاتصال.")

elif mode == "⚡ ديمو (Demo)":
    st.title("⚡ تجربة حية")
    st.plotly_chart(px.bar(x=['A','B'], y=[10,20]), use_container_width=True)

elif mode == "📂 رفع وتحليل ملف":
    st.title("📂 تحليل البيانات (وضع الاختبار)")
    uploaded_file = st.file_uploader("ارفع ملف Excel/CSV", type=['xlsx', 'csv'])
    
    # محاكاة وجود ملف للتسهيل عليك (حتى لو لم ترفعي ملفاً)
    st.info("💡 جربي كتابة الإيميل الآن لنختبر الاتصال بجوجل شيت:")
    
    with st.form("test_form"):
        name = st.text_input("الاسم:")
        email = st.text_input("البريد الإلكتروني:")
        submit = st.form_submit_button("🔓 اختبار الحفظ")
        
        if submit:
            if "@" in email:
                st.write("جاري محاولة الاتصال بجوجل...")
                
                # استدعاء الدالة وطباعة النتيجة
                success, message = save_to_google_sheets(name, email)
                
                if success:
                    st.balloons()
                    st.success(f"✅ نجحنا! البيانات ظهرت في الشيت الآن.")
                else:
                    st.error(f"❌ حدث خطأ، صوري هذه الرسالة وأرسليها لي:")
                    st.error(message) # هذه هي الرسالة المهمة
            else:
                st.warning("اكتبي إيميلاً صحيحاً.")
