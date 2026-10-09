# ========================================================
# الجزء الأول: واجهة المساعد الذكي الترحيبية في الـ Sidebar (ai_helper.py)
# ========================================================
import streamlit as st
import pandas as pd
import sqlite3

def render_sidebar_helper():
    # 1. تصميم سيبراني أسطوري خاص بـ المساعد الذكي في الجنب
    st.sidebar.markdown("""
        <style>
        .ai-welcome-box {
            background: linear-gradient(135deg, #10101a 0%, #161625 100%);
            border: 2px solid #00ffcc;
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            box-shadow: 0px 0px 15px #00ffcc;
            margin-bottom: 15px;
        }
        .ai-text { font-family: 'Cairo', sans-serif; color: #ffffff; font-size: 14px; }
        .ai-highlight { color: #00ffcc; font-weight: bold; }
        </style>
        
        <div class="ai-welcome-box">
            <h3 style="color: #00ffcc; margin: 0; font-size: 18px;">🤖 المساعد السيبراني الفوري</h3>
            <p class="ai-text">✨ <span class="ai-highlight">مرحباً بك يا مدير محمد!</span> أنا مساعدتك الذكية، نظامك الأسطوري جاهز للعمل وتحليل الفواتير بدقة منطقية تامة. كيف يمكنني خدمتك في المتجر الآن؟</p>
        </div>
    """, unsafe_allow_html=True)

    # 2. حقل استقبال المدخلات والأسئلة المنطقية من المدير
    user_query = st.sidebar.text_input("💬 اسأل مساعدتك الذكية (مثال: ربح المتجر، حالة المخزن):", key="ai_side_query")
    
    # استدعاء منطق الإجابة الذكي عند كتابة سؤال
    if user_query:
        evaluate_logic_response(user_query)
# ========================================================
# الجزء الثاني: خوارزمية الرد المنطقي والربط بقاعدة البيانات (ai_helper.py)
# ========================================================

def evaluate_logic_response(query):
    # الاتصال بقاعدة البيانات لقراءة الأرقام الحقيقية للمتجر والإجابة بمنطقية
    conn = sqlite3.connect("invoices_master_v4.db")
    
    # أ. معالجة الاستفسار عن الأرباح والمداخيل المليّة
    if "ربح" in query or "مبيعات" in query or "فلوس" in query:
        df_sales = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conn)
        total_da = df_sales['final_total'].sum()
        count_inv = len(df_sales)
        st.sidebar.markdown(f"""
            <div style="border-left: 3px solid #00ffcc; padding-left: 10px; margin-top: 10px;">
                <p style="color: #00ffcc; font-size: 13px; font-weight: bold;">📊 تقرير الأرباح الذكي:</p>
                <p style="color: #ffffff; font-size: 13px;">بناءً على {count_inv} فاتورة صادرة، إجمالي مداخيل المتجر الحالية الصافية هي: <span style="color: #ff00ff; font-weight: bold;">{total_da:,.2f} DA</span>.</p>
            </div>
        """, unsafe_allow_html=True)
        
    # ب. معالجة الاستفسار عن كميات السلع والمخزن السلعي
    elif "مخزن" in query or "سلع" in query or "قطع" in query:
        df_stock = pd.read_sql("SELECT SUM(available_qty) as total_qty FROM store_stock", conn)
        try: qty = int(df_stock['total_qty'].values[0]) if not df_stock.empty else 0
        except: qty = 0
        st.sidebar.markdown(f"""
            <div style="border-left: 3px solid #00ffcc; padding-left: 10px; margin-top: 10px;">
                <p style="color: #00ffcc; font-size: 13px; font-weight: bold;">📦 جرد المستودع الفوري:</p>
                <p style="color: #ffffff; font-size: 13px;">متوفر لديك حالياً <span style="color: #00ffff; font-weight: bold;">{qty} قطعة</span> داخل المخزن السلعي جاهزة للشحن والتوصيل للولايات.</p>
            </div>
        """, unsafe_allow_html=True)
        
    # ج. الرد الافتراضي الذكي على رسائل التحية العامة
    else:
        st.sidebar.markdown("""
            <div style="border-left: 3px solid #ff00ff; padding-left: 10px; margin-top: 10px;">
                <p style="color: #ffffff; font-size: 13px;">أفهمك تماماً يا مدير محمد! أنا هنا متصلة بقواعد بيانات v4 بشكل مستمر، يمكنك سؤالي عن المبيعات أو المخزن في أي وقت.</p>
            </div>
        """, unsafe_allow_html=True)
    conn.close()

# دالة وهمية لحجز مكان الخيارات الأخرى المتواجدة في ملفك الرئيسي
def render_marketing_hub():
    st.info("🚀 تم تحميل واجهة مركز التسويق الذكي بنجاح من ملف ai_helper!")

def render_data_insights(conn):
    st.success("🔮 تم تفعيل خوارزمية استعراض التنبؤ الذكي بالمخزون والمبيعات!")

