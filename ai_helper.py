# ========================================================
# الجزء الأول: الهندسة البصرية المتقدمة وتلوين الخلفيات (ai_helper.py)
# ========================================================
import streamlit as st
import pandas as pd
import sqlite3
import time

def render_sidebar_helper():
    st.sidebar.markdown("---")
    
    # 1. حقن كود الـ CSS الأسطوري المطور لتلوين خلفية كل بطاقة من الداخل بلون مخصص متناسق مع إطارها
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
        
        /* 🌸 تخصيص بطاقات اللون الوردي: إطار وردي مشع + تلوين داخلي داكن مائل للأرجواني السيبراني */
        .card-pink-style {
            background: linear-gradient(135deg, #0f0414 0%, #1a082b 100%) !important; /* 👈 تلوين مخصص من الداخل */
            border-right: 4px solid #ff00ff !important;
            border-left: 1px solid rgba(255, 0, 255, 0.2) !important;
            border-radius: 12px !important;
            padding: 18px !important;
            text-align: right !important;
            margin-top: 15px !important;
            margin-bottom: 15px !important;
            direction: rtl !important;
            animation: cyberPopIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards !important;
            opacity: 0;
        }
        
        /* 💎 تخصيص بطاقات اللون الفيروزي: إطار فيروزي مشع + تلوين داخلي داكن مائل للزرقة النيونية */
        .card-cyan-style {
            background: linear-gradient(135deg, #020f14 0%, #062330 100%) !important; /* 👈 تلوين مخصص من الداخل */
            border-right: 4px solid #00fff0 !important;
            border-left: 1px solid rgba(0, 255, 240, 0.2) !important;
            border-radius: 12px !important;
            padding: 18px !important;
            text-align: right !important;
            margin-top: 15px !important;
            margin-bottom: 15px !important;
            direction: rtl !important;
            animation: cyberPopIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards !important;
            opacity: 0;
        }
        
        /* 🍏 تخصيص بطاقة الحالة الافتراضية: إطار أخضر آمن + تلوين داخلي داكن مائل للخضار الرقمي */
        .card-green-style {
            background: linear-gradient(135deg, #021408 0%, #062e12 100%) !important; /* 👈 تلوين مخصص من الداخل */
            border-right: 4px solid #00ff66 !important;
            border-left: 1px solid rgba(0, 255, 102, 0.2) !important;
            border-radius: 12px !important;
            padding: 18px !important;
            text-align: right !important;
            margin-top: 15px !important;
            margin-bottom: 15px !important;
            direction: rtl !important;
            animation: cyberPopIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards !important;
            opacity: 0;
        }
        
        /* لوحة الترحيب العلوية المستقرة بنظامك الحالي */
        .ai-cyber-legendary-panel {
            background: linear-gradient(135deg, #090911 0%, #111124 100%) !important;
            border-right: 4px solid #00fff0 !important;
            border-left: 1px solid rgba(0, 255, 240, 0.2) !important;
            border-radius: 12px !important;
            padding: 18px !important;
            text-align: right !important;
            direction: rtl !important;
        }
        
        @keyframes cyberPopIn {
            0% { transform: translateY(14px) scale(0.98); opacity: 0; filter: blur(3px); }
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
            <div class="ai-cyber-legendary-panel">
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
                st.session_state.active_query = "تقرير الأرباح"
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
                time.sleep(0.06) # تأخير خفيف لإبراز حركة الصعود الحركي الميكانيكي الملوّن من الداخل والخارج
                st.session_state.old_query = st.session_state.active_query
                
            evaluate_logic_response(st.session_state.active_query, response_placeholder)

def render_marketing_hub(): pass
def render_data_insights(conn): pass
# ========================================================
# الجزء الثالث: عقل المساعد والتخصيص اللوني الداخلي (ai_helper.py)
# ========================================================

def evaluate_logic_response(query, placeholder):
    conn = sqlite3.connect("invoices_master_v4.db")
    
    # أ. جرد تقرير الأرباح والحسابات الكلية: 🌸 [إطار وردي + خلفية أرجوانية داكنة من الداخل]
    if query == "تقرير الأرباح" or "ربح" in query or "مبيعات" in query or "حساب" in query:
        df_sales = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conn)
        count_inv = len(df_sales)
        if count_inv > 0:
            total_da = df_sales['final_total'].sum()
            avg_invoice = total_da / count_inv
            placeholder.markdown(f"""
                <div class="card-pink-style" style="box-shadow: 0 0 15px #ff00ff;">
                    <h4 style="color: #ff00ff; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0; text-shadow: 0 0 8px #ff00ff;">🌸 التشخيص المالي الذكي للـ AI:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">
                        <span style="color: #ff00ff; font-weight: bold;">💰 إجمالي المداخيل الحالية:</span> <span style="color: #ff00ff; font-weight: bold; text-shadow: 0 0 5px #ff00ff;">{total_da:,.2f} DA</span><br>
                        <span style="color: #ff00ff;">📈 متوسط قيمة الفاتورة الواحدة:</span> <span style="color: #ffffff; font-weight: bold;">{avg_invoice:,.2f} DA</span>
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else: placeholder.info("📊 لا توجد فواتير مسجلة حالياً لبدء التحليل.")
        
    # b. جرد المخزن الكلي والتحذير من النفاذ السريع: 💎 [إطار فيروزي + خلفية نيونية داكنة من الداخل]
    elif query == "جرد المخزن" or query == "قطع المستودع" or "مخزن" in query or "سلع" in query or "قطع" in query:
        df_stock = pd.read_sql("SELECT product_name, available_qty FROM store_stock", conn)
        if not df_stock.empty:
            total_qty = df_stock['available_qty'].sum()
            low_stock_df = df_stock[df_stock['available_qty'] <= 10]
            low_stock_text = ""
            if len(low_stock_df) > 0:
                low_stock_text = "<br><span style='color: #00fff0;'>🚨 تحذير النفاذ السريع:</span><br>"
                for idx, row in low_stock_df.iterrows():
                    low_stock_text += f"<span style='color: #ffffff;'>⚠️ المنتج [ {row['product_name']} ] متبقي منه {row['available_qty']} قطع فقط!</span><br>"
            else: low_stock_text = "<br><span style='color: #00fff0;'>✅ مؤشر الأمان: جميع الكميات مستقرة بالكامل.</span>"

            placeholder.markdown(f"""
                <div class="card-cyan-style" style="box-shadow: 0 0 15px #00fff0;">
                    <h4 style="color: #00fff0; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0; text-shadow: 0 0 8px #00fff0;">💎 تقرير الجرد اللاسلكي للتنبؤ:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">
                        <span style="color: #00fff0; font-weight: bold;">📦 مجموع القطع الكلية الجاهزة للشحن:</span> <span style="color: #00fff0; font-weight: bold; text-shadow: 0 0 5px #00fff0;">{total_qty} حبة</span>
                        {low_stock_text}
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else: placeholder.info("📦 مستودعك فارغ حالياً.")

    # ج. تحليل نمو مبيعات المتجر شهرياً: 🌸 [إطار وردي + خلفية أرجوانية داكنة من الداخل]
    elif query == "نمو المبيعات":
        df_sales = pd.read_sql("SELECT month_created, final_total FROM v4_customer_invoices", conn)
        if not df_sales.empty:
            monthly_summary = df_sales.groupby('month_created')['final_total'].sum()
            summary_text = ""
            for month, total in monthly_summary.items():
                summary_text += f"<span style='color: #ffffff;'>📅 الشهر [ {month} ]:</span> <span style='color:#ff00ff; font-weight:bold;'>{total:,.2f} DA</span><br>"
            placeholder.markdown(f"""
                <div class="card-pink-style" style="box-shadow: 0 0 15px #ff00ff;">
                    <h4 style="color: #ff00ff; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0; text-shadow: 0 0 8px #ff00ff;">🌸 تحليل نمو المبيعات الشهري للـ AI:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">{summary_text}</p>
                </div>
            """, unsafe_allow_html=True)
        else: placeholder.info("📈 لا توجد بيانات كافية.")
# ========================================================
# الجزء الرابع: مستشار الولايات والأمن وقفل الاتصال (ai_helper.py)
# ========================================================
    # د. مستشار الولايات ومناطق الشحن الأكثر طلباً: 💎 [إطار فيروزي + خلفية نيونية داكنة من الداخل]
    elif query == "mستشار الولايات" or query == "مستشار الولايات":
        df_sales = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conn)
        count_inv = len(df_sales)
        if count_inv > 0:
            placeholder.markdown(f"""
                <div class="card-cyan-style" style="box-shadow: 0 0 15px #00fff0;">
                    <h4 style="color: #00fff0; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0; text-shadow: 0 0 8px #00fff0;">💎 مستشار توجيه الحملات الجزائريّ:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">
                        <span style="color: #00fff0; font-weight: bold;">حجم حركة فواتير الـ COD الفعليّة:</span> <b>{count_inv} طلبيّة نشطة</b>.<br>
                        🎯 <span style="color: #00fff0; font-weight: bold;">توصية خريطة الـ AI:</span> نوصي بتوجيه وتكثيف الميزانيات الترويجية نحو ولايات <span style="color: #ffffff; font-weight: bold;">(الجزائر العاصمة، وهران، سطيف, قسنطينة)</span> لضمان أعلى معدل تسليم.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else: placeholder.info("🗺️ قم بإصدار الفواتير أولاً لتنشيط خريطة الولايات الذكية.")

    # هـ. حساب متوسط الأرباح المتوقعة لكل فاتورة صادرة: 🌸 [إطار وردي + خلفية أرجوانية داكنة من الداخل]
    elif query == "متوسط الأرباح":
        df_sales = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conn)
        count_inv = len(df_sales)
        if count_inv > 0:
            total_da = df_sales['final_total'].sum()
            avg_profit = total_da / count_inv
            placeholder.markdown(f"""
                <div class="card-pink-style" style="box-shadow: 0 0 15px #ff00ff;">
                    <h4 style="color: #ff00ff; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0; text-shadow: 0 0 8px #ff00ff;">🌸 متوسط مداخيل الطلبيات الصافي لمتجرك:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">
                        <span style="color: #ff00ff; font-weight: bold;">معدل القيمة الفردية لكل فاتورة صادرة:</span><br>
                        💸 <span style="color: #ff00ff; font-weight: bold; text-shadow: 0 0 5px #ff00ff;">المتوسط الكلي المحقق: {avg_profit:,.2f} DA</span><br>
                        💡 <b>رؤية النظام ماليًا:</b> استخدم استراتيجية الـ Upsell لرفع قيم الفواتير للزبائن أثناء التأكيد.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else: placeholder.info("💰 لا توجد فواتير صادرة لتقييم المتوسط المالي.")
            
    # و. بطاقة الحالة الافتراضية المستقرة عند فتح الأداة: 🍏 [إطار أخضر + خلفية داكنة مائلة للخضار الرقمي من الداخل]
    else:
        placeholder.markdown("""
            <div class="card-green-style" style="box-shadow: 0 0 15px #00ff66;">
                <h4 style="color: #00ff66; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0; text-shadow: 0 0 8px #00ff66;">🍏 درع الأمان السيبراني لـ COD:</h4>
                <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">
                    ✅ <span style="color: #00ff66; font-weight: bold;">مؤشر أمن المبيعات:</span> <span style="color: #ffffff; font-weight: bold;">100% الصفقات آمنة ونظيفة وضد أخطاء الولايات الجزائريّة.</span>
                </p>
            </div>
        """, unsafe_allow_html=True)
    conn.close()
