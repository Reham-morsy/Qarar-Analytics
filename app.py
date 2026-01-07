import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="Qarar | قرار",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS لتحسين المظهر وإخفاء العلامات المائية
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    .stTextInput > div > div > input {background-color: #f0f2f6;}
</style>
""", unsafe_allow_html=True)

# --- القائمة الجانبية ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3094/3094851.png", width=80)
    st.title("منصة قرار")
    st.caption("حوّل بياناتك إلى أرباح 🚀")
    
    st.markdown("---")
    st.info("🔒 النسخة الآمنة V1.0")
    st.markdown("© 2024 Dr. Reham Morsy")

# --- الواجهة الرئيسية ---
st.title("📊 منصة تحليل المبيعات الذكية")
st.markdown("قم برفع ملف مبيعاتك، وسيقوم النظام باستخراج الأخطاء والفرص الضائعة فوراً.")

# متغير لتخزين حالة الدخول
if 'email_submitted' not in st.session_state:
    st.session_state.email_submitted = False

# 1. منطقة رفع الملف (مفتوحة للجميع)
uploaded_file = st.file_uploader("📥 الخطوة 1: ارفع ملف البيانات (Excel/CSV)", type=['xlsx', 'csv'])

df = None

# قراءة الملف
if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # إظهار معاينة صغيرة فقط (للتشويق)
        st.success("✅ تم قراءة الملف بنجاح! يحتوي على {} صفاً.".format(len(df)))
        st.write("🔎 **معاينة سريعة للبيانات:**")
        st.dataframe(df.head(3)) # عرض أول 3 صفوف فقط
        
    except Exception as e:
        st.error("حدث خطأ في قراءة الملف. تأكد أنه سليم.")

# 2. بوابة الإيميل (The Gate)
if df is not None:
    st.markdown("---")
    
    # إذا لم يسجل الدخول بعد
    if not st.session_state.email_submitted:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.warning("🔒 **للحصول على التقرير التحليلي الكامل والرسوم البيانية:**")
            st.markdown("يرجى تسجيل بريدك الإلكتروني لفتح قفل الداشبورد.")
            
            with st.form("lead_form"):
                name = st.text_input("الاسم الكريم:")
                email = st.text_input("البريد الإلكتروني للعمل:")
                phone = st.text_input("رقم الواتساب (اختياري):")
                
                submitted = st.form_submit_button("🔓 فتح التحليل الآن")
                
                if submitted:
                    if email and "@" in email:
                        st.session_state.email_submitted = True
                        st.session_state.user_email = email
                        st.session_state.user_name = name
                        st.balloons()
                        st.rerun() # إعادة تحميل الصفحة لفتح القفل
                    else:
                        st.error("يرجى كتابة بريد إلكتروني صحيح.")
    
    # 3. عرض الداشبورد (فقط بعد التسجيل)
    else:
        st.success(f"مرحباً بك يا {st.session_state.user_name} 👋 | تم فتح التقرير الكامل.")
        
        # --- منطقة التحليل (نفس الكود السابق) ---
        total_sales = df.select_dtypes(include=['number']).iloc[:, 0].sum()
        count_ops = len(df)
        
        # KPIs
        k1, k2, k3 = st.columns(3)
        k1.metric("إجمالي المبيعات", f"{total_sales:,.0f}", "مكتمل")
        k2.metric("عدد العمليات", count_ops)
        k3.metric("حالة البيانات", "نشطة ✅")
        
        # Charts
        c1, c2 = st.columns(2)
        cat_cols = df.select_dtypes(include=['object']).columns
        num_cols = df.select_dtypes(include=['number']).columns
        
        with c1:
            if len(cat_cols) > 0:
                st.subheader("تحليل الأداء")
                fig = px.bar(df, x=cat_cols[0], y=num_cols[0] if len(num_cols)>0 else df.index)
                st.plotly_chart(fig, use_container_width=True)
                
        with c2:
            st.subheader("توزيع النسب")
            if len(num_cols) > 0:
                 fig2 = px.pie(df, values=num_cols[0], names=cat_cols[0] if len(cat_cols)>0 else None)
                 st.plotly_chart(fig2, use_container_width=True)

        # رسالة في النهاية
        st.info(f"💡 تم تسجيل دخولك بـ: {st.session_state.user_email}")
        st.markdown("**هل تريد تحليل المزيد من الملفات؟** تواصل معنا للترقية للباقة المدفوعة.")
