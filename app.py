import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from datetime import datetime
import os

# ---------------------------------------------------------
# 1. إعدادات الصفحة
# ---------------------------------------------------------
st.set_page_config(
    page_title="Qarar | قرار",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS للتجميل
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 1px solid #ddd;
    }
    .stButton > button {
        border-radius: 10px;
        width: 100%;
        font-weight: bold;
    }
    /* تنسيق كروت الأرقام */
    div[data-testid="stMetricValue"] {
        font-size: 24px;
        color: #2E86C1;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. دالة الربط (Backend) - Google Sheets
# ---------------------------------------------------------
def save_to_google_sheets(name, email):
    try:
        if "gcp_service_account" in st.secrets:
            gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
            sh = gc.open("QararLeads")
            worksheet = sh.sheet1
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            worksheet.append_row([name, email, current_time])
            return True, "تم الحفظ"
        else:
            return False, "المفاتيح غير موجودة"
    except Exception as e:
        return False, str(e)

# ---------------------------------------------------------
# 3. القائمة الجانبية
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3094/3094851.png", width=80)
    st.title("منصة قرار")
    st.markdown("---")
    
    mode = st.radio("القائمة:", 
                    ["🏠 الصفحة الرئيسية", "⚡ تجربة النظام (Demo)", "📂 رفع وتحليل ملفي"], 
                    index=0)
    
    st.markdown("---")
    st.header("📞 تواصل معنا")
    st.markdown("[LinkedIn 🔗](https://www.linkedin.com/in/reham-morsy-45b61a192/)")
    st.caption("© 2026 Dr. Reham Morsy")

# ---------------------------------------------------------
# 4. المحتوى الرئيسي
# ---------------------------------------------------------

if 'email_submitted' not in st.session_state:
    st.session_state.email_submitted = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = "Guest"

# --- 🏠 الصفحة الرئيسية ---
if mode == "🏠 الصفحة الرئيسية":
    st.markdown("<h1 style='text-align: center; color: #2E86C1;'>منصة قرار: عندما تتحدث الأرقام.. نصنع نحن القرار 🎯</h1>", unsafe_allow_html=True)
    st.write("---")

    col_profile, col_bio = st.columns([1, 2.5])
    
    with col_profile:
        if os.path.exists("profile.png"):
            st.image("profile.png", width=200)
        elif os.path.exists("photo.jpg"):
             st.image("photo.jpg", width=200)
        else:
            st.image("https://cdn-icons-png.flaticon.com/512/4140/4140048.png", width=180)
        st.caption("د. ريهام مرسي")
    
    with col_bio:
        st.markdown("""
        ### مرحباً، أنا د. ريهام مرسي 👋
        **شريكك الاستراتيجي في تحليل الأعمال والمالية**
        
        أؤمن أن خلف كل رقم في شركتك قصة، وخلف كل جدول بيانات فرصة ضائعة أو ربح منتظر. 
        دوري ليس مجرد حساب الأرقام، بل **ترجمتها إلى لغة يفهمها صناع القرار**.
        """)
        st.markdown("[تواصل معي على LinkedIn 🔗](https://www.linkedin.com/in/reham-morsy-45b61a192/)")

    st.write("---")
    
    col_cta1, col_cta2 = st.columns([3, 1])
    with col_cta1:
        st.info("📢 **هل بياناتك جاهزة لتروي قصتها؟** انتقلي لصفحة التحليل الآن.")

# --- ⚡ الديمو ---
elif mode == "⚡ تجربة النظام (Demo)":
    st.title("⚡ تجربة حية (مثال)")
    st.write("هذا مثال لما ستحصل عليه عند رفع ملفك:")
    data = {'المدينة': ['الرياض', 'جدة', 'الدمام', 'مكة']*5, 'المبيعات': [5000, 3000, 4500, 2000]*5}
    st.plotly_chart(px.bar(pd.DataFrame(data), x='المدينة', y='المبيعات', color='المدينة'), use_container_width=True)

# --- 📂 رفع وتحليل ملفي (القسم المطور) ---
elif mode == "📂 رفع وتحليل ملفي":
    st.title("📂 تحليل البيانات الخاص")
    uploaded_file = st.file_uploader("ارفع ملف Excel/CSV", type=['xlsx', 'csv'])
    
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success("✅ تم قراءة الملف بنجاح!")
            
            # --- بوابة التسجيل ---
            if not st.session_state.email_submitted:
                st.markdown("---")
                col_gate1, col_gate2 = st.columns([2, 1])
                with col_gate1:
                    st.warning("🔒 **التقرير محمي:** يرجى التسجيل للمتابعة.")
                    with st.form("gate_form"):
                        name = st.text_input("الاسم:")
                        email = st.text_input("البريد الإلكتروني:")
                        if st.form_submit_button("🔓 فتح التقرير"):
                            if "@" in email:
                                st.session_state.email_submitted = True
                                st.session_state.user_name = name
                                saved, msg = save_to_google_sheets(name, email)
                                st.balloons()
                                st.rerun()
                            else:
                                st.error("الرجاء إدخال إيميل صحيح")
            else:
                # --- لوحة التحكم (بعد الفتح) ---
                st.info(f"مرحباً {st.session_state.user_name}، إليك تحليل بياناتك:")
                
                num_cols = df.select_dtypes(include=['number']).columns
                cat_cols = df.select_dtypes(include=['object']).columns
                
                if len(num_cols) > 0:
                    # 💰 القسم الجديد: حاسبة الربحية الذكية
                    st.markdown("### 💰 مؤشرات الربحية والنمو")
                    st.caption("حدد الأعمدة الخاصة بالإيرادات والتكاليف لحساب صافي الربح:")
                    
                    c_sel1, c_sel2 = st.columns(2)
                    with c_sel1:
                        rev_col = st.selectbox("اختر عمود (المبيعات/الإيراد):", num_cols, index=0)
                    with c_sel2:
                        # محاولة اختيار عمود آخر افتراضياً إن وجد
                        def_idx = 1 if len(num_cols) > 1 else 0
                        cost_col = st.selectbox("اختر عمود (التكلفة/المصروفات):", num_cols, index=def_idx)
                    
                    # الحسابات
                    total_revenue = df[rev_col].sum()
                    total_cost = df[cost_col].sum()
                    net_profit = total_revenue - total_cost
                    profit_margin = (net_profit / total_revenue * 100) if total_revenue > 0 else 0
                    
                    st.markdown("---")
                    
                    # عرض النتائج في كروت
                    kpi1, kpi2, kpi3 = st.columns(3)
                    with kpi1:
                        st.metric("إجمالي المبيعات", f"{total_revenue:,.0f}")
                    with kpi2:
                        st.metric("إجمالي التكاليف", f"{total_cost:,.0f}")
                    with kpi3:
                        st.metric("صافي الربح", f"{net_profit:,.0f}", delta=f"{profit_margin:.1f}% هامش ربح")
                    
                    st.markdown("---")

                # --- زر الدفع ---
                col_p1, col_p2 = st.columns([3, 1])
                with col_p1:
                    st.write("💡 **هل تريد تحليلاً أعمق؟ (توقعات المستقبل + خطة تقليل التكاليف)**")
                with col_p2:
                    st.link_button("💳 شراء التقرير الكامل", "https://buy.stripe.com/test_123")
                st.markdown("---")

                # الرسوم البيانية
                if len(num_cols) > 0:
                    if len(cat_cols) > 0:
                        st.plotly_chart(px.bar(df, x=cat_cols[0], y=rev_col, title=f"تحليل {rev_col} حسب التصنيف"), use_container_width=True)
                    else:
                        st.line_chart(df[rev_col])
                else:
                    st.dataframe(df)

        except Exception as e:
            st.error("حدث خطأ أثناء قراءة الملف.")
            st.error(e)
