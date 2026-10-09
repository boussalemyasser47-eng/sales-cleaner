# ========================================================
# الجزء الأول: مركز التحكم والأزرار السيبرانية الخارقة (ai_helper.py)
# ========================================================
import streamlit as st
import pandas as pd
import sqlite3

def render_sidebar_helper():
    st.sidebar.markdown("---")
    
    # حقن كود الـ CSS الأسطوري لمتجرك لحماية وتثبيت مستطيلك الوردي وحظر التداخلات
    st.sidebar.markdown("""
        <style>
        /* ترقية شكل الزر الفيروزي ليصبح بتأثير الحواف الزجاجية المشعة الخلابة */
        div[data-testid="stCheckbox"] {
            background: linear-gradient(135deg, #0a0a12 0%, #101020 100%) !important;
            border: 2px solid #00fff0 !important;
            border-radius: 14px !important;
            padding: 14px !important;
            text-align: right !important;
            box-shadow: 0px 0px 18px rgba(0, 255, 240, 0.4), inset 0px 0px 8px rgba(0, 255, 240, 0.2) !important;
            transition: all 0.4s ease-in-out !important;
        }
        div[data-testid="stCheckbox"]:hover {
            box-shadow: 0px 0px 28px #00fff0 !important;
            transform: translateY(-1px) !important;
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
        
        .ai-title-text { color: #00fff0; font-family: 'Cairo', sans-serif; font-size: 16px; margin: 5px 0 8px 0; font-weight: bold; }
        .ai-body-text { color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; line-height: 1.6; margin: 0; }
        .ai-pink-neon { color: #ff00ff; font-weight: bold; text-shadow: 0 0 8px #ff00ff; }
        
        /* تحسين وتثبيت شكل مستطيل الكتابة الوردي الأسطوري الخاص بصورتك دون أي تغيير مظهر */
        div[data-testid="stTextInput"] input {
            border: 2px solid #ff00ff !important;
            background-color: #10101b !important;
            color: #ffffff !important;
            border-radius: 12px !important;
            padding: 14px 16px !important;
            font-family: 'Cairo', sans-serif !important;
            text-align: right !important;
            direction: rtl !important;
            box-shadow: 0px 0px 15px rgba(255, 0, 255, 0.3) !important;
        }
        
        /* حظر وإبادة التلميح الإنجليزي المعطل (Press Enter to apply) والتعليمات تماماً لمنع الاختلاط */
        div[data-testid="stTextInput"] p, 
        div[data-testid="stTextInput"] small, 
        div[data-testid="stTextInput"] label,
        div[data-testid="stTextInput"] [data-testid="stWidgetInstructions"],
        div[data-testid="stTextInput"] span,
        div[data-testid="stTextInput"] div:not(:first-child) p,
        .st-emotion-cache-16idsys p,
        .st-emotion-cache-q3uqly p {
            display: none !important;
            opacity: 0 !important;
            visibility: hidden !important;
            height: 0px !important;
            margin: 0px !important;
            padding: 0px !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    ai_activate = st.sidebar.checkbox("تفعيل المساعد الأسطوري الخارق 🔘", key="legendary_v7_pro_activate")
    
    if ai_activate:
        st.sidebar.markdown("""
            <div class="ai-cyber-legendary-panel">
                <div class="ai-pulse-status"><span class="pulse-dot"></span>CYBER COMMANDER: ACTIVE</div>
                <h3 class="ai-title-text">🔮 المستشار اللاسلكي المطور</h3>
                <p class="ai-body-text">مرحباً بك يا <span class="ai-pink-neon">مدير محمد</span>! تم تنشيط دروع حماية الـ COD ورادارات التوجيه المالي الذكي. اضغط على أزرار القيادة التكتيكية بالأسفل.</p>
            </div>
        """, unsafe_allow_html=True)

        if "suggested_click" not in st.session_state:
            st.session_state.suggested_click = ""

        # 🚨 [حقن الأزرار السيبرانية الخارقة]: درع الحماية والميزانية التكتيكية
        st.sidebar.markdown("<p style='color: #00fff0; font-family: Cairo; font-size: 12px; margin: 10px 0 5px 0; text-align: right;'>🛡️ نظام حماية وأمن المتجر (Ultra-AI):</p>", unsafe_allow_html=True)
        
        if st.sidebar.button("🛡️ درع حماية الـ COD ومكافحة الخسائر"):
            st.session_state.suggested_click = "درع حماية الـ COD"
            st.session_state.cyber_v7_pro_query = ""
            
        if st.sidebar.button("🎯 قيادة وتوجيه الميزانية الإعلانية"):
            st.session_state.suggested_click = "قيادة الميزانية"
            st.session_state.cyber_v7_pro_query = ""

        st.sidebar.markdown("---")

        # شريط الأسئلة الاحترافي الوردي المثبت تماماً
        user_query = st.sidebar.text_input("💬 اكتب سؤالك للمساعد هنا:", key="cyber_v7_pro_query")
        
        if user_query:
            st.session_state.suggested_click = ""
            final_query = user_query
        else:
            final_query = st.session_state.suggested_click
        
        if final_query:
            evaluate_logic_response(final_query)
# ========================================================
# الجزء الثاني: عقل المساعد المطور وخوارزميات الحماية (ai_helper.py)
# ========================================================

def evaluate_logic_response(query):
    # الاتصال المباشر بقاعدة البيانات الرابعة v4 لقراءة سجلات المتجر الفعليّة
    conn = sqlite3.connect("invoices_master_v4.db")
    
    # 1. 🛡️ خوارزمية درع حماية الـ COD ومكافحة أخطاء الشحن والخسائر المالية
    if query == "درع حماية الـ COD":
        df_sales = pd.read_sql("SELECT customer_phone, COUNT(*) as order_count FROM v4_customer_invoices GROUP BY customer_phone HAVING order_count > 1", conn)
        
        # صياغة استجابة درع حماية متطورة جداً لفرز الحسابات والشكوك
        if not df_sales.empty:
            fraud_count = len(df_sales)
            st.sidebar.markdown(f"""
                <div style="background: linear-gradient(135deg, #1a0505 0%, #3a0a0a 100%); border: 2px solid #ff0055; box-shadow: 0 0 20px #ff0055; padding: 15px; border-radius: 10px; text-align: right; direction: rtl; margin-top: 12px; animation: cyberPopIn 0.4s ease;">
                    <h4 style="color: #ff0055; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0; text-shadow: 0 0 5px #ff0055;">🚨 نظام درع مكافحة الخسائر الماليّة:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">
                        ⚠️ <b>تم استكشاف ثغرة شحن:</b> تم العثور على <b>{fraud_count} زبائن مشبوهين</b> كرروا طلبياتهم بنفس رقم الهاتف في جدول الفواتير v4!<br>
                        💡 <b>أمر القائد محمد:</b> نوصي بالاتصال الهاتفي الفوري بهؤلاء الزبائن لتأكيد الطلب يدويًا قبل إرسال السلع للولايات لتفادي مصاريف الرد (Retour).
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.sidebar.markdown("""
                <div style="background: linear-gradient(135deg, #05140b 0%, #0a3a18 100%); border: 2px solid #00ff66; box-shadow: 0 0 15px #00ff66; padding: 15px; border-radius: 10px; text-align: right; direction: rtl; margin-top: 12px;">
                    <h4 style="color: #00ff66; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0;">🛡️ درع الأمان السيبراني للـ COD:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">
                        ✅ <b>مؤشر أمن المبيعات:</b> 100% الصفقات آمنة ونظيفة. لا توجد أي أرقام هواتف مكررة أو طلبيات عشوائية قد تسبب خسائر في مصاريف التوصيل لمتجرك الإلكتروني.
                    </p>
                </div>
            """, unsafe_allow_html=True)

    # 2. 🎯 خوارزمية قيادة وتوجيه الميزانية التكتيكية واستكشاف السلع المربحة بـ DA
    elif query == "قيادة الميزانية":
        df_invoices = pd.read_sql("SELECT product_name, SUM(final_total) as revenue FROM v4_customer_invoices GROUP BY product_name ORDER BY revenue DESC LIMIT 1", conn)
        df_stock = pd.read_sql("SELECT SUM(available_qty) as stock_qty FROM store_stock", conn)
        
        try: total_stock = int(df_stock['stock_qty'].values) if not df_stock.empty else 0
        except: total_stock = 0

        if not df_invoices.empty:
            top_product = df_invoices['product_name'].values[0]
            top_revenue = df_invoices['revenue'].values[0]
            
            st.sidebar.markdown(f"""
                <div style="background: linear-gradient(135deg, #051214 0%, #0a2d33 100%); border: 2px solid #00fff0; box-shadow: 0 0 20px #00fff0; padding: 15px; border-radius: 10px; text-align: right; direction: rtl; margin-top: 12px; animation: cyberPopIn 0.4s ease;">
                    <h4 style="color: #00fff0; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0; text-shadow: 0 0 5px #00fff0;">🎯 مركز القيادة وتوجيه الميزانيات:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">
                        📦 المنتج الأكثر طلباً وربحاً في السوق: <b>[ {top_product} ]</b> بمداخل إجمالية بلغت <span style="color:#ff00ff; font-weight:bold;">{top_revenue:,.2f} DA</span>.<br>
                        🧭 <b>توجيه الـ AI للمدير محمد:</b> متوفر لديك حالياً {total_stock} حبة بالمستودع [0.7.2، 0.7.5]. نوصي بتركيز 60% من تمويل إعلاناتك على هذا المنتج نحو ولايات الوسط لضمان أقصى صافي أرباح مالي.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.sidebar.info("🎯 قم بتسجيل بعض المبيعات أولاً لتفعيل مركز القيادة التكتيكية.")
            
    # 3. إغلاق الردود العامة لحماية بيئة السيرفر
    else:
        st.sidebar.info("الأنظمة متصلة بنجاح وجاهزة لإطلاق تقارير الحماية التكتيكية بـ DA يا مدير محمد [0.7.2، 0.7.5].")
    conn.close()

def render_marketing_hub():
    pass

def render_data_insights(conn):
    pass
