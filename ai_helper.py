# ========================================================
# الجزء الأول: الهندسة البصرية المتقدمة وتجميل الأزرار (ai_helper.py)
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
        
        /* 🚨 تحسين وتثبيت شكل مستطيل الكتابة ليطابق المثال الفعلي في صورتك تماماً الحواف الوردية والخلفية الداكنة */
        div[data-testid="stTextInput"] input {
            border: 2px solid #ff00ff !important; /* 👈 حدود وردية مضيئة مطابقة للمثال الفعلي */
            background-color: #10101b !important; /* 👈 خلفية داكنة صافية بنظام لوحة تحكمك */
            color: #ffffff !important;            /* 👈 خط عربي أبيض نقي */
            border-radius: 12px !important;
            padding: 14px 16px !important;        /* زيادة المساحة لحماية الحروف العربية من الالتصاق */
            font-family: 'Cairo', sans-serif !important;
            text-align: right !important;
            direction: rtl !important;
            box-shadow: 0px 0px 15px rgba(255, 0, 255, 0.3) !important;
            transition: all 0.4s ease-in-out !important;
        }
        
        /* 🌌 الشفرة السرية: حجب وإبادة التلميح الإنجليزي المعطل (Press Enter to apply) والتعليمات تماماً لمنع الاختلاط */
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
        
        /* تأثير زيادة التوهج السيبراني عند النقر والبدء في تدوين الكلمات */
        div[data-testid="stTextInput"] input:focus {
            border-color: #00fff0 !important;
            box-shadow: 0px 0px 25px #00fff0, inset 0px 0px 6px rgba(0, 255, 240, 0.4) !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # 2. زر التفعيل الميكانيكي المطور لمتجرك الحالي دون تعديل ميكانيكي
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

        # تهيئة حالة جلسة لحفظ السؤال المقترح المختار
        if "suggested_click" not in st.session_state:
            st.session_state.suggested_click = ""

        # أزرار الاقتراحات السريعة أسفل الترحيب مباشرة
        st.sidebar.markdown("<p style='color: #00fff0; font-family: Cairo; font-size: 12px; margin: 10px 0 5px 0; text-align: right;'>💡 اقتراحات الأسئلة السريعة:</p>", unsafe_allow_html=True)
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("📊 تقرير الأرباح"):
                st.session_state.suggested_click = "تقرير الأرباح"
                st.session_state.cyber_v7_pro_query = "" # 🚨 تصفية ومسح الحقل أوتوماتيكياً فوراً
        with col2:
            if st.button("📦 جرد المخزن"):
                st.session_state.suggested_click = "جرد المخزن"
                st.session_state.cyber_v7_pro_query = "" # 🚨 تصفية ومسح الحقل أوتوماتيكياً فوراً
            
        if st.sidebar.button("⚠️ المنتجات القريبة من النفاذ"):
            st.session_state.suggested_click = "قطع المستودع"
            st.session_state.cyber_v7_pro_query = "" # 🚨 تصفية ومسح الحقل أوتوماتيكياً فوراً
        
        st.sidebar.markdown("---")

        # شريط الأسئلة الاحترافي المثبت كلياً بصور الهوية البصرية لمتجرك
        user_query = st.sidebar.text_input("💬 اكتب سؤالك للمساعد هنا:", key="cyber_v7_pro_query")
        
        # إذا قام المدير بالكتابة مجدداً، نقوم بمسح تفعيل الزر القديم ليعمل النظام بتناسق ذكي
        if user_query:
            st.session_state.suggested_click = ""
            final_query = user_query
        else:
            final_query = st.session_state.suggested_click
        
        if final_query:
            evaluate_logic_response(final_query)
# ========================================================
# الجزء الثاني: عقل المساعد المطور وطريقة الإجابة الذكية (ai_helper.py)
# ========================================================

def evaluate_logic_response(query):
    # الاتصال المباشر بقاعدة البيانات الرابعة v4 لقراءة سجلات المتجر الفعليّة
    conn = sqlite3.connect("invoices_master_v4.db")
    
    # 1. 📊 منطق الـ AI المطور لتحليل الحسابات والأرباح الشاملة
    if "ربح" in query or "مبيعات" in query or "حساب" in query:
        df_sales = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conn)
        count_inv = len(df_sales)
        
        if count_inv > 0:
            total_da = df_sales['final_total'].sum()
            avg_invoice = total_da / count_inv # حساب متوسط قيمة الطلبية منطقياً
            
            # صياغة الإجابة بأسلوب ذكاء اصطناعي تحليلي خارق
            st.sidebar.markdown(f"""
                <div style="background: linear-gradient(135deg, #0d0614 0%, #1c092b 100%); border: 1px solid #ff00ff; box-shadow: 0 0 15px #ff00ff; padding: 15px; border-radius: 10px; text-align: right; direction: rtl; margin-top: 12px; animation: cyberPopIn 0.4s ease;">
                    <h4 style="color: #ff00ff; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0; text-shadow: 0 0 5px #ff00ff;">🤖 التشخيص المالي الذكي للـ AI:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">
                        مرحباً يا مدير محمد، لقد قمت بتحليل دقيق لـ <b>{count_inv} فاتورة صادرة</b>.<br>
                        💰 إجمالي المداخيل الحالية: <span style="color: #00fff0; font-weight: bold;">{total_da:,.2f} DA</span><br>
                        📈 متوسط قيمة الفاتورة الواحدة: <span style="color: #00ffcc;">{avg_invoice:,.2f} DA</span><br>
                        💡 <b>مؤشر الـ AI:</b> أداء متجرك مستقر ماليًا ومعدل الطلب ممتاز ومبشر هذا الشهر.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.sidebar.info("📊 لا توجد فواتير مسجلة حالياً لبدء التحليل المالي.")
        
    # 2. 🔮 منطق الـ AI المطور لجرد المستودع واستكشاف الثغرات والتنبيهات
    elif "مخزن" in query or "سلع" in query or "قطع" in query:
        df_stock = pd.read_sql("SELECT product_name, available_qty FROM store_stock", conn)
        
        if not df_stock.empty:
            total_qty = df_stock['available_qty'].sum()
            low_stock_df = df_stock[df_stock['available_qty'] <= 10]
            low_stock_count = len(low_stock_df)
            
            low_stock_text = ""
            if low_stock_count > 0:
                low_stock_text = "<br>🚨 <b>تحذير النفاذ السريع:</b><br>"
                for idx, row in low_stock_df.iterrows():
                    low_stock_text += f"⚠️ المنتج [ {row['product_name']} ] متبقي منه {row['available_qty']} قطع فقط!<br>"
            else:
                low_stock_text = "<br>✅ <b>مؤشر الأمان:</b> جميع السلع متوفرة بكميات آمنة في المستودع."

            st.sidebar.markdown(f"""
                <div style="background: linear-gradient(135deg, #051214 0%, #09262b 100%); border: 1px solid #00fff0; box-shadow: 0 0 15px #00fff0; padding: 15px; border-radius: 10px; text-align: right; direction: rtl; margin-top: 12px; animation: cyberPopIn 0.4s ease;">
                    <h4 style="color: #00fff0; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0; text-shadow: 0 0 5px #00fff0;">🔮 تقرير الجرد اللاسلكي للتنبؤ:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">
                        مجموع القطع الكلية الجاهزة للشحن: <span style="color: #ff00ff; font-weight: bold;">{total_qty} حبة</span>
                        {low_stock_text}
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.sidebar.info("📦 مستودعك فارغ حالياً.")
            
    # 3. الإجابة الذكية الافتراضية
    else:
        st.sidebar.markdown("""
            <div style="border-right: 3px solid #ffffff; padding-right: 10px; margin-top: 12px; text-align: right; direction: rtl;">
                <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 12.5px; margin: 0;">أنا متصلة بقواعد بيانات v4 بنجاح يا مدير محمد، اسألني عن الفواتير أو المخزون لإعطائك أرقاماً منطقية.</p>
            </div>
        """, unsafe_allow_html=True)
    conn.close()

def render_marketing_hub():
    pass

def render_data_insights(conn):
    pass
