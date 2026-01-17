import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from datetime import datetime
import os

# --- 1. إعداد الصفحة (Config) ---
st.set_page_config(
    page_title="Qarar Analytics",
    page_icon="💎",
    layout="wide"
)

# --- 2. إدارة اللغات (Translation System) ---
if 'language' not in st.session_state:
    st.session_state.language = 'ar'

def toggle_language():
    if st.session_state.language == 'ar':
        st.session_state.language = 'en'
    else:
        st.session_state.language = 'ar'

# قاموس النصوص (Dictionary)
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
        'login_sub': 'احصل على تجربة كاملة مجاناً',
        'name_label': 'الاسم',
        'email_label': 'الإيميل',
        'start_btn': '🚀 ابدأ الآن',
        'welcome': 'أهلاً بك',
        'go_analysis': '📂 الانتقال للتحليل',
        'hero_name': 'د. ريهام مرسي',
        'hero_role': 'شريكك الاستراتيجي في تحليل الأعمال',
        'hero_desc': 'حول بياناتك المعقدة إلى قرارات رابحة.',
        'services_title': '🚀 خدماتنا المتميزة',
        'serv_1_t': 'تحليل مالي',
        'serv_1_d': 'داشبورد فوري',
        'serv_2_t': 'دراسات جدوى',
        'serv_2_d': 'تقييم المخاطر',
        'serv_3_t': 'استشارات نمو',
        'serv_3_d': 'رفع الكفاءة',
        'exp_title': '🎓 رحلة العلم والخبرة',
        'exp_1': 'بكالوريوس إدارة',
        'exp_2': 'ماجستير تمويل',
        'exp_3': 'محاضر جامعي',
        'exp_4': 'استشارات شركات',
        'footer': 'جميع الحقوق محفوظة لمنصة قرار 2026',
        'error_auth': '🔒 يجب التسجيل أولاً',
        'back_btn': '🔙 عودة',
        'upload_txt': 'ارفع ملف Excel/CSV',
        'success_read': '✅ تم القراءة',
        'calc_title': '💰 حاسبة الربحية',
        'col_rev': 'المبيعات:',
        'col_cost': 'التكلفة:',
        'm_rev': 'المبيعات',
        'm_cost': 'التكاليف',
        'm_prof': 'الربح',
        'err_file': 'خطأ في الملف'
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
        'email_label': 'Email',
        'start_btn': '🚀 Get Started',
        'welcome': 'Welcome',
        'go_analysis': '📂 Go to Analysis',
        'hero_name': 'Dr. Reham Morsi',
        'hero_role': 'Strategic Business Partner',
        'hero_desc': 'Transforming complex data into profitable decisions.',
        'services_title': '🚀 Our Services',
        'serv_1_t': 'Financial Analysis',
        'serv_1_d': 'Instant Dashboards',
        'serv_2_t': 'Feasibility Studies',
        'serv_2_d': 'Risk Assessment',
        'serv_3_t': 'Growth Consulting',
        'serv_3_d': 'Efficiency Optimization',
        'exp_title': '🎓 Education & Experience',
        'exp_1': 'B.A. Business',
        'exp_2': 'M.Sc. Finance',
        'exp_3': 'Academic Lecturer',
        'exp_4': 'Corporate Consultant',
        'footer': '© 2026 Qarar Analytics. All Rights Reserved.',
        'error_auth': '🔒 Login Required',
        'back_btn': '🔙 Go Back',
        'upload_txt': 'Upload Excel/CSV File',
        'success_read': '✅ File Loaded',
        'calc_title': '💰 Profitability Calculator',
        'col_rev': 'Revenue:',
        'col_cost': 'Cost:',
        'm_rev': 'Revenue',
        'm_cost': 'Cost',
        'm_prof': 'Profit',
        'err_file': 'File Error'
    }
}

# تحديد اللغة الحالية
lang = st.session_state.language
txt = t[lang]

# --- 3. CSS ديناميكي (حسب اللغة) ---
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

html, body, [class*="css"] {{ 
    font-family: {txt['font']}; 
    direction: {txt['dir']};
    text-align: {txt['align']};
}}

