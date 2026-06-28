import flask
from flask import render_template, redirect, url_for, request, session, jsonify
import pymysql
import os
import sys

# 添加当前目录到系统路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)


def get_db_connection():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='lhl123456',
                                 database='python_final_project',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

app = flask.Flask(__name__, static_folder=os.path.join(BASE_DIR, 'static'))
app.secret_key = 'lhl123456'

@app.route('/')
def go_login():
    return redirect('/login')

@app.route('/login',  methods = ['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return render_template('login.html')
    elif request.method =='POST':
        input_username = request.form['username']
        input_password = request.form['password']

        connection = get_db_connection()
        cursor = connection.cursor()
        sql = 'SELECT username, password FROM users WHERE username="{}" and password="{}"'.format(input_username, input_password)
        cursor.execute(sql)
        user = cursor.fetchone()
        connection.close()

        if user:
            session['username'] = input_username
            return flask.redirect(url_for('index', name = input_username))
        else:
            return flask.render_template('login.html')

@app.route('/login/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method =='POST':
        register_username = request.form['username']
        register_password = request.form['password']

        connection = get_db_connection()
        cursor = connection.cursor()
        
        sql_query_username = 'SELECT * FROM users WHERE username = %s'
        cursor.execute(sql_query_username, (register_username))
        username_exists = cursor.fetchall()
        if username_exists:
            return '用户已存在'
        else:
            sql_inserte = 'INSERT INTO users (username, password) VALUES (%s, %s)'
            cursor.execute(sql_inserte, (register_username, register_password))
            connection.commit()

            cursor.execute(sql_query_username, (register_username))
            new_user = cursor.fetchall()

            if new_user:
                session['username'] = register_username
                return redirect(url_for('index', name = register_username))
            else:
                return '注册失败'


@app.route('/welcome')
def welcome():
    username = session.get('username')
    return render_template('welcome.html', name = username)

@app.route('/index')
def index():
    username = session.get('username')
    return render_template('index.html', name = username)

@app.route('/search', methods=['GET'])
def search():
    try:
        field_to_chinese = {
            'Stock_code': '股票代码',
            'Stock_name': '股票名称',
            'Company_name': '公司名称',
            'Province': '省份',
            'City': '城市',
            'IPO_date': '上市日期',
            'Founded_date': '成立日期',
            'Person': '法人',
            'Employ_num': '员工人数',
            'Product': '主营产品',
        }

        # 获取前端请求参数
        search_column = request.args.get('column')
        keyword = request.args.get('keyword')
        page = request.args.get('page', 1, type=int)
        per_page = 10  # 每页记录数

        fields_to_select = [field for field in field_to_chinese.keys()]
        select_clause = ', '.join(fields_to_select)

        # 计算偏移量
        offset = (page - 1) * per_page

        # 创建数据库连接
        connection = get_db_connection()
        
        # 构建SQL查询，使用参数化查询来防止SQL注入
        query = f"SELECT {select_clause} FROM listed_companies WHERE `{search_column}` LIKE %s LIMIT %s OFFSET %s"
        with connection.cursor() as cursor:
            cursor.execute(query, ('%' + keyword + '%', per_page, offset))
            results = cursor.fetchall()
            total_count_query = "SELECT COUNT(*) FROM listed_companies WHERE `{}` LIKE %s".format(search_column)
            cursor.execute(total_count_query, ('%' + keyword + '%',))
            total_count = cursor.fetchone()['COUNT(*)']

        # 关闭数据库连接
        connection.close()

        # 计算总页数
        total_pages = (total_count + per_page - 1) // per_page

        mapped_results = [
            {field_to_chinese[field]: value for field, value in result.items()}
            for result in results
        ]

        return jsonify({
            'results': mapped_results,
            'total_pages': total_pages,
            'current_page': page,
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/apitest/')
def apitest():
    username = request.args.get('username', 'default_username')

    # 构造要返回的 JSON 数据
    response_data = {
        'username': username
    }

    # 使用 jsonify 将字典转换为 JSON 响应
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug = True)
