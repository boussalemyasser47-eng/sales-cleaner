# ========================================================
# الجزء الأول: الهندسة البصرية المتقدمة والمجموعات الأولى (ai_helper.py)
# ========================================================
import streamlit as st
import pandas as pd
import sqlite3

def render_sidebar_helper():
    st.sidebar.markdown("---")
    
    # 1. حقن كود الـ CSS الأسطوري المخصص لتحسين شكل الزر وشريط الكتابة ومنع التداخل
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
        
        /* تثبيت شكل مستطيل الكتابة ليطابق لقطة صورتك تماماً الحواف الوردية والخلفية الداكنة */
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
                <p class="ai-body-text">مرحباً بك يا <span class="ai-pink-neon">مدير محمد</span>! تم دمج الـ 8 خلايا الاستراتيجية بنجاح لمراقبة الفواتير والمخزن والمخاطر لحظياً.</p>
            </div>
        """, unsafe_allow_html=True)

        if "suggested_click" not in st.session_state:
            st.session_state.suggested_click = ""

        # 🚨 [المجموعة 1]: الاقتراحات الحسابية والسلعية الكلاسيكية
        st.sidebar.markdown("<p style='color: #00fff0; font-family: Cairo; font-size: 11px; margin: 5px 0 2px 0; text-align: right;'>💡 جرد الحسابات والمخزن الأساسي:</p>", unsafe_allow_html=True)
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("📊 تقرير الأرباح"):
                st.session_state.suggested_click = "تقرير الأرباح"
                st.session_state.cyber_v7_pro_query = ""
        with col2:
            if st.button("📦 جرد المخزن"):
                st.session_state.suggested_click = "جرد المخزن"
                st.session_state.cyber_v7_pro_query = ""
        if st.sidebar.button("⚠️ المنتجات القريبة من النفاذ"):
            st.session_state.suggested_click = "قطع المستودع"
            st.session_state.cyber_v7_pro_query = ""
        
        # 🚨 [المجموعة 2]: تحليلات الـ AI المتقدمة للنمو
        st.sidebar.markdown("<p style='color: #ff00ff; font-family: Cairo; font-size: 11px; margin: 5px 0 2px 0; text-align: right;'>🚀 تحليلات الـ AI المتقدمة للنمو:</p>", unsafe_allow_html=True)
        col3, col4 = st.sidebar.columns(2)
        with col3:
            if st.button("📈 نمو المبيعات"):
                st.session_state.suggested_click = "نمو المبيعات"
                st.session_state.cyber_v7_pro_query = ""
        with col4:
            if st.button("🗺️ مستشار الولايات"):
                st.session_state.suggested_click = "مستشار الولايات"
                st.session_state.cyber_v7_pro_query = ""
# ========================================================
# الجزء الثاني: بقية الأزرار وميكانيكية المسح الآلي (ai_helper.py)
# ========================================================

        if st.sidebar.button("💰 متوسط الأرباح المتوقعة"):
            st.session_state.suggested_click = "متوسط الأرباح"
            st.session_state.cyber_v7_pro_query = ""
            
        # 🚨 [المجموعة 3]: دروع الأمن وقيادة الميزانيات السيبرانية الخارقة
        st.sidebar.markdown("<p style='color: #00ffcc; font-family: Cairo; font-size: 11px; margin: 5px 0 2px 0; text-align: right;'>🛡️ القيادة التكتيكية وأمن الـ COD:</p>", unsafe_allow_html=True)
        col5, col6 = st.sidebar.columns(2)
        with col5:
            if st.button("🛡️ درع حماية الـ COD"):
                st.session_state.suggested_click = "درع حماية الـ COD"
                st.session_state.cyber_v7_pro_query = ""
        with col6:
            if st.button("🎯 قيادة الميزانية"):
                st.session_state.suggested_click = "قيانية الميزانية"
                st.session_state.cyber_v7_pro_query = ""

        st.sidebar.markdown("---")

        # شريط الأسئلة الاحترافي الوردي الثابت لمتجرك بحواف ناصعة
        user_query = st.sidebar.text_input("💬 اكتب سؤالك للمساعد هنا:", key="cyber_v7_pro_query")
        
        if user_query:
            st.session_state.suggested_click = ""
            final_query = user_query
        else:
            final_query = st.session_state.suggested_click
        
        if final_query:
            evaluate_logic_response(final_query)

# دالتان وهميتان لحجز مكان الميزات الأخرى المذكورة في ملفك الرئيسي لمنع أي خطأ تعطل للموقع
def render_marketing_hub(): pass
def render_data_insights(conn): pass
# ========================================================
# الجزء الثالث: عقل المساعد المطور والـ 4 استجابات أولى (ai_helper.py)
# ========================================================

def evaluate_logic_response(query):
    conn = sqlite3.connect("invoices_master_v4.db")
    
    # 1. 📊 تقرير الأرباح والحسابات الشاملة
    if query == "تقرير الأرباح" or "ربح" in query or "حساب" in query:
        df_sales = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conn)
        count_inv = len(df_sales)
        if count_inv > 0:
            total_da = df_sales['final_total'].sum()
            st.sidebar.markdown(f"""
                <div style="background: linear-gradient(135deg, #0d0614 0%, #1c092b 100%); border: 1px solid #ff00ff; box-shadow: 0 0 15px #ff00ff; padding: 15px; border-radius: 10px; text-align: right; direction: rtl; margin-top: 12px;">
                    <h4 style="color: #ff00ff; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0;">🤖 التشخيص المالي للـ AI:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0;">
                        💰 إجمالي المداخيل الحالية: <span style="color: #00fff0; font-weight: bold;">{total_da:,.2f} DA</span><br>
                        📊 عدد الفواتير المسجلة: <span style="color: #00ffcc;">{count_inv} فاتورة</span>
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else: st.sidebar.info("📊 لا توجد فواتير مسجلة حالياً.")
        
    # 2. 📦 جرد المخزن الكلي والتحذير من النفاذ السريع
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
                <div style="background: linear-gradient(135deg, #051214 0%, #09262b 100%); border: 1px solid #00fff0; box-shadow: 0 0 15px #00fff0; padding: 15px; border-radius: 10px; text-align: right; direction: rtl; margin-top: 12px;">
                    <h4 style="color: #00fff0; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0;">🔮 تقرير الجرد اللاسلكي للتنبؤ:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">
                        مجموع القطع بالمستودع: <span style="color: #ff00ff; font-weight: bold;">{total_qty} حبة</span>
                        {low_stock_text}
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else: st.sidebar.info("📦 مستودعك فارغ حالياً.")

    # 3. 📈 تحليل نمو مبيعات المتجر الإلكتروني شهرياً
    elif query == "نمو المبيعات":
        df_sales = pd.read_sql("SELECT month_created, final_total FROM v4_customer_invoices", conn)
        if not df_sales.empty:
            monthly_summary = df_sales.groupby('month_created')['final_total'].sum()
            summary_text = ""
            for month, total in monthly_summary.items():
                summary_text += f"📅 الشهر [ {month} ]: {total:,.2f} DA<br>"
            st.sidebar.markdown(f"""
                <div style="background: linear-gradient(135deg, #0d0614 0%, #1c092b 100%); border: 1px solid #ff00ff; box-shadow: 0 0 15px #ff00ff; padding: 15px; border-radius: 10px; text-align: right; direction: rtl; margin-top: 12px;">
                    <h4 style="color: #ff00ff; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0;">📈 تحليل نمو المبيعات الشهري:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">{summary_text}</p>
                </div>
            """, unsafe_allow_html=True)
        else: st.sidebar.info("📈 لا توجد بيانات كافية لحساب معدلات النمو.")

    # 4. 🗺️ مستشار الولايات ومناطق الشحن الأكثر طلباً للـ COD الجزائري
    elif query == "مستشار الولايات":
        df_sales = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conn)
        count_inv = len(df_sales)
        if count_inv > 0:
            st.sidebar.markdown(f"""
                <div style="background: linear-gradient(135deg, #051214 0%, #09262b 100%); border: 1px solid #00fff0; box-shadow: 0 0 15px #00fff0; padding: 15px; border-radius: 10px; text-align: right; direction: rtl; margin-top: 12px;">
                    <h4 style="color: #00fff0; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0;">🗺️ مستشار توجيه الحملات الجزائريّ:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">
                        حجم حركة الفواتير الفعليّة: <b>{count_inv} طلبية نشطة</b>.<br>
                        🎯 <b>توصية الـ AI:</b> نوصي بتوجيه وتكثيف الميزانيات الترويجية نحو ولايات <b>(الجزائر العاصمة، وهران، سطيف، قسنطينة)</b> لضمان أعلى معدل تسليم.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else: st.sidebar.info("🗺️ قم بإصدار الفواتير أولاً لتنشيط خريطة الولايات الذكية.")
        
    # [تكملة بقية الاستجابات في الجزء الرابع تالياً...]
    # 5. 💰 حساب متوسط قيمة الأرباح لكل فاتورة صادرة
    elif query == "متوسط الأرباح":
        df_sales = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conn)
        count_inv = len(df_sales)
        if count_inv > 0:
            total_da = df_sales['final_total'].sum()
            avg_profit = total_da / count_inv
            st.sidebar.markdown(f"""
                <div style="background: linear-gradient(135deg, #0d0614 0%, #1c092b 100%); border: 1px solid #ff00ff; box-shadow: 0 0 15px #ff00ff; padding: 15px; border-radius: 10px; text-align: right; direction: rtl; margin-top: 12px;">
                    <h4 style="color: #ff00ff; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0;">💰 متوسط مداخيل الطلبيات الصافي:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">
                        💸 <b>المتوسط المحقق:</b> <span style="color: #00fff0; font-weight: bold; font-size: 15px;">{avg_profit:,.2f} DA</span><br>
                        💡 استخدم ميزة الـ Upsell لرفع معدل الفاتورة للزبون.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else: st.sidebar.info("💰 لا توجد فواتير صادرة لتقييم المتوسط المالي.")

    # 6. 🛡️ خوارزمية درع حماية الـ COD ومكافحة الخسائر الماليّة المشبوهة
    elif query == "درع حماية الـ COD":
        df_sales = pd.read_sql("SELECT customer_phone, COUNT(*) as order_count FROM v4_customer_invoices GROUP BY customer_phone HAVING order_count > 1", conn)
        if not df_sales.empty:
            fraud_count = len(df_sales)
            st.sidebar.markdown(f"""
                <div style="background: linear-gradient(135deg, #1a0505 0%, #3a0a0a 100%); border: 2px solid #ff0055; box-shadow: 0 0 20px #ff0055; padding: 15px; border-radius: 10px; text-align: right; direction: rtl; margin-top: 12px;">
                    <h4 style="color: #ff0055; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0; text-shadow: 0 0 5px #ff0055;">🚨 نظام درع مكافحة الخسائر الماليّة:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">
                        ⚠️ <b>تم استكشاف ثغرة شحن:</b> تم العثور على <b>{fraud_count} زبائن كرروا طلبياتهم بنفس رقم الهاتف</b> في الفواتير v4!<br>
                        💡 اتصل بهم لتأكيد الطلب يدوياً قبل التوصيل للولايات لتفادي مصاريف الـ Retour.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.sidebar.markdown("""
                <div style="background: linear-gradient(135deg, #05140b 0%, #0a3a18 100%); border: 2px solid #00ff66; box-shadow: 0 0 15px #00ff66; padding: 15px; border-radius: 10px; text-align: right; direction: rtl; margin-top: 12px;">
                    <h4 style="color: #00ff66; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0;">🛡️ درع الأمان السيبراني للـ COD:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">✅ <b>مؤشر أمن المبيعات:</b> 100% الصفقات آمنة ونظيفة. لا توجد أي أرقام هواتف مكررة.</p>
                </div>
            """, unsafe_allow_html=True)

    # 7. 🎯 مركز توجيه وقيادة الميزانيات الترويجية
    elif query == "قيانية الميزانية":
        df_invoices = pd.read_sql("SELECT product_name, SUM(final_total) as revenue FROM v4_customer_invoices GROUP BY product_name ORDER BY revenue DESC LIMIT 1", conn)
        df_stock = pd.read_sql("SELECT SUM(available_qty) as stock_qty FROM store_stock", conn)
        try: total_stock = int(df_stock['stock_qty'].values) if not df_stock.empty else 0
        except: total_stock = 0

        if not df_invoices.empty:
            top_product = df_invoices['product_name'].values
            top_revenue = df_invoices['revenue'].values
            st.sidebar.markdown(f"""
                <div style="background: linear-gradient(135deg, #051214 0%, #0a2d33 100%); border: 2px solid #00fff0; box-shadow: 0 0 20px #00fff0; padding: 15px; border-radius: 10px; text-align: right; direction: rtl; margin-top: 12px;">
                    <h4 style="color: #00fff0; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0; text-shadow: 0 0 5px #00fff0;">🎯 مركز القيادة وتوجيه الميزانيات:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">
                        📦 المنتج الأكثر طلباً: <b>[ {top_product} ]</b> بمداخل بلغت <span style="color:#ff00ff; font-weight:bold;">{top_revenue:,.2f} DA</span>.<br>
                        🧭 نوصي بتركيز 60% من التمويل الإعلاني نحو هذا المنتج في ولايات الوسط لتعظيم الأأرباح.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else: st.sidebar.info("🎯 قم بتسجيل بعض المبيعات أولاً لتفعيل مركز القيادة.")
            
    # 8. الإجابة الذكية الافتراضية السيبرانية لحماية النظام
    else:
        st.sidebar.markdown("""
            <div style="border-right: 3px solid #ffffff; padding-right: 10px; margin-top: 12px; text-align: right; direction: rtl;">
                <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 12.5px; margin: 0;">الأنظمة السيبرانية v4 متصلة بكفاءة. اضغط على خيارات التحكم الـ 8 لاستدعاء بطاقات الأرقام والولايات فوراً بـ **DA**.</p>
            </div>
        """, unsafe_allow_html=True)
    conn.close()
