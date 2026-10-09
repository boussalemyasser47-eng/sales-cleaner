# ========================================================
# الجزء الأول: نظام الأزرار الاقتراحية السيبرانية (ai_helper.py)
# ========================================================
import streamlit as st
import pandas as pd
import sqlite3

def render_sidebar_helper():
    st.sidebar.markdown("---")
    
    # حقن كود الـ CSS الأسطوري لحظر التداخلات وتنسيق أزرار الاقتراحات
    st.sidebar.markdown("""
        <style>
        /* تنسيق زر التفعيل الفيروزي لمتجرك الحالي دون تغيير */
        div[data-testid="stCheckbox"] {
            background: linear-gradient(135deg, #0a0a12 0%, #101020 100%) !important;
            border: 2px solid #00fff0 !important;
            border-radius: 14px !important;
            padding: 14px !important;
            text-align: right !important;
            box-shadow: 0px 0px 18px rgba(0, 255, 240, 0.4);
        }
        
        /* تصميم صندوق الترحيب الداخلي المنسق بدقة */
        .ai-cyber-legendary-panel {
            background: linear-gradient(135deg, #090911 0%, #111124 100%);
            border-right: 4px solid #00fff0;
            border-left: 1px solid rgba(0, 255, 240, 0.2);
            border-radius: 12px;
            padding: 18px;
            text-align: right;
            direction: rtl;
        }
        
        /* 🚨 تحسين وتثبيت شكل مستطيل الكتابة الوردي الأسطوري الخاص بك */
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
        
        /* مسح وحظر نص التلميح الإنجليزي والتعليمات تماماً لمنع الاختلاط */
        div[data-testid="stTextInput"] p, 
        div[data-testid="stTextInput"] small, 
        div[data-testid="stTextInput"] label,
        div[data-testid="stTextInput"] [data-testid="stWidgetInstructions"] {
            display: none !important;
            opacity: 0 !important;
            visibility: hidden !hidden;
            height: 0px !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    ai_activate = st.sidebar.checkbox("تفعيل المساعد الأسطوري الخارق 🔘", key="legendary_v7_pro_activate")
    
    if ai_activate:
        st.sidebar.markdown("""
            <div class="ai-cyber-legendary-panel">
                <h3 style="color:#00fff0; font-family:'Cairo'; font-size:16px; margin:0;">🔮 المستشار اللاسلكي المطور</h3>
                <p style="color:#fff; font-family:'Cairo'; font-size:13px; margin:5px 0 0 0;">مرحباً بك مجدداً يا مدير محمد! أنظمتي جاهزة لقراءة وتحليل قواعد البيانات. اختر أحد الاقتراحات السريعة بالأسفل أو اكتب استفسارك.</p>
            </div>
        """, unsafe_allow_html=True)

        # 🚨 نظام الاقتراحات الذكية: أزرار نيون سريعة تظهر بمجرد تشغيل النظام وتغنيك عن الكتابة
        st.sidebar.markdown("<p style='color: #00fff0; font-family: Cairo; font-size: 12px; margin: 10px 0 5px 0; text-align: right;'>💡 اقتراحات الأسئلة الذكية الفورية:</p>", unsafe_allow_html=True)
        
        # حجز متغير لحفظ السؤال المقترح
        suggested_query = ""
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("📊 تقرير الأرباح"):
                suggested_query = "تقرير الأرباح"
        with col2:
            if st.button("📦 جرد المستودع"):
                suggested_query = "جرد المخزن"
                
        if st.sidebar.button("⚠️ المنتجات القريبة من النفاذ"):
            suggested_query = "قطع المستودع"

        st.sidebar.markdown("---")

        # حقل الكتابة الوردي المتوهج الخاص بك
        user_query = st.sidebar.text_input("💬 اكتب سؤالك للمساعد هنا:", key="cyber_v7_pro_query")
        
        # دمج استعلام الأزرار المقترحة مع حقل الإدخال ليعمل النظام أوتوماتيكياً
        final_query = user_query if user_query else suggested_query
        
        if final_query:
            evaluate_logic_response(final_query)
# ========================================================
# الجزء الثاني: بطاقات التقارير وعقل الـ AI المطور (ai_helper.py)
# ========================================================

def evaluate_logic_response(query):
    conn = sqlite3.connect("invoices_master_v4.db")
    
    # أ. جرد وحساب الأرباح وعرضها بأسلوب ذكاء اصطناعي تحليلي خارق
    if "ربح" in query or "مبيعات" in query or "حساب" in query:
        df_sales = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conn)
        count_inv = len(df_sales)
        
        if count_inv > 0:
            total_da = df_sales['final_total'].sum()
            avg_invoice = total_da / count_inv
            st.sidebar.markdown(f"""
                <div style="background: linear-gradient(135deg, #0d0614 0%, #1c092b 100%); border: 1px solid #ff00ff; box-shadow: 0 0 15px #ff00ff; padding: 15px; border-radius: 10px; text-align: right; direction: rtl; margin-top: 12px;">
                    <h4 style="color: #ff00ff; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0;">🤖 التشخيص المالي للـ AI:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">
                        مداخيل المتجر الصافية بناءً على {count_inv} فاتورة:<br>
                        💰 الإجمالي: <span style="color: #00fff0; font-weight: bold;">{total_da:,.2f} DA</span><br>
                        📈 متوسط قيمة الطلب: <span style="color: #00ffcc;">{avg_invoice:,.2f} DA</span>
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.sidebar.info("📊 لا توجد فواتير مسجلة لبدء التحليل.")
        
    # ب. جرد قطع المستودع وفحص السلع القريبة من النفاذ تلقائياً
    elif "مخزن" in query or "سلع" in query or "قطع" in query:
        df_stock = pd.read_sql("SELECT product_name, available_qty FROM store_stock", conn)
        if not df_stock.empty:
            total_qty = df_stock['available_qty'].sum()
            low_stock_df = df_stock[df_stock['available_qty'] <= 10]
            
            low_stock_text = ""
            if len(low_stock_df) > 0:
                low_stock_text = "<br>🚨 <b>تحذير النفاذ السريع:</b><br>"
                for idx, row in low_stock_df.iterrows():
                    low_stock_text += f"⚠️ [ {row['product_name']} ] متبقي: {row['available_qty']} قطع!<br>"
            else:
                low_stock_text = "<br>✅ <b>مؤشر الأمان:</b> الكميات مستقرة."

            st.sidebar.markdown(f"""
                <div style="background: linear-gradient(135deg, #051214 0%, #09262b 100%); border: 1px solid #00fff0; box-shadow: 0 0 15px #00fff0; padding: 15px; border-radius: 10px; text-align: right; direction: rtl; margin-top: 12px;">
                    <h4 style="color: #00fff0; font-family: 'Cairo', sans-serif; font-size: 14px; margin: 0 0 6px 0;">🔮 تقرير الجرد والتنبؤ الفوري:</h4>
                    <p style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 13px; margin: 0; line-height: 1.6;">
                        القطع الجاهزة للشحن: <span style="color: #ff00ff; font-weight: bold;">{total_qty} حبة</span>
                        {low_stock_text}
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.sidebar.info("📦 مستودعك فارغ حالياً.")
    conn.close()

def render_marketing_hub():
    pass

def render_data_insights(conn):
    pass
