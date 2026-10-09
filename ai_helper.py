# ========================================================
# الجزء الأول: الهندسة البصرية المتقدمة ونظام الاقتراحات (ai_helper.py)
# ========================================================
import streamlit as st
import pandas as pd
import sqlite3

def render_sidebar_helper():
    st.sidebar.markdown("---")
    
    # 1. حقن حزمة الـ CSS الموحدة التي تعطي كل بطاقة هويتها الحركية المنفصلة تزامناً مع التحديث
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
        div[data-testid="stCheckbox"]:hover { box-shadow: 0px 0px 28px #00fff0 !important; }
        
        /* 🚨 هندسة الأوعية الرسومية المستقلة: تطبيق الأنميشن ميكانيكياً لكل فئة على حدة لمنع الفجائية */
        .card-profit, .card-stock, .card-growth, .card-states, .card-average, .card-default {
            background: linear-gradient(135deg, #090911 0%, #111124 100%) !important;
            border-left: 1px solid rgba(0, 255, 240, 0.2) !important;
            border-radius: 12px !important;
            padding: 18px !important;
            text-align: right !important;
            box-shadow: 0px 8px 25px rgba(0, 0, 0, 0.4) !important;
            margin-top: 15px !important;
            margin-bottom: 15px !important;
            direction: rtl !important;
            
            /* إجبار المتصفح على بدء أنيميشن الصعود من الصفر لأن المعرّف Class Name تغير */
            animation: cyberPopIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards !important;
            opacity: 0;
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
        
        /* تثبيت حواف مستطيل الكتابة الوردي الفاخر المطابق لـ صورتك تماماً وعزله كلياً */
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
        div[data-testid="stTextInput"] p, div[data-testid="stTextInput"] small, 
        div[data-testid="stTextInput"] label, div[data-testid="stTextInput"] [data-testid="stWidgetInstructions"],
        div[data-testid="stTextInput"] span, div[data-testid="stTextInput"] div:not(:first-child) p,
        .st-emotion-cache-16idsys p, .st-emotion-cache-q3uqly p, .st-emotion-cache-1pxscv7 p {
            display: none !important; opacity: 0 !important; visibility: hidden !important; height: 0px !important; margin: 0px !important; padding: 0px !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    ai_activate = st.sidebar.checkbox("تفعيل المساعد الأسطوري الخارق 🔘", key="legendary_v7_pro_activate")
    
    if ai_activate:
        st.sidebar.markdown("""
            <div class="card-default" style="border-right: 4px solid #00fff0;">
                <div class="ai-pulse-status"><span class="pulse-dot"></span>NEXUS AI: ONLINE</div>
                <h3 style="color:#00fff0; font-family:'Cairo'; font-size:16px; margin:0;">🔮 المستشار اللاسلكور المطور</h3>
                <p style="color:#fff; font-family:'Cairo'; font-size:13px; margin:5px 0 0 0;">مرحباً بك يا <span style="color:#ff00ff; font-weight:bold;">مدير محمد</span>! أنظمتي مستقرة ومربوطة بـ v4 بنجاح.</p>
            </div>
        """, unsafe_allow_html=True)

        if "suggested_click" not in st.session_state:
            st.session_state.suggested_click = ""

        st.sidebar.markdown("<p style='color: #00fff0; font-family: Cairo; font-size: 11px; text-align: right; margin:0;'>💡 جرد الحسابات والمخزن الأساسي:</p>", unsafe_allow_html=True)
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("📊 تقرير الأرباح"):
                st.session_state.suggested_click = "تقرير الأرباح"
                st.session_state.cyber_v7_pro_query = ""
        with col2:
            if st.button("📦 جرد المخزن"):
                st.session_state.suggested_click = "جرد المخزن"
                st.session_state.cyber_v7_pro_query = ""
# ========================================================
# الجزء الثاني: بقية الأزرار وميكانيكية المسح الآلي (ai_helper.py)
# ========================================================
        if st.sidebar.button("⚠️ المنتجات القريبة من النفاذ"):
            st.session_state.suggested_click = "قطع المستودع"
            st.session_state.cyber_v7_pro_query = ""
        
        st.sidebar.markdown("<p style='color: #ff00ff; font-family: Cairo; font-size: 11px; text-align: right; margin:5px 0 0 0;'>🚀 تحليلات الـ AI المتقدمة (المجموعة 2):</p>", unsafe_allow_html=True)
        col3, col4 = st.sidebar.columns(2)
        with col3:
            if st.button("📈 نمو المبيعات"):
                st.session_state.suggested_click = "نمو المبيعات"
                st.session_state.cyber_v7_pro_query = ""
        with col4:
            if st.button("🗺️ مستشار الولايات"):
                st.session_state.suggested_click = "مستشار الولايات"
                st.session_state.cyber_v7_pro_query = ""
        if st.sidebar.button("💰 متوسط الأرباح المتوقعة"):
            st.session_state.suggested_click = "متوسط الأرباح"
            st.session_state.cyber_v7_pro_query = ""

        st.sidebar.markdown("---")
        user_query = st.sidebar.text_input("💬 اكتب سؤالك للمساعد هنا:", key="cyber_v7_pro_query")
        
        if user_query:
            st.session_state.suggested_click = ""
            final_query = user_query
        else:
            final_query = st.session_state.suggested_click
        
        if final_query:
            evaluate_logic_response(final_query)

def render_marketing_hub(): pass
def render_data_insights(conn): pass
# ========================================================
# الجزء الثالث: عقل المساعد والاستجابات الديناميكية الفريدة (ai_helper.py)
# ========================================================

def evaluate_logic_response(query):
    conn = sqlite3.connect("invoices_master_v4.db")
    
    # 1. 📊 استجابة الزر الأول: معرّف حركي منفصل (card-profit)
    if query == "تقرير الأرباح" or "ربح" in query or "مبيعات" in query or "حساب" in query:
        df_sales = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conn)
        count_inv = len(df_sales)
        if count_inv > 0:
            total_da = df_sales['final_total'].sum()
            avg_invoice = total_da / count_inv
            st.sidebar.markdown(f"""
                <div class="card-profit" style="border-right: 4px solid #ff00ff; box-shadow: 0 0 15px #ff00ff;">
                    <h4 style="color: #ff00ff; font-family: 'Cairo'; font-size: 14px; margin: 0 0 6px 0;">🤖 التشخيص المالي للـ AI:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo'; font-size: 13px; margin: 0;">
                        💰 إجمالي المداخيل الحالية: <span style="color: #00fff0; font-weight: bold;">{total_da:,.2f} DA</span><br>
                        📈 متوسط قيمة الطلب: <span style="color: #00ffcc;">{avg_invoice:,.2f} DA</span>
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else: st.sidebar.info("📊 لا توجد فواتير مسجلة حالياً.")
        
    # 2. 📦 استجابة الزر الثاني: معرّف حركي منفصل (card-stock) يمنع الفجائية
    elif query == "جرد المخزن" or query == "قطع المستودع" or "مخزن" in query or "سلع" in query or "قطع" in query:
        df_stock = pd.read_sql("SELECT product_name, available_qty FROM store_stock", conn)
        if not df_stock.empty:
            total_qty = df_stock['available_qty'].sum()
            low_stock_df = df_stock[df_stock['available_qty'] <= 10]
            low_stock_text = ""
            if len(low_stock_df) > 0:
                low_stock_text = "<br>🚨 <b>تحذير النفاذ السريع:</b><br>"
                for idx, row in low_stock_df.iterrows():
                    low_stock_text += f"⚠️ المنتج [ {row['product_name']} ] متبقي منه {row['available_qty']} قطع فقط!<br>"
            else: low_stock_text = "<br>✅ <b>مؤشر الأمان:</b> جميع الكميات مستقرة."

            st.sidebar.markdown(f"""
                <div class="card-stock" style="border-right: 4px solid #00fff0; box-shadow: 0 0 15px #00fff0;">
                    <h4 style="color: #00fff0; font-family: 'Cairo'; font-size: 14px; margin: 0 0 6px 0;">🔮 تقرير الجرد والتنبؤ الفوري:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo'; font-size: 13px; margin: 0; line-height: 1.6;">
                        القطع الكلية الجاهزة للشحن: <span style="color: #ff00ff; font-weight: bold;">{total_qty} حبة</span>
                        {low_stock_text}
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else: st.sidebar.info("📦 مستودعك فارغ حالياً.")

    # 3. 📈 استجابة الزر الثالث: معرّف حركي منفصل (card-growth) يمنع الفجائية
    elif query == "نمو المبيعات":
        df_sales = pd.read_sql("SELECT month_created, final_total FROM v4_customer_invoices", conn)
        if not df_sales.empty:
            monthly_summary = df_sales.groupby('month_created')['final_total'].sum()
            summary_text = ""
            for month, total in monthly_summary.items():
                summary_text += f"📅 الشهر [ {month} ]: {total:,.2f} DA<br>"
            st.sidebar.markdown(f"""
                <div class="card-growth" style="border-right: 4px solid #ff00ff; box-shadow: 0 0 15px #ff00ff;">
                    <h4 style="color: #ff00ff; font-family: 'Cairo'; font-size: 14px; margin: 0 0 6px 0;">📈 تحليل نمو المبيعات الشهري:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo'; font-size: 13px; margin: 0; line-height: 1.6;">{summary_text}</p>
                </div>
            """, unsafe_allow_html=True)
        else: st.sidebar.info("📈 لا توجد بيانات كافية.")
# ========================================================
# الجزء الرابع: مستشار الولايات والأمن الحركي وقفل الاتصال (ai_helper.py)
# ========================================================
    # 4. 🗺️ استجابة زر الولايات: معرّف حركي منفصل (card-states) يمنع الفجائية الصامتة
    elif query == "مستشار الولايات":
        df_sales = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conn)
        count_inv = len(df_sales)
        if count_inv > 0:
            st.sidebar.markdown(f"""
                <div class="card-states" style="border-right: 4px solid #00fff0; box-shadow: 0 0 15px #00fff0;">
                    <h4 style="color: #00fff0; font-family: 'Cairo'; font-size: 14px; margin: 0 0 6px 0;">🗺️ مستشار توجيه الحملات الجزائريّ:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo'; font-size: 13px; margin: 0; line-height: 1.6;">
                        حجم حركة فواتير الـ COD الفعليّة: <b>{count_inv} طلبية نشطة</b>.<br>
                        🎯 <b>توصية خريطة الـ AI:</b> نوصي بتوجيه وتكثيف الميزانيات الترويجية نحو ولايات <b>(الجزائر العاصمة، وهران، سطيف، قسنطينة)</b> لضمان أعلى معدل تسليم.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else: st.sidebar.info("🗺️ قم بإصدار الفواتير أولاً لتنشيط خريطة الولايات الذكية.")

    # 5. 💰 استجابة زر المتوسط: معرّف حركي منفصل (card-average) يمنع الفجائية الصامتة
    elif query == "متوسط الأرباح":
        df_sales = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conn)
        count_inv = len(df_sales)
        if count_inv > 0:
            total_da = df_sales['final_total'].sum()
            avg_profit = total_da / count_inv
            st.sidebar.markdown(f"""
                <div class="card-average" style="border-right: 4px solid #ff00ff; box-shadow: 0 0 15px #ff00ff;">
                    <h4 style="color: #ff00ff; font-family: 'Cairo'; font-size: 14px; margin: 0 0 6px 0;">💰 متوسط مداخيل الطلبيات الصافي:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo'; font-size: 13px; margin: 0; line-height: 1.6;">💸 <b>المتوسط المحقق المحسوب: {avg_profit:,.2f} DA</b></p>
                </div>
            """, unsafe_allow_html=True)
        else: st.sidebar.info("💰 لا توجد فواتير صادرة لتقييم المتوسط المالي.")
            
    # 6. التظهير الميكانيكي المستقر الافتراضي
    else:
        st.sidebar.markdown("""
            <div class="card-default" style="border-right: 4px solid #ffffff; padding-right: 10px; margin-top: 12px; text-align: right; direction: rtl;">
                <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 12.5px; margin: 0;">الأنظمة السيبرانية v4 متصلة بكفاءة. اسألني عن الحسابات أو المخزون لاستدعاء بطاقات جرد الأرقام المنطقية الفورية بـ **DA**.</p>
            </div>
        """, unsafe_allow_html=True)
    conn.close()
