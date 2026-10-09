# ========================================================
# الجزء الأول: الأنميشن والانبثاق التلقائي الخلاب للواجهة (ai_helper.py)
# ========================================================
import streamlit as st
import pandas as pd
import sqlite3

def render_sidebar_helper():
    st.sidebar.markdown("---")
    
    # 1. حقن حزمة CSS حركية أسطورية لتوليد تأثير الانبثاق والانسياب التلقائي
    st.sidebar.markdown("""
        <style>
        /* التنسيق الأسطوري لزر التفعيل الفيروزي المطابق لـ لوحة تحكمك */
        div[data-testid="stCheckbox"] {
            background-color: #0c0c14;
            border: 2px solid #00fff0;
            border-radius: 12px;
            padding: 15px;
            text-align: right;
            box-shadow: 0px 0px 20px #00fff0, inset 0px 0px 10px rgba(0, 255, 240, 0.3);
            transition: all 0.4s ease-in-out;
        }
        div[data-testid="stCheckbox"]:hover {
            box-shadow: 0px 0px 30px #00fff0;
            transform: scale(1.02);
            cursor: pointer;
        }
        
        /* خوارزمية الانبثاق التلقائي الخلاب (Legendary Pop-in Animation) */
        .ai-legendary-panel {
            background: linear-gradient(135deg, #0d0d15 0%, #121222 100%);
            border-right: 4px solid #00fff0;
            border-left: 1px solid rgba(0, 255, 240, 0.3);
            border-radius: 10px;
            padding: 18px;
            text-align: right;
            margin-top: 15px;
            margin-bottom: 15px;
            direction: rtl;
            
            /* تفعيل الحركة التلقائية الخلابة عند الضغط */
            animation: cyberPopIn 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
            opacity: 0;
        }
        
        @keyframes cyberPopIn {
            0% { transform: translateY(20px) scale(0.95); opacity: 0; filter: blur(5px); }
            100% { transform: translateY(0) scale(1); opacity: 1; filter: blur(0); }
        }
        
        .ai-legendary-title { color: #00fff0; font-family: 'Cairo', sans-serif; font-size: 16px; margin: 0 0 6px 0; font-weight: bold; text-shadow: 0 0 10px #00fff0; }
        .ai-legendary-text { color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; line-height: 1.6; margin: 0; }
        .ai-neon-pink { color: #ff00ff; font-weight: bold; text-shadow: 0 0 5px #ff00ff; }
        
        /* جعل حقل تدوين الأسئلة يتوهج تدريجياً بشكل محترف */
        div[data-testid="stTextInput"] input {
            border: 1px solid rgba(0, 255, 240, 0.3) !important;
            background-color: #0c0c14 !important;
            color: #ffffff !important;
            transition: all 0.3s ease-in-out;
        }
        div[data-testid="stTextInput"] input:focus {
            border-color: #ff00ff !important;
            box-shadow: 0 0 15px #ff00ff !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # 2. زر التفعيل المتناسق مع الهوية البصرية لمتجرك
    ai_activate = st.sidebar.checkbox("تفعيل المساعد الأسطوري الخارق 🔘", key="legendary_auto_activate")
    
    if ai_activate:
        # ظهور تلقائي خلاب لصندوق الترحيب فور الضغط على الخيار
        st.sidebar.markdown("""
            <div class="ai-legendary-panel">
                <h3 class="ai-legendary-title">⚡ تم دمج وخلق النظام التلقائي</h3>
                <p class="ai-legendary-text">أهلاً بك يا <span class="ai-neon-pink">مدير محمد</span>! خلايا الذكاء الاصطناعي ممتدة وجاهزة للمراقبة، اكتب سؤالك المنطقي في الصندوق المتوهج تالياً.</p>
            </div>
        """, unsafe_allow_html=True)

        # شريط الأسئلة الذكي المطور ذو المظهر الاحترافي
        user_query = st.sidebar.text_input("💬 اكتب سؤالك للمساعد هنا:", key="cyber_auto_query")
        
        if user_query:
            evaluate_logic_response(user_query)
# ========================================================
# الجزء الثاني: المحرك المنطقي وجرد الفواتير والمخزن (ai_helper.py)
# ========================================================

def evaluate_logic_response(query):
    # الاتصال التلقائي بقاعدة البيانات الرابعة v4 لقراءة أرقام المتجر الفعلية
    conn = sqlite3.connect("invoices_master_v4.db")
    
    # أ. جرد وحساب مداخيل وأرباح متجرك الإلكتروني
    if "ربح" in query or "مبيعات" in query or "حساب" in query:
        df_sales = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conn)
        total_da = df_sales['final_total'].sum()
        count_inv = len(df_sales)
        st.sidebar.markdown(f"""
            <div style="border-right: 3px solid #ff00ff; padding-right: 10px; margin-top: 12px; text-align: right; direction: rtl; animation: cyberPopIn 0.4s ease-out;">
                <p style="color: #ff00ff; font-size: 13px; font-weight: bold; margin: 0; text-shadow: 0 0 5px #ff00ff;">📊 تقرير المبيعات المالي:</p>
                <p style="color: #ffffff; font-size: 13px; margin: 4px 0 0 0;">إجمالي المداخيل المستخلصة بناءً على {count_inv} فاتورة هو: <span style="color: #00fff0; font-weight: bold;">{total_da:,.2f} DA</span>.</p>
            </div>
        """, unsafe_allow_html=True)
        
    # ب. معالجة عمليات جرد القطع والسلع المتوفرة بالمستودع الكلي
    elif "مخزن" in query or "سلع" in query or "قطع" in query:
        df_stock = pd.read_sql("SELECT SUM(available_qty) as total_qty FROM store_stock", conn)
        try: qty = int(df_stock['total_qty'].values) if not df_stock.empty else 0
        except: qty = 0
        st.sidebar.markdown(f"""
            <div style="border-right: 3px solid #00fff0; padding-right: 10px; margin-top: 12px; text-align: right; direction: rtl; animation: cyberPopIn 0.4s ease-out;">
                <p style="color: #00fff0; font-size: 13px; font-weight: bold; margin: 0; text-shadow: 0 0 5px #00fff0;">📦 جرد قطع المستودع:</p>
                <p style="color: #ffffff; font-size: 13px; margin: 4px 0 0 0;">متوفر حالياً داخل مخزن المتجر: <span style="color: #ff00ff; font-weight: bold;">{qty} حبة</span> جاهزة للشحن الفوري للولايات.</p>
            </div>
        """, unsafe_allow_html=True)
        
    # ج. الإجابات العامة
    else:
        st.sidebar.markdown("""
            <div style="border-right: 3px solid #ffffff; padding-right: 10px; margin-top: 12px; text-align: right; direction: rtl;">
                <p style="color: #ffffff; font-size: 13px; margin: 0;">أنا متصلة ببيانات الجدول v4 بنجاح يا مدير محمد، اسألني عن الحسابات أو المخزون لإعطائك أرقاماً منطقية.</p>
            </div>
        """, unsafe_allow_html=True)
    conn.close()

# الحفاظ على حجز مكان الدوال الأخرى الثابتة في تطبيقك لمنع أي خطأ تعطل
def render_marketing_hub():
    pass

def render_data_insights(conn):
    pass
