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

# تخصيص CSS: جعل الأزرار والواجهة أجمل
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    /* تحسين شكل صندوق الإدخال */
    .stTextInput > div > div > input {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3094/3094851.png", width=80)
    st.markdown("### 📊 منصة قرار")
    st.caption("من بيانات صامتة.. إلى قرارات ناطقة")
    
    st.markdown("---")
    
    # 🔘 التحكم في الوضع
    st.markdown("**⚙️ اختر الوضع:**")
    mode = st.radio("", ["🏠 الصفحة الرئيسية", "⚡ تجربة النظام (Demo)", "📂 رفع وتحليل ملفي"], index=0)
    
    st.markdown("---")
    
    # 📞 قسم التواصل (مهم جداً للعملاء)
    st.header("📞 تواصل معنا")
    st.info("لطلب تصميم نظام مخصص لشركتك:")
    
    # روابط تواصل احترافية
    st.markdown("""
    <div style='display: flex; flex-direction: column; gap: 10px;'>
        <a href='https://www.linkedin.com/in/reham-morsy-45b61a192/' target='_blank' style='text-decoration: none;'>
            <button style='width: 100%; background-color: #0077B5; color: white; border: none; padding: 8px; border-radius: 5px; cursor: pointer;'>
                LinkedIn Profile 🔗
            </button>
        </a>
        <a href='mailto:riham@example.com' style='text-decoration: none;'>
            <button style='width: 100%; background-color: #333; color: white; border: none; padding: 8px; border-radius: 5px; cursor: pointer;'>
                 Email Me 📧
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.caption("© 2024 Dr. Reham Morsy")

# --- المتغيرات العامة ---
if 'email_submitted' not in st.session_state:
    st.session_state.email_submitted = False

# --- الصفحة 1: الواجهة الرئيسية (Landing Page) ---
if mode == "🏠 الصفحة الرئيسية":
    col1, col2 = st.columns([1, 1])
    with col1:
        st.title("حوّل فوضى الأرقام.. إلى استراتيجيات واضحة 🚀")
        st.markdown("""
        ### هل تعاني من تكدس ملفات الإكسيل؟
        منصة **قرار** تساعدك على فهم مبيعاتك، مخزونك، وأداء موظفيك في لوحة تحكم واحدة.
        
        **لماذا تختار قرار؟**
        * ✅ تحليل فوري بدون خبرة تقنية.
        * ✅ رسوم بيانية تفاعلية.
        * ✅ كشف الفرص الضائعة.
        """)
        st.warning("👈 ابدأ باختيار (تجربة النظام) أو (رفع ملف) من القائمة الجانبية.")
    
    with col2:
        # صورة تعبيرية للواجهة
        st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=2070&auto=format&fit=crop", caption="شكل التقارير التي ستحصل عليها")


# --- الصفحة 2: الديمو (مفتوح للجميع للإبهار) ---
elif mode == "⚡ تجربة النظام (Demo)":
    st.title("⚡ تجربة حية وتفاعلية")
    st.markdown("هذه بيانات وهمية لتجربة سرعة النظام.")
    
    # بيانات وهمية
    data = {
        'الفرع': ['الرياض', 'جدة', 'الدمام', 'مكة', 'الخبر'] * 20,
        'المبيعات': [5000, 3000, 1500, 800, 200] * 20,
        'المنتج': ['A', 'B', 'C', 'D', 'E'] * 20
    }
    df_demo = pd.DataFrame(data)
    
    # فلتر تفاعلي
    city = st.selectbox("📍 اختر الفرع لتصفية البيانات:", ["الكل"] + list(df_demo['الفرع'].unique()))
    if city != "الكل":
        df_demo = df_demo[df_demo['الفرع'] == city]
        
    # رسم بياني
    fig = px.bar(df_demo, x='الفرع', y='المبيعات', color='المنتج', title="توزيع المبيعات")
    st.plotly_chart(fig, use_container_width=True)


# --- الصفحة 3: رفع الملف (محمية ببوابة الإيميل) ---
elif mode == "📂 رفع وتحليل ملفي":
    st.title("📂 تحليل البيانات الخاص")
    
    uploaded_file = st.file_uploader("ارفع ملف مبيعاتك (Excel أو CSV)", type=['xlsx', 'csv'])
    
    if uploaded_file:
        # قراءة الملف
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
                
            st.success("✅ تم استلام الملف بنجاح!")
            
            # --- بوابة القفل (The Gate) ---
            if not st.session_state.email_submitted:
                st.markdown("---")
                col_gate1, col_gate2 = st.columns([2, 1])
                with col_gate1:
                    st.warning("🔒 **هذا التقرير محمي.**")
                    st.markdown("للحفاظ على خصوصية بياناتك وعرض التقرير الاستراتيجي الكامل، يرجى تسجيل بياناتك.")
                    
                    with st.form("gate_form"):
                        name = st.text_input("الاسم:")
                        email = st.text_input("البريد الإلكتروني:")
                        submit = st.form_submit_button("🔓 فتح التقرير الآن")
                        
                        if submit:
                            if "@" in email:
                                st.session_state.email_submitted = True
                                st.session_state.user_name = name
                                st.balloons()
                                st.rerun()
                            else:
                                st.error("يرجى كتابة بريد صحيح")
            
            # --- عرض الداشبورد (بعد الفتح) ---
            else:
                st.info(f"مرحباً {st.session_state.user_name}، إليك تحليل بياناتك 👇")
                
                # KPIs
                total = df.select_dtypes(include=['number']).iloc[:, 0].sum()
                st.metric("إجمالي القيمة", f"{total:,.0f}")
                
                # Charts
                num_cols = df.select_dtypes(include=['number']).columns
                cat_cols = df.select_dtypes(include=['object']).columns
                
                if len(num_cols) > 0 and len(cat_cols) > 0:
                    fig_real = px.bar(df, x=cat_cols[0], y=num_cols[0])
                    st.plotly_chart(fig_real, use_container_width=True)
                else:
                    st.dataframe(df)

        except:
            st.error("الملف لا يحتوي على بيانات قابلة للقراءة.")
