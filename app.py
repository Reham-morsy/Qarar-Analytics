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

# تنسيق CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
html, body, [class*="css"] { font-family: 'Cairo', sans-serif; }
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.service-card {
    background-color: #f8f9fa; padding: 20px; border-radius: 10px;
    border-left: 5px solid #2E86C1; text-align: center; margin-bottom: 10px; height: 160px;
}
.footer {
    position: fixed; left: 0; bottom: 0; width: 100%;
    background-color: #f1f1f1; color: #555; text-align: center; padding: 10px; z-index: 100;
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
    # محاولة عرض الشعار
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
    st.markdown("<h1 style='text-align: center; color: #2E86C1;'>منصة قرار 🎯</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>عندما تتحدث الأرقام.. نصنع نحن القرار</h3>", unsafe_allow_html=True)
    st.write("---")
    
    c1, c2 = st.columns([1, 2.5])
    with c1:
        # --- كود الصورة الآمن الجديد ---
        image_shown = False
        if os.path.exists("profile.png"):
            try:
                st.image("profile.png", width=200)
                image_shown = True
            except:
                pass # إذا فشلت الصورة الحقيقية، تجاوزها
        
        if not image_shown:
            st.image("https://cdn-icons-png.flaticon.com/512/4140/4140048.png", width=180)
        # -------------------------------
        st.caption("د. ريهام مرسي")

    with c2:
        st.markdown("### مرحباً، أنا د. ريهام مرسي 👋\n**شريكك الاستراتيجي في تحليل الأعمال والمالية**\n\nأؤمن أن خلف كل رقم في شركتك قصة، وخلف كل جدول بيانات فرصة ضائعة أو ربح منتظر. دوري ترجمتها للغة القرارات.")

    st.write("---")
    st.subheader("🛠️ خدماتنا")
    s1, s2, s3 = st.columns(3)
    s1.markdown('<div class="service-card"><h3>📊 تحليل مالي</h3><p>داشبورد تفاعلية تكشف مواطن الربح والخسارة.</p></div>', unsafe_allow_html=True)
    s2.markdown('<div class="service-card"><h3>💡 دراسات جدوى</h3><p>تقييم المشاريع وحساب العائد المتوقع ROI بدقة.</p></div>', unsafe_allow_html=True)
    s3.markdown('<div class="service-card"><h3>📉 خفض التكاليف</h3><p>استراتيجيات ذكية لتقليل الهدر ورفع الكفاءة.</p></div>', unsafe_allow_html=True)

    st.write("---")
    st.subheader("🎓 الخبرات")
    e1, e2, e3, e4 = st.columns(4)
    e1.success("🏗️ **2013**"); e1.write("بكالوريوس إدارة.")
    e2.info("📈 **2017**"); e2.write("ماجستير تمويل.")
    e3.warning("🏛️ **الأكاديمية**"); e3.write("محاضر جامعي.")
    e4.error("💼 **2020**"); e4.write("استشارات مالية.")
    
    st.markdown('<div class="footer"><p>© 2026 جميع الحقوق محفوظة لمنصة قرار</p></div>', unsafe_allow_html=True)

# === الديمو ===
elif mode == "⚡ تجربة النظام (Demo)":
    st.title("⚡ تجربة حية")
    data = {'المدينة': ['الرياض', 'جدة', 'الدمام']*5, 'المبيعات': [5000, 3000, 4500]*5}
    st.plotly_chart(px.bar(pd.DataFrame(data), x='المدينة', y='المبيعات'), use_container_width=True)

# === التحليل ===
elif mode == "📂 رفع وتحليل ملفي":
    st.title("📂 تحليل البيانات الخاص")
    uploaded_file = st.file_uploader("ارفع ملف Excel/CSV", type=['xlsx', 'csv'])
    
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'): df = pd.read_csv(uploaded_file)
            else: df = pd.read_excel(uploaded_file)
            st.success("✅ تم قراءة الملف")

            if not st.session_state.email_submitted:
                st.markdown("---")
                c_gate1, c_gate2 = st.columns([2, 1])
                with c_gate1:
                    st.warning("🔒 يرجى التسجيل للمتابعة.")
                    with st.form("gate_form"):
                        name = st.text_input("الاسم:")
                        email = st.text_input("البريد الإلكتروني:")
                        if st.form_submit_button("🔓 فتح التقرير"):
                            if "@" in email:
                                st.session_state.email_submitted = True
                                st.session_state.user_name = name
                                save_to_google_sheets(name, email)
                                st.rerun()
                            else: st.error("إيميل غير صحيح")
            else:
                st.info(f"مرحباً {st.session_state.user_name}")
                num_cols = df.select_dtypes(include=['number']).columns
                
                if len(num_cols) > 0:
                    st.markdown("### 💰 مؤشرات الربحية")
                    sel1, sel2 = st.columns(2)
                    rev_col = sel1.selectbox("المبيعات:", num_cols, index=0)
                    cost_col = sel2.selectbox("التكلفة:", num_cols, index=(1 if len(num_cols)>1 else 0))
