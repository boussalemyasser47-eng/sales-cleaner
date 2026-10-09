# ========================================================
# الجزء الأول: تصاميم النيون الحركية ومؤشر الحالة الحي (ai_helper.py)
# ========================================================
import streamlit as st
import pandas as pd
import sqlite3

def render_sidebar_helper():
    st.sidebar.markdown("---")
    
    # 1. حقن أقوى حزمة CSS سيبرانية لترقية الواجهة الرسومية بشكل خارق
    st.sidebar.markdown("""
        <style>
        /* تنسيق زر التفعيل ليطابق لقطة شاشتك مع توهج نيون مستقر */
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
            box-shadow: 0px 0px 30px #00fff0, 0px 0px 40px rgba(0, 255, 240, 0.5);
            transform: scale(1.02);
            cursor: pointer;
        }
        
        /* لوحة المساعد الأسطورية مع خلفية متدرجة متحركة وانبثاق تلقائي خلاب */
        .ai-cyber-legendary-panel {
            background: linear-gradient(135deg, #090911 0%, #111124 100%);
            border: 2px solid transparent;
            background-image: linear-gradient(#090911, #111124), linear-gradient(135deg, #00fff0, #ff00ff);
            background-origin: border-box;
            background-clip: padding-box, border-box;
            border-radius: 14px;
            padding: 20px;
            text-align: right;
            box-shadow: 0px 10px 30px rgba(0, 255, 240, 0.3);
            margin-top: 15px;
            margin-bottom: 15px;
            direction: rtl;
            animation: cyberPopIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
        }
        
        /* مؤشر الحالة الرقمي النبضي */
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
        
        .ai-title-text { color: #00fff0; font-family: 'Cairo', sans-serif; font-size: 17px; margin: 5px 0 8px 0; font-weight: bold; text-shadow: 0 0 10px #00fff0; }
        .ai-body-text { color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13.5px; line-height: 1.6; margin: 0; }
        .ai-pink-neon { color: #ff00ff; font-weight: bold; text-shadow: 0 0 8px #ff00ff; }
        
        /* ترقية وتجميل شريط إدخال الأسئلة المحترف */
        div[data-testid="stTextInput"] input {
            border: 2px solid rgba(0, 255, 240, 0.2) !important;
            background-color: #07070d !important;
            color: #ffffff !important;
            border-radius: 8px !important;
            padding: 10px !important;
            font-family: 'Cairo', sans-serif !important;
            transition: all 0.3s ease-in-out !important;
        }
        div[data-testid="stTextInput"] input:focus {
            border-color: #ff00ff !important;
            box-shadow: 0 0 18px rgba(255, 0, 255, 0.6) !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # 2. توليد زر التفعيل المطابق تماماً لأبعاد صورتك الحالية
    ai_activate = st.sidebar.checkbox("تفعيل المساعد الأسطوري الخارق 🔘", key="legendary_v5_pro_activate")
    
    if ai_activate:
        # انطلاق لوحة التحكم السيبرانية الفخمة والترحيب التلقائي
        st.sidebar.markdown("""
            <div class="ai-cyber-legendary-panel">
                <div class="ai-pulse-status"><span class="pulse-dot"></span>NEXUS AI: ONLINE</div>
                <h3 class="ai-title-text">🔮 المستشار اللاسلكي المطور</h3>
                <p class="ai-body-text">مرحباً بك مجدداً يا <span class="ai-pink-neon">مدير محمد</span>! خلايا النظام مستقرة ومربوطة بـ v4 بنجاح. اطرح أي سؤال مالي أو سلعي تالياً لبدء الجرد الفوري.</p>
            </div>
        """, unsafe_allow_html=True)

        # شريط الأسئلة الاحترافي المتوهج تدريجياً
        user_query = st.sidebar.text_input("💬 اكتب سؤالك للمساعد هنا:", key="cyber_v5_pro_query")
        
        if user_query:
            evaluate_logic_response(user_query)
# ========================================================
# الجزء الثاني: بطاقات التقارير النيونية المنفصلة بـ DA (ai_helper.py)
# ========================================================

def evaluate_logic_response(query):
    # الاتصال المباشر بقاعدة الحسابات v4 لقراءة سجلات المتجر الفعلية
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
        
    # ج. الإجابة الذكية الافتراضية السيبرانية
    else:
        st.sidebar.markdown("""
            <div style="border-right: 3px solid #ffffff; padding-right: 10px; margin-top: 12px; text-align: right; direction: rtl;">
                <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 12.5px; margin: 0;">الأنظمة السيبرانية v4 متصلة بكفاءة يا مدير محمد. اسألني عن الفواتير أو السلع لاستدعاء بطاقات جرد الأرقام المنطقية الفورية.</p>
            </div>
        """, unsafe_allow_html=True)
    conn.close()

# الحفاظ على حجز مكان الميزتين 3 و 4 في مشروعك لضمان عدم حدوث أي خطأ تعطل
def render_marketing_hub():
    pass

def render_data_insights(conn):
    pass
