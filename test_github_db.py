import streamlit as st
import requests
import base64
import json
import pandas as pd

st.set_page_config(page_title="مختبر قاعدة بيانات GitHub", page_icon="🚀")
st.title("🚀 مختبر الحفظ الدائم في GitHub")

TOKEN = st.secrets["GITHUB_TOKEN"]
REPO = "boussalemyasser47-eng/tijaratna-dataDZ"
FILE_PATH = "merchants_data.json"
API_URL = f"https://github.com{REPO}/contents/{FILE_PATH}"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

def load_merchants():
    res = requests.get(API_URL, headers=HEADERS)
    if res.status_code == 200:
        data = res.json()
        raw_text = base64.b64decode(data["content"]).decode("utf-8").strip()
        records = json.loads(raw_text) if raw_text else []
        return records, data["sha"]
    else:
        st.error(f"⚠️ خطأ في القراءة ({res.status_code}): {res.text}")
        return [], None

def save_merchants(records, sha):
    encoded = base64.b64encode(
        json.dumps(records, ensure_ascii=False, indent=2).encode("utf-8")
    ).decode("utf-8")
    payload = {
        "message": "تحديث بيانات التجار",
        "content": encoded,
        "sha": sha
    }
    res = requests.put(API_URL, headers=HEADERS, json=payload)
    if res.status_code in (200, 201):
        return True
    st.error(f"⚠️ خطأ في الحفظ ({res.status_code}): {res.text}")
    return False

merchants, current_sha = load_merchants()

# 1. استمارة تسجيل تاجر جديد
with st.form("register_merchant"):
    st.subheader("➕ تسجيل تاجر جديد")
    c1, c2 = st.columns(2)
    em = c1.text_input("البريد الإلكتروني:", "merchant_dz@gmail.com")
    pw = c2.text_input("كلمة السر:", "123456")
    ph = c1.text_input("رقم الهاتف:", "0655112233")
    pk = c2.selectbox("الباقة:", ["29k", "45k", "65k"])
    if st.form_submit_button("💾 حفظ التاجر فوراً"):
        if current_sha:
            merchants.append({
                "email": em.strip(),
                "password": pw.strip(),
                "status": "⏳ في انتظار التفعيل",
                "package": pk,
                "created_at": "2026-11-19",
                "phone": ph.strip()
            })
            if save_merchants(merchants, current_sha):
                st.success("✅ تم حفظ التاجر في GitHub للأبد!")
                st.rerun()

st.divider()

# 2. لوحة تحكم المالك (عرض وتعديل وحذف)
st.subheader(f"📋 قائمة التجار المحفوظة ({len(merchants)})")
if merchants:
    st.dataframe(pd.DataFrame(merchants), use_container_width=True)
    for idx, m in enumerate(merchants):
        with st.container(border=True):
            col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
            col1.write(f"**{m.get('email')}** | 📞 {m.get('phone')}")
            col2.write(f"{m.get('status')} ({m.get('package')})")
            if col3.button("⚡ قبول", key=f"ok_{idx}"):
                merchants[idx]["status"] = "🟢 مفعّل ونشط"
                if save_merchants(merchants, current_sha):
                    st.rerun()
            if col4.button("🗑️ حذف", key=f"del_{idx}"):
                merchants.pop(idx)
                if save_merchants(merchants, current_sha):
                    st.rerun()
else:
    st.info("الجدول فارغ حالياً؛ جرب تسجيل تاجر جديد من الأعلى!")
