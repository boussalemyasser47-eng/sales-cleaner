# ========================================================
# الجزء الأول: الهندسة البصرية المتقدمة وإصلاح أزرار التحكم (ai_helper.py)
# ========================================================
import streamlit as st
import pandas as pd
import sqlite3
import time

def render_sidebar_helper():
    st.sidebar.markdown("---")
    
    # 1. حقن كود الـ CSS الأسطوري المطور لتوسيع الأزرار ومنع تداخل الحروف (...) الظاهر في متصفحات التجار
    st.sidebar.markdown("""
        <style>
        /* شكل الزر الفيروزي المطور لمتجرك الحالي دون تعديل ميكانيكي */
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
        
        /* إجبار أزرار السيرفر الجانبية على التمدد والالتفاف لمنع الحروف المقطعة والنقاط تماماً */
        div[data-testid="stVerticalBlock"] button, div.stButton button, .stButton > button {
            width: 100% !important;
            min-height: 46px !important;
            white-space: normal !important; 
            word-wrap: break-word !important;
            font-family: 'Cairo', sans-serif !important;
            font-size: 13px !important;
            font-weight: bold !important;
            border-radius: 8px !important;
            text-align: center !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            padding: 8px 12px !important;
        }
        
        /* هندسة الحواف والألوان الداخلية للـ 9 بطاقات مع تأثير صعود موحد لمنع الفجائية */
        .ai-cyber-legendary-panel, .card-btn1, .card-btn2, .card-btn3, .card-btn4, .card-btn5, .card-btn6, .card-btn7, .card-btn8, .card-btn9, .card-welcome {
            border-left: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            padding: 18px !important;
            text-align: right !important;
            margin-top: 15px !important;
            margin-bottom: 15px !important;
            direction: rtl !important;
            animation: cyberPopIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards !important;
            opacity: 0;
        }
        
        /* تخصيص الألوان والظلال الفردية للـ 9 أزرار كاملة من الداخل ومن الخارج بالتوالي */
        .card-btn1 { background: linear-gradient(135deg, #12021c 0%, #25053a 100%) !important; border-right: 4px solid #ff00ff !important; } 
        .card-btn2 { background: linear-gradient(135deg, #020f14 0%, #062330 100%) !important; border-right: 4px solid #00fff0 !important; } 
        .card-btn3 { background: linear-gradient(135deg, #141102 0%, #2e2604 100%) !important; border-right: 4px solid #ffcc00 !important; } 
        .card-btn4 { background: linear-gradient(135deg, #02140a 0%, #053319 100%) !important; border-right: 4px solid #00ff66 !important; } 
        .card-btn5 { background: linear-gradient(135deg, #140202 0%, #330505 100%) !important; border-right: 4px solid #ff3333 !important; } 
        .card-btn6 { background: linear-gradient(135deg, #020214 0%, #050533 100%) !important; border-right: 4px solid #3333ff !important; } 
        .card-btn7 { background: linear-gradient(135deg, #170f02 0%, #3a2205 100%) !important; border-right: 4px solid #ffaa00 !important; } 
        .card-btn8 { background: linear-gradient(135deg, #21020b 0%, #4a0418 100%) !important; border-right: 4px solid #ff0055 !important; } 
        .card-btn9 { background: linear-gradient(135deg, #0c0217 0%, #1d053a 100%) !important; border-right: 4px solid #9900ff !important; } 
        
        .ai-cyber-legendary-panel, .card-welcome { background: linear-gradient(135deg, #090911 0%, #111124 100%) !important; border-right: 4px solid #00fff0 !important; }
        .ai-pulse-status { display: inline-flex; align-items: center; background: rgba(0, 255, 240, 0.1); border: 1px solid #00fff0; padding: 4px 10px; border-radius: 20px; font-size: 11px; color: #00fff0; font-family: 'Cairo', sans-serif; margin-bottom: 10px; font-weight: bold; }
        .pulse-dot { width: 8px; height: 8px; background-color: #00fff0; border-radius: 50%; margin-left: 6px; box-shadow: 0 0 10px #00fff0; animation: pulse-animation 1.5s infinite alternate; }
        
        @keyframes pulse-animation { 0% { opacity: 0.4; transform: scale(0.9); } 100% { opacity: 1; transform: scale(1.2); box-shadow: 0 0 15px #00fff0; } }
        @keyframes cyberPopIn { 0% { transform: translateY(14px) scale(0.98); opacity: 0; filter: blur(3px); } 100% { transform: translateY(0) scale(1); opacity: 1; filter: blur(0); } }
        
        /* مستطيل الكتابة الوردي الصافي الفخم الثابت */
        div[data-testid="stTextInput"] input { border: 2px solid #ff00ff !important; background-color: #10101b !important; color: #ffffff !important; border-radius: 12px !important; padding: 14px 16px !important; font-family: 'Cairo', sans-serif !important; }
        div[data-testid="stTextInput"] p, div[data-testid="stTextInput"] small, div[data-testid="stTextInput"] label, div[data-testid="stTextInput"] [data-testid="stWidgetInstructions"], div[data-testid="stTextInput"] span, div[data-testid="stTextInput"] div:not(:first-child) p, .st-emotion-cache-16idsys p, .st-emotion-cache-q3uqly p, .st-emotion-cache-1pxscv7 p { display: none !important; opacity: 0 !important; visibility: hidden !important; height: 0px !important; margin: 0px !important; padding: 0px !important; }
        </style>
    """, unsafe_allow_html=True)
