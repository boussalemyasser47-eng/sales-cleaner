import pandas as pd
import streamlit as st

def process_sales_file(uploaded_file):
    """ دالة برمجية مستقلة لقراءة وتطهير ملفات المبيعات وعزل الأخطاء مع قفل النسخة المجانية """
    if uploaded_file.name.endswith('.csv'):
        df_raw = pd.read_csv(uploaded_file)
    else:
        df_raw = pd.read_excel(uploaded_file)
        
    # 🔒 القفل السحري لحماية تعبك وكسب المال:
    if len(df_raw) > 10:
        st.error("⚠️ تنبيه: النسخة المجانية تدعم تجربة ملفات تحتوي على 10 أسطر أو أقل فقط!")
        st.info("📥 لتطهير ملفات متجرك الكبيرة بدون قيود، وحساب أرباح الولايات الـ 58 تلقائياً، تواصل مع المطور في الخاص لتفعيل اشتراكك الفخم عبر BaridiMob.")
        st.stop() # إيقاف تشغيل بقية الكود فوراً لحظر التاجر
        
    df = df_raw.copy()
    
    if 'item_price' in df.columns:
        df['item_price'] = df['item_price'].astype(str).str.replace(' DA', '').astype(float)
    
    duplicated_rows = df[df.duplicated(subset=['product_name'], keep='first')].copy()
    df.drop_duplicates(subset=['product_name'], keep='first', inplace=True)
    
    bad_prices = df[df['item_price'] <= 0].copy()
    df = df[df['item_price'] > 0]
    
    if 'sale_date' in df.columns:
        df['sale_date'] = pd.to_datetime(df['sale_date'], dayfirst=True, format='mixed', errors='coerce')
        df.dropna(subset=['sale_date'], inplace=True)
    
    df['total_row_sales'] = df['item_price'] * df['quantity_sold']
    if not duplicated_rows.empty and 'item_price' in duplicated_rows.columns:
        duplicated_rows['total_row_sales'] = duplicated_rows['item_price'] * duplicated_rows['quantity_sold']
        
    return df_raw, df, duplicated_rows, bad_prices

