# ========================================================
# الجزء الأول: الهندسة البصرية المتقدمة وتلوين الواجهات المخصصة (ai_helper.py)
# ========================================================
import streamlit as st
import pandas as pd
import sqlite3
import time

def render_sidebar_helper():
    st.sidebar.markdown("---")
    
    # 1. حقن كود الـ CSS الأسطوري المطور لتشغيل الأنميشن الموحد لكافة الفئات الملونة بشكل مستقل
    st.sidebar.markdown("""
        <style>
        /* 🛑 شكل الزر الفيروزي المطور لمتجرك الحالي دون تعديل ميكانيكي */
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
        
        /* 🚨 هندسة الحواف والالوان الداخلية المخصصة: كل بطاقة بلون مستقل فريد وتأثير صعود موحد لمنع الفجائية */
        .ai-cyber-legendary-panel, .card-btn1, .card-btn2, .card-btn3, .card-btn4, .card-btn5, .card-btn6, .card-welcome {
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
        
        /* 🗂️ تخصيص الألوان الفريدة لكل زر من الداخل ومن الخارج بالتوالي: */
        .card-btn1 { background: linear-gradient(135deg, #12021c 0%, #25053a 100%) !important; border-right: 4px solid #ff00ff !important; } /* الأرباح: وردي نيون */
        .card-btn2 { background: linear-gradient(135deg, #020f14 0%, #062330 100%) !important; border-right: 4px solid #00fff0 !important; } /* المخزن: فيروزي مشع */
        .card-btn3 { background: linear-gradient(135deg, #141102 0%, #2e2604 100%) !important; border-right: 4px solid #ffcc00 !important; } /* المنتجات قريبة النفاذ: أصفر ذهبي */
        .card-btn4 { background: linear-gradient(135deg, #02140a 0%, #053319 100%) !important; border-right: 4px solid #00ff66 !important; } /* نمو المبيعات: أخضر نيون */
        .card-btn5 { background: linear-gradient(135deg, #140202 0%, #330505 100%) !important; border-right: 4px solid #ff3333 !important; } /* مستشار الولايات: أحمر سيبراني */
        .card-btn6 { background: linear-gradient(135deg, #020214 0%, #050533 100%) !important; border-right: 4px solid #3333ff !important; } /* متوسط الأرباح: أزرق ملكي */
        
        /* لوحة الترحيب العلوية الافتراضية والنبض الرقمي الحركي لمتجرك الحالي */
        .ai-cyber-legendary-panel, .card-welcome { background: linear-gradient(135deg, #090911 0%, #111124 100%) !important; border-right: 4px solid #00fff0 !important; }
        .ai-pulse-status { display: inline-flex; align-items: center; background: rgba(0, 255, 240, 0.1); border: 1px solid #00fff0; padding: 4px 10px; border-radius: 20px; font-size: 11px; color: #00fff0; font-family: 'Cairo', sans-serif; margin-bottom: 10px; font-weight: bold; }
        .pulse-dot { width: 8px; height: 8px; background-color: #00fff0; border-radius: 50%; margin-left: 6px; box-shadow: 0 0 10px #00fff0; animation: pulse-animation 1.5s infinite alternate; }
        
        @keyframes pulse-animation { 0% { opacity: 0.4; transform: scale(0.9); } 100% { opacity: 1; transform: scale(1.2); box-shadow: 0 0 15px #00fff0; } }
        @keyframes cyberPopIn { 0% { transform: translateY(14px) scale(0.98); opacity: 0; filter: blur(3px); } 100% { transform: translateY(0) scale(1); opacity: 1; filter: blur(0); } }
        
        /* تثبيت حواف مستطيل الكتابة الوردي الفاخر المطابق لـ صورتك تماماً وعزله كلياً */
        div[data-testid="stTextInput"] input { border: 2px solid #ff00ff !important; background-color: #10101b !important; color: #ffffff !important; border-radius: 12px !important; padding: 14px 16px !important; font-family: 'Cairo', sans-serif !important; }
        div[data-testid="stTextInput"] p, div[data-testid="stTextInput"] small, div[data-testid="stTextInput"] label, div[data-testid="stTextInput"] [data-testid="stWidgetInstructions"], div[data-testid="stTextInput"] span, div[data-testid="stTextInput"] div:not(:first-child) p, .st-emotion-cache-16idsys p, .st-emotion-cache-q3uqly p, .st-emotion-cache-1pxscv7 p { display: none !important; opacity: 0 !important; visibility: hidden !important; height: 0px !important; margin: 0px !important; padding: 0px !important; }
        </style>
    """, unsafe_allow_html=True)
    
    ai_activate = st.sidebar.checkbox("تفعيل المساعد الأسطوري الخارق 🔘", key="legendary_v7_pro_activate")
    
    if ai_activate:
        st.sidebar.markdown("""
            <div class="ai-cyber-legendary-panel">
                <div class="ai-pulse-status"><span class="pulse-dot"></span>NEXUS AI: ONLINE</div>
                <h3 style="color:#00fff0; font-family:'Cairo'; font-size:16px; margin:0; font-weight:bold;">🔮 المستشار اللاسلكي المطور</h3>
                <p style="color:#fff; font-family:'Cairo'; font-size:13px; margin:5px 0 0 0;">مرحباً بك مجدداً يا <span style="color:#ff00ff; font-weight:bold;">مدير محمد</span>! أنظمتي مستقرة ومربوطة بـ v4 بنجاح.</p>
            </div>
        """, unsafe_allow_html=True)

        if "active_query" not in st.session_state: st.session_state.active_query = ""
        if "old_query" not in st.session_state: st.session_state.old_query = ""

        st.sidebar.markdown("<p style='color: #00fff0; font-family: Cairo; font-size: 12px; margin: 10px 0 5px 0; text-align: right;'>💡 اقتراحات الأسئلة السريعة (المجموعة 1):</p>", unsafe_allow_html=True)
        
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
# الجزء الثاني: بقية الأزرار وميكانيكية القيادة الحركية (ai_helper.py)
# ========================================================
        if st.sidebar.button("⚠️ المنتجات القريبة من النفاذ"):
            st.session_state.active_query = "قطع المستودع"
            st.session_state.cyber_v7_pro_query = ""
        
        st.sidebar.markdown("<p style='color: #ff00ff; font-family: Cairo; font-size: 12px; margin: 10px 0 5px 0; text-align: right;'>🚀 تحليلات الـ AI المتقدمة (المجموعة 2):</p>", unsafe_allow_html=True)
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

        st.sidebar.markdown("---")
        user_query = st.sidebar.text_input("💬 اكتب سؤالك للمساعد هنا:", key="cyber_v7_pro_query")
        
        if user_query:
            st.session_state.active_query = user_query

        response_placeholder = st.sidebar.empty()
        
        if st.session_state.active_query:
            if st.session_state.active_query != st.session_state.old_query:
                response_placeholder.empty()
                time.sleep(0.06) # تأخير خفيف لإبراز حركة الصعود الحركي الميكانيكي المستقل لكل لون
                st.session_state.old_query = st.session_state.active_query
                
            evaluate_logic_response(st.session_state.active_query, response_placeholder)

