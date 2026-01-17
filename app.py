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

# --- 2. CSS (تصميم Landing Page) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
html, body, [class*="css"] { font-family: 'Cairo', sans-serif; }

/* تنسيق الأزرار */
div.stButton > button {
    background-color: #27AE60; color: white; border: none;
    border-radius: 10px; padding: 10px 20px; font-weight: bold;
    width: 100%; transition: 0.3s;
}
div.stButton > button:hover {
    background-color: #219150; border-color: #219150; color: white;
}

/* صندوق التسجيل (Login Box) */
.login-box {
    background-color: white;
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    border-top: 6px solid #27AE60;
    text-align: right;
    direction: rtl;
}

.service-box {
    background-color: white; padding: 20px;
    border-radius: 15px; text-align: center;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    border-top: 5px solid #27AE60;
    height: 220px; margin-bottom: 20px;
}
.hero-box {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    padding: 40px; border-radius: 20px;
    margin-bottom: 30px; text-align: right; direction: rtl;
    border-right: 6px solid #27AE60;
}
.footer {
    position: fixed; left: 0; bottom: 0; width: 100%;
    background-color: #f1f1f1; color: #555; 
    text-align: center; padding: 10px; z-index: 100;
    font-size: 13px; border-top: 1px solid #ddd;
}
</style>
""", unsafe_allow_html=True)

# --- 3. دالة الحفظ (تعمل مع إعداداتك الحالية) ---
def save_data(n, e):
    try:
        if "gcp_service_account" in st.secrets:
            creds = st.secrets["gcp_service_account"]
            gc = gspread.service_account_from_dict(creds)
            sh = gc.open("QararLeads") # تأكدي أن اسم الملف في جوجل شيت هو QararLeads
            wks = sh.sheet1
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            wks.append_row([n, e, now])
            return True
        return False
    except:
        return False

# --- 4. القائمة الجانبية ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_column_width=True)
    else:
        st.image("https://cdn-icons-png.flaticon.com/512/3094/3094851.png", width=80)
    
    st.markdown("""
        <h2 style='text-align: center; color: #27AE60; margin-top: -20px; padding-top: 0;'>
        منصة قرار
        </h2>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # إدارة التنقل
    if 'page' not in st.session_state: st.session_state.page = "🏠 الرئيسية"
    def set_page(p): st.session_state.page = p
    
    # حالة الدخول
    if 'auth' not in st.session_state: st.session_state.auth = False
    if 'user' not in st.session_state: st.session_state.user = "Guest"
    
    # القوائم
    if st.button("🏠 الرئيسية", use_container_width=True): set_page("🏠 الرئيسية")
    
    # إخفاء باقي القوائم لغير المسجلين (اختياري - هنا تركتها ظاهرة للتحفيز)
    if st.button("⚡ ديمو", use_container_width=True): set_page("⚡ ديمو")
    if st.button("📂 التحليل", use_container_width=True): set_page("📂 التحليل")
    
    st.markdown("---")
    if st.session_state.auth:
        st.success(f"👤 {st.session_state.user}")
        if st.button("تسجيل خروج"):
            st.session_state.auth = False
            st.session_state.user = "Guest"
            st.rerun()
            
    st.markdown("[LinkedIn 🔗](https://www.linkedin.com/in/reham-morsy-45b61a192/)")
    st.caption("© 2026 Dr. Reham Morsy")

# --- 5. المحتوى ---

