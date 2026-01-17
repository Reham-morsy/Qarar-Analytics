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

# --- 2. CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
html, body, [class*="css"] { font-family: 'Cairo', sans-serif; }

h1, h2, h3 { color: #27AE60; }

div.stButton > button {
    background-color: #27AE60; color: white; border: none;
    border-radius: 8px; padding: 8px 20px; font-weight: bold;
    width: 100%; transition: 0.3s;
}
div.stButton > button:hover {
    background-color: #219150; border-color: #219150; color: white;
}

.service-card {
    background-color: #f9f9f9; padding: 20px;
    border-radius: 10px; text-align: center;
    border-top: 4px solid #27AE60;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    margin-bottom: 10px;
    height: 180px;
}

.footer {
    position: fixed; left: 0; bottom: 0; width: 100%;
    background-color: #f1f1f1; color: #555; 
    text-align: center; padding: 8px; z-index: 100;
    font-size: 12px; border-top: 1px solid #ddd;
}
</style>
""", unsafe_allow_html=True)

# --- 3. دالة الحفظ ---
def save_data(n, e):
    try:
        if "gcp_service_account" in st.secrets:
            creds = st.secrets["gcp_service_account"]
            gc = gspread.service_account_from_dict(creds)
            sh = gc.open("QararLeads")
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
        st.header("💎 Qarar")
    
    st.markdown("<h3 style='text-align: center; color: #27AE60;'>منصة قرار</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    # إدارة الصفحات
    if 'page' not in st.session_state: st.session_state.page = "🏠 الرئيسية"
    def set_page(p): st.session_state.page = p
    
    if 'auth' not in st.session_state: st.session_state.auth = False
    if 'user' not in st.session_state: st.session_state.user = "Guest"
    
    # الأزرار
    if st.button("🏠 الرئيسية", use_container_width=True): set_page("🏠 الرئيسية")
    if st.button("⚡ ديمو", use_container_width=True): set_page("⚡ ديمو")
    if st.button("📂 التحليل", use_container_width=True): set_page("📂 التحليل")
    
    st.markdown("---")
    if st.session_state.auth:
        st.caption(f"👤 {st.session_state.user}")
        if st.button("تسجيل خروج"):
            st.session_state.auth = False
            st.session_state.user = "Guest"
            st.rerun()
            
    st.markdown("[LinkedIn 🔗](https://www.linkedin.com/in/reham-morsy-45b61a192/)")
    st.caption("© 2026 Dr. Reham Morsy")

# --- 5. المحتوى ---

# === الرئيسية ===
if st.session_state.page == "🏠 الرئيسية":
    
    c1, c2 = st.columns([1, 2])
    
    # --- العمود الأيسر: التسجيل ---
    with c1:
        st.write("")
        st.write("")
        if not st.session_state.auth:
            with st.container(border=True):
                st.markdown("#### 🔐 سجل للبدء")
                st.caption("احصل على تجربة كاملة مجاناً")
                with st.form("login_form"):
                    name_in = st.text_input("الاسم", placeholder="الاسم الكريم")
                    email_in = st.text_input("الإيميل", placeholder="example@mail.com")
                    btn = st.form_submit_button("🚀 ابدأ الآن")
                    
                    if btn:
                        if "@" in email_in and len(name_in) > 2:
                            save_data(name_in, email_in)
                            st.session_state.auth = True
                            st.session_state.user = name_in
                            st.rerun()
                        else:
                            st.error("البيانات غير صحيحة")
        else:
            with st.container(border=True):
                st.success(f"أهلاً {st.session_state.user}")
                if st.button("📂 الانتقال للتحليل"):
                    set_page("📂 التحليل")
                    st.rerun()

    # --- العمود الأيمن: التعريف ---
    with c2:
        r1, r2 = st.columns([1, 3])
        with r1:
            if os.path.exists("profile.png"):
                st.image("profile.png", width=140)
            else:
                st.image("https://cdn-icons-png.flaticon.com/512/949/949635.png", width=140)
        with r2:
            st.markdown("## د. ريهام مرسي")
            st.markdown("**شريكك الاستراتيجي في تحليل الأعمال**")
            st.write("حول بياناتك المعقدة إلى قرارات رابحة.")

        st.markdown("---")
        st.markdown("#### 🚀 خدماتنا المتميزة")
        
        # كود الخدمات (تم فصله لتجنب الأخطاء)
        html_s1 = """
        <div class="service-card">
            <h3>📊</h3>
            <b>تحليل مالي</b><br>
            <small>داشبورد فوري</small>
        </div>
        """
        html_s2 = """
        <div class="service-card">
            <h3>💡</h3>
            <b>دراسات جدوى</b><br>
            <small>تقييم المخاطر</small>
        </div>
        """
        html_s3 = """
        <div class="service-card">
            <h3>📈</h3>
            <b>استشارات نمو</b><br>
            <small>رفع الكفاءة</small>
        </div>
        """
        
        sc1, sc2, sc3 = st.columns(3)
        with sc1: st.markdown(html_s1, unsafe_allow_html=True)
        with sc2: st.markdown(html_s2, unsafe_allow_html=True)
        with sc3: st.markdown(html_s3, unsafe_allow_html=True)

    st.write("---")
    
    # --- قسم الخبرات ---
    st.markdown("### 🎓 رحلة العلم والخبرة")
    e1, e2, e3, e4 = st.columns(4)
    
    with e1:
        st.success("🏗️ **2013**")
        st.caption("بكالوريوس إدارة أعمال")
    
    with e2:
        st.info("📈 **2017**")
        st.caption("ماجستير في التمويل")
        
    with e3:
        st.warning("🏛️ **الأكاديمية**")
        st.caption("محاضر جامعي وباحث")
        
    with e4:
        st.error("💼 **2020**")
        st.caption("استشارات مالية للشركات")

    st.markdown('<div class="footer">جميع الحقوق محفوظة لمنصة قرار 2026</div>', unsafe_allow_html=True)

# === ديمو ===
elif st.session_state.page == "⚡ ديمو":
    st.header("⚡ تجربة حية")
    data = {'الفرع': ['الرياض', 'جدة']*5, 'المبيعات': [45000, 32000]*5}
    fig = px.bar(
        pd.DataFrame(data), 
        x='الفرع', 
        y='المبيعات', 
        color_discrete_sequence=['#27AE60']
    )
    st.plotly_chart(fig)

# === التحليل ===
elif st.session_state.page == "📂 التحليل":
    if not st.session_state.auth:
        st.warning("🔒 يجب التسجيل أولاً")
        if st.button("🔙 عودة"):
            set_page("🏠 الرئيسية")
            st.rerun()
    else:
        st.header("📂 تحليل البيانات الخاص")
        up_file = st.file_uploader(
            "ارفع ملف Excel/CSV", 
            type=['xlsx', 'csv']
        )
        
        if up_file:
            try:
                if up_file.name.endswith('.csv'):
                    df = pd.read_csv(up_file)
                else:
                    df = pd.read_excel(up_file)
                st.success("✅ تم القراءة")
                
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
                    
                    fig = px.bar(
                        df, 
                        x=df.columns[0], 
                        y=v1, 
                        color_discrete_sequence=['#27AE60']
                    )
                    st.plotly_chart(fig)
                else:
                    st.dataframe(df)
            except:
                st.error("خطأ في الملف")
