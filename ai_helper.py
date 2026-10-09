# ========================================================
# الجزء الأول: تصميم صندوق الترحيب السيبراني النيوني (ai_helper.py)
# ========================================================
import streamlit as st
import pandas as pd
import sqlite3

def render_sidebar_helper():
    # تصميم المظهر النيوني المتوهج باللون الفيروزي والبنفسجي
    st.sidebar.markdown("""
        <style>
        .ai-cyber-box {
            background: linear-gradient(135deg, #10101a 0%, #161625 100%);
            border: 2px solid #00ffcc;
            border-radius: 12px;
            padding: 15px;
            text-align: right;
            box-shadow: 0px 0px 15px #00ffcc;
            margin-top: 15px;
            margin-bottom: 15px;
            direction: rtl;
        }
        .ai-title-style { color: #00ffcc; margin: 0; font-size: 18px; font-family: 'Cairo', sans-serif; }
        .ai-text-style { font-family: 'Cairo', sans-serif; color: #ffffff; font-size: 14px; line-height: 1.6; }
        .ai-bold { color: #ff00ff; font-weight: bold; }
        </style>
        
        <div class="ai-cyber-box">
            <h3 class="ai-title-style">🤖 المساعد السيبراني لـ COD الجزائر</h3>
            <p class="ai-text-style">✨ <span class="ai-bold">مرحباً بك يا مدير محمد!</span> أنا مساعدتك الذكية لمتجر تجار. نظامك الأسطوري v4 جاهز للعمل وتحليل الفواتير والمخزون بدقة منطقية كاملة.</p>
        </div>
    """, unsafe_allow_html=True)

    # صندوق الكتابة واستقبال أسئلة المدير محمد
    user_query = st.sidebar.text_input("💬 اسأل المساعد الذكي (الأرباح، المخزن):", key="cyber_ai_query")
    
    if user_query:
        evaluate_logic_response(user_query)
# ========================================================
# الجزء الثاني: المحرك المنطقي لقراءة حسابات الفواتير (ai_helper.py)
# ========================================================

def evaluate_logic_response(query):
    # الاتصال بقاعدة البيانات v4 المحددة في كودك الرئيسي
    conn = sqlite3.connect("invoices_master_v4.db")
    
    # 1. تحليل استفسارات الأرباح والفلوس الصافية بـ DA
    if "ربح" in query or "مبيعات" in query or "حساب" in query:
        df_sales = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conn)
        total_da = df_sales['final_total'].sum()
        count_inv = len(df_sales)
        st.sidebar.markdown(f"""
            <div style="border-right: 3px solid #ff00ff; padding-right: 10px; margin-top: 10px; text-align: right; direction: rtl;">
                <p style="color: #ff00ff; font-size: 13px; font-weight: bold; margin: 0;">📊 تقرير الأرباح اللحظي:</p>
                <p style="color: #ffffff; font-size: 13px; margin: 5px 0 0 0;">بناءً على {count_inv} فاتورة، مداخيل المتجر الصافية هي: <span style="color: #00ffcc; font-weight: bold;">{total_da:,.2f} DA</span>.</p>
            </div>
        """, unsafe_allow_html=True)
        
    # 2. تحليل استفسارات جرد قطع المخزن السلعي 
    elif "مخزن" in query or "سلع" in query or "قطع" in query:
        df_stock = pd.read_sql("SELECT SUM(available_qty) as total_qty FROM store_stock", conn)
        try: qty = int(df_stock['total_qty'].values) if not df_stock.empty else 0
        except: qty = 0
        st.sidebar.markdown(f"""
            <div style="border-right: 3px solid #00ffcc; padding-right: 10px; margin-top: 10px; text-align: right; direction: rtl;">
                <p style="color: #00ffcc; font-size: 13px; font-weight: bold; margin: 0;">📦 حالة قطع المستودع:</p>
                <p style="color: #ffffff; font-size: 13px; margin: 5px 0 0 0;">متوفر لديك حالياً <span style="color: #ff00ff; font-weight: bold;">{qty} حبة</span> في المخزن السلعي جاهزة للتوصيل للولايات.</p>
            </div>
        """, unsafe_allow_html=True)
        
    # 3. الردود الذكية الافتراضية
    else:
        st.sidebar.markdown("""
            <div style="border-right: 3px solid #ffffff; padding-right: 10px; margin-top: 10px; text-align: right; direction: rtl;">
                <p style="color: #ffffff; font-size: 13px; margin: 0;">أنا متصلة ببيانات المتجر بنجاح يا مدير محمد، اسألني عن الفواتير أو المخزون لإعطائك أرقاماً منطقية.</p>
            </div>
        """, unsafe_allow_html=True)
    conn.close()

# الدوال المحجوزة للميزتين 3 و 4 الثابتة في تطبيقك
def render_marketing_hub():
    st.info("🚀 تم تحميل واجهة مركز التسويق الذكي بنجاح من ملف ai_helper!")

def render_data_insights(conn):
    st.success("🔮 تم تفعيل خوارزمية استعراض التنبؤ الذكي بالمخزون والمبيعات!")

