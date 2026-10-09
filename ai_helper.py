# ========================================================
# الجزء الأول: زر التشغيل التفاعلي وواجهة المساعد (ai_helper.py)
# ========================================================
import streamlit as st
import pandas as pd
import sqlite3

def render_sidebar_helper():
    st.sidebar.markdown("---")
    
    # 1. زر تشغيل المساعد الذكي بشكل أسطوري
    # قمنا باستخدام عنصر checkbox بتصميم زر أو يمكنك الضغط عليه لتفعيل الحالة
    ai_activate = st.sidebar.checkbox("🤖 تشغيل المساعد السيبراني الفوري", key="activate_ai_system")
    
    if ai_activate:
        # تصميم صندوق الترحيب النيوني المضيء المتوهج الفيروزي عند التفعيل
        st.sidebar.markdown("""
            <style>
            .ai-cyber-toggle-box {
                background: linear-gradient(135deg, #10101a 0%, #161625 100%);
                border: 2px solid #00ffcc;
                border-radius: 12px;
                padding: 12px;
                text-align: right;
                box-shadow: 0px 0px 15px #00ffcc;
                margin-top: 10px;
                margin-bottom: 10px;
                direction: rtl;
            }
            .ai-title { color: #00ffcc; margin: 0; font-size: 16px; font-family: 'Cairo', sans-serif; }
            .ai-text { font-family: 'Cairo', sans-serif; color: #ffffff; font-size: 13px; line-height: 1.5; }
            .ai-bold { color: #ff00ff; font-weight: bold; }
            </style>
            
            <div class="ai-cyber-toggle-box">
                <h3 class="ai-title">⚡ تم تفعيل المساعد بنجاح</h3>
                <p class="ai-text">مرحباً بك مجدداً يا <span class="ai-bold">مدير محمد</span>! شريط السؤال جاهز في الأسفل لقراءة الحسابات والمخزن منطقياً.</p>
            </div>
        """, unsafe_allow_html=True)

        # 2. شريط كتابة السؤال الذي يظهر فقط عند الضغط والتفعيل
        user_query = st.sidebar.text_input("💬 اكتب سؤالك للمساعد هنا:", key="cyber_toggle_query")
        
        if user_query:
            evaluate_logic_response(user_query)
# ========================================================
# الجزء الثاني: الخوارزمية المنطقية للرد وقراءة قاعدة البيانات (ai_helper.py)
# ========================================================

def evaluate_logic_response(query):
    # الاتصال المباشر بقاعدة بيانات v4 لقراءة الحسابات الحقيقية للمتجر
    conn = sqlite3.connect("invoices_master_v4.db")
    
    # أ. معالجة استفسار الأرباح والمداخيل الكلية
    if "ربح" in query or "مبيعات" in query or "حساب" in query:
        df_sales = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conn)
        total_da = df_sales['final_total'].sum()
        count_inv = len(df_sales)
        st.sidebar.markdown(f"""
            <div style="border-right: 3px solid #ff00ff; padding-right: 10px; margin-top: 10px; text-align: right; direction: rtl;">
                <p style="color: #ff00ff; font-size: 13px; font-weight: bold; margin: 0;">📊 تقرير الأرباح:</p>
                <p style="color: #ffffff; font-size: 13px; margin: 5px 0 0 0;">إجمالي مداخيل المتجر الصافية بناءً على {count_inv} فاتورة هي: <span style="color: #00ffcc; font-weight: bold;">{total_da:,.2f} DA</span>.</p>
            </div>
        """, unsafe_allow_html=True)
        
    # ب. معالجة استفسار جرد وفحص قطع المستودع
    elif "مخزن" in query or "سلع" in query or "قطع" in query:
        df_stock = pd.read_sql("SELECT SUM(available_qty) as total_qty FROM store_stock", conn)
        try: qty = int(df_stock['total_qty'].values) if not df_stock.empty else 0
        except: qty = 0
        st.sidebar.markdown(f"""
            <div style="border-right: 3px solid #00ffcc; padding-right: 10px; margin-top: 10px; text-align: right; direction: rtl;">
                <p style="color: #00ffcc; font-size: 13px; font-weight: bold; margin: 0;">📦 حالة المخزن السلعي:</p>
                <p style="color: #ffffff; font-size: 13px; margin: 5px 0 0 0;">متوفر حالياً <span style="color: #ff00ff; font-weight: bold;">{qty} قطعة</span> جاهزة للتسليم والتوصيل.</p>
            </div>
        """, unsafe_allow_html=True)
        
    # ج. الردود العامة
    else:
        st.sidebar.markdown("""
            <div style="border-right: 3px solid #ffffff; padding-right: 10px; margin-top: 10px; text-align: right; direction: rtl;">
                <p style="color: #ffffff; font-size: 13px; margin: 0;">أنا متصلة بقاعدة البيانات وجاهزة لإعطائك إحصائيات منطقية عن المتجر يا مدير محمد.</p>
            </div>
        """, unsafe_allow_html=True)
    conn.close()

# الدوال الفرعية الثابتة والمحجوزة للميزتين الثالثة والرابعة في مشروعك
def render_marketing_hub():
    pass

def render_data_insights(conn):
    pass
