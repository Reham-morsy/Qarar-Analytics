import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from datetime import datetime
import os

# ---------------------------------------------------------
# 1. الإعدادات
# ---------------------------------------------------------
st.set_page_config(page_title="Qarar | قرار", page_icon="💎", layout="wide")

# تنسيق CSS (احترافي جداً)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
html, body, [class*="css"] { font-family: 'Cairo', sans-serif; }
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* تصميم بطاقة الخدمات */
.service-card {
    background-color: white; 
    padding: 20px; 
    border-radius: 15px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    border-top: 5px solid #2E86C1; 
    text-align: center; 
    margin-bottom: 20px; 
    height: 180px;
    transition: transform 0.3s;
}
.service-card:hover { transform: translateY(-5px); }

/* تصميم الافتتاحية (Hero Section) */
.hero-container {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    padding: 40px;
    border-radius: 20px;
    margin-bottom: 30px;
    text-align: right;
    direction: rtl;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}

.footer {
    position: fixed; left: 0; bottom: 0; width: 100%;
    background-color: #f8f9fa; color: #555; text-align: center; padding: 10px; z-index: 100;
    font-size: 12px; border-top: 1px solid #ddd;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. دالة جوجل شيت
# ---------------------------------------------------------
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

# ---------------------------------------------------------
# 3. القائمة الجانبية
# ---------------------------------------------------------
with st.sidebar:
    try:
        st.image("https://cdn-icons-png.flaticon.com/512/3094/3094851.png", width=80)
    except:
        st.write("💎")
        
    st.title("منصة قرار")
    st.markdown("---")
    mode = st.radio("القائمة:", ["🏠 الصفحة الرئيسية", "⚡ تجربة النظام (Demo)", "📂 رفع وتحليل ملفي"])
    st.markdown("---")
    st.header("📞 تواصل معنا")
    st.markdown("[LinkedIn 🔗](https://www.linkedin.com/in/reham-morsy-45b61a192/)")
    st.caption("© 2026 Dr. Reham Morsy")

if 'email_submitted' not in st.session_state: st.session_state.email_submitted = False
if 'user_name' not in st.session_state: st.session_state.user_name = "Guest"

# ---------------------------------------------------------
# 4. المحتوى
# ---------------------------------------------------------

# === الرئيسية ===
if mode == "🏠 الصفحة الرئيسية":
    
    # --- التصميم الجديد للافتتاحية (Hero Section) ---
    with st.container():
        st.markdown('<div class="hero-container">', unsafe_allow_html=True)
        
        col_hero1, col_hero2 = st.columns([1, 3])
        
        with col_hero1:
            # كود الصورة الآمن (مع بديل نسائي محترم)
            image_shown = False
            if os.path.exists("profile.png"):
                try:
                    st.image("profile.png", width=200)
                    image_shown = True
                except:
                    pass
            
            if not image_shown:
                # صورة بديلة (سيدة أعمال) بدل الرجل
                st.image("https://cdn-icons-png.flaticon.com/512/949/949635.png", width=180)
        
        with col_hero2:
            st.markdown("""
            <h1 style='color: #2E86C1; margin-bottom: 0;'>د. ريهام مرسي</h1>
            <h4 style='color: #555; margin-top: 5px;'>شريكك الاستراتيجي في تحليل الأعمال والمالية</h4>
            <p style='font-size: 18px; line-height: 1.6;'>
            أساعد الشركات ورواد الأعمال على تحويل جداول البيانات المعقدة إلى 
            <b>قرارات استراتيجية مربحة</b>. <br>
            خبرة تجمع بين الدقة الأكاديمية والعمل الميداني لتحقيق أعلى عائد على الاستثمار (ROI).
            </p>
            """, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

    # --- الخدمات ---
    st.markdown("<h3 style='text-align: center; color: #333;'>🚀 خدماتنا المتميزة</h3><br>", unsafe_allow_html=True)
    
    s1, s2, s3 = st.columns(3)
    s1.markdown("""
    <div class="service-card">
        <img src="https://cdn-icons-png.flaticon.com/512/2910/2910791.png" width="50">
        <h3>تحليل مالي متقدم</h3>
        <p style='font-size:14px; color:#666;'>لوحات بيانات تفاعلية تكشف خبايا الأرقام.</p>
    </div>
    """, unsafe_allow_html=True)
    
    s2.markdown("""
    <div class="service-card">
        <img src="https://cdn-icons-png.flaticon.com/512/1570/1570992.png" width="50">
        <h3>دراسات جدوى</h3>
        <p style='font-size:14px; color:#666;'>تقييم دقيق للمخاطر والعوائد قبل البدء.</p>
    </div>
    """, unsafe_allow_html=True)
    
    s3.markdown("""
    <div class="service-card">
        <img src="https://cdn-icons-png.flaticon.com/512/1624/1624568.png" width="50">
        <h3>استشارات النمو</h3>
        <p style='font-size:14px; color:#666;'>خطط عملية لخفض التكاليف وزيادة الربحية.</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("---")
    
    # --- الفوتر ---
    st.markdown('<div class="footer"><p>© 2026 جميع الحقوق محفوظة لمنصة قرار | تطوير: د. ريهام مرسي</p></div>', unsafe_allow_html=True)

# === الديمو ===
elif mode == "⚡ تجربة النظام (Demo)":
    st.title("⚡ تجربة حية")
    data = {'المدينة': ['الرياض', 'جدة', 'الدمام']*5, 'المبيعات': [5000, 3000, 4500]*5}
    st.plotly_chart(px.bar(pd.DataFrame(data), x='المدينة', y='المبيعات'), use_container_width=True)

# === التحليل ===
elif mode == "📂 رفع وتحليل ملفي":
    st.title("📂 تحليل البيانات الخاص")
    uploaded_file = st.file_uploader("ارفع
