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

# --- 2. Language System ---
if 'language' not in st.session_state:
    st.session_state.language = 'ar'

# Dictionary
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

lang = st.session_state.language
txt = t[lang]

# --- 3. CSS Dynamic ---
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.
