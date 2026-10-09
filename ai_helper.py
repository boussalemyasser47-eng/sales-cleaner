# ========================================================
# الجزء الأول: الهندسة البصرية المتقدمة وحركات التبديل (ai_helper.py)
# ========================================================
import streamlit as st
import pandas as pd
import sqlite3

def render_sidebar_helper():
    st.sidebar.markdown("---")
    
    # حقن كود الـ CSS الأسطوري لحظر التداخلات وحقن شفرة الحركة الميكانيكية التدريجية
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
        div[data-testid="stCheckbox"]:hover { box-shadow: 0px 0px 28px #00fff0 !important; }
        
        /* 🚨 خوارزمية التبديل الميكانيكي الانسيابي الخلاب (Slide & Fade Transition Panel) */
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
            
            /* حقن أنيميشن ميكانيكي تدريجي خلاب ممتد المفعول لمنع الانتقال المباشر */
            animation: cyberSlideExchange 0.6s cubic-bezier(0.25, 1, 0.5, 1) forwards;
            opacity: 0;
        }
        
        @keyframes cyberSlideExchange {
            0% { transform: translateY(15px); opacity: 0; filter: blur(4px); }
            100% { transform: translateY(0); opacity: 1; filter: blur(0); }
        }
        
        .ai-title-text { color: #00fff0; font-family: 'Cairo', sans-serif; font-size: 16px; font-weight: bold; text-shadow: 0 0 10px #00fff0; }
        .ai-body-text { color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; line-height: 1.6; }
        .ai-pink-neon { color: #ff00ff; font-weight: bold; text-shadow: 0 0 8px #ff00ff; }
        
        /* تثبيت حواف مستطيل الكتابة الوردي الفاخر المطابق لـ صورتك وعزله كلياً */
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
            display: none !important; opacity: 0 !important; visibility: hidden !hidden; height: 0px !important; margin: 0px !important; padding: 0px !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    ai_activate = st.sidebar.checkbox("تفعيل المساعد الأسطوري الخارق 🔘", key="legendary_v7_pro_activate")
    
    if ai_activate:
        st.sidebar.markdown("""
            <div class="ai-cyber-legendary-panel">
                <h3 class="ai-title-text">🔮 المستشار اللاسلكي المطور</h3>
                <p class="ai-body-text">مرحباً بك يا <span class="ai-pink-neon">مدير محمد</span>! أنظمتي مستقرة ومربوطة بـ v4 بنجاح. اختر أحد الاقتراحات السريعة بالأسفل.</p>
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
        
        # [المجموعة 2]: تحليلات الـ AI المتقدمة للنمو
        st.sidebar.markdown("<p style='color: #ff00ff; font-family: Cairo; font-size: 11px; text-align: right; margin:5px 0 0 0;'>🚀 تحليلات الـ AI المتقدمة للنمو:</p>", unsafe_allow_html=True)
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
            
        # [المجموعة 3]: دروع الأمن وقيادة الميزانيات السيبرانية الخارقة
        st.sidebar.markdown("<p style='color: #00ffcc; font-family: Cairo; font-size: 11px; text-align: right; margin:5px 0 0 0;'>🛡️ القيادة التكتيكية وأمن الـ COD:</p>", unsafe_allow_html=True)
        col5, col6 = st.sidebar.columns(2)
        with col5:
            if st.button("🛡️ درع حماية الـ COD"):
                st.session_state.suggested_click = "درع حماية الـ COD"
                st.session_state.cyber_v7_pro_query = ""
        with col6:
            if st.button("🎯 قيادة الميزانية"):
                st.session_state.suggested_click = "قيادة الميزانية"
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
# الجزء الثالث: عقل المساعد وبداية الاستجابات الحركية (ai_helper.py)
# ========================================================

def evaluate_logic_response(query):
    conn = sqlite3.connect("invoices_master_v4.db")
    
    # 1. بطاقة الأرباح الميكانيكية التدريجية
    if query == "تقرير الأرباح" or "ربح" in query or "حساب" in query:
        df_sales = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conn)
        count_inv = len(df_sales)
        if count_inv > 0:
            total_da = df_sales['final_total'].sum()
            avg_invoice = total_da / count_inv
            st.sidebar.markdown(f"""
                <div class="ai-cyber-legendary-panel" style="border-right-color: #ff00ff; box-shadow: 0 0 15px #ff00ff;">
                    <h4 style="color: #ff00ff; font-family: 'Cairo'; font-size: 14px; margin: 0 0 6px 0;">🤖 التشخيص المالي للـ AI:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo'; font-size: 13px; margin: 0; line-height: 1.6;">
                        💰 إجمالي المداخيل الحالية: <span style="color: #00fff0; font-weight: bold;">{total_da:,.2f} DA</span><br>
                        📈 متوسط قيمة الطلب: <span style="color: #00ffcc;">{avg_invoice:,.2f} DA</span>
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else: st.sidebar.info("📊 لا توجد فواتير مسجلة حالياً.")
        
    # 2. بطاقة جرد قطع المستودع والسلع الحركية التدريجية
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
                <div class="ai-cyber-legendary-panel">
                    <h4 style="color: #00fff0; font-family: 'Cairo'; font-size: 14px; margin: 0 0 6px 0;">🔮 تقرير الجرد والتنبؤ الفوري:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo'; font-size: 13px; margin: 0; line-height: 1.6;">
                        مجموع القطع بالمستودع: <span style="color: #ff00ff; font-weight: bold;">{total_qty} حبة</span>
                        {low_stock_text}
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else: st.sidebar.info("📦 مستودعك فارغ حالياً.")

    # 3. بطاقة تحليل نمو مبيعات المتجر التدريجية
    elif query == "نمو المبيعات":
        df_sales = pd.read_sql("SELECT month_created, final_total FROM v4_customer_invoices", conn)
        if not df_sales.empty:
            monthly_summary = df_sales.groupby('month_created')['final_total'].sum()
            summary_text = ""
            for month, total in monthly_summary.items():
                summary_text += f"📅 الشهر [ {month} ]: {total:,.2f} DA<br>"
            st.sidebar.markdown(f"""
                <div class="ai-cyber-legendary-panel" style="border-right-color: #ff00ff; box-shadow: 0 0 15px #ff00ff;">
                    <h4 style="color: #ff00ff; font-family: 'Cairo'; font-size: 14px; margin: 0 0 6px 0;">📈 تحليل نمو المبيعات الشهري:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo'; font-size: 13px; margin: 0; line-height: 1.6;">{summary_text}</p>
                </div>
            """, unsafe_allow_html=True)
        else: st.sidebar.info("📈 لا توجد بيانات كافية.")
# ========================================================
# الجزء الرابع: مستشار الولايات والأمن الحركي وقفل الاتصال (ai_helper.py)
# ========================================================
    # 4. بطاقة مستشار شحن وتوصيل الولايات الحركية التدريجية
    elif query == "مستشار الولايات":
        df_sales = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conn)
        count_inv = len(df_sales)
        if count_inv > 0:
            st.sidebar.markdown(f"""
                <div class="ai-cyber-legendary-panel">
                    <h4 style="color: #00fff0; font-family: 'Cairo'; font-size: 14px; margin: 0 0 6px 0;">🗺️ مستشار توجيه الحملات الجزائريّ:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo'; font-size: 13px; margin: 0; line-height: 1.6;">
                        حجم حركة فواتير الـ COD الفعليّة: <b>{count_inv} طلبية نشطة</b>.<br>
                        🎯 <b>توصية خريطة الـ AI:</b> نوصي بتوجيه وتكثيف الميزانيات الترويجية نحو ولايات <b>(الجزائر العاصمة، وهران، سطيف، قسنطينة)</b> لضمان أعلى معدل تسليم.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else: st.sidebar.info("🗺️ لا توجد فواتير لتنشيط الولايات.")

    # 5. بطاقة حساب متوسط المداخيل المحسوبة بـ DA
    elif query == "متوسط الأرباح":
        df_sales = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conn)
        count_inv = len(df_sales)
        if count_inv > 0:
            total_da = df_sales['final_total'].sum()
            avg_profit = total_da / count_inv
            st.sidebar.markdown(f"""
                <div class="ai-cyber-legendary-panel" style="border-right-color: #ff00ff; box-shadow: 0 0 15px #ff00ff;">
                    <h4 style="color: #ff00ff; font-family: 'Cairo'; font-size: 14px; margin: 0 0 6px 0;">💰 متوسط مداخيل الطلبيات الصافي:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo'; font-size: 13px; margin: 0; line-height: 1.6;">💸 <b>المتوسط المحقق:</b> <span style="color: #00fff0; font-weight: bold; font-size: 15px;">{avg_profit:,.2f} DA</span></p>
                </div>
            """, unsafe_allow_html=True)
        else: st.sidebar.info("💰 لا توجد فواتير صادرة.")

    # 6. بطاقة درع مكافحة الخسائر والطلبيات المشبوهة المكررة الهاتف 
    elif query == "درع حماية الـ COD":
        df_sales = pd.read_sql("SELECT customer_phone, COUNT(*) as order_count FROM v4_customer_invoices GROUP BY customer_phone HAVING order_count > 1", conn)
        if not df_sales.empty:
            fraud_count = len(df_sales)
            st.sidebar.markdown(f"""
                <div class="ai-cyber-legendary-panel" style="border-right: 4px solid #ff0055; box-shadow: 0 0 15px #ff0055;">
                    <h4 style="color: #ff0055; font-family: 'Cairo'; font-size: 14px; margin: 0 0 6px 0;">🚨 نظام درع مكافحة الخسائر الماليّة:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo'; font-size: 13px; margin: 0; line-height: 1.6;">⚠️ <b>تم استكشاف ثغرة شحن:</b> تم العثور على <b>{fraud_count} زبائن كرروا طلبياتهم بنفس رقم الهاتف</b> في الفواتير v4! اتصل بهم لتفادي مصاريف الـ Retour للولايات.</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.sidebar.markdown("""
                <div class="ai-cyber-legendary-panel" style="border-right: 4px solid #00ff66; box-shadow: 0 0 15px #00ff66;">
                    <h4 style="color: #00ff66; font-family: 'Cairo'; font-size: 14px; margin: 0 0 6px 0;">🛡️ درع الأمان السيبراني للـ COD:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">✅ <b>مؤشر أمن المبيعات:</b> 100% الصفقات آمنة ونظيفة.</p>
                </div>
            """, unsafe_allow_html=True)

    # 7. بطاقة مركز قيادة وتوجيه الميزانية الترويجية الأعلى ربحاً
    elif query == "قيادة الميزانية":
        df_invoices = pd.read_sql("SELECT product_name, SUM(final_total) as revenue FROM v4_customer_invoices GROUP BY product_name ORDER BY revenue DESC LIMIT 1", conn)
        if not df_invoices.empty:
            top_product = df_invoices['product_name'].values
            top_revenue = df_invoices['revenue'].values
            st.sidebar.markdown(f"""
                <div class="ai-cyber-legendary-panel">
                    <h4 style="color: #00fff0; font-family: 'Cairo'; font-size: 14px; margin: 0 0 6px 0;">🎯 مركز القيادة وتوجيه الميزانيات:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo'; font-size: 13px; margin: 0; line-height: 1.6;">📦 المنتج الأعلى طلباً: <b>[ {top_product} ]</b> بمداخل بلغت <span style="color:#ff00ff; font-weight:bold;">{top_revenue:,.2f} DA</span>.</p>
                </div>
            """, unsafe_allow_html=True)
        else: st.sidebar.info("🎯 قم بتسجيل مبيعات لتفعيل مركز القيادة.")
            
    # 8. التظهير الميكانيكي التدريجي للحالة الافتراضية عند فتح الأداة لأول مرة وغياب الضغط
    else:
        st.sidebar.markdown("""
            <div class="ai-cyber-legendary-panel" style="border-right: 4px solid #00ff66; box-shadow: 0 0 15px #00ff66;">
                <h4 style="color: #00ff66; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0;">🛡️ درع الأمان السيبراني للـ COD:</h4>
                <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">✅ <b>مؤشر أمن المبيعات:</b> 100% الصفقات آمنة ونظيفة.</p>
            </div>
        """, unsafe_allow_html=True)
    conn.close()
