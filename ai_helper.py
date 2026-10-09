# ========================================================
# الجزء الأول: الهندسة البصرية المتقدمة وتجميل الأزرار (ai_helper.py)
# ========================================================
import streamlit as st
import pandas as pd
import sqlite3

def render_sidebar_helper():
    st.sidebar.markdown("---")
    
    # 1. حقن كود الـ CSS الأسطوري المخصص لتحسين شكل الزر وشريط الكتابة فقط
    st.sidebar.markdown("""
        <style>
        /* 🛑 ترقية شكل الزر الفيروزي ليصبح بتأثير الحواف الزجاجية المشعة الخلابة */
        div[data-testid="stCheckbox"] {
            background: linear-gradient(135deg, #0a0a12 0%, #101020 100%) !important;
            border: 2px solid #00fff0 !important;
            border-radius: 14px !important;
            padding: 14px !important;
            text-align: right !important;
            box-shadow: 0px 0px 18px rgba(0, 255, 240, 0.4), inset 0px 0px 8px rgba(0, 255, 240, 0.2) !important;
            transition: all 0.4s ease-in-out !important;
        }
        
        /* زيادة كثافة التوهج المشع حول الزر عند مرور مؤشر الماوس */
        div[data-testid="stCheckbox"]:hover {
            box-shadow: 0px 0px 28px #00fff0, 0px 0px 35px rgba(0, 255, 240, 0.5) !important;
            transform: translateY(-1px) !important;
            cursor: pointer !important;
        }
        
        /* تصميم صندوق الترحيب الداخلي المنسق بدقة */
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
            animation: cyberPopIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
        }
        
        /* مؤشر النبض الرقمي الحي */
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
        @keyframes cyberPopIn {
            0% { transform: translateY(15px) scale(0.97); opacity: 0; filter: blur(3px); }
            100% { transform: translateY(0) scale(1); opacity: 1; filter: blur(0); }
        }
        
        .ai-title-text { color: #00fff0; font-family: 'Cairo', sans-serif; font-size: 16px; margin: 5px 0 8px 0; font-weight: bold; text-shadow: 0 0 10px #00fff0; }
        .ai-body-text { color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; line-height: 1.6; margin: 0; }
        .ai-pink-neon { color: #ff00ff; font-weight: bold; text-shadow: 0 0 8px #ff00ff; }
        
        /* 🚨 تحسين وتجميل شكل شريط كتابة السؤال ليصبح أسطورياً ومحترفاً بالكامل */
        div[data-testid="stTextInput"] input {
            border: 2px solid #00fff0 !important;
            background-color: #07070d !important;
            color: #ffffff !important;
            border-radius: 10px !important;
            padding: 12px !important;
            font-family: 'Cairo', sans-serif !important;
            text-align: right !important;
            direction: rtl !important;
            box-shadow: 0px 0px 12px rgba(0, 255, 240, 0.2) !important;
            transition: all 0.4s ease-in-out !important;
        }
        
        /* تأثير التوهج الأرجواني السيبراني الخلاب اللحظي بمجرد الضغط داخل حقل الكتابة */
        div[data-testid="stTextInput"] input:focus {
            border-color: #ff00ff !important;
            box-shadow: 0px 0px 22px #ff00ff, inset 0px 0px 6px rgba(255, 0, 255, 0.4) !important;
            transform: scale(1.01) !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # 2. زر التفعيل الميكانيكي المطور بشكله الجديد الخلاب
    ai_activate = st.sidebar.checkbox("تفعيل المساعد الأسطوري الخارق 🔘", key="legendary_v7_pro_activate")
    
    if ai_activate:
        # انطلاق لوحة التحكم التلقائية والترحيب الفوري الموجه للمدير محمد
        st.sidebar.markdown("""
            <div class="ai-cyber-legendary-panel">
                <div class="ai-pulse-status"><span class="pulse-dot"></span>NEXUS AI: ONLINE</div>
                <h3 class="ai-title-text">🔮 المستشار اللاسلكي المطور</h3>
                <p class="ai-body-text">مرحباً بك مجدداً يا <span class="ai-pink-neon">مدير محمد</span>! خلايا النظام مستقرة ومربوطة بـ v4 بنجاح. اطرح أي سؤال مالي أو سلعي تالياً لبدء الجرد الفوري.</p>
            </div>
        """, unsafe_allow_html=True)

        # شريط الأسئلة الاحترافي الجديد والمعدل كلياً بمظهر خلاب
        user_query = st.sidebar.text_input("💬 اكتب سؤالك للمساعد هنا:", key="cyber_v7_pro_query")
        
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
            <div style="background: linear-gradient(135deg, #0d0614 0%, #1c092b 100%); border: 1px solid #ff00ff; box-shadow: 0 0 15px #ff00ff, inset 0 0 5px rgba(255, 0, 255, 0.3); padding: 15px; border-radius: 10px; text-align: right; direction: rtl; margin-top: 12px; animation: cyberPopIn 0.4s ease;">
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
            <div style="background: linear-gradient(135deg, #051214 0%, #09262b 100%); border: 1px solid #00fff0; box-shadow: 0 0 15px #00fff0, inset 0 0 5px rgba(0, 255, 240, 0.3); padding: 15px; border-radius: 10px; text-align: right; direction: rtl; margin-top: 12px; animation: cyberPopIn 0.4s ease;">
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

# ضمان حجز مكان الميزتين الثالثة والرابعة في مشروعك لمنع أي خطأ تعطل
def render_marketing_hub():
    pass

def render_data_insights(conn):
    pass
