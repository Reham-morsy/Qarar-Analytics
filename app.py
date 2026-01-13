import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from datetime import datetime
import os

# ---------------------------------------------------------
# 1. إعدادات الصفحة والتصميم
# ---------------------------------------------------------
st.set_page_config(
    page_title="Qarar | قرار",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS للتجميل والخطوط
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
    }
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
        background-color: #2E86C1;
        color: white;
    }
    .service-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #2E86C1;
        text-align: center;
        margin-bottom: 10px;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f1f1f1;
        color: #555;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        z-index: 100;
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
    st.caption("© 2026 Dr. Reham Morsy")

# ---------------------------------------------------------
# 4. المحتوى الرئيسي
# ---------------------------------------------------------

if 'email_submitted' not in st.session_state:
    st.session_state.email_submitted = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = "Guest"

# --- 🏠 الصفحة الرئيسية ---
if mode == "🏠 الصفحة الرئيسية":
    st.markdown("<h1 style='text-align: center; color: #2E86C1;'>منصة قرار: عندما تتحدث الأرقام.. نصنع نحن القرار 🎯</h1>", unsafe_allow_html=True)
    st.write("---")

    col_profile, col_bio = st.columns([1, 2.5])
    
    with col_profile:
        if os.path.exists("profile.png"):
            st.image("profile.png", width=200)
        elif os.path.exists("photo.jpg"):
             st.image("photo.jpg", width=200)
        else:
            st.image("https://cdn-icons-png.flaticon.com/512/4140/4140048.png", width=180)
        st.caption("د. ريهام مرسي")
    
    with col_bio:
        st.markdown("""
        ### مرحباً، أنا د. ريهام مرسي 👋
        **شريكك الاستراتيجي في تحليل الأعمال والمالية**
        
        أؤمن أن خلف كل رقم في شركتك قصة، وخلف كل جدول بيانات فرصة ضائعة أو ربح منتظر. 
        دوري ليس مجرد حساب الأرقام، بل **ترجمتها إلى لغة يفهمها صناع القرار**.
        """)
        st.markdown("[تواصل معي على LinkedIn 🔗](https://www.linkedin.com/in/reham-morsy-45b61a192/)")

    st.write("---")

    # 1. قسم الخدمات (جديد)
    st.subheader("🛠️ ماذا نقدم لك؟")
    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown("""
        <div class="service-card">
        <h3>📊 تحليل مالي</h3>
        <p>تحويل البيانات إلى داشبورد تفاعلية تكشف مواطن الربح والخسارة.</p>
        </div>
        """, unsafe_allow_html=True)
    with s2:
        st.markdown("""
        <div class="service-card">
        <h3>💡 دراسات جدوى</h3>
        <p>تقييم المشاريع الجديدة وحساب العائد المتوقع (ROI) بدقة.</p>
        </div>
        """, unsafe_allow_html=True)
    with s3:
        st.markdown("""
        <div class="service-card">
        <h3>📉 خفض التكاليف</h3>
        <p>استراتيجيات ذكية لتقليل الهدر المالي ورفع كفاءة التشغيل.</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")

    # قسم الرحلة والخبرة
    st.subheader("🎓 رحلة العلم والخبرة")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.success("🏗️ **2013: الأساس**")
        st.write("بكالوريوس إدارة أعمال (جيد جداً).")
    with c2:
        st.info("📈 **2017: التخصص**")
        st.write("ماجستير في التمويل والاستثمار.")
    with c3:
        st.warning("🏛️ **الأكاديمية**")
        st.write("محاضر جامعي وباحث مالي.")
    with c4:
        st.error("💼 **2020: الميدان**")
        st.write("استشارات مالية وإدارية.")

    st.write("---")
    
    # 2. قسم الأسئلة الشائعة (جديد)
    st.subheader("❓ أسئلة شائعة")
    with st.expander("هل بياناتي آمنة على المنصة؟"):
        st.write("نعم، المنصة تقوم بمعالجة البيانات لحظياً ولا نقوم بتخزين ملفاتك على سيرفراتنا. الأرقام تُعالج وتُحذف فور إغلاق الجلسة.")
    with st.expander("كيف يمكنني طلب استشارة خاصة؟"):
        st.write("يمكنك التواصل مباشرة عبر زر LinkedIn أو حجز استشارة مدفوعة بعد تحليل ملفك.")
    with st.expander("ما هي أنواع الملفات المدعومة؟"):
        st.write("ندعم ملفات Excel (.xlsx) و CSV حالياً. تأكد من وجود صف رؤوس الأعمدة (Header) في ملفك.")

    st.write("---")
    
    col_cta1, col_cta2 = st.columns([3, 1])
    with col_cta1:
        st.info("📢 **هل بياناتك جاهزة لتروي قصتها؟** انتقلي لصفحة التحليل الآن.")

    # 3. الفوتر (جديد)
    st.markdown("""
    <div class="footer">
    <p>© 2026 جميع الحقوق محفوظة لمنصة قرار | تطوير د. ريهام مرسي</p>
    </div>
    """, unsafe_allow_html=True)

# --- ⚡ الديمو ---
elif mode == "⚡ تجربة النظام (Demo)":
    st.title("⚡ تجربة حية (مثال)")
    st.write("هذا مثال لما ستحصل عليه عند رفع ملفك:")
    data = {'المدينة': ['الرياض', 'جدة', 'الدمام', 'مكة']*5, 'المبيعات': [5000, 3000, 4500, 2000]*5}
    st.plotly_chart(px.bar(pd.DataFrame(data), x='المدينة', y='المبيعات', color='المدينة'), use_container_width=True)

# --- 📂 رفع وتحليل ملفي ---
elif mode == "📂 رفع وتحليل ملفي":
    st.title("📂 تحليل البيانات الخاص")
    uploaded_file = st.file_uploader("ارفع ملف Excel/CSV", type=['xlsx', 'csv'])
    
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success("✅ تم قراءة الملف بنجاح!")
            
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
                                saved, msg = save_to_google_sheets(name, email)
                                st.balloons()
                                st.rerun()
                            else:
                                st.error("الرجاء إدخال إيميل صحيح")
            else:
                st.info(f"مرحباً {st.session_state.user_name}، إليك تحليل بياناتك:")
                
                num_cols = df.select_dtypes(include=['number']).columns
                cat_cols = df.select_dtypes(include=['object']).columns
                
                if len(num_cols) > 0:
                    st.markdown("### 💰 مؤشرات الربحية وال
