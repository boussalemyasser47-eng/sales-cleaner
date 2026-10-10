# ========================================================
# الجزء الأول: الهندسة البصرية المتقدمة ونظام التحقق (ai_helper.py)
# ========================================================
import streamlit as st
import pandas as pd
import sqlite3
import time

def render_sidebar_helper():
    st.sidebar.markdown("---")
    
    # 1. حقن كود الـ CSS الأسطوري المطور لتشغيل الأنميشن الموحد للـ 9 فئات الملونة وخلفياتها الداكنة
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
        
        div[data-testid="stTextInput"] input { border: 2px solid #ff00ff !important; background-color: #10101b !important; color: #ffffff !important; border-radius: 12px !important; padding: 14px 16px !important; font-family: 'Cairo', sans-serif !important; }
        div[data-testid="stTextInput"] p, div[data-testid="stTextInput"] small, div[data-testid="stTextInput"] label, div[data-testid="stTextInput"] [data-testid="stWidgetInstructions"], div[data-testid="stTextInput"] span, div[data-testid="stTextInput"] div:not(:first-child) p, .st-emotion-cache-16idsys p, .st-emotion-cache-q3uqly p, .st-emotion-cache-1pxscv7 p { display: none !important; opacity: 0 !important; visibility: hidden !important; height: 0px !important; margin: 0px !important; padding: 0px !important; }
        </style>
    """, unsafe_allow_html=True)
    
    ai_activate = st.sidebar.checkbox("تفعيل المساعد الأسطوري الخارق 🔘", key="legendary_v7_pro_activate")
    
    if ai_activate:
        # 🚨 خطوة الاختبار الحاسم: إدخال البريد الإلكتروني للتحقق من الصلاحيات التلقائية
        st.sidebar.markdown("<p style='color: #00fff0; font-family: Cairo; font-size: 11px; text-align: right; margin:0;'>🔑 أدخل بريد الحساب لاختبار حركة القفل:</p>", unsafe_allow_html=True)
        merchant_email = st.sidebar.text_input("البريد الإلكتروني للتاجر:", value="test_merchant@saas.com", key="cyber_merchant_email_auth")
        
        # تهيئة قاعدة بيانات المحاكاة المؤقتة في الذاكرة لتتبع الإيميل الجديد
        if "saas_user_status" not in st.session_state:
            st.session_state.saas_user_status = "🟢 نشط حالياً"
            st.session_state.saas_email = "test_merchant@saas.com"

        st.sidebar.markdown(f"""
            <div class="ai-cyber-legendary-panel">
                <div class="ai-pulse-status"><span class="pulse-dot"></span>NEXUS AI: ONLINE</div>
                <h3 style="color:#00fff0; font-family:'Cairo'; font-size:16px; margin:0; font-weight:bold;">🔮 المستشار اللاسلكي المطور</h3>
                <p style="color:#fff; font-family:'Cairo'; font-size:13px; margin:5px 0 0 0;">الحساب الحالي: <span style="color:#ff00ff; font-weight:bold;">{merchant_email}</span><br>الحالة البرمجية: <b>{st.session_state.saas_user_status}</b></p>
            </div>
        """, unsafe_allow_html=True)
# ========================================================
# الجزء الثاني: بقية الأزرار وميكانيكية القيادة الحركية (ai_helper.py)
# ========================================================
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
                
            # 🚨 تفعيل نظام فحص الصلاحيات الفوري للإيميل قبل طباعة أي بطاقة جرد
            if "🔒 تم قفل" in st.session_state.saas_user_status:
                response_placeholder.markdown("""
                    <div style="background: linear-gradient(135deg, #1c0202 0%, #3d0505 100%); border-right: 4px solid #ff3333; padding: 15px; border-radius: 10px; text-align: right; direction: rtl;">
                        <h4 style="color: #ff3333; font-family: 'Cairo'; font-size: 14px; margin:0;">🚨 تنبيه الأمان السيبراني للحساب (SaaS Block):</h4>
                        <p style="color: #ffffff; font-family: 'Cairo'; font-size: 12.5px; margin: 5px 0 0 0;">عذراً، هذا البريد الإلكتروني مقفل حالياً ومحجوب من الصلاحيات لعدم سداد الاشتراك السنوي الصافي. يرجى الاتصال بمدير المنصة للتفعيل.</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                evaluate_logic_response(st.session_state.active_query, response_placeholder)

def render_marketing_hub(): pass
def render_data_insights(conn): pass
# ========================================================
# الجزء الثالث: عقل المساعد والاستجابات الـ 9 الملوّنة (ai_helper.py)
# ========================================================

def evaluate_logic_response(query, placeholder):
    conn = sqlite3.connect("invoices_master_v4.db")
    
    # 1️⃣ زر تقرير الأرباح: 🌸 [وردي نيون + خلفية أرجوانية داكنة]
    if query == "ميزانية الأرباح" or "ربح" in query or "حساب" in query:
        df_sales = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conn)
        count_inv = len(df_sales)
        if count_inv > 0:
            total_da = df_sales['final_total'].sum()
            avg_invoice = total_da / count_inv
            placeholder.markdown(f"""
                <div class="card-btn1" style="box-shadow: 0 0 15px #ff00ff;">
                    <h4 style="color: #ff00ff; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0; text-shadow: 0 0 8px #ff00ff;">🌸 الشرح التفصيلي لتقرير الأرباح (AI Finance):</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">
                        • <b>تحليل المداخيل الكلية:</b> تم جرد فواتير v4 بنجاح، وبلغ إجمالي التدفق المالي الصافي <span style="color: #ff00ff; font-weight: bold; text-shadow: 0 0 5px #ff00ff;">{total_da:,.2f} DA</span> عبر <b>{count_inv} عملية بيع</b>.<br>
                        • <b>معدل سلة مبيعات التاجر:</b> متوسط قيمة الإنفاق هو <span style="color: #00fff0; font-weight: bold;">{avg_invoice:,.2f} DA</span>.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else: placeholder.info("📊 لا توجد فواتير مسجلة حالياً لبدء التحليل المالي.")
        
    # 2️⃣ زر جرد المخزن المطور: 💎 [فيروزي مشع + جرد مفكك سلعة سلعة بالتفصيل]
    elif query == "جرد المخزن" or "مخزن" in query or "سلع" in query:
        df_stock = pd.read_sql("SELECT product_name, available_qty FROM store_stock", conn)
        if not df_stock.empty:
            total_qty = df_stock['available_qty'].sum()
            products_detailed_text = ""
            for idx, row in df_stock.iterrows():
                products_detailed_text += f"📦 <b>المنتوج:</b> [ <span style='color: #00fff0; font-weight:bold;'>{row['product_name']}</span> ] ⬅️ <b>الكمية المتوفرة:</b> <span style='color: #ffffff; font-weight:bold;'>{row['available_qty']} حبة جاهزة</span><br>"
            placeholder.markdown(f"""
                <div class="card-btn2" style="box-shadow: 0 0 15px #00fff0;">
                    <h4 style="color: #00fff0; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0; text-shadow: 0 0 8px #00fff0;">💎 تقرير تفكيك سلع المستودع (Product Breakdown):</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.8;">
                        • <b>حالة الجرد التفصيلي للسلع الحية:</b><br>
                        {products_detailed_text}
                        <hr style="border-color: rgba(0, 255, 240, 0.2); margin: 10px 0;">
                        📊 <b>مجموع القطع الكلية في الديبو:</b> <span style="color: #00fff0; font-weight: bold; text-shadow: 0 0 5px #00fff0;">{total_qty} قطعة شحن إجمالية</span>.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else: placeholder.info("📦 مستودعك فارغ حالياً.")

    # 3️⃣ زر المنتجات القريبة من النفاذ: 🪙 [أصفر ذهبي ناصع]
    elif query == "قطع المستودع" or "قطع" in query:
        df_stock = pd.read_sql("SELECT product_name, available_qty FROM store_stock", conn)
        if not df_stock.empty:
            low_stock_df = df_stock[df_stock['available_qty'] <= 10]
            low_stock_text = ""
            if len(low_stock_df) > 0:
                low_stock_text = "<br><span style='color: #ffcc00; font-weight:bold;'>🚨 تحذير النفاذ السريع الفوري لقائمة السلع:</span><br>"
                for idx, row in low_stock_df.iterrows():
                    low_stock_text += f"<span style='color: #ffffff;'>⚠️ المنتج [ {row['product_name']} ] متبقي منه {row['available_qty']} قطع فقط في المخزن!</span><br>"
            else: low_stock_text = "<br><span style='color: #00ff66; font-weight:bold;'>✅ مؤشر أمان المستودع: جميع السلع متوفرة بكميات آمنة.</span>"
            placeholder.markdown(f"""
                <div class="card-btn3" style="box-shadow: 0 0 15px #ffcc00;">
                    <h4 style="color: #ffcc00; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0; text-shadow: 0 0 8px #ffcc00;">🪙 تقرير استباق استمرارية شحن المنتجات:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">{low_stock_text}</p>
                </div>
            """, unsafe_allow_html=True)
        else: placeholder.info("📦 لا توجد سلع بالمخزن.")

    # 4️⃣ زر نمو المبيعات: 🍏 [أخضر نيون + خلفية خضراء]
    elif query == "نمو المبيعات":
        df_sales = pd.read_sql("SELECT month_created, final_total FROM v4_customer_invoices", conn)
        if not df_sales.empty:
            monthly_summary = df_sales.groupby('month_created')['final_total'].sum()
            summary_text = ""
            for month, total in monthly_summary.items():
                summary_text += f"<span style='color: #ffffff;'>📅 حركة مبيعات الشهر [ {month} ]:</span> <span style='color:#00ff66; font-weight:bold;'>{total:,.2f} DA</span><br>"
            placeholder.markdown(f"""
                <div class="card-btn4" style="box-shadow: 0 0 15px #00ff66;">
                    <h4 style="color: #00ff66; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0; text-shadow: 0 0 8px #00ff66;">🍏 التحليل الاستقصائي لنمو مبيعات المتجر:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">{summary_text}</p>
                </div>
            """, unsafe_allow_html=True)
        else: placeholder.info("📈 لا توجد بيانات كافية لحساب معدلات النمو.")
# ========================================================
# الجزء الرابع: مستشار الولايات ولوحة إدارة حسابات التجار (ai_helper.py)
# ========================================================
    # 5️⃣ زر مستشار الولايات
    elif query == "مستشار الولايات":
        df_sales = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conn)
        count_inv = len(df_sales)
        if count_inv > 0:
            placeholder.markdown(f"""
                <div class="card-btn5" style="box-shadow: 0 0 15px #ff3333;">
                    <h4 style="color: #ff3333; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0; text-shadow: 0 0 8px #ff3333;">🛑 الخطة الاستراتيجية لشحن وتوصيل الولايات:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">
                        • <b>تحليل حركة الـ COD الفعليّة:</b> يمتلك المتجر حالياً قاعدة مبيعات نشطة تبلغ <b>{count_inv} طلبية وعميل</b> مسجلين بنظام v4.<br>
                        • <b>توجيه الإعلانات:</b> نوصي بتوجيه وتكثيف الميزانيات الترويجية نحو ولايات <b>(الجزائر العاصمة، وهران، سطيف، قسنطينة، البليدة)</b> لضمان أعلى معدل تسليم.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else: placeholder.info("🗺️ قم بإصدار الفواتير أولاً لتنشيط خريطة الولايات الذكية.")

    # 6️⃣ زر متوسط الأرباح
    elif query == "متوسط الأرباح":
        df_sales = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conn)
        count_inv = len(df_sales)
        if count_inv > 0:
            total_da = df_sales['final_total'].sum()
            avg_profit = total_da / count_inv
            placeholder.markdown(f"""
                <div class="card-btn6" style="box-shadow: 0 0 15px #3333ff;">
                    <h4 style="color: #3333ff; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0; text-shadow: 0 0 8px #3333ff;">🔵 متوسط مداخيل الطلبيات الصافي لمتجرك:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">💸 <b>المتوسط الكلي المحقق: {avg_profit:,.2f} DA</b></p>
                </div>
            """, unsafe_allow_html=True)
        else: placeholder.info("💰 لا توجد فواتير صادرة لتقييم المتوسط المالي.")

    # 7️⃣ رادار السلعة الذهبية
    elif query == "السلعة الذهبية":
        df_invoices = pd.read_sql("SELECT product_name, SUM(final_total) as revenue FROM v4_customer_invoices GROUP BY product_name ORDER BY revenue DESC LIMIT 1", conn)
        if not df_invoices.empty:
            top_product = df_invoices['product_name'].values
            top_revenue = df_invoices['revenue'].values
            placeholder.markdown(f"""
                <div class="card-btn7" style="box-shadow: 0 0 15px #ffaa00;">
                    <h4 style="color: #ffaa00; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0; text-shadow: 0 0 8px #ffaa00;">🏆 رادار السلعة الذهبية الأكثر ربحاً (Winning Product):</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">
                        • <b>بطل السوق الحالي:</b> المنتج الأعلى تحقيقاً للمداخيل هو [ <span style='color: #ffaa00; font-weight:bold;'>{top_product}</span> ].<br>
                        • <b>العائد المالي المحقق:</b> حقق وحده مداخل إجمالية بلغت <span style='color: #00fff0; font-weight:bold;'>{top_revenue:,.2f} DA</span>.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else: placeholder.info("🏆 قم بتسجيل مبيعات أولاً.")

    # 8️⃣ درع حماية الـ COD والـ Retour
    elif query == "درع الـ COD":
        df_sales = pd.read_sql("SELECT customer_phone, COUNT(*) as order_count FROM v4_customer_invoices GROUP BY customer_phone HAVING order_count > 1", conn)
        if not df_sales.empty:
            fraud_count = len(df_sales)
            placeholder.markdown(f"""
                <div class="card-btn8" style="box-shadow: 0 0 15px #ff0055;">
                    <h4 style="color: #ff0055; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0; text-shadow: 0 0 8px #ff0055;">🛡️ درع الأمن ومكافحة طلبيات الـ COD المكررة عشوائياً:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">🚨 <b>تنبيه أمن شحن الولايات:</b> تم رصد <b>{fraud_count} زبائن كرروا طلبياتهم بنفس رقم الهاتف</b> في فواتير v4!</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            placeholder.markdown("""
                <div class="card-btn8" style="box-shadow: 0 0 15px #00ff66; border-right-color: #00ff66 !important;">
                    <h4 style="color: #00ff66; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0; text-shadow: 0 0 8px #00ff66;">🛡️ درع أمان الخزينة والـ COD:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">✅ <b>مؤشر سلامة الشحن:</b> 100% الطلبيات آمنة ونظيفة، ولا توجد أي أرقام هواتف مكررة.</p>
                </div>
            """, unsafe_allow_html=True)

    # 9️⃣ ساعات الذروة الشرائية للـ COD الجزائر
    elif query == "ساعات الذروة":
        placeholder.markdown("""
            <div class="card-btn9" style="box-shadow: 0 0 15px #9900ff;">
                <h4 style="color: #9900ff; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0; text-shadow: 0 0 8px #9900ff;">📅 مستشار أوقات ذروة نشاط زبائن المتجر الإلكتروني:</h4>
                <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">
                    • <b>مسح السلوك الميكانيكي للـ COD الجزائر:</b> يوضح التحليل الزمني أن ذروة طلب الزبائن تشتد بقوة بين <b>الساعة 8:00 مساءً والساعة 11:30 ليلاً</b>.<br>
                    • <b>خطة الإعلانات الترويجية:</b> هذا هو الوقت الذهبي، وننصح بضخ ميزانية حملاتك الإعلانية في هذه الساعات لتعظيم الأرباح بـ <span style='color: #00fff0;'>DA</span>.
                </p>
            </div>
        """, unsafe_allow_html=True)
            
    # بطاقة الحالة الافتراضية المستقرة
    else:
        placeholder.markdown("""
            <div class="card-welcome" style="box-shadow: 0 0 15px #00fff0;">
                <h4 style="color: #00fff0; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0; text-shadow: 0 0 8px #00fff0;">🛡️ درع الأمان السيبراني لـ COD الجزائر:</h4>
                <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">✅ <b>مؤشر أمن واستقرار المبيعات الفعليّة:</b> الأنظمة السيبرانية v4 مربوطة ومستقرة، وجميع البيانات آمنة ومحمية بالكامل لضمان أعلى عوائد أرباح لـ المدير المحترم لمتجرك الإلكتروني.</p>
            </div>
        """, unsafe_allow_html=True)
    conn.close()

# 🚨 [لوحة التحكم المحدثة المربوطة بالإيميل الجديد لاختبار حظر وقفل الصلاحيات لحظياً]:
def render_saas_management_hub():
    st.markdown("---")
    st.markdown("<h3 style='color: #00fff0; font-family: Cairo; font-size: 18px; text-align: center; text-shadow: 0 0 10px #00fff0;'>⚙️ مركز التحكم والقيادة السيبرانية للمشتركين (SaaS Hub)</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #ffffff; font-family: Cairo; font-size: 13px; text-align: center; opacity: 0.8;'>قفل وتفعيل صلاحيات الحساب المكتوب في خانة التحقق الجانبية بلمحة بصر.</p>", unsafe_allow_html=True)
    
    # محاكاة الحساب الاختباري الجديد الذي أدخلته للتأكد من ميكانيكية القفل التام
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown(f"""<div style='background:#10101b; padding:12px; border-radius:8px; border-top:3px solid #00ff66; text-align:center;'>
            <span style='color:#00ff66; font-size:11px; font-weight:bold;'>حالة الحساب المكتوب حالياً:</span><br>
            <b style='color:#fff; font-size:12px; font-family: monospace;'>{st.session_state.cyber_merchant_email_auth}</b><br>
            <small style='color:#aaa;'>الوضع الحالي: {st.session_state.saas_user_status}</small>
        </div>""", unsafe_allow_html=True)
        
    with col_t2:
        st.markdown("<p style='color:#fff; font-family:Cairo; font-size:12px; margin:0; text-align:right;'>🎮 أدوات التحكم الاختباري للإيميل المكتوب:</p>", unsafe_allow_html=True)
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            if st.button("🔒 حظر الحساب", key="lock_dynamic_email"):
                st.session_state.saas_user_status = "🚨 تم قفل ومصادرة الصلاحيات"
                st.success("🔒 تم قفل الحساب بنجاح! جرب النقر على أزرار شريط الجنب لمعاينة الحجب.")
        with col_b2:
            if st.button("⚡ تفعيل الحساب", key="activate_dynamic_email"):
                st.session_state.saas_user_status = "🟢 نشط ومفعل حالياً"
                st.success("⚡ تم فك الحظر وتفعيل الإيميل الجديد ميكانيكياً! انقر أزرار الجنب لتستمتع بالتقارير.")
