import sqlite3
from flask import Flask, request, render_template_string, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'DA_returns_sovereignty_super_secret_key_2026'

# إعداد قاعدة البيانات الوهمية للـ SQL وتجهيز جدول التجار والبيانات الحساسة
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS merchants (
            id INTEGER PRIMARY KEY AUTO_INCREMENT,
            email TEXT,
            password TEXT
        )
    ''')
    # إضافة تاجر تجريبي إذا كان الجدول فارغاً
    cursor.execute("SELECT COUNT(*) FROM merchants")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO merchants (email, password) VALUES ('new_merchant_2026@saas.com', 'FreePass9988!')")
    conn.commit()
    conn.close()

# القالب المرئي الشبحي الموسط مع التأثيرات النيونية المضيئة وثبات الجلسة ضد الـ Refresh
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>بوابة السيادة الكبرى 2026</title>
    <style>
        body {
            background-color: #0d0d11;
            color: #ffffff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
        }
        /* الكتلة الموسطة الشبحية للوحة الموافقات */
        .ghost-panel {
            background: rgba(20, 20, 25, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(15px);
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
            text-align: center;
            max-width: 450px;
            width: 100%;
        }
        .input-group {
            margin-bottom: 20px;
            text-align: right;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #aaa;
            font-size: 14px;
        }
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 12px;
            border-radius: 8px;
            border: 1px solid #333;
            background: #15151e;
            color: #fff;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 12px;
            border: none;
            border-radius: 8px;
            background: #3a3af2;
            color: white;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s;
        }
        button:hover {
            background: #5050ff;
        }
        /* تأثير الأصفر النيوني المضيء للإيميل والباسورد */
        .neon-glow {
            margin-top: 25px;
            padding: 15px;
            border: 2px dashed #ccff00;
            border-radius: 8px;
            background: rgba(204, 255, 0, 0.05);
            color: #ccff00;
            font-weight: bold;
            text-shadow: 0 0 10px #ccff00, 0 0 20px #ccff00;
            font-size: 16px;
            word-break: break-all;
        }
        /* زر الحذف النهائي الحقيقي للـ SQL */
        .btn-danger-sql {
            margin-top: 20px;
            background: #ff0055;
            box-shadow: 0 0 15px rgba(255, 0, 85, 0.4);
        }
        .btn-danger-sql:hover {
            background: #ff2a74;
        }
        .error {
            color: #ff3333;
            margin-bottom: 15px;
            font-size: 14px;
        }
    </style>
</head>
<body>

    <div class="ghost-panel">
        <h2>لوحة الموافقات السيادية الـ 9</h2>
        <p style="color: #666; font-size: 13px; margin-bottom: 25px;">نظام الحماية النشط: admin_master_v4</p>
        
        {% if not session.get('authenticated') %}
            <!-- نموذج قفل الهوية بمنتصف الشاشة -->
            <form method="POST" action="{{ url_for('login', role='boss') }}">
                {% if error %}
                    <div class="error">{{ error }}</div>
                {% endif %}
                <div class="input-group">
                    <label>اسم الهوية الأعلى</label>
                    <input type="text" name="username" required autocomplete="off">
                </div>
                <div class="input-group">
                    <label>كلمة السر المشفرة</label>
                    <input type="password" name="password" required>
                </div>
                <button type="submit">تفعيل القفل والولوج</button>
            </form>
        {% else %}
            <!-- عند نجاح الدخول: ينبثق إيميل التاجر بالنيوني المضيء ومستقر ضد الـ Refresh -->
            <div class="neon-glow">
                🚀 تم الاستدعاء بنجاح!<br>
                البريد: {{ merchant_email }}<br>
                الرمز الحر: {{ merchant_pass }}
            </div>

            <!-- زر حذف نهائي حقيقي للـ SQL -->
            <form method="POST" action="{{ url_for('purge_sql', role='boss') }}">
                <button type="submit" class="btn-danger-sql" onclick="return confirm('هل أنت متأكد من تفعيل الحقن التطهيري وحذف سجلات الـ SQL نهائياً؟')">
                    💥 إطلاق أمر الحذف النهائي الـ SQL
                </button>
            </form>
        {% endif %}
    </div>

</body>
</html>
"""

@app.route('/')
def index():
    # الشرط الصارم: لا تفتح للعامة وتختفي شبحياً إلا بمتغير الـ URL علوياً ?role=boss
    if request.args.get('role') != 'boss':
        return "404 Not Found - السيادة تمنع الوصول العام.", 404
    
    # مزامنة استقرار الجلسة ضد الـ Refresh لمنع الخلط كلياً 100%
    if session.get('authenticated'):
        return render_template_string(
            HTML_TEMPLATE, 
            merchant_email=session.get('m_email'), 
            merchant_pass=session.get('m_pass')
        )
    
    return render_template_string(HTML_TEMPLATE)

@app.route('/login', methods=['POST'])
def login():
    if request.args.get('role') != 'boss':
        return "أمر مرفوض كلياً.", 403
        
    username = request.form.get('username')
    password = request.form.get('password')
    
    # التحقق الصارم من الهوية المطلوبة وباسورد عام 2026
    if username == 'admin_master_v4' and password == 'SaasPassword2026':
        # جلب بيانات التاجر الجديد فوراً من الـ SQL
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT email, password FROM merchants ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        conn.close()
        
        if result:
            # تخزين البيانات في الـ Session لمنع الخلط ولتثبيتها ضد الـ Refresh
            session['authenticated'] = True
            session['m_email'] = result[0]
            session['m_pass'] = result[1]
        else:
            session['authenticated'] = True
            session['m_email'] = "no_merchant_found@saas.com"
            session['m_pass'] = "N/A"
            
        return redirect(url_for('index', role='boss'))
    else:
        return render_template_string(HTML_TEMPLATE, error="بيانات الهوية غير صالحة للسيادة الكبرى!")

@app.route('/purge_sql', methods=['POST'])
def purge_sql():
    if request.args.get('role') != 'boss' or not session.get('authenticated'):
        return "غير مصرح لك بإطلاق هذا السلاح.", 403
        
    # تنفيذ زر الحذف النهائي الحقيقي للـ SQL
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM merchants")
    conn.commit()
    conn.close()
    
    # تحديث بيانات الجلسة لتعكس الحذف الفوري النيوني
    session['m_email'] = "[تم المسح والتطهير نهائياً من الـ SQL]"
    session['m_pass'] = "[معدوم]"
    
    return redirect(url_for('index', role='boss'))

if __name__ == '__main__':
    # تهيئة الـ DB والتشغيل الفوري
    # init_db()  # قم بإلغاء التعليق عند التشغيل الفعلي لتوليد قاعدة البيانات
    app.run(debug=True, port=5000)
