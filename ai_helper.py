# ========================================================
# الجزء الأول: واجهة المساعد الذكي المركزية في وسط الصفحة (ai_helper.py)
# ========================================================
import streamlit as st
import pandas as pd
import sqlite3

# نترك دالة الشريط الجانبي فارغة تماماً بناءً على طلبك لكي لا يظهر المساعد في الجنب
def render_sidebar_helper():
    pass

def render_marketing_hub():
    # 1. تصميم سيبراني خارق وممتد لـ صندوق الترحيب في منتصف الشاشة الرئيسية
    st.markdown("""
        <style>
        .ai-main-center-box {
            background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%);
            border: 2px solid #00ffcc;
            border-radius: 15px;
            padding: 25px;
            text-align: right;
            box-shadow: 0px 0px 25px rgba(0, 255, 204, 0.4);
            margin-top: 20px;
            margin-bottom: 25px;
            direction: rtl;
        }
        .ai-main-title { color: #00ffcc; font-family: 'Cairo', sans-serif; font-size: 26px; margin-bottom: 10px; font-weight: bold; }
        .ai-main-text { font-family: 'Cairo', sans-serif; color: #ffffff; font-size: 16px; line-height: 1.8; }
        .ai-main-highlight { color: #ff00ff; font-weight: bold; }
        </style>
        
        <div class="ai-main-center-box">
            <h2 class="ai-main-title">🤖 المساعد السيبراني المركزي لـ COD الجزائر</h2>
            <p class="ai-main-text">✨ <span class="ai-main-highlight">مرحباً بك يا مدير محمد!</span> لقد تم نقل المساعد الذكي إلى الواجهة الكبرى بنجاح. أنا هنا متصلة بقواعد بيانات v4 بشكل مباشر، اكتب سؤالك في الشريط أدناه لتحليل الأرباح وجرد المستودع منطقياً.</p>
        </div>
    """, unsafe_allow_html=True)

    # 2. شريط استقبال الأسئلة المركزي الممتد بعرض الصفحة
    user_query = st.text_input("💬 اسأل مساعدتك الذكية الآن (مثال: أرباح المتجر، جرد السلع):", key="main_center_ai_query")
    
    if user_query:
        evaluate_logic_response(user_query)
# ========================================================
# الجزء الثاني: المحرك المنطقي وقراءة الحسابات في وسط الصفحة (ai_helper.py)
# ========================================================

def evaluate_logic_response(query):
    # الاتصال المباشر بقاعدة البيانات الرابعة v4 لقراءة الحسابات الحقيقية
    conn = sqlite3.connect("invoices_master_v4.db")
    
    st.markdown("---")
    
    # أ. جرد وحساب مداخيل وأرباح المتجر الإلكتروني وعرضها في المنتصف
    if "ربح" in query or "مبيعات" in query or "حساب" in query:
        df_sales = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conn)
        total_da = df_sales['final_total'].sum()
        count_inv = len(df_sales)
        st.markdown(f"""
            <div style="background: rgba(255, 0, 255, 0.05); border-right: 5px solid #ff00ff; padding: 15px; border-radius: 8px; text-align: right; direction: rtl;">
                <h3 style="color: #ff00ff; font-family: 'Cairo', sans-serif; font-size: 18px; margin: 0 0 8px 0;">📊 تقرير الحسابات الصافي للمتجر:</h3>
                <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 15px; margin: 0;">بناءً على <b>{count_inv} فاتورة صادرة</b>، إجمالي المداخيل المحققة حالياً هو: <span style="color: #00ffcc; font-weight: bold; font-size: 18px;">{total_da:,.2f} DA</span></p>
            </div>
        """, unsafe_allow_html=True)
        
    # ب. جرد كميات قطع المخزن السلعي للمستودع وعرضها في المنتصف
    elif "مخزن" in query or "سلع" in query or "قطع" in query:
        df_stock = pd.read_sql("SELECT SUM(available_qty) as total_qty FROM store_stock", conn)
        try: qty = int(df_stock['total_qty'].values) if not df_stock.empty else 0
        except: qty = 0
        st.markdown(f"""
            <div style="background: rgba(0, 255, 204, 0.05); border-right: 5px solid #00ffcc; padding: 15px; border-radius: 8px; text-align: right; direction: rtl;">
                <h3 style="color: #00ffcc; font-family: 'Cairo', sans-serif; font-size: 18px; margin: 0 0 8px 0;">📦 تقرير جرد المستودع الفوري:</h3>
                <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 15px; margin: 0;">متوفر لديك حالياً <span style="color: #ff00ff; font-weight: bold; font-size: 18px;">{qty} قطعة</span> داخل المخزن السلعي جاهزة للتسليم والتوصيل الفوري للولايات.</p>
            </div>
        """, unsafe_allow_html=True)
        
    # ج. الإجابة الذكية الافتراضية الممتدة
    else:
        st.markdown("""
            <div style="background: rgba(255, 255, 255, 0.05); border-right: 5px solid #ffffff; padding: 15px; border-radius: 8px; text-align: right; direction: rtl;">
                <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0;">أنا متصلة بقواعد بيانات v4 بنجاح يا مدير محمد وجاهزة لإعطائك إحصائيات منطقية، اسألني عن الفواتير أو المخزون في أي وقت.</p>
            </div>
        """, unsafe_allow_html=True)
    conn.close()

# دالة حجز المكان للميزة الثالثة لمنع أي خطأ تعطل في كودك الرئيسي
def render_data_insights(conn):
    pass
