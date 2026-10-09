import streamlit as st
import pandas as pd
import sqlite3

def render_sidebar_helper():
    st.sidebar.markdown("---")
    
    # حقن شفرة النيون وحظر التداخلات بشكل صارم ومضمون
    st.sidebar.markdown("""
        <style>
        /* تنسيق زر التفعيل الفيروزي الحالي الخاص بك دون أي تغيير */
        div[data-testid="stCheckbox"] {
            background: linear-gradient(135deg, #0a0a12 0%, #101020 100%) !important;
            border: 2px solid #00fff0 !important;
            border-radius: 14px !important;
            padding: 14px !important;
            text-align: right !important;
            box-shadow: 0px 0px 18px rgba(0, 255, 240, 0.4), inset 0px 0px 8px rgba(0, 255, 240, 0.2) !important;
        }
        
        /* تصميم صندوق الترحيب الداخلي المنسق بدقة */
        .ai-cyber-legendary-panel {
            background: linear-gradient(135deg, #090911 0%, #111124 100%);
            border-right: 4px solid #00fff0;
            border-left: 1px solid rgba(0, 255, 240, 0.2);
            border-radius: 12px;
            padding: 18px;
            text-align: right;
            direction: rtl;
        }
        
        /* تحسين وتجميل شكل شريط كتابة السؤال ليصبح أسطورياً ومحترفاً بالكامل */
        div[data-testid="stTextInput"] input {
            border: 2px solid #00fff0 !important;
            background-color: #07070d !important;
            color: #ffffff !important;
            border-radius: 10px !important;
            padding: 14px 16px !important;
            font-family: 'Cairo', sans-serif !important;
            text-align: right !important;
            direction: rtl !important;
            box-shadow: 0px 0px 12px rgba(0, 255, 240, 0.2) !important;
        }
        
        /* 🌌 حظر التلميحات وتعليمات الإدخال وكافة عناصر التداخل النصي نهائياً */
        div[data-testid="stTextInput"] p, 
        div[data-testid="stTextInput"] small, 
        div[data-testid="stTextInput"] label,
        div[data-testid="stTextInput"] [data-testid="stWidgetInstructions"],
        div[data-testid="stTextInput"] div,
        .st-emotion-cache-16idsys p,
        .st-emotion-cache-q3uqly p {
            display: none !important;
            opacity: 0 !important;
            visibility: hidden !important;
            height: 0px !important;
            margin: 0px !important;
            padding: 0px !important;
        }
        
        /* تأثير التوهج الأرجواني عند النقر والكتابة */
        div[data-testid="stTextInput"] input:focus {
            border-color: #ff00ff !important;
            box-shadow: 0px 0px 22px #ff00ff, inset 0px 0px 6px rgba(255, 0, 255, 0.4) !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    ai_activate = st.sidebar.checkbox("تفعيل المساعد الأسطوري الخارق 🔘", key="legendary_v7_pro_activate")
    
    if ai_activate:
        st.sidebar.markdown("""
            <div class="ai-cyber-legendary-panel">
                <h3 style="color:#00fff0; font-family:'Cairo'; font-size:16px; margin:0;">🔮 المستشار اللاسلكي المطور</h3>
                <p style="color:#fff; font-family:'Cairo'; font-size:13px; margin:5px 0 0 0;">مرحباً بك مجدداً يا مدير محمد! خلايا النظام مستقرة ومربوطة بـ v4 بنجاح.</p>
            </div>
        """, unsafe_allow_html=True)

        user_query = st.sidebar.text_input("💬 اكتب سؤالك للمساعد هنا:", key="cyber_v7_pro_query")
        
        if user_query:
            evaluate_logic_response(user_query)

def evaluate_logic_response(query):
    conn = sqlite3.connect("invoices_master_v4.db")
    if "ربح" in query or "مبيعات" in query or "حساب" in query:
        df_sales = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conn)
        total_da = df_sales['final_total'].sum()
        st.sidebar.write(f"إجمالي الأرباح: {total_da:,.2f} DA")
    conn.close()

def render_marketing_hub():
    pass

def render_data_insights(conn):
    pass
