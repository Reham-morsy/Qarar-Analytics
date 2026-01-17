import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from datetime import datetime
import os

# --- 1. Config ---
st.set_page_config(
    page_title="Qarar Analytics",
    page_icon="💎",
    layout="wide"
)

# --- 2. Initialization (الحل الجذري للمشكلة) ---
# هذه السطور تضمن تعريف الذاكرة قبل أي شيء آخر
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'user' not in st.session_state:
    st.session_state.user = "Guest"
if 'language' not in st.session_state:
    st.session_state.language = 'ar'
if 'page' not in st.session_state:
    st.session_state.page = "home"

# --- 3. Language & Text ---
t = {
    'ar': {
        'font': "'Cairo', sans-serif",
        'dir': 'rtl',
        'align': 'right',
        'sidebar_title': 'منصة قرار',
        'nav_home': '🏠 الرئيسية',
        'nav_demo': '⚡ ديمو',
        'nav_analysis': '📂 التحليل',
        'logout': 'تسجيل خروج',
        'login_title': '🔐 سجل للبدء',
        'login_sub': 'احصل على وصول كامل مجاناً',
        'name_label': 'الاسم',
        'email_label': 'البريد الإلكتروني',
        'start_btn': '🚀 ابدأ الرحلة الآن',
        'welcome': 'مرحباً بك',
        'go_analysis': '📂 الذهاب للتحليل',
        'hero_name': 'د. ريهام مرسي',
        'hero_role': 'شريكك الاستراتيجي في تحليل الأعمال',
        'hero_desc': 'هل لديك بيانات كثيرة ولكن قرارات قليلة؟ منصة قرار تساعدك على تحويل الجداول الجامدة إلى رؤى استراتيجية واضحة.',
        'services_title': '🚀 خدماتنا المتميزة',
        's1_t': 'تحليل مالي', 's1_d': 'لوحات تفاعلية تكشف الربحية',
        's2_t': 'دراسات جدوى', 's2_d': 'تقييم المخاطر بدقة عالية',
        's3_t': 'استشارات نمو', 's3_d': 'خطط لرفع كفاءة التشغيل',
        'exp_title': '🎓 رحلة العلم والخبرة',
        'footer': 'جميع الحقوق محفوظة لمنصة قرار 2026',
        'error_auth': '🔒 يجب التسجيل أولاً',
        'back_btn': '🔙 عودة',
        'upload_txt': 'ارفع ملف Excel/CSV',
        'success_read': '✅ تم قراءة الملف بنجاح',
        'calc_title': '💰 حاسبة الربحية',
        'm_rev': 'المبيعات', 'm_cost': 'التكاليف', 'm_prof': 'صافي الربح',
        'linkedin_btn': 'تواصل معي على LinkedIn 🔗'
    },
    'en': {
        'font': "'Poppins', sans-serif",
        'dir': 'ltr',
        'align': 'left',
        'sidebar_title': 'Qarar Analytics',
        'nav_home': '🏠 Home',
        'nav_demo': '⚡ Demo',
        'nav_analysis': '📂 Analysis',
        'logout': 'Logout',
        'login_title': '🔐 Login to Start',
        'login_sub': 'Get full access for free',
        'name_label': 'Name',
        'email_label': 'Email Address',
        'start_btn': '🚀 Get Started',
        'welcome': 'Welcome',
        'go_analysis': '📂 Go to Analysis',
        'hero_name': 'Dr. Reham Morsi',
        'hero_role': 'Strategic Business Partner',
        'hero_desc': 'Do you have lots of data but few decisions? Qarar helps you turn static spreadsheets into clear strategic insights.',
        'services_title': '🚀 Our Services',
        's1_t': 'Financial Analysis', 's1_d': 'Interactive Profitability Dashboards',
        's2_t': 'Feasibility Studies', 's2_d': 'Accurate Risk Assessment',
        's3_t': 'Growth Consulting', 's3_d': 'Operational Efficiency Plans',
        'exp_title': '🎓 Education & Experience',
        'footer': '© 2026 Qarar Analytics. All Rights Reserved.',
        'error_auth': '🔒 Login Required',
        'back_btn': '🔙 Go Back',
        'upload_txt': 'Upload Excel/CSV File',
        'success_read': '✅ File Loaded Successfully',
        'calc_title': '💰 Profitability Calculator',
        'm_rev': 'Revenue', 'm_cost': 'Cost', 'm_prof': 'Net Profit',
        'linkedin_btn': 'Connect on LinkedIn 🔗'
    }
}