# === الرئيسية (Landing Page) ===
if st.session_state.page == "🏠 الرئيسية":
    
    with st.container():
        st.markdown('<div class="hero-box">', unsafe_allow_html=True)
        c1, c2 = st.columns([1.2, 2])
        
        # --- الجزء الأيسر: نموذج التسجيل (أو الترحيب) ---
        with c1:
            if not st.session_state.auth:
                st.markdown('<div class="login-box">', unsafe_allow_html=True)
                st.markdown("### 🔓 سجل دخولك للبدء")
                st.write("احصل على وصول كامل لأدوات التحليل مجاناً.")
                
                with st.form("landing_form"):
                    name_in = st.text_input("الاسم الكريم:")
                    email_in = st.text_input("البريد الإلكتروني:")
                    submit_btn = st.form_submit_button("🚀 ابدأ الرحلة الآن")
                    
                    if submit_btn:
                        if "@" in email_in and len(name_in) > 2:
                            # حفظ البيانات
                            save_data(name_in, email_in)
                            # تفعيل الدخول
                            st.session_state.auth = True
                            st.session_state.user = name_in
                            st.success("تم التسجيل بنجاح! جاري التحويل...")
                            st.rerun()
                        else:
                            st.error("يرجى إدخال بيانات صحيحة")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                # إذا كان مسجلاً بالفعل
                st.markdown('<div class="login-box">', unsafe_allow_html=True)
                st.markdown(f"### مرحباً بك يا {st.session_state.user} 🌟")
                st.write("حسابك مفعل وجاهز للاستخدام.")
                if st.button("📂 الانتقال لأداة التحليل"):
                    set_page("📂 التحليل")
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        # --- الجزء الأيمن: التعريف ---
        with c2:
            st.markdown("## <span style='color:#27AE60'>د. ريهام مرسي</span>", unsafe_allow_html=True)
            st.markdown("#### شريكك الاستراتيجي في تحليل الأعمال")
            st.markdown("""
            <div style='font-size: 18px; line-height: 1.8;'>
            <b>هل لديك بيانات كثيرة ولكن قرارات قليلة؟</b><br>
            منصة قرار تساعدك على تحويل جداول البيانات الجامدة إلى رؤى استراتيجية واضحة.
            <br><br>
            ✅ لوحات بيانات تفاعلية.<br>
            ✅ كشف مواطن الهدر المالي.<br>
            ✅ دعم اتخاذ القرار بدقة أكاديمية.
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

    # الخدمات (تظهر للجميع)
    st.markdown("### 🚀 لماذا تختار منصة قرار؟")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="service-box">
            <img src="https://cdn-icons-png.flaticon.com/512/2910/2910791.png" width="50">
            <h3>تحليل مالي فوري</h3>
            <p>ارفع ملفك واحصل على الداشبورد في ثوانٍ.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="service-box">
            <img src="https://cdn-icons-png.flaticon.com/512/1570/1570992.png" width="50">
            <h3>قاعدة بيانات آمنة</h3>
            <p>بياناتك تُعالج بخصوصية تامة ولا يتم مشاركتها.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="service-box">
            <img src="https://cdn-icons-png.flaticon.com/512/1624/1624568.png" width="50">
            <h3>قرارات ذكية</h3>
            <p>نحول الأرقام المعقدة إلى لغة يفهمها المديرون.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="footer">جميع الحقوق محفوظة لمنصة قرار 2026</div>', unsafe_allow_html=True)

# === ديمو ===
elif st.session_state.page == "⚡ ديمو":
    st.header("⚡ تجربة حية (Demo)")
    st.write("هذا نموذج لما ستحصل عليه بعد رفع بياناتك.")
    data = {'الفرع': ['الرياض', 'جدة']*5, 'المبيعات': [45000, 32000]*5}
    fig = px.bar(
        pd.DataFrame(data), 
        x='الفرع', 
        y='المبيعات',
        color_discrete_sequence=['#27AE60']
    )
    st.plotly_chart(fig)
    
    if not st.session_state.auth:
        st.info("💡 لرفع بياناتك الخاصة، يرجى التسجيل في الصفحة الرئيسية.")

# === التحليل ===
elif st.session_state.page == "📂 التحليل":
    # حماية الصفحة: إذا لم يسجل، نعيده للرئيسية أو نطلب منه التسجيل
    if not st.session_state.auth:
        st.warning("🔒 هذه الصفحة متاحة للأعضاء المسجلين فقط.")
        st.write("يرجى تسجيل الدخول للوصول إلى أدوات التحليل.")
        if st.button("🔙 العودة للتسجيل"):
            set_page("🏠 الرئيسية")
            st.rerun()
    else:
        # المحتوى المحمي للمسجلين فقط
        st.header("📂 تحليل البيانات الخاص")
        st.write("أهلاً بك في منطقة التحليل المتقدم.")
        
        up_file = st.file_uploader(
            "ارفع ملف Excel/CSV",
            type=['xlsx', 'csv']
        )
        
        if up_file is not None:
            try:
                if up_file.name.endswith('.csv'):
                    df = pd.read_csv(up_file)
                else:
                    df = pd.read_excel(up_file)
                st.success("✅ تم قراءة الملف")
                
                nums = df.select_dtypes(include=['number']).columns
                
                if len(nums) > 0:
                    st.subheader("💰 حاسبة الربحية")
                    c1, c2 = st.columns(2)
                    v1 = c1.selectbox("المبيعات:", nums, index=0)
                    idx = 1 if len(nums) > 1 else 0
                    v2 = c2.selectbox("التكلفة:", nums, index=idx)
                    
                    rev = df[v1].sum()
                    cost = df[v2].sum()
                    prof = rev - cost
                    
                    k1, k2, k3 = st.columns(3)
                    k1.metric("المبيعات", f"{rev:,.0f}")
                    k2.metric("التكاليف", f"{cost:,.0f}")
                    k3.metric("الربح", f"{prof:,.0f}")
                    
                    fig_chart = px.bar(
                        df, 
                        x=df.columns[0], 
                        y=v1,
                        color_discrete_sequence=['#27AE60']
                    )
                    st.plotly_chart(fig_chart)
                else:
                    st.dataframe(df)
            except Exception as e:
                st.error("خطأ في الملف")