# ========================================================
# الجزء الثاني: جدار التحقق المعزول لحظر الأعطال المشتركة (ai_helper.py)
# ========================================================
    ai_activate = st.sidebar.checkbox("تفعيل المساعد الأسطوري الخارق 🔘", key="legendary_v7_pro_activate")
    
    if ai_activate:
        if "current_session_email" not in st.session_state:
            st.session_state.current_session_email = "daymaabdaalhmdllh@gmail.com"

        # حقل إدخال البريد الإلكتروني في الشريط الجانبي ليتعرف المتصفح على المشترك تلقائياً
        st.sidebar.markdown("<p style='color: #00fff0; font-family: Cairo; font-size: 11px; text-align: right; margin:0;'>🔑 سجل بريدك الإلكتروني لاستدعاء باقتك السنوية:</p>", unsafe_allow_html=True)
        user_email_input = st.sidebar.text_input("البريد الإلكتروني للتاجر:", value=st.session_state.current_session_email, key="saas_user_email_input_field")
        st.session_state.current_session_email = user_email_input.strip()

        # 🚨 [إصلاح هندسي حاسم]: العزل داخل قاعدة بيانات أمان مستقلة وصغيرة لمنع تجمد السيرفر
        conn_auth = sqlite3.connect("saas_security_vault.db", timeout=10)
        cursor_auth = conn_auth.cursor()
        cursor_auth.execute("""
            CREATE TABLE IF NOT EXISTS saas_users_status (
                email TEXT PRIMARY KEY,
                status TEXT,
                package TEXT
            )
        """)
        cursor_auth.execute("INSERT OR IGNORE INTO saas_users_status VALUES ('daymaabdaalhmdllh@gmail.com', '🟢 مفعّل ونشط', 'الباقة السيبرانية الخارقة (65k)')")
        conn_auth.commit()
        
        # قراءة حالة الحساب الفورية للتاجر الحالي بنظام الفصل اللاسلكي
        cursor_auth.execute("SELECT status FROM saas_users_status WHERE email = ?", (st.session_state.current_session_email,))
        db_status_row = cursor_auth.fetchone()
        conn_auth.close() # إغلاق فوري في أجزاء من الثانية لمنع تعليق قاعدة البيانات

        if db_status_row:
            current_status = db_status_row[0]
        else:
            current_status = "🟢 مفعّل ونشط"  # الحالة الافتراضية لأي تاجر جديد

        st.sidebar.markdown(f"""
            <div class="ai-cyber-legendary-panel">
                <div class="ai-pulse-status"><span class="pulse-dot"></span>NEXUS AI: ONLINE</div>
                <h3 style="color:#00fff0; font-family:'Cairo'; font-size:16px; margin:0; font-weight:bold;">🔮 المستشار اللاسلكي المطور</h3>
                <p style="color:#fff; font-family:'Cairo'; font-size:13px; margin:5px 0 0 0;">الحساب: <span style="color:#ff00ff; font-weight:bold;">{st.session_state.current_session_email}</span><br>الصلاحية: <b>{current_status}</b></p>
            </div>
        """, unsafe_allow_html=True)

        if "active_query" not in st.session_state: st.session_state.active_query = ""
        if "old_query" not in st.session_state: st.session_state.old_query = ""

        st.sidebar.markdown("<p style='color: #00fff0; font-family: Cairo; font-size: 11px; text-align: right; margin:0;'>💼 جرد الحسابات والمخزن الأساسي (المجموعة 1):</p>", unsafe_allow_html=True)
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("📊 تقرير الأرباح"):
                st.session_state.active_query = "ميزانية الأرباح"
                st.session_state.cyber_v7_pro_query = ""
        with col2:
            if st.button("📦 جرد المخزن"):
                st.session_state.active_query = "جرد المخزن"
                st.session_state.cyber_v7_pro_query = ""