h1, h2, h3 {{ color: #27AE60; }}

div.stButton > button {{
    background-color: #27AE60; color: white; border: none;
    border-radius: 8px; padding: 8px 20px; font-weight: bold;
    width: 100%; transition: 0.3s;
}}
div.stButton > button:hover {{
    background-color: #219150; border-color: #219150; color: white;
}}

.service-card {{
    background-color: #f9f9f9; padding: 20px;
    border-radius: 10px; text-align: center;
    border-top: 4px solid #27AE60;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    margin-bottom: 10px;
    height: 180px;
}}

.footer {{
    position: fixed; left: 0; bottom: 0; width: 100%;
    background-color: #f1f1f1; color: #555; 
    text-align: center; padding: 8px; z-index: 100;
    font-size: 12px; border-top: 1px solid #ddd;
}}
</style>
""", unsafe_allow_html=True)

# --- 4. دالة الحفظ ---
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

# --- 5. القائمة الجانبية (Sidebar) ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_column_width=True)
    else:
        st.header("💎 Qarar")
    
    # زر تبديل اللغة
    col_lang1, col_lang2 = st.columns(2)
    with col_lang1:
        if st.button("🇺🇸 English"):
            st.session_state.language = 'en'
            st.rerun()
    with col_lang2:
        if st.button("🇪🇬 العربية"):
            st.session_state.language = 'ar'
            st.rerun()

    st.markdown("---")
    st.markdown(f"<h3 style='text-align: center; color: #27AE60;'>{txt['sidebar_title']}</h3>", unsafe_allow_html=True)
    
    # التنقل
    if 'page' not in st.session_state: st.session_state.page = "home"
    def set_page(p): st.session_state.page = p
    
    if 'auth' not in st.session_state: st.session_state.auth = False
    if 'user' not in st.session_state: st.session_state.user = "Guest"
    
    if st.button(txt['nav_home'], use_container_width=True): set_page("home")
    if st.button(txt['nav_demo'], use_container_width=True): set_page("demo")
    if st.button(txt['nav_analysis'], use_container_width=True): set_page("analysis")
    
    st.markdown("---")
    if st.session_state.auth:
        st.caption(f"👤 {st.session_state.user}")
        if st.button(txt['logout']):
            st.session_state.auth = False
            st.session_state.user = "Guest"
            st.rerun()
            
    st.markdown("[LinkedIn 🔗](https://www.linkedin.com/in/reham-morsy-45b61a192/)")
    st.caption("© 2026 Dr. Reham Morsi")

# --- 6. المحتوى ---

# === HOME ===
if st.session_state.page == "home":
    
    c1, c2 = st.columns([1, 2])
    
    # Left: Login
    with c1:
        st.write("")
        st.write("")
        if not st.session_state.auth:
            with st.container(border=True):
                st.markdown(f"#### {txt['login_title']}")
                st.caption(txt['login_sub'])
                with st.form("login_form"):
                    name_in = st.text_input(txt['name_label'])
                    email_in = st.text_input(txt['email_label'])
                    btn = st.form_submit_button(txt['start_btn'])
                    
                    if btn:
                        if "@" in email_in and len(name_in) > 2:
                            save_data(name_in, email_in)
                            st.session_state.auth = True
                            st.session_state.user = name_in
                            st.rerun()
                        else:
                            st.error("Error")
        else:
            with st.container(border=True):
                st.success(f"{txt['welcome']} {st.session_state.user} 🌟")
                if st.button(txt['go_analysis']):
                    set_page("analysis")
                    st.rerun()

    # Right: Info
    with c2:
        r1, r2 = st.columns([1, 3])
        with r1:
            if os.path.exists("profile.png"):
                st.image("profile.png", width=140)
            else:
                st.image("https://cdn-icons-png.flaticon.com/512/949/949635.png", width=140)
        with r2:
            st.markdown(f"## {txt['hero_name']}")
            st.markdown(f"**{txt['hero_role']}**")
            st.write(txt['hero_desc'])

        st.markdown("---")
        st.markdown(f"#### {txt['services_title']}")
        
        # Services
        html_s1 = f"""
        <div class="service-card">
            <h3>📊</h3>
            <b>{txt['serv_1_t']}</b><br>
            <small>{txt['serv_1_d']}</small>
        </div>
        """
        html_s2 = f"""
        <div class="service-card">
            <h3>💡</h3>
            <b>{txt['serv_2_t']}</b><br>
            <small>{txt['serv_2_d']}</small>
        </div>
        """
        html_s3 = f"""
        <div class="service-card">
            <h3>📈</h3>
            <b>{txt['serv_3_t']}</b><br>
            <small>{txt['serv_3_d']}</small>
        </div>
        """
        
        sc1, sc2, sc3 = st.columns(3)
        with sc1: st.markdown(html_s1, unsafe_allow_html=True)
        with sc2: st.markdown(html_s2, unsafe_allow_html=True)
        with sc3: st.markdown(html_s3, unsafe_allow_html=True)

    st.write("---")
    
    # Experience
    st.markdown(f"### {txt['exp_title']}")
    e1, e2, e3, e4 = st.columns(4)
    
    with e1:
        st.success("🏗️ **2013**")
        st.caption(txt['exp_1'])
    
    with e2:
        st.info("📈 **2017**")
        st.caption(txt['exp_2'])
        
    with e3:
        st.warning("🏛️ **Academic**")
        st.caption(txt['exp_3'])
        
    with e4:
        st.error("💼 **2020**")
        st.caption(txt['exp_4'])

    st.markdown(f'<div class="footer">{txt["footer"]}</div>', unsafe_allow_html=True)

# === DEMO ===
elif st.session_state.page == "demo":
    st.header(txt['nav_demo'])
    data = {'Branch': ['Riyadh', 'Jeddah']*5, 'Sales': [45000, 32000]*5}
    fig = px.bar(
        pd.DataFrame(data), 
        x='Branch', 
        y='Sales', 
        color_discrete_sequence=['#27AE60']
    )
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
                if up_file.name.endswith('.csv'):
                    df = pd.read_csv(up_file)
                else:
                    df = pd.read_excel(up_file)
                st.success(txt['success_read'])
                
                nums = df.select_dtypes(include=['number']).columns
                if len(nums) > 0:
                    st.subheader(txt['calc_title'])
                    c1, c2 = st.columns(2)
                    v1 = c1.selectbox(txt['col_rev'], nums, index=0)
                    
                    idx = 1 if len(nums) > 1 else 0
                    v2 = c2.selectbox(txt['col_cost'], nums, index=idx)
                    
                    rev = df[v1].sum()
                    cost = df[v2].sum()
                    prof = rev - cost
                    
                    k1, k2, k3 = st.columns(3)
                    k1.metric(txt['m_rev'], f"{rev:,.0f}")
                    k2.metric(txt['m_cost'], f"{cost:,.0f}")
                    k3.metric(txt['m_prof'], f"{prof:,.0f}")
                    
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
                st.error(txt['err_file'])