lang = st.session_state.language
txt = t[lang]

# --- 4. CSS ---
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

html, body, [class*="css"] {{ 
    font-family: {txt['font']}; 
    direction: {txt['dir']};
    text-align: {txt['align']};
}}

h1, h2, h3 {{ color: #27AE60; }}

div.stButton > button {{
    background-color: #27AE60; color: white; border: none;
    border-radius: 8px; padding: 10px 20px; font-weight: bold;
    width: 100%; transition: 0.3s;
}}
div.stButton > button:hover {{
    background-color: #219150; border-color: #219150; color: white;
}}

.service-card {{
    background-color: #ffffff; padding: 25px;
    border-radius: 12px; text-align: center;
    border-top: 5px solid #27AE60;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    margin-bottom: 15px;
    height: 200px;
    transition: transform 0.3s;
}}
.service-card:hover {{
    transform: translateY(-5px);
}}

.footer {{
    position: fixed; left: 0; bottom: 0; width: 100%;
    background-color: #f8f9fa; color: #6c757d; 
    text-align: center; padding: 10px; z-index: 100;
    font-size: 13px; border-top: 1px solid #e9ecef;
}}
</style>
""", unsafe_allow_html=True)

# --- 5. Functions ---
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

def draw_card(icon, title, desc):
    st.markdown(f"""
    <div class="service-card">
        <h2 style='margin:0; padding-bottom:10px;'>{icon}</h2>
        <h4 style='color:#27AE60; margin:0;'>{title}</h4>
        <p style='color:#666; font-size:14px; margin-top:10px;'>{desc}</p>
    </div>
    """, unsafe_allow_html=True)

# --- 6. Sidebar ---
with st.sidebar:
    # Logo Check
    logo_ok = False
    if os.path.exists("logo.png"):
        try:
            st.image("logo.png", use_column_width=True)
            logo_ok = True
        except: pass
    if not logo_ok:
        st.header("💎 Qarar")
    
    # Language
    c_l1, c_l2 = st.columns(2)
    with c_l1:
        if st.button("🇺🇸 EN", use_container_width=True):
            st.session_state.language = 'en'
            st.rerun()
    with c_l2:
        if st.button("🇪🇬 AR", use_container_width=True):
            st.session_state.language = 'ar'
            st.rerun()

    st.markdown("---")
    st.markdown(f"<h3 style='text-align: center; color: #27AE60;'>{txt['sidebar_title']}</h3>", unsafe_allow_html=True)
    
    # Navigation
    def set_page(p): st.session_state.page = p
    
    if st.button(txt['nav_home'], use_container_width=True): set_page("home")
    if st.button(txt['nav_demo'], use_container_width=True): set_page("demo")
    if st.button(txt['nav_analysis'], use_container_width=True): set_page("analysis")
    
    st.markdown("---")
    
    # LinkedIn
    st.link_button(
        txt['linkedin_btn'], 
        "https://www.linkedin.com/in/reham-morsy-45b61a192/",
        use_container_width=True
    )
    
    if st.session_state.auth:
        st.divider()
        st.caption(f"👤 {st.session_state.user}")
        if st.button(txt['logout'], use_container_width=True):
            st.session_state.auth = False
            st.session_state.user = "Guest"
            st.rerun()

# --- 7. Content ---

# === HOME ===
if st.session_state.page == "home":
    c1, c2 = st.columns([1, 2])
    
    # Left
    with c1:
        st.write("") 
        st.write("")
        if not st.session_state.auth:
            with st.container(border=True):
                st.markdown(f"### {txt['login_title']}")
                st.write(txt['login_sub'])
                with st.form("login_form"):
                    name_in = st.text_input(txt['name_label'])
                    email_in = st.text_input(txt['email_label'])
                    st.write("")
                    btn = st.form_submit_button(txt['start_btn'])
                    if btn:
                        if "@" in email_in and len(name_in) > 2:
                            save_data(name_in, email_in)
                            st.session_state.auth = True
                            st.session_state.user = name_in
                            st.rerun()
                        else:
                            st.error("Please check details")
        else:
            with st.container(border=True):
                st.success(f"{txt['welcome']} {st.session_state.user} 🌟")
                if st.button(txt['go_analysis']):
                    set_page("analysis")
                    st.rerun()

    # Right
    with c2:
        r1, r2 = st.columns([1, 3])
        with r1:
            img_shown = False
            if os.path.exists("profile.png"):
                try:
                    st.image("profile.png", width=150)
                    img_shown = True
                except: pass
            if not img_shown:
                st.image("https://cdn-icons-png.flaticon.com/512/949/949635.png", width=150)

        with r2:
            st.markdown(f"## {txt['hero_name']}")
            st.markdown(f"##### {txt['hero_role']}")
            st.write(txt['hero_desc'])

        st.markdown("---")
        st.markdown(f"#### {txt['services_title']}")
        
        sc1, sc2, sc3 = st.columns(3)
        with sc1: draw_card("📊", txt['s1_t'], txt['s1_d'])
        with sc2: draw_card("💡", txt['s2_t'], txt['s2_d'])
        with sc3: draw_card("📈", txt['s3_t'], txt['s3_d'])

    st.write("---")
    
    st.markdown(f"### {txt['exp_title']}")
    e1, e2, e3, e4 = st.columns(4)
    with e1:
        st.success("2013")
        st.caption(f"B.A. Business")
    with e2:
        st.info("2017")
        st.caption(f"M.Sc. Finance")
    with e3:
        st.warning("Academic")
        st.caption(f"Lecturer")
    with e4:
        st.error("2020")
        st.caption(f"Consultant")

    st.markdown(f'<div class="footer">{txt["footer"]}</div>', unsafe_allow_html=True)

# === DEMO ===
elif st.session_state.page == "demo":
    st.header(txt['nav_demo'])
    data = {'Branch': ['Riyadh', 'Jeddah']*5, 'Sales': [45000, 32000]*5}
    fig = px.bar(pd.DataFrame(data), x='Branch', y='Sales', color_discrete_sequence=['#27AE60'])
    st.plotly_chart(fig)

# === ANALYSIS ===
elif st.session_state.page == "analysis":
    if not st.session_state.auth:
        st.warning(txt['error_auth'])
        if st.button(txt['back_btn']):
            set_page("home")
            st.rerun()
    else:
        st.header(txt['nav_analysis'])
        up_file = st.file_uploader(txt['upload_txt'], type=['xlsx', 'csv'])
        
        if up_file:
            try:
                if up_file.name.endswith('.csv'): df = pd.read_csv(up_file)
                else: df = pd.read_excel(up_file)
                st.success(txt['success_read'])
                
                nums = df.select_dtypes(include=['number']).columns
                if len(nums) > 0:
                    st.subheader(txt['calc_title'])
                    c1, c2 = st.columns(2)
                    v1 = c1.selectbox(txt['m_rev'], nums, index=0)
                    idx = 1 if len(nums) > 1 else 0
                    v2 = c2.selectbox(txt['m_cost'], nums, index=idx)
                    
                    rev = df[v1].sum()
                    cost = df[v2].sum()
                    prof = rev - cost
                    
                    k1, k2, k3 = st.columns(3)
                    k1.metric(txt['m_rev'], f"{rev:,.0f}")
                    k2.metric(txt['m_cost'], f"{cost:,.0f}")
                    k3.metric(txt['m_prof'], f"{prof:,.0f}")
                    
                    fig = px.bar(df, x=df.columns[0], y=v1, color_discrete_sequence=['#27AE60'])
                    st.plotly_chart(fig)
                else:
                    st.dataframe(df)
            except:
                st.error("File Error")
