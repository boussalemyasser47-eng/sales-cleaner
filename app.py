import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="صانع الفواتير السريع للمتاجر", layout="centered")

st.title("📄 صانع الفواتير الرقمية السريع للمتاجر الجزائرية 🇩🇿")
st.write("اصنع فاتورة احترافية لزبونك في أقل من دقيقة وأبهر عملاءك!")

# 🏪 1. معلومات المتجر الأساسية
st.subheader("🏪 معلومات متجرك:")
shop_name = st.text_input("اسم متجرك الإلكتروني (مثال: DZ Store):", "متجري الإلكتروني")

# 👤 2. معلومات الزبون
st.subheader("👤 معلومات الزبون:")
col_c1, col_c2 = st.columns(2)
with col_c1:
    customer_name = st.text_input("اسم الزبون الكامل:")
with col_c2:
    customer_phone = st.text_input("رقم هاتف الزبون:")

customer_address = st.text_input("عنوان التوصيل والولاية:")

# 📦 3. تفاصيل السلعة والحسابات الرياضية بالباندا
st.subheader("📦 تفاصيل السلعة المبيعة:")
col_p1, col_p2, col_p3 = st.columns(3)

with col_p1:
    product_name = st.text_input("اسم المنتج:")
with col_p2:
    price = st.number_input("سعر القطعة بالدينار (DA):", min_value=0, value=1200)
with col_p3:
    quantity = st.number_input("الكمية المباعة:", min_value=1, value=1)

# شحن وتوصيل
shipping_cost = st.number_input("مصاريف الشحن والتوصيل (DA):", min_value=0, value=600)

# ⚡ 4. توليد الفاتورة بضغطة زر
if st.button("إصدار الفاتورة الاحترافية"):
    if not customer_name or not product_name:
        st.error("❌ من فضلك أدخل اسم الزبون واسم المنتج لإصدار الفاتورة!")
    else:
        # حساب الرياضيات بالبايثون
        product_total = price * quantity
        final_total = product_total + shipping_cost
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # 🎨 تصميم شكل الفاتورة التي ستظهر للتاجر
        st.success("✅ تم توليد الفاتورة بنجاح! انسخ النص بالأسفل وأرسله لزبونك:")
        
        invoice_text = f"""
        ===================================
        🧾 فاتورة شراء من: {shop_name} 🧾
        ===================================
        📅 التاريخ: {current_date}
        
        👤 معلومات الزبون:
        -----------------
        - الاسم: {customer_name}
        - الهاتف: {customer_phone}
        - العنوان: {customer_address}
        
        📦 تفاصيل الطلبية:
        -----------------
        - المنتج: {product_name}
        - السعر: {price:,} DA
        - الكمية: {quantity}
        
        -----------------
        💰 المجموع الفرعي: {product_total:,} DA
        🚚 مصاريف الشحن: {shipping_cost:,} DA
        📊 الإجمالي الصافي للدفع: {final_total:,} DA
        
        ===================================
        🙏 شكراً لثقتكم بنا وتسوقكم من متجرنا! 🙏
        ===================================
        """
        
        # عرض الفاتورة داخل صندوق نظيف لكي يقوم التاجر بنسخها بضغطة زر
        st.code(invoice_text, language="text")
        st.info("💡 يمكن للتاجر الضغط على زر النسخ في زاوية الصندوق العلوي وإرسالها فوراً للزبون عبر فيسبوك أو إنستغرام!")