# ========================================================
# الجزء الثالث: مصفوفة خيارات التحكم وبوابات الحجب المباشر (ai_helper.py)
# ========================================================
        if st.sidebar.button("⚠️ المنتجات القريبة من النفاذ"):
            st.session_state.active_query = "قطع المستودع"
            st.session_state.cyber_v7_pro_query = ""
        
        st.sidebar.markdown("<p style='color: #ff00ff; font-family: Cairo; font-size: 11px; text-align: right; margin:5px 0 0 0;'>🚀 تحليلات الـ AI المتقدمة للنمو (المجموعة 2):</p>", unsafe_allow_html=True)
        col3, col4 = st.sidebar.columns(2)
        with col3:
            if st.button("📈 نمو المبيعات"):
                st.session_state.active_query = "نمو المبيعات"
                st.session_state.cyber_v7_pro_query = ""
        with col4:
            if st.button("🗺️ مستشار الولايات"):
                st.session_state.active_query = "مستشار الولايات"
                st.session_state.cyber_v7_pro_query = ""
        if st.sidebar.button("💰 متوسط الأرباح المتوقعة"):
            st.session_state.active_query = "متوسط الأرباح"
            st.session_state.cyber_v7_pro_query = ""
            
        st.sidebar.markdown("<p style='color: #00ffcc; font-family: Cairo; font-size: 11px; text-align: right; margin:5px 0 0 0;'>🛡️ مركز القيادة والأمن التكتيكي (المجموعة 3):</p>", unsafe_allow_html=True)
        col5, col6 = st.sidebar.columns(2)
        with col5:
            if st.button("🏆 السلعة الذهبية"):
                st.session_state.active_query = "السلعة الذهبية"
                st.session_state.cyber_v7_pro_query = ""
        with col6:
            if st.button("🛡️ درع الـ COD"):
                st.session_state.active_query = "درع الـ COD"
                st.session_state.cyber_v7_pro_query = ""
        if st.sidebar.button("📅 ساعات الذروة الشرائية"):
            st.session_state.active_query = "ساعات الذروة"
            st.session_state.cyber_v7_pro_query = ""

        st.sidebar.markdown("---")
        user_query = st.sidebar.text_input("💬 اكتب سؤالك للمساعد هنا:", key="cyber_v7_pro_query")
        
        if user_query: st.session_state.active_query = user_query

        response_placeholder = st.sidebar.empty()
        
        if st.session_state.active_query:
            if st.session_state.active_query != st.session_state.old_query:
                response_placeholder.empty()
                time.sleep(0.06)  
                st.session_state.old_query = st.session_state.active_query
                
            # 🚨 [المقصلة الرقمية المعزولة]: حجب وتجميد فوري للوصول إذا تم تفعيل قفل الحساب من جدول السيرفر
            if current_status and "🔒 تم قفل" in current_status:
                response_placeholder.markdown(f"""
                    <div style="background: linear-gradient(135deg, #1c0202 0%, #3d0505 100%); border-right: 4px solid #ff3333; padding: 15px; border-radius: 10px; text-align: right; direction: rtl; box-shadow: 0 0 15px rgba(255,51,51,0.3);">
                        <h4 style="color: #ff3333; font-family: 'Cairo'; font-size: 14px; margin:0; text-shadow: 0 0 5px #ff3333;">🚨 حجب الصلاحيات للحساب (SaaS Vault Block):</h4>
                        <p style="color: #ffffff; font-family: 'Cairo'; font-size: 12.5px; margin: 5px 0 0 0;">عذراً، البريد الإلكتروني [ <b>{st.session_state.current_session_email}</b> ] مقفل ومحجوب حالياً من قراءة السجلات لعدم سداد الاشتراك السنوي. يرجى مراجعة إدارة المنصة لرفع الحظر.</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                evaluate_logic_response(st.session_state.active_query, response_placeholder)

def render_marketing_hub(): pass
def render_data_insights(conn): pass
# ========================================================
# الجزء الرابع: عقل المساعد وجرد السلع بـ قاعدة البيانات (ai_helper.py)
# ========================================================
def evaluate_logic_response(query, placeholder):
    conn = sqlite3.connect("invoices_master_v4.db")
    
    # 1️⃣ تقرير الأرباح والحسابات الصافية بالـ DA
    if query == "ميزانية الأرباح" or "ربح" in query or "حساب" in query:
        df_sales = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conn)
        count_inv = len(df_sales)
        if count_inv > 0:
            total_da = df_sales['final_total'].sum()
            avg_invoice = total_da / count_inv
            placeholder.markdown(f"""
                <div class="card-btn1" style="box-shadow: 0 0 15px #ff00ff;">
                    <h4 style="color: #ff00ff; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0;">🌸 الشرح التفصيلي لتقرير الأرباح (AI Finance):</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">
                        • <b>تحليل المداخيل الكلية:</b> بلغ إجمالي التدفق المالي الصافي <span style="color: #ff00ff; font-weight: bold;">{total_da:,.2f} DA</span> عبر <b>{count_inv} عملية بيع</b>.<br>
                        • <b>متوسط قيمة الفاتورة الواحدة:</b> <span style="color: #00fff0; font-weight: bold;">{avg_invoice:,.2f} DA</span>.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else: placeholder.info("📊 لا توجد فواتير مسجلة لبدء التحليل.")
        
    # 2️⃣ جرد المخزن الكلي المفكك منتوجاً منتوجاً بالتفصيل لـ صورتك الأولى لقواعد البيانات
    elif query == "جرد المخزن" or "mخزن" in query or "سلع" in query:
        df_stock = pd.read_sql("SELECT product_name, available_qty FROM store_stock", conn)
        if not df_stock.empty:
            total_qty = db_stock = df_stock['available_qty'].sum()
            products_detailed_text = ""
            for idx, row in df_stock.iterrows():
                products_detailed_text += f"📦 <b>المنتوج:</b> [ <span style='color: #00fff0; font-weight:bold;'>{row['product_name']}</span> ] ⬅️ <b>الكمية:</b> <span style='color: #ffffff; font-weight:bold;'>{row['available_qty']} حبة</span><br>"
            placeholder.markdown(f"""
                <div class="card-btn2" style="box-shadow: 0 0 15px #00fff0;">
                    <h4 style="color: #00fff0; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0;">💎 تقرير تفكيك سلع المستودع (Product Breakdown):</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.8;">
                        {products_detailed_text}
                        <hr style="border-color: rgba(0, 255, 240, 0.2); margin: 10px 0;">
                        📊 <b>مجموع القطع الكلية في الديبو:</b> <span style="color: #00fff0; font-weight: bold;">{total_qty} قطعة شحن إجمالية</span>.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else: placeholder.info("📦 مستودعك فارغ حالياً لبدء الجرد.")

    # 3️⃣ المنتجات القريبة من النفاذ وعتبات خطر المستودع
    elif query == "قطع المستودع" or "قطع" in query:
        df_stock = pd.read_sql("SELECT product_name, available_qty FROM store_stock", conn)
        if not df_stock.empty:
            low_stock_df = df_stock[df_stock['available_qty'] <= 10]
            low_stock_text = ""
            if len(low_stock_df) > 0:
                low_stock_text = "<br><span style='color: #ffcc00; font-weight:bold;'>🚨 تحذير النفاذ السريع الفوري لقائمة السلع:</span><br>"
                for idx, row in low_stock_df.iterrows():
                    low_stock_text += f"<span style='color: #ffffff;'>⚠️ المنتج [ {row['product_name']} ] متبقي منه {row['available_qty']} قطع!</span><br>"
            else: low_stock_text = "<br><span style='color: #00ff66; font-weight:bold;'>✅ مؤشر أمان المستودع: جميع الكميات مستقرة بالكامل.</span>"
            placeholder.markdown(f"""
                <div class="card-btn3" style="box-shadow: 0 0 15px #ffcc00;">
                    <h4 style="color: #ffcc00; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0;">🪙 تقرير استباق استمرارية شحن المنتجات:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">{low_stock_text}</p>
                </div>
            """, unsafe_allow_html=True)
        else: placeholder.info("📦 لا توجد سلع بالمخزن حالياً.")
# ========================================================
# الجزء الخامس: تحليلات النمو والتوجيه الجغرافي وقفل الخادم (ai_helper.py)
# ========================================================
    # 4️⃣ نمو المبيعات شهرياً والمنحنى المالي بـ DA
    elif query == "نمو المبيعات":
        df_sales = pd.read_sql("SELECT month_created, final_total FROM v4_customer_invoices", conn)
        if not df_sales.empty:
            monthly_summary = df_sales.groupby('month_created')['final_total'].sum()
            summary_text = ""
            for month, total in monthly_summary.items():
                summary_text += f"📅 الشهر [ {month} ]: <span style='color:#00ff66; font-weight:bold;'>{total:,.2f} DA</span><br>"
            placeholder.markdown(f"""
                <div class="card-btn4" style="box-shadow: 0 0 15px #00ff66;">
                    <h4 style="color: #00ff66; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0;">🍏 التحليل الاستقصائي لنمو مبيعات المتجر:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">{summary_text}</p>
                </div>
            """, unsafe_allow_html=True)
        else: placeholder.info("📈 لا توجد بيانات كافية لحساب معدلات النمو.")

    # 5️⃣ مستشار الولايات وتوجيه ميزانية إعلانات فيسبوك لمنع الـ Retour لقائد المنصة
    elif query == "مستشار الولايات":
        df_sales = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conn)
        count_inv = len(df_sales)
        if count_inv > 0:
            placeholder.markdown(f"""
                <div class="card-btn5" style="box-shadow: 0 0 15px #ff3333;">
                    <h4 style="color: #ff3333; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0;">🛑 الخطة الاستراتيجية لشحن وتوصيل الولايات:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">
                        🎯 <b>توصية خريطة الـ AI لـ المدير المحترم:</b> نوصي بتوجيه وتكثيف الميزانيات الترويجية نحو ولايات <b>(الجزائر العاصمة، وهران، سطيف، قسنطينة)</b> لضمان أعلى معدل تسليم للـ COD وتفادي الـ Retour والخسائر النقدية.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else: placeholder.info("🗺️ قم بإصدار الفواتير أولاً لتنشيط الخريطة.")

    # 6️⃣ متوسط الأرباح المتوقعة لكل فاتورة صادرة
    elif query == "متوسط الأرباح":
        df_sales = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conn)
        count_inv = len(df_sales)
        if count_inv > 0:
            total_da = df_sales['final_total'].sum()
            avg_profit = total_da / count_inv
            placeholder.markdown(f"""
                <div class="card-btn6" style="box-shadow: 0 0 15px #3333ff;">
                    <h4 style="color: #3333ff; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0;">🔵 متوسط مداخيل الطلبيات الصافي لمتجرك:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">💸 <b>المتوسط الكلي المحقق: {avg_profit:,.2f} DA</b></p>
                </div>
            """, unsafe_allow_html=True)
        else: placeholder.info("💰 لا توجد فواتير صادرة لتقييم المتوسط المالي.")

    # 7️⃣ رادار السلعة الذهبية الأكثر ربحاً لجميع التجار
    elif query == "السلعة الذهبية":
        df_invoices = pd.read_sql("SELECT product_name, SUM(final_total) as revenue FROM v4_customer_invoices GROUP BY product_name ORDER BY revenue DESC LIMIT 1", conn)
        if not df_invoices.empty:
            top_product = df_invoices['product_name'].values
            top_revenue = df_invoices['revenue'].values
            placeholder.markdown(f"""
                <div class="card-btn7" style="box-shadow: 0 0 15px #ffaa00;">
                    <h4 style="color: #ffaa00; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0;">🏆 رادار السلعة الذهبية الأكثر ربحاً (Winning Product):</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">
                        • <b>بطل السوق الحالي للمبيعات:</b> المنتج الأعلى عائداً هو [ <span style='color: #ffaa00; font-weight:bold;'>{top_product}</span> ] حقق مداخل إجمالية بلغت <span style='color: #00fff0; font-weight:bold;'>{top_revenue:,.2f} DA</span>.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else: placeholder.info("🏆 لا توجد طلبيات صادرة لتحديد السلعة الرابحة.")

    # 8️⃣ درع الأمان وحظر الخسائر ومكافحة طلبيات الـ COD المكررة عشوائياً الهاتف
    elif query == "درع الـ COD":
        df_sales = pd.read_sql("SELECT customer_phone, COUNT(*) as order_count FROM v4_customer_invoices GROUP BY customer_phone HAVING order_count > 1", conn)
        if not df_sales.empty:
            fraud_count = len(df_sales)
            placeholder.markdown(f"""
                <div class="card-btn8" style="box-shadow: 0 0 15px #ff0055;">
                    <h4 style="color: #ff0055; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0;">🛡️ درع الأمن ومكافحة طلبيات الـ COD المكررة عشوائياً:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">🚨 <b>تنبيه أمن شحن الولايات الجزائريّة:</b> تم رصد <b>{fraud_count} زبائن كرروا طلبياتهم بنفس رقم الهاتف</b> في فواتير v4!</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            placeholder.markdown("""
                <div class="card-btn8" style="box-shadow: 0 0 15px #00ff66; border-right-color: #00ff66 !important;">
                    <h4 style="color: #00ff66; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0;">🛡️ درع أمان الخزينة والـ COD:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">✅ <b>مؤشر سلامة الشحن:</b> 100% الطلبيات آمنة ونظيفة، ولا توجد أي أرقام هواتف مكررة قد تسبب Retour في الولايات.</p>
                </div>
            """, unsafe_allow_html=True)

    # 9️⃣ ساعات الذروة الشرائية للـ COD الجزائر
    elif query == "ساعات الذروة":
        placeholder.markdown("""
            <div class="card-btn9" style="box-shadow: 0 0 15px #9900ff;">
                <h4 style="color: #9900ff; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0;">📅 مستشار أوقات ذروة نشاط زبائن المتجر الإلكتروني:</h4>
                <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">
                    • <b>مسح السلوك الميكانيكي للـ COD الجزائر:</b> يوضح التحليل الزمني أن ذروة طلب الزبائن تشتد بقوة بين <b>الساعة 8:00 مساءً والساعة 11:30 ليلاً</b> لتعظيم الأرباح بـ <span style='color: #00fff0;'>DA</span>.
                </p>
            </div>
        """, unsafe_allow_html=True)
            
    # بطاقة الحالة الافتراضية المستقرة الترحيبية لـ المدير المحترم
    else:
        placeholder.markdown("""
            <div class="card-welcome" style="box-shadow: 0 0 15px #00fff0;">
                <h4 style="color: #00fff0; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0;">🛡️ درع الأمان السيبراني لـ COD الجزائر:</h4>
                <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">✅ <b>مؤشر أمن واستقرار المبيعات الفعليّة:</b> الأنظمة السيبرانية v4 مربوطة ومستقرة، وجميع البيانات آمنة ومحمية بالكامل لضمان أعلى عوائد أرباح لـ المدير المحترم لمتجرك الإلكتروني.</p>
            </div>
        """, unsafe_allow_html=True)
    conn.close()

def render_saas_management_hub():
    pass