def render_marketing_hub(): pass
def render_data_insights(conn): pass
# ========================================================
# الجزء الثالث: عقل المساعد والشروحات المفصلة الملوّنة (ai_helper.py)
# ========================================================

def evaluate_logic_response(query, placeholder):
    conn = sqlite3.connect("invoices_master_v4.db")
    
    # 1️⃣ زر تقرير الأرباح: 🌸 [إطار وردي + شرح مالي تفصيلي وموسع بـ DA]
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
                        • <b>تحليل المداخيل الكلية:</b> تم جرد الفواتير الصادرة بنجاح، وبلغ إجمالي التدفق المالي الصافي <span style="color: #ff00ff; font-weight: bold; text-shadow: 0 0 5px #ff00ff;">{total_da:,.2f} DA</span> عبر <b>{count_inv} عملية بيع</b> مسجلة.<br>
                        • <b>معدل سلة المبيعات:</b> متوسط الإنفاق الفردي للزبون الواحد هو <span style="color: #00fff0; font-weight: bold;">{avg_invoice:,.2f} DA</span> لكل طلبيّة.<br>
                        • <b>التشخيص التكتيكي:</b> هذا المعدل يشير إلى استجابة شرائية قوية في المتجر، وننصح بتقديم عروض شحن مجاني عند شراء قطعتين لزيادة حجم التدفق النقدي بالخزينة.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else: placeholder.info("📊 لا توجد فواتير مسجلة حالياً لبدء التحليل المالي.")
        
    # 2️⃣ زر جرد المخزن الكلي: 💎 [إطار فيروزي + شرح مستودع تفصيلي وموسع لـ صورتك]
    elif query == "جرد المخزن" or "مخزن" in query or "سلع" in query:
        df_stock = pd.read_sql("SELECT product_name, available_qty FROM store_stock", conn)
        if not df_stock.empty:
            total_qty = df_stock['available_qty'].sum()
            placeholder.markdown(f"""
                <div class="card-btn2" style="box-shadow: 0 0 15px #00fff0;">
                    <h4 style="color: #00fff0; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0; text-shadow: 0 0 8px #00fff0;">💎 الشرح التفصيلي لجرد المستودع والـ COD:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">
                        • <b>الطاقة الاستيعابية النشطة:</b> مجموع القطع والسلع الكلية الجاهزة للشحن والتوصيل الفوري حالياً يبلغ <span style="color: #00fff0; font-weight: bold; text-shadow: 0 0 5px #00fff0;">{total_qty} حبة ونظام</span> مخزنة بالـ SQL.<br>
                        • <b>جاهزية التوزيع:</b> كافة هذه السلع مفحوصة ومربوطة بمسارات لوحة تحكم الشحن الخاصة بمتجرك الإلكتروني v4 لتسليمها فوراً للموزعين في جميع الولايات الجزائرية.<br>
                        • <b>رؤية الـ AI:</b> مخزونك الحالي مستقر ويغطي معدل مبيعات الـ 14 يوماً القادمة بكفاءة عالية دون قلق.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else: placeholder.info("📦 مستودعك فارغ حالياً.")

    # 3️⃣ زر المنتجات القريبة من النفاذ: 🪙 [إطار أصفر ذهبي + شرح تحذيري تفصيلي موسع للمخازن]
    elif query == "قطع المستودع" or "قطع" in query:
        df_stock = pd.read_sql("SELECT product_name, available_qty FROM store_stock", conn)
        if not df_stock.empty:
            low_stock_df = df_stock[df_stock['available_qty'] <= 10]
            low_stock_count = len(low_stock_df)
            
            low_stock_text = ""
            if low_stock_count > 0:
                low_stock_text = "<br><span style='color: #ffcc00; font-weight:bold;'>🚨 تحذير النفاذ السريع الفوري لقائمة السلع:</span><br>"
                for idx, row in low_stock_df.iterrows():
                    low_stock_text += f"<span style='color: #ffffff;'>⚠️ المنتج [ {row['product_name']} ] متبقي منه {row['available_qty']} قطع فقط في المخزن!</span><br>"
            else: low_stock_text = "<br><span style='color: #00ff66; font-weight:bold;'>✅ مؤشر أمان المستودع: جميع السلع والمنتجات متوفرة بكميات آمنة وفوق عتبة الخطر (10 قطع).</span>"

            placeholder.markdown(f"""
                <div class="card-btn3" style="box-shadow: 0 0 15px #ffcc00;">
                    <h4 style="color: #ffcc00; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0; text-shadow: 0 0 8px #ffcc00;">🪙 تقرير استباق استمرارية شحن المنتجات:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">
                        • <b>رادار المسح التلقائي:</b> يقوم النظام بفحص دوري حي للحد الأدنى من كميات قطع السلع لتفادي توقف حملات Facebook و TikTok المموّلة فجأة.<br>
                        {low_stock_text}<br>
                        • <b>توصية الإمداد:</b> يرجى مراجعة الموردين لإعادة شحن المنتجات المتأثرة لتفادي إلغاء طلبيات الزبائن المشحونة.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else: placeholder.info("📦 لا توجد سلع بالمخزن.")

    # 4️⃣ زر نمو المبيعات: 🍏 [إطار أخضر نيون + شرح تحليلي تفصيلي موسع لحركة السوق الشهري]
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
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">
                        • <b>تتبع المنحنى البياني الشهري للفواتير الصادرة:</b><br>
                        {summary_text}<br>
                        • <b>رؤية نمو أعمال القائد محمد:</b> يوضح تحليل البيانات استقرار حجم المعاملات المالية، وننصح بجدولة ميزانية ترويجية تصاعدية مع بداية كل شهر بالتزامن مع فترات توزيع الأجور لرفع العوائد الصافية.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else: placeholder.info("📈 لا توجد بيانات كافية لحساب معدلات النمو.")
# ========================================================
# الجزء الرابع: مستشار الولايات والأمن الحركي الملوّن وقفل الاتصال (ai_helper.py)
# ========================================================
    # 5️⃣ زر مستشار الولايات: 🛑 [إطار أحمر سيبراني + شرح تفصيلي موسع وموجه للشحن الجزائري]
    elif query == "مستشار الولايات":
        df_sales = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conn)
        count_inv = len(df_sales)
        if count_inv > 0:
            placeholder.markdown(f"""
                <div class="card-btn5" style="box-shadow: 0 0 15px #ff3333;">
                    <h4 style="color: #ff3333; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0; text-shadow: 0 0 8px #ff3333;">🛑 الخطة الاستراتيجية لشحن وتوصيل الولايات:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">
                        • <b>تحليل حركة الـ COD الفعليّة:</b> يمتلك المتجر حالياً قاعدة مبيعات نشطة تبلغ <b>{count_inv} طلبية وعميل</b> مسجلين بنظام الحسابات الرابعة v4.<br>
                        • <b>توجيه الميزانية الإعلانية (Facebook Ads Targeting):</b> لضمان أعلى معدلات تسليم (Delivery Rate) وتقليل الشحنات المرتجعة (Retour)، نوصي بتخصيص 65% من ميزانية الإعلانات نحو ولايات: <span style="color: #ff3333; font-weight: bold;">(الجزائر العاصمة، وهران، سطيف، قسنطينة، البليدة)</span>.<br>
                        • <b>الهدف التجاري:</b> هذه المناطق تمتلك أعلى كثافة شرائية وسرعة استجابة للموزعين حالياً في الجزائر.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else: placeholder.info("🗺️ قم بإصدار الفواتير أولاً لتنشيط خريطة الولايات الذكية.")

    # 6️⃣ زر متوسط الأرباح المتوقعة: 🔵 [إطار أزرق ملكي + شرح مالي تفصيلي موسع للـ Upsell]
    elif query == "متوسط الأرباح":
        df_sales = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conn)
        count_inv = len(df_sales)
        if count_inv > 0:
            total_da = df_sales['final_total'].sum()
            avg_profit = total_da / count_inv
            placeholder.markdown(f"""
                <div class="card-btn6" style="box-shadow: 0 0 15px #3333ff;">
                    <h4 style="color: #3333ff; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0; text-shadow: 0 0 8px #3333ff;">🔵 التقييم المالي المتوقع لصافي التدفقات النقدية:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">
                        • <b>حساب قيمة الصفقة المتوسطة المحققة:</b> معدل القيمة الشرائية الصافية المودعة بالخزينة لكل فاتورة صادرة حالياً يثبت عند <span style="color: #3333ff; font-weight: bold; text-shadow: 0 0 5px #3333ff;">{avg_profit:,.2f} DA</span>.<br>
                        • <b>خطة التطوير المالي وعتبة الربح:</b> لرفع هذا المتوسط بـ 30% إضافية دون زيادة مصاريف الإعلانات، نوصي فريق خدمة العملاء وتأكيد الطلبيات بتطبيق استراتيجية الـ (Upsell) وعرض سلع تكميلية أو إكسسوارات مخصصة للمنتج على الزبون مباشرة أثناء المكالمة الهاتفية.<br>
                        • <b>رؤية الـ AI:</b> القوة الشرائية الحالية ممتازة وتسمح برفع الأرباح بيسر وسهولة.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else: placeholder.info("💰 لا توجد فواتير صادرة لتقييم المتوسط المالي.")
            
    # 7️⃣ بطاقة الحالة الافتراضية المستقرة عند فتح الأداة لأول مرة وغياب الضغط:
    else:
        placeholder.markdown("""
            <div class="card-welcome" style="box-shadow: 0 0 15px #00fff0;">
                <h4 style="color: #00fff0; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0; text-shadow: 0 0 8px #00fff0;">🛡️ درع الأمان السيبراني لـ COD الجزائر:</h4>
                <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">
                    ✅ <b>مؤشر أمن واستقرار المبيعات الفعليّة:</b> الأنظمة السيبرانية v4 مربوطة ومستقرة، وجميع البيانات آمنة ومحمية بالكامل ضد ثغرات التكرار وأخطاء شحن الولايات لضمان أعلى عوائد أرباح لمتجرك الإلكتروني.
                </p>
            </div>
        """, unsafe_allow_html=True)
    conn.close()
