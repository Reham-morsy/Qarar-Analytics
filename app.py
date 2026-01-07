import streamlit as st
import pandas as pd
import plotly.express as px

# 1. إعدادات الصفحة والهوية
st.set_page_config(
    page_title="Qarar | قرار",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تخصيص CSS لإخفاء القوائم الافتراضية وجعل المظهر احترافياً
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    div[data-testid="stMetricValue"] {font-size: 24px;}
</style>
""", unsafe_allow_html=True)

# --- القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3094/3094851.png", width=70)
    st.markdown("### منصة قرار | Qarar")
    st.caption("ذكاء الأعمال لرواد الأعمال 🚀")
    
    st.markdown("---")
    
    # زر التبديل الرئيسي
    st.markdown("**⚙️ وضع العرض:**")
    mode = st.radio("", ["رفع ملف خاص 📂", "تجرية النظام (Demo) ⚡"], index=0)
    
    st.markdown("---")
    
    # قسم التواصل (تم تحديث الرابط هنا)
    st.markdown("### 📞 احجز استشارتك")
    st.info("هل تريد تصميم نظام مخصص لشركتك؟")
    
    # روابط التواصل
    st.markdown("""
    <div style='display: flex; gap: 10px; align-items: center;'>
        <a href='https://www.linkedin.com/in/reham-morsy-45b61a192/' target='_blank'>
            <img src='https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin&logoColor=white' width='140'>
        </a>
    </div>
    <br>
    <a href='mailto:riham@example.com' style='text-decoration: none; color: #333; font-weight: bold;'>📧 تواصل عبر الإيميل</a>
    """, unsafe_allow_html=True)
    
    st.write("---")
    st.caption("© 2024 Dr. Reham Morsy")

# --- الصفحة الرئيسية ---

# الهيدر الترحيبي
if mode == "رفع ملف خاص 📂":
    st.title("حوّل بياناتك إلى قرارات.. في ثوانٍ ⏱️")
    st.markdown("##### المنصة الأولى لتحليل بيانات المبيعات وبناء لوحات التحكم الآلية.")
else:
    st.title("⚡ تجربة حية (Live Demo)")
    st.markdown("##### جرب تغيير الفلاتر وشاهد كيف يتفاعل نظام (قرار) مع البيانات.")

st.markdown("---")

# --- المنطق البرمجي (The Logic) ---
df = None

# السيناريو 1: الديمو التفاعلي
if mode == "تجرية النظام (Demo) ⚡":
    # بيانات وهمية ذكية
    data = {
        'المنتج': ['لابتوب Pro', 'هاتف X', 'ساعة ذكية', 'سماعة Pro', 'شاحن سريع'] * 20,
        'الفرع': ['الرياض', 'جدة', 'الدمام', 'مكة', 'الخبر'] * 20,
        'المبيعات': [5000, 3000, 1500, 800, 200] * 20,
        'الكمية': [10, 20, 30, 40, 50] * 20,
        'الأرباح': [1000, 500, 300, 150, 50] * 20
    }
    df = pd.DataFrame(data)
    
    # 🔥 إضافة فلتر تفاعلي
    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        selected_city = st.selectbox("📍 اختر الفرع لعرض نتائجه:", ["الكل"] + list(df['الفرع'].unique()))
    
    if selected_city != "الكل":
        df = df[df['الفرع'] == selected_city]
    
    st.success(f"✅ يتم عرض تحليل مبيعات: **{selected_city}**")

# السيناريو 2: رفع الملف
else:
    uploaded_file = st.file_uploader("📥 ارفع ملف المبيعات (Excel/CSV)", type=['xlsx', 'csv'])
    
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            st.success("✅ تم تحليل الملف بنجاح!")
        except:
            st.error("عذراً، تأكد من صحة الملف.")
    else:
        # صورة توضيحية تظهر فقط إذا لم يرفع الملف
        st.info("👈 لترى السحر، انتقل لوضع (تجربة النظام) من القائمة الجانبية، أو ارفع ملفك.")
        st.image("https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=2015&auto=format&fit=crop", caption="لوحات تحكم احترافية")

# --- عرض الداشبورد (Dashboard Engine) ---
if df is not None:
    # تنسيق الأرقام
    total_sales = df.select_dtypes(include=['number']).iloc[:, 0].sum()
    if df.shape[1] > 1: # التأكد من وجود أعمدة كافية للأرباح
         total_profit = df.select_dtypes(include=['number']).iloc[:, -1].sum()
    else:
         total_profit = 0
         
    count_ops = len(df)
    
    # صف الأرقام القياسية (KPIs)
    st.markdown("### 📊 نظرة عامة")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("إجمالي المبيعات", f"{total_sales:,.0f} SAR", "12% 🔼")
    kpi2.metric("صافي الأرباح (تقديري)", f"{total_profit:,.0f} SAR", "8% 🔼")
    kpi3.metric("عدد العمليات", count_ops, "نشط")
    avg_basket = total_sales/count_ops if count_ops > 0 else 0
    kpi4.metric("متوسط السلة", f"{avg_basket:,.0f} SAR")
    
    st.markdown("---")
    
    # صف الرسومات البيانية
    col_chart1, col_chart2 = st.columns([2, 1])
    
    # محاولة ذكية لاكتشاف الأعمدة
    cat_cols = df.select_dtypes(include=['object']).columns
    num_cols = df.select_dtypes(include=['number']).columns
    
    if len(cat_cols) > 0 and len(num_cols) > 0:
        with col_chart1:
            st.subheader(f"تحليل {num_cols[0]} حسب {cat_cols[0]}")
            fig_bar = px.bar(df, x=cat_cols[0], y=num_cols[0], color=num_cols[0], template="plotly_white")
            st.plotly_chart(fig_bar, use_container_width=True)
            
        with col_chart2:
            st.subheader("نسبة التوزيع")
            fig_pie = px.pie(df, names=cat_cols[0], values=num_cols[0], hole=0.4, template="plotly_white")
            st.plotly_chart(fig_pie, use_container_width=True)
            
    # عرض البيانات الخام
    with st.expander("🔎 عرض البيانات التفصيلية (Excel View)"):
        st.dataframe(df, use_container_width=True)
