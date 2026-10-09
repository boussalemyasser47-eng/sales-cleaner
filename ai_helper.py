# ========================================================
# الجزء الأول: هندسة وتوسيع شريط الكتابة ومنع اختلاط النص (ai_helper.py)
# ========================================================
import streamlit as st
import pandas as pd
import sqlite3

def render_sidebar_helper():
    st.sidebar.markdown("---")
    
    # 1. حقن حزمة CSS الأسطورية لإصلاح شريط الكتابة وتجميله كلياً
    st.sidebar.markdown("""
        <style>
        /* التنسيق المستقر والإطار المشع الفيروزي لزر التفعيل الحالي في صورتك */
        div[data-testid="stCheckbox"] {
            background-color: #0c0c14 !important;
            border: 2px solid #00fff0 !important;
            border-radius: 12px !important;
            padding: 15px !important;
            text-align: right !important;
            box-shadow: 0px 0px 20px #00fff0, inset 0px 0px 10px rgba(0, 255, 240, 0.3) !important;
        }
        
        /* لوحة المساعد السيبرانية الأسطورية المتطابقة تماماً مع لقطة شاشتك */
        .ai-cyber-legendary-panel {
            background: linear-gradient(135deg, #090911 0%, #111124 100%);
            border-right: 4px solid #00fff0;
            border-left: 1px solid rgba(0, 255, 240, 0.2);
            border-radius: 12px;
            padding: 18px;
            text-align: right;
            box-shadow: 0px 8px 25px rgba(0, 0, 0, 0.4);
            margin-top: 15px;
            margin-bottom: 15px;
            direction: rtl;
        }
        
        .ai-pulse-status {
            display: inline-flex;
            align-items: center;
            background: rgba(0, 255, 240, 0.1);
            border: 1px solid #00fff0;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 11px;
            color: #00fff0;
            font-family: 'Cairo', sans-serif;
            margin-bottom: 10px;
            font-weight: bold;
        }
        .pulse-dot {
            width: 8px;
            height: 8px;
            background-color: #00fff0;
            border-radius: 50%;
            margin-left: 6px;
            box-shadow: 0 0 10px #00fff0;
            animation: pulse-animation 1.5s infinite alternate;
        }
        @keyframes pulse-animation {
            0% { opacity: 0.4; transform: scale(0.9); }
            100% { opacity: 1; transform: scale(1.2); box-shadow: 0 0 15px #00fff0; }
        }
        
        .ai-title-text { color: #00fff0; font-family: 'Cairo', sans-serif; font-size: 16px; margin: 5px 0 8px 0; font-weight: bold; }
        .ai-body-text { color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; line-height: 1.6; margin: 0; }
        .ai-pink-neon { color: #ff00ff; font-weight: bold; }
        
        /* 🚨 تحسين وتفكيك شريط الكتابة: معالجة شاملة لمنع اختلاط الكلمات واختفائها */
        div[data-testid="stTextInput"] input {
            border: 2px solid #00fff0 !important;
            background-color: #07070d !important;
            color: #ffffff !important;
            border-radius: 10px !important;
            padding: 14px 16px !important; /* زيادة المساحة الداخلية لحماية الحروف من الاختناق */
            font-family: 'Cairo', sans-serif !important;
            font-size: 14px !important;
            text-align: right !important;
            direction: rtl !important;
            box-shadow: 0px 0px 12px rgba(0, 255, 240, 0.2) !important;
            transition: all 0.4s ease-in-out !important;
        }
        
        /* إخفاء نص التلميح الإنجليزي المعطل (Press Enter to apply) تماماً لمنع التشوه */
        div[data-testid="stTextInput"] p {
            display: none !important;
        }
        
        /* تحويل الإطار إلى توهج أرجواني سيبراني خلاب ومحترف بمجرد وضع الفأرة أو بدء الكتابة */
        div[data-testid="stTextInput"] input:focus {
            border-color: #ff00ff !important;
            box-shadow: 0px 0px 22px #ff00ff, inset 0px 0px 6px rgba(255, 0, 255, 0.4) !important;
            transform: scale(1.01) !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # 2. زر تشغيل المساعد ذو التظهير الميكانيكي المستقر والآمن
    ai_activate = st.sidebar.checkbox("تفعيل المساعد الأسطوري الخارق 🔘", key="legendary_v8_pro_activate")
    
    if ai_activate:
        st.sidebar.markdown("""
            <div class="ai-cyber-legendary-panel">
                <div class="ai-pulse-status"><span class="pulse-dot"></span>NEXUS AI: ONLINE</div>
                <h3 class="ai-title-text">🔮 المستشار اللاسلكي المطور</h3>
                <p class="ai-body-text">مرحباً بك مجدداً يا <span class="ai-pink-neon">مدير محمد</span>! خلايا النظام مستقرة ومربوطة بـ v4 بنجاح. اطرح أي سؤال مالي أو سلعي تالياً لبدء الجرد الفوري.</p>
            </div>
        """, unsafe_allow_html=True)

        # شريط الأسئلة الاحترافي الجديد الخالي تماماً من تداخل النصوص والكلمات الإنجليزية
        user_query = st.sidebar.text_input("💬 اكتب سؤالك للمساعد هنا:", key="cyber_v8_pro_query")
        
        if user_query:
            evaluate_logic_response(user_query)
# ========================================================
# الجزء الثاني: بطاقات التقارير النيونية المنفصلة بـ DA (ai_helper.py)
# ========================================================

def evaluate_logic_response(query):
    # الاتصال المباشر بقاعدة البيانات الرابعة v4 لقراءة سجلات المتجر الحقيقية
    conn = sqlite3.connect("invoices_master_v4.db")
    
    # أ. جرد وحساب الأرباح وعرضها داخل بطاقة نيونية بنفسجية مشعة منفصلة
    if "ربح" in query or "مبيعات" in query or "حساب" in query:
        df_sales = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conn)
        total_da = df_sales['final_total'].sum()
        count_inv = len(df_sales)
        st.sidebar.markdown(f"""
            <div style="background: linear-gradient(135deg, #0d0614 0%, #1c092b 100%); border: 1px solid #ff00ff; box-shadow: 0 0 15px #ff00ff, inset 0 0 5px rgba(255, 0, 255, 0.3); padding: 15px; border-radius: 10px; text-align: right; direction: rtl; margin-top: 12px;">
                <h4 style="color: #ff00ff; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0; text-shadow: 0 0 5px #ff00ff;">📊 تقرير الخزينة الحقيقي:</h4>
                <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.5;">بناءً على <b>{count_inv} فاتورة صادرة</b>، مداخيل المتجر الصافية هي:<br><span style="color: #00fff0; font-weight: bold; font-size: 15px; text-shadow: 0 0 5px #00fff0;">{total_da:,.2f} DA</span></p>
            </div>
        """, unsafe_allow_html=True)
        
    # ب. جرد كميات قطع المستودع وعرضها داخل بطاقة نيونية فيروزية منفصلة
    elif "مخزن" in query or "سلع" in query or "قطع" in query:
        df_stock = pd.read_sql("SELECT SUM(available_qty) as total_qty FROM store_stock", conn)
        try: qty = int(df_stock['total_qty'].values) if not df_stock.empty else 0
        except: qty = 0
        st.sidebar.markdown(f"""
            <div style="background: linear-gradient(135deg, #051214 0%, #09262b 100%); border: 1px solid #00fff0; box-shadow: 0 0 15px #00fff0, inset 0 0 5px rgba(0, 255, 240, 0.3); padding: 15px; border-radius: 10px; text-align: right; direction: rtl; margin-top: 12px;">
                <h4 style="color: #00fff0; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0; text-shadow: 0 0 5px #00fff0;">📦 جرد مستودع الـ COD:</h4>
                <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.5;">متوفر حالياً في المخزن السلعي جاهزاً للشحن والتوصيل:<br><span style="color: #ff00ff; font-weight: bold; font-size: 15px; text-shadow: 0 0 5px #ff00ff;">{qty} قطعة ونظام</span></p>
            </div>
        """, unsafe_allow_html=True)
        
    # ج. الإجابة الذكية الافتراضية
    else:
        st.sidebar.markdown("""
            <div style="border-right: 3px solid #ffffff; padding-right: 10px; margin-top: 12px; text-align: right; direction: rtl;">
                <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 12.5px; margin: 0;">الأنظمة السيبرانية v4 متصلة بكفاءة يا مدير محمد. اسألني عن الفواتير أو السلع لاستدعاء بطاقات جرد الأرقام المنطقية الفورية.</p>
            </div>
        """, unsafe_allow_html=True)
    conn.close()

def render_marketing_hub():
    pass

def render_data_insights(conn):
    pass
