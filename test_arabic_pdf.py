import streamlit as st
import io
import os
import urllib.request
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

st.set_page_config(page_title="اختبار اللغة العربية في PDF", page_icon="🧪")
st.title("🧪 مختبر فحص وتوليد PDF باللغة العربية")

# 1. دالة معالجة الحروف العربية
def fix_arabic(text):
    if not text:
        return ""
    reshaped_text = arabic_reshaper.reshape(str(text))
    return get_display(reshaped_text)

# 2. تحميل وتسجيل خط عربي قياسي (Amiri-Regular.ttf) مضمون 100% مع ReportLab
FONT_FILE = "Amiri-Regular.ttf"
FONT_URL = "https://raw.githubusercontent.com/google/fonts/main/ofl/amiri/Amiri-Regular.ttf"

st.subheader("1️⃣ حالة الخط العربي:")

try:
    if not os.path.exists(FONT_FILE) or os.path.getsize(FONT_FILE) < 10000:
        st.info("جاري تحميل الخط العربي من السيرفر...")
        urllib.request.urlretrieve(FONT_URL, FONT_FILE)
    
    file_size = os.path.getsize(FONT_FILE)
    st.success(f"✅ تم العثور على ملف الخط بنجاح! الحجم: {file_size:,} بايت")
    
    pdfmetrics.registerFont(TTFont('CustomArabic', FONT_FILE))
    st.success("✅ تم تسجيل الخط داخل مكتبة ReportLab بنجاح!")
    FONT_READY = True
except Exception as e:
    st.error(f"❌ حدث خطأ أثناء تحميل أو تسجيل الخط: {e}")
    FONT_READY = False

st.markdown("---")
st.subheader("2️⃣ تجربة توليد الفاتورة:")

test_name = st.text_input("أدخل اسماً باللغة العربية:", "محمد الأمين الجزائري")
test_city = st.text_input("أدخل الولاية:", "الجزائر العاصمة - باب الزوار")

if st.button("📄 توليد وتحميل ملف PDF التجريبي"):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    font_to_use = 'CustomArabic' if FONT_READY else 'Helvetica'
    
    c.setFont(font_to_use, 18)
    c.drawString(200, 750, fix_arabic("فاتورة تجريبية - منصة نيكسوس"))
    
    c.setFont(font_to_use, 14)
    c.drawString(100, 700, fix_arabic(f"اسم الزبون: {test_name}"))
    c.drawString(100, 670, fix_arabic(f"العنوان: {test_city}"))
    c.drawString(100, 640, fix_arabic("المبلغ الإجمالي: 3500 دج"))
    
    c.save()
    buffer.seek(0)
    
    st.download_button(
        label="📥 اضغط هنا لتحميل الفاتورة التجريبية",
        data=buffer.getvalue(),
        file_name="test_arabic_success.pdf",
        mime="application/pdf"
    )
