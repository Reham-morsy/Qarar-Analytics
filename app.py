import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="Qarar | قرار",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS التجميلي
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    .stTextInput > div > div > input {border-radius: 10px;}
</style>
""", unsafe_allow_html=True)

# --- دالة الربط مع جوجل شيت (تعمل في الخفاء) ---
def save_to_google_sheets(name, email):
    try:
        # الاتصال بالمفاتيح السرية
        gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
        sh = gc.open("Qarar Leads") 
        worksheet = sh.sheet1
        
        # حفظ البيانات
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        worksheet.append_row([name, email, current_time])
        return True
    except:
        return False

# --- القائمة الجانبية ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3094/3094851.png", width=80)
    st.markdown("### 📊 منصة قرار")
    st.caption("من بيانات صامتة.. إلى قرارات ناطقة")
    st.markdown("---")
    
    mode = st.radio("القائمة:", ["🏠 الصفحة الرئيسية", "⚡ تجربة النظام (Demo)", "📂 رفع وتحليل ملفي"], index=0)
    
    st.markdown("---")
    st.header("📞 تواصل معنا")
    st.markdown("""
    <a href='https://www.linkedin.com/in/reham-morsy-45b61a192/' target='_blank'>
        <img src='https://img.shields.io/badge/LinkedIn-Connect-0077B5?logo=linkedin' width='120'>
    </a>
    <br><br>
    <a href='mailto:rehammorsy2012@gmail.com' style='text-decoration: none; color: #333;'>📧 Email Me</a>
    """, unsafe_allow_html=True)
    st.caption("© 2024 Dr. Reham Morsy")

# --- المتغيرات ---
if 'email_submitted' not in st.session_state:
    st.session_state.email_submitted = False

# --- الصفحات ---

# 1. الرئيسية
if mode == "🏠 الصفحة الرئيسية":
    col1, col2 = st.columns([1, 1])
    with col1:
        st.title("حوّل بياناتك إلى استراتيجيات 🚀")
        st.markdown("""
        ### منصة قرار لتحليل الأعمال
        نساعدك على تحويل ملفات الإكسيل المعقدة إلى لوحات تحكم تفاعلية في ثوانٍ.
        
        * ✅ تحليل المبيعات والأرباح.
        * ✅ كشف المنتجات الأكثر مبيعاً.
        * ✅ تقارير جاهزة لاتخاذ القرار.
        """)
        st.info("👈 ابدأ الآن باختيار (تجربة النظام) أو (رفع ملف).")
    with col2:
        st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71", caption="Dashboard Preview")

# 2. الديمو
elif mode == "⚡ تجربة النظام (Demo)":
    st.title("⚡ تجربة حية")
    st.markdown("غيّر الفلاتر لترى كيف تتفاعل البيانات:")
    
    data = {'الفرع': ['الرياض', 'جدة', 'الدمام']*10, 'المبيعات': [5000, 3000, 7000]*10, 'المنتج': ['A', 'B', 'C']*10}
    df_demo = pd.DataFrame(data)
    
    city = st.selectbox("المدينة:", ["الكل"] + list(df_demo['الفرع'].unique()))
    if city != "الكل": df_demo = df_demo[df_demo['الفرع'] == city]
    
    st.plotly_chart(px.bar(df_demo, x='الفرع', y='المبيعات', color='المنتج'), use_container_width=True)

# 3. الرفع والتحليل (محمي)
elif mode == "📂 رفع وتحليل ملفي":
    st.title("📂 تحليل البيانات الخاص")
    uploaded_file = st.file_uploader("ارفع ملف Excel/CSV", type=['xlsx', 'csv'])
    
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'): df = pd.read_csv(uploaded_file)
            else: df = pd.read_excel(uploaded_file)
            
            st.success("✅ تم قراءة الملف!")
            
            # --- بوابة القفل (The Gate) ---
            if not st.session_state.email_submitted:
                st.markdown("---")
                c1, c2 = st.columns([2,1])
                with c1:
                    st.warning("🔒 **التقرير محمي:** يرجى تسجيل بياناتك لفتح لوحة التحكم الكاملة.")
                    with st.form("gate"):
                        name = st.text_input("الاسم:")
                        email = st.text_input("البريد الإلكتروني:")
                        submit = st.form_submit_button("🔓 فتح التقرير")
                        
                        if submit:
                            if "@" in email:
                                st.session_state.email_submitted = True
                                st.session_state.user_name = name
                                # حفظ في جوجل شيت
                                save_to_google_sheets(name, email)
                                st.balloons()
                                st.rerun()
                            else:
                                st.error("إيميل غير صحيح")
            
            # --- العرض بعد الفتح ---
            else:
                st.info(f"مرحباً {st.session_state.user_name} | تم فتح التحليل الكامل 👇")
                
                # KPIs
                total = df.select_dtypes(include=['number']).iloc[:, 0].sum()
                st.metric("إجمالي القيمة", f"{total:,.0f}")
                
                # Charts
                num = df.select_dtypes(include=['number']).columns
                cat = df.select_dtypes(include=['object']).columns
                
                if len(num)>0 and len(cat)>0:
                    c1, c2 = st.columns(2)
                    c1.plotly_chart(px.bar(df, x=cat[0], y=num[0]), use_container_width=True)
                    c2.plotly_chart(px.pie(df, values=num[0], names=cat[0]), use_container_width=True)
                else:
                    st.dataframe(df)
        except:
            st.error("الملف غير مدعوم") 
