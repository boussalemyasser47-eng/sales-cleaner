# ========================================================
# الجزء الأول: زر التفعيل السيبراني الأسطوري والمتحرك (ai_helper.py)
# ========================================================
import streamlit as st
import pandas as pd
import sqlite3

def render_sidebar_helper():
    st.sidebar.markdown("---")
    
    # 1. حقن كود CSS أسطوري لتحويل الزر إلى تصميم سيبراني متوهج ومتحرك
    st.sidebar.markdown("""
        <style>
        /* تصميم مخصص لإخفاء صندوق الفحص التقليدي وجعله بطاقة نيون تفاعلية */
        div[data-testid="stCheckbox"] {
            background: linear-gradient(45deg, #10101a, #1a1a3a);
            border: 2px solid #00ffcc;
            border-radius: 10px;
            padding: 12px;
            box-shadow: 0 0 10px #00ffcc, inset 0 0 5px #00ffcc;
            transition: all 0.4s ease-in-out;
            animation: pulse-glow 2s infinite alternate;
        }
        div[data-testid="stCheckbox"]:hover {
            border-color: #ff00ff;
            box-shadow: 0 0 20px #ff00ff, inset 0 0 10px #ff00ff;
            transform: scale(1.02);
            cursor: pointer;
        }
        /* أنيميشن التوهج النبضي الأسطوري */
        @keyframes pulse-glow {
            0% { box-shadow: 0 0 8px #00ffcc; }
            100% { box-shadow: 0 0 18px #00ffcc, 0 0 25px #00ffcc; }
        }
        
        /* تنسيق صندوق الترحيب الداخلي المشرق */
        .ai-legendary-box {
            background: rgba(16, 16, 26, 0.95);
            border-right: 4px solid #ff00ff;
            border-left: 1px solid #00ffcc;
            border-radius: 8px;
            padding: 15px;
            text-align: right;
            box-shadow: 0px 5px 15px rgba(0, 255, 204, 0.2);
            margin-top: 15px;
            margin-bottom: 15px;
            direction: rtl;
        }
        .ai-title { color: #00ffcc; font-family: 'Cairo', sans-serif; font-size: 16px; margin: 0 0 5px 0; font-weight: bold; }
        .ai-text { color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; line-height: 1.6; margin: 0; }
        .ai-highlight { color: #ff00ff; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)
    
    # 2. زر التشغيل الفعلي الذي سيتأثر بالتصميم السيبراني أعلاه
    ai_activate = st.sidebar.checkbox("🤖 تفعيل المساعد الأسطوري الخارق", key="activate_legendary_ai")
    
    if ai_activate:
        # ظهور رسالة الترحيب الأسطورية للمدير محمد فور تفعيل الزر المتوهج
        st.sidebar.markdown("""
            <div class="ai-legendary-box">
                <h3 class="ai-title">⚡ النظام الذكي متصل بنجاح</h3>
                <p class="ai-text">أهلاً بك يا <span class="ai-highlight">مدير محمد</span>! شريكك الرقمي جاهز للتحليل المنطقي الفوري، اكتب استفسارك في الشريط أدناه.</p>
            </div>
        """, unsafe_allow_html=True)

        # شريط كتابة السؤال المنسق بدقة
        user_query = st.sidebar.text_input("💬 اكتب سؤالك للمساعد هنا:", key="cyber_legendary_query")
        
        if user_query:
            evaluate_logic_response(user_query)
# ========================================================
# الجزء الثاني: معالجة الردود المنطقية وقواعد البيانات (ai_helper.py)
# ========================================================

def evaluate_logic_response(query):
    # الاتصال المباشر بقاعدة البيانات الرابعة v4 لقراءة الحسابات الحقيقية
    conn = sqlite3.connect("invoices_master_v4.db")
    
    # أ. جرد وحساب مداخيل وأرباح المتجر الإلكتروني
    if "ربح" in query or "مبيعات" in query or "حساب" in query:
        df_sales = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conn)
        total_da = df_sales['final_total'].sum()
        count_inv = len(df_sales)
        st.sidebar.markdown(f"""
            <div style="border-right: 3px solid #ff00ff; padding-right: 10px; margin-top: 12px; text-align: right; direction: rtl;">
                <p style="color: #ff00ff; font-size: 13px; font-weight: bold; margin: 0;">📊 تقرير الحسابات الصافي:</p>
                <p style="color: #ffffff; font-size: 13px; margin: 4px 0 0 0;">إجمالي المداخيل بناءً على {count_inv} فاتورة صادرة هو: <span style="color: #00ffcc; font-weight: bold;">{total_da:,.2f} DA</span>.</p>
            </div>
        """, unsafe_allow_html=True)
        
    # ب. جرد كميات قطع المخزن السلعي للمستودع
    elif "مخزن" in query or "سلع" in query or "قطع" in query:
        df_stock = pd.read_sql("SELECT SUM(available_qty) as total_qty FROM store_stock", conn)
        try: qty = int(df_stock['total_qty'].values) if not df_stock.empty else 0
        except: qty = 0
        st.sidebar.markdown(f"""
            <div style="border-right: 3px solid #00ffcc; padding-right: 10px; margin-top: 12px; text-align: right; direction: rtl;">
                <p style="color: #00ffcc; font-size: 13px; font-weight: bold; margin: 0;">📦 حالة قطع المستودع:</p>
                <p style="color: #ffffff; font-size: 13px; margin: 4px 0 0 0;">متوفر لديك حالياً <span style="color: #ff00ff; font-weight: bold;">{qty} حبة</span> في المخزن السلعي شاشتك جاهزة للشحن والتوصيل للولايات.</p>
            </div>
        """, unsafe_allow_html=True)
        
    # ج. الإجابة الذكية الافتراضية
    else:
        st.sidebar.markdown("""
            <div style="border-right: 3px solid #ffffff; padding-right: 10px; margin-top: 12px; text-align: right; direction: rtl;">
                <p style="color: #ffffff; font-size: 13px; margin: 0;">أنا متصلة بقواعد بيانات v4 بنجاح يا مدير محمد، اسألني عن الفواتير أو المخزون لإعطائك أرقاماً منطقية.</p>
            </div>
        """, unsafe_allow_html=True)
    conn.close()

# ضمان حجز مكان الدوال الأخرى الثابتة في تطبيقك لمنع أي خطأ تعطل
def render_marketing_hub():
    pass

def render_data_insights(conn):
    pass


