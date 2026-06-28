#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据预处理脚本：从 MySQL 数据库读取上市公司数据，
统计各省份上市公司数量，生成 ECharts 饼图所需的 JSON 文件。
"""

import pymysql
import json
import os

# 数据库连接配置（与 app.py 保持一致）
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'lhl123456',
    'database': 'python_final_project',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    """建立并返回 MySQL 连接"""
    return pymysql.connect(**DB_CONFIG)

def generate_province_json():
    """从数据库统计各省份上市公司数量，输出 JSON 文件"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 查询每个省份的上市公司数量
    sql = """
        SELECT Province, COUNT(*) AS count
        FROM listed_companies
        WHERE Province IS NOT NULL AND Province != ''
        GROUP BY Province
        ORDER BY count DESC
    """
    cursor.execute(sql)
    results = cursor.fetchall()

    # 转换成 {省份名: 数量} 的格式
    province_data = {}
    for row in results:
        province = row['Province']
        count = row['count']
        province_data[province] = count

    # 输出路径：static/data/SSGS_province_counts.json
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'static', 'data', 'SSGS_province_counts.json'
    )

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(province_data, f, ensure_ascii=False, indent=2)

    print(f"✅ 生成成功：{output_path}")
    print(f"   共统计 {len(province_data)} 个省份，{sum(province_data.values())} 条记录")

    cursor.close()
    conn.close()

if __name__ == '__main__':
    generate_province_json()
