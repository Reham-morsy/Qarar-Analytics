import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from datetime import datetime

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
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. دالة الربط (Backend)
# ---------------------------------------------------------
def save_to_google_sheets(name, email):
    try:
        if "gcp_service_account" in st.secrets:
            gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
            # اسم الملف مطابق لما أنشأتِه في جوجل درايف (بدون مسافات)
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
    st.caption("© 2024 Dr. Reham Morsy")

# ---------------------------------------------------------
# 4. المحتوى
# ---------------------------------------------------------

if 'email_submitted' not in st.session_state:
    st.session_state.email_submitted = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = "Guest"

# --- الصفحة الرئيسية ---
if mode == "🏠 الصفحة الرئيسية":
    c1, c2 = st.columns(2)
    with c1:
        st.title("حوّل بياناتك إلى أرباح 🚀")
        st.markdown("### منصة قرار لتحليل الأعمال")
        st.info("👈 ابدأ من القائمة الجانبية.")
    with c2:
        st.image("https://images.unsplash.com/photo-1460925895917-afdab827c52f")

# --- الديمو ---
elif mode == "⚡ تجربة النظام (Demo)":
    st.title("⚡ تجربة حية")
    data = {'المدينة': ['الرياض', 'جدة']*10, 'المبيعات': [5000, 3000]*10}
    st.plotly_chart(px.bar(pd.DataFrame(data), x='المدينة', y='المبيعات'), use_container_width=True)

# --- رفع الملف (المنتج الأساسي) ---
elif mode == "📂 رفع وتحليل ملفي":
    st.title("📂 تحليل البيانات الخاص")
    uploaded_file = st.file_uploader("ارفع ملف Excel/CSV", type=['xlsx', 'csv'])
    
    if uploaded_file:
        try:
            # قراءة الملف
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success("✅ تم قراءة الملف!")
            
            # البوابة (The Gate)
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
                                
                                # محاولة الحفظ
                                saved, msg = save_to_google_sheets(name, email)
                                if saved:
                                    st.toast("تم حفظ بياناتك بنجاح!")
                                else:
                                    # إظهار الخطأ إذا فشل الحفظ
                                    st.error(f"⚠️ تنبيه: لم يتم حفظ الإيميل ({msg}) ولكن التقرير سيفتح.")
                                
                                st.balloons()
                                st.rerun()
                            else:
                                st.error("إيميل غير صحيح")
            else:
                # العرض بعد الفتح
                st.info(f"مرحباً {st.session_state.user_name}")
                
                # عرض الإجمالي
                num_cols = df.select_dtypes(include=['number']).columns
                cat_cols = df.select_dtypes(include=['object']).columns
                
                if len(num_cols) > 0:
                    st.metric("الإجمالي", f"{df[num_cols[0]].sum():,.0f}")
                
                # --- قسم الدفع ---
                st.markdown("---")
                col_p1, col_p2 = st.columns([3, 1])
                with col_p1:
                    st.write("💡 **هل تريد تقريراً احترافياً PDF؟** (يتضمن توصيات بالذكاء الاصطناعي)")
                with col_p2:
                    st.link_button("💳 شراء التقرير الكامل", "https://buy.stripe.com/test_123")
                st.markdown("---")

                # الرسوم البيانية
                if len(num_cols) > 0:
                    if len(cat_cols) > 0:
                        st.plotly_chart(px.bar(df, x=cat_cols[0], y=num_cols[0]), use_container_width=True)
                    else:
                        st.line_chart(df[num_cols[0]])
                else:
                    st.dataframe(df)

        except Exception as e:
            st.error("الملف غير مدعوم أو تالف.")
