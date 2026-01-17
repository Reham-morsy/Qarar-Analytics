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
        'align
