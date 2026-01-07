import streamlit as st
import pandas as pd
import plotly.express as px

# 1. إعدادات الصفحة
st.set_page_config(page_title="Qarar | قرار", page_icon="📊", layout="wide")

# --- القائمة الجانبية ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3094/3094851.png", width=80)
    st.title("منصة قرار")
    st.header("⚙️ خيارات العرض")
    use_demo = st.toggle("👀 عرض نموذج تجريبي (Demo)", value=False)
    st.markdown("---")
    st.header("📞 تواصل معنا")
    st.info("هل تحتاج لتحليل مخصص لشركتك؟")
    st.markdown("[🔗 LinkedIn](https://www.linkedin.com) | [📧 Email](mailto:test@test.com)")
    st.write("© 2024 Dr. Riham Morsi")

# --- الواجهة ---
col1, col2 = st.columns([3, 1])
with col1:
    st.title("مرحباً بك في عالم البيانات الذكية 🧠")
    st.markdown("##### لا تدع أرقامك صامتة.. اجعلها تخبرك أين يختبئ القرار الصحيح.")

df = None
show_dashboard = False

if use_demo:
    data = {
        'المنتج': ['لابتوب', 'هاتف', 'ساعة', 'سماعة', 'لابتوب', 'هاتف', 'ساعة', 'شاحن', 'ماوس', 'كيبورد'],
        'الفئة': ['إلكترونيات', 'إلكترونيات', 'اكسسوارات', 'اكسسوارات', 'إلكترونيات', 'إلكترونيات', 'اكسسوارات', 'اكسسوارات', 'اكسسوارات', 'اكسسوارات'],
        'المبيعات': [5000, 3000, 1500, 800, 5200, 3100, 1600, 200, 150, 300],
        'المنطقة': ['الرياض', 'جدة', 'الرياض', 'مكة', 'الدمام', 'الرياض', 'جدة', 'الرياض', 'مكة', 'الدمام']
    }
    df = pd.DataFrame(data)
    st.success("✅ أنت الآن تشاهد بيانات تجريبية (Demo Mode)")
    show_dashboard = True
else:
    st.write("### 📂 ارفع ملف مبيعاتك")
    uploaded_file = st.file_uploader("Excel / CSV", type=['xlsx', 'csv'])
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'): df = pd.read_csv(uploaded_file)
            else: df = pd.read_excel(uploaded_file)
            show_dashboard = True
        except: st.error("خطأ في الملف")
    
    if not show_dashboard:
        st.markdown("---")
        st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71", caption="شكل التقرير النهائي")

if show_dashboard and df is not None:
    st.markdown("---")
    total_sales = df.select_dtypes(include=['number']).iloc[:, 0].sum()
    st.metric("إجمالي المبيعات", f"{total_sales:,.0f} $")
    
    c1, c2 = st.columns(2)
    num_cols = df.select_dtypes(include=['number']).columns
    cat_cols = df.select_dtypes(include=['object']).columns
    
    with c1:
        if len(num_cols)>0 and len(cat_cols)>0:
            st.plotly_chart(px.bar(df, x=cat_cols[0], y=num_cols[0]), use_container_width=True)
    with c2:
        if len(num_cols)>0:
            st.plotly_chart(px.pie(df, values=num_cols[0], names=cat_cols[0] if len(cat_cols)>0 else None), use_container_width=True)
