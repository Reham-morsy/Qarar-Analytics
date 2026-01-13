import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from datetime import datetime
import os

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="Qarar | قرار",
    page_icon="💎",
    layout="wide"
)

# 2. التنسيق CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
html, body, [class*="css"] { font-family: 'Cairo', sans-serif; }
.service-card {
    background-color: white; padding: 20px; 
    border-radius: 15px; border-top: 5px solid #2E86C1;
    text-align: center; margin-bottom: 20px; height: 180px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.hero-container {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    padding: 30px; border-radius: 20px; margin-bottom: 30px;
    text-align: right; direction: rtl;
}
</style>
""", unsafe_allow_html=True)

# 3. دالة الحفظ
def save_to_google_sheets(name, email):
    try:
        if "gcp_service_account" in st.secrets:
            gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
            sh = gc.open("QararLeads")
            worksheet = sh.sheet1
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            worksheet.append_row([name, email, current_time])
            return True
        return False
    except:
        return False

# 4. القائمة الجانبية
with st.sidebar:
    try:
        st.image("https://cdn-icons-png.flaticon.com/512/3094/3094851.png", width=80)
    except:
        st.write("💎")
    st.title("منصة قرار")
    mode = st.radio(
        "القائمة:",
        ["🏠 الصفحة الرئيسية", "⚡ تجربة النظام (Demo)", "📂 رفع وتحليل ملفي"]
    )
    st.markdown("---")
    st.caption("© 2026 Dr. Reham Morsy")

if 'email_submitted' not in st.session_state: st.session_state.email_submitted = False
if 'user_name' not in st.session_state: st.session_state.user_name = "Guest"

# 5. المحتوى

# --- الرئيسية ---
if mode == "🏠 الصفحة الرئيسية":
    with st.container():
        st.markdown('<div class="hero-container">', unsafe_allow_html=True)
        c1, c2 = st.columns([1, 3])
        with c1:
            # محاولة عرض الصورة بشكل آمن
            img_path = "profile.png"
            if os.path.exists(img_path):
                try:
                    st.image(img_path, width=200)
                except:
                    st.image("https://cdn-icons-png.flaticon.com/512/949/949635.png", width=180)
            else:
                st.image("https://cdn-icons-png.flaticon.com/512/949/949635.png", width=180)
        
        with c2:
            st.markdown("## د. ريهام مرسي")
            st.markdown("#### شريكك الاستراتيجي في تحليل الأعمال والمالية")
            st.write("تحويل جداول البيانات المعقدة إلى قرارات استراتيجية مربحة.")
        st.markdown('</div>', unsafe_allow_html=True)

    # الخدمات
    st.markdown("### 🚀 خدماتنا المتميزة")
    s1, s2, s3 = st.columns(3)
    s1.info("📊 **تحليل مالي متقدم**\n\nلوحات بيانات تفاعلية.")
    s2.success("💡 **دراسات جدوى**\n\nتقييم دقيق للمخاطر والعوائد.")
    s3.warning("📉 **استشارات النمو**\n\nخطط لخفض التكاليف.")

# --- الديمو ---
elif mode == "⚡ تجربة النظام (Demo)":
    st.header("⚡ تجربة حية")
    data = {'المدينة': ['الرياض', 'جدة']*5, 'المبيعات': [5000, 3000]*5}
    st.plotly_chart(px.bar(pd.DataFrame(data), x='المدينة', y='المبيعات'))

# --- التحليل (تم تقسيم السطور هنا لمنع الخطأ) ---
elif mode == "📂 رفع وتحليل ملفي":
    st.header("📂 تحليل البيانات الخاص")
    
    # هنا تم تقسيم السطر الطويل لسطرين قصيرين
    uploaded_file = st.file_uploader(
        "ارفع ملف Excel/CSV", 
        type=['xlsx', 'csv']
    )
    
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            st.success("✅ تم قراءة الملف")

            # بوابة الدخول
            if not st.session_state.email_submitted:
                st.warning("🔒 يرجى التسجيل للمتابعة")
                with st.form("gate"):
                    n = st.text_input("الاسم")
                    e = st.text_input("الايميل")
                    if st.form_submit_button("عرض التقرير"):
                        if "@" in e:
                            st.session_state.email_submitted = True
                            st.session_state.user_name = n
                            save_to_google_sheets(n, e)
                            st.rerun()
            else:
                # لوحة البيانات
                st.info(f"أهلاً {st.session_state.user_name}")
                nums = df.select_dtypes(include=['number']).columns
                
                if len(nums) > 0:
                    st.subheader("💰 مؤشرات الربحية")
                    col_sel1, col_sel2 = st.columns(2)
                    
                    # تقسيم السطور الطويلة
                    v1 = col_sel1.selectbox(
                        "المبيعات:", 
                        nums, 
                        index=0
                    )
                    
                    idx2 = 1 if len(nums) > 1 else 0
                    v2 = col_sel2.selectbox(
                        "التكلفة:", 
                        nums, 
                        index=idx2
                    )
                    
                    # الحسابات
                    rev = df[v1].sum()
                    cost = df[v2].sum()
                    prof = rev - cost
                    
                    k1, k2, k3 = st.columns(3)
                    k1.metric("المبيعات", f"{rev:,.0f}")
                    k2.metric("التكاليف", f"{cost:,.0f}")
                    k3.metric("الربح", f"{prof:,.0f}")
                    
                    st.plotly_chart(px.bar(df, x=df.columns[0], y=v1))
                else:
                    st.dataframe(df)

        except Exception as e:
            st.error("حدث خطأ في الملف")
