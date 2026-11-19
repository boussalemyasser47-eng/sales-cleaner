import streamlit as st
import requests
import pandas as pd

SCRIPT_ID = "AKfycbwjhXSfX65fU5nisCXZXPWFlnquUv_KE-LeEIJ61mDrjLbrCnP6uTL1qmTUeENrsYLTTQ"
WEBHOOK_URL = f"https://google.com{SCRIPT_ID}/exec"


st.title("🧪 مختبر اختبار Google Sheets المباشر")

# 1. إضافة تاجر جديد
with st.form("add_form"):
    em = st.text_input("البريد الإلكتروني:", "test_merchant@gmail.com")
    pw = st.text_input("كلمة السر:", "123456")
    ph = st.text_input("الهاتف:", "0655112233")
    if st.form_submit_button("➕ إرسال وحفظ في Google Sheets"):
        res = requests.get(WEBHOOK_URL, params={
            "action": "upsert", "email": em, "password": pw,
            "status": "⏳ في انتظار التفعيل", "package": "29k",
            "created_at": "2026-11-19", "phone": ph
        })
        st.success(f"رد السيرفر: {res.text}")

st.divider()

# 2. قراءة البيانات والتحكم بها
if st.button("🔄 تحديث البيانات من الجدول"):
    st.rerun()

res = requests.get(WEBHOOK_URL)
if res.status_code == 200 and res.text.strip().startswith("["):
    df = pd.DataFrame(res.json())
    st.dataframe(df)
    if not df.empty:
        target = st.selectbox("اختر تاجراً للتحكم:", df["email"].tolist())
        c1, c2, c3 = st.columns(3)
        if c1.button("⚡ تفعيل"):
            row = df[df["email"] == target].iloc[0]
            requests.get(WEBHOOK_URL, params={"action": "upsert", "email": target, "password": row["password"], "status": "🟢 مفعّل ونشط", "package": row["package"], "created_at": row["created_at"], "phone": row["phone"]})
            st.rerun()
        if c2.button("🔒 حظر"):
            row = df[df["email"] == target].iloc[0]
            requests.get(WEBHOOK_URL, params={"action": "upsert", "email": target, "password": row["password"], "status": "🔴 محظور", "package": row["package"], "created_at": row["created_at"], "phone": row["phone"]})
            st.rerun()
        if c3.button("🗑️ حذف"):
            requests.get(WEBHOOK_URL, params={"action": "delete", "email": target})
            st.rerun()
else:
    st.warning(f"الرد المستلم: {res.text}")
