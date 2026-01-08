import streamlit as st
import gspread

st.title("🕵️‍♀️ كشف الخطأ النهائي")

if st.button("جرب الكتابة"):
    try:
        # 1. الاتصال
        gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
        
        # 2. فتح الملف (تأكدي أن الاسم هنا يطابق ملفك تماماً)
        sh = gc.open("QararLeads") 
        
        # 3. الكتابة
        sh.sheet1.append_row(["تجربة", "test@test.com", "نجحنا"])
        
        st.success("✅ تم الحفظ! المشكلة كانت في الكود القديم فقط.")
    except Exception as e:
        st.error("❌ الخطأ هو:")
        st.code(e) # هذا السطر سيفضح المشكلة
