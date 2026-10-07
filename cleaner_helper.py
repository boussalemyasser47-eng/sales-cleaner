import pandas as pd

def process_sales_file(uploaded_file):
    """ دالة برمجية مستقلة لقراءة وتطهير ملفات المبيعات وعزل الأخطاء والتكرارات """
    # فحص صيغة الملف وقراءته بالباندا
    if uploaded_file.name.endswith('.csv'):
        df_raw = pd.read_csv(uploaded_file)
    else:
        df_raw = pd.read_excel(uploaded_file)
        
    df = df_raw.copy()
    
    # تنظيف الأسعار وتحويلها لأرقام
    if 'item_price' in df.columns:
        df['item_price'] = df['item_price'].astype(str).str.replace(' DA', '').astype(float)
    
    # عزل وحذف التكرارات بناءً على اسم المنتج
    duplicated_rows = df[df.duplicated(subset=['product_name'], keep='first')].copy()
    df.drop_duplicates(subset=['product_name'], keep='first', inplace=True)
    
    # عزل وحذف الأسعار السالبة والأخطاء
    bad_prices = df[df['item_price'] <= 0].copy()
    df = df[df['item_price'] > 0]
    
    # تنظيف التواريخ الناقصة
    if 'sale_date' in df.columns:
        df['sale_date'] = pd.to_datetime(df['sale_date'], dayfirst=True, format='mixed', errors='coerce')
        df.dropna(subset=['sale_date'], inplace=True)
    
    # حساب الأرباح الإجمالية لكل سطر (السعر × الكمية)
    df['total_row_sales'] = df['item_price'] * df['quantity_sold']
    if not duplicated_rows.empty and 'item_price' in duplicated_rows.columns:
        duplicated_rows['total_row_sales'] = duplicated_rows['item_price'] * duplicated_rows['quantity_sold']
        
    return df_raw, df, duplicated_rows, bad_prices
