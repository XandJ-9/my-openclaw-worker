#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股实时行情数据抓取脚本
获取上证指数、深证成指、创业板指的实时行情
"""

import requests
import csv
import time
from datetime import datetime

def get_stock_data():
    """获取A股主要指数的实时行情数据"""

    # 指数代码映射
    stock_codes = {
        'sh000001': '上证指数',
        'sz399001': '深证成指',
        'sz399006': '创业板指'
    }

    # 东方财富网API
    url = "http://push2his.eastmoney.com/api/qt/clist/get"

    results = []

    for code, name in stock_codes.items():
        try:
            print(f"正在获取{name}({code})数据...")

            # 构建请求参数
            params = {
                'pn': 1,  # 第1页
                'pz': 20,  # 每页20条
                'po': 1,  # 排序方式：1为升序
                'np': 1,  # 是否下一页
                'fltt': 2,  # 数据类型：2为行情数据
                'invt': 2,  # 通用标识：2为前端展示用
                'fid': 'f3',  # 排序字段：f3为涨跌幅
                'fs': f'm:{code.split("_")[0]}+t:{code.split("_")[1] if len(code.split("_")) > 1 else "6"}',  # 市场代码
                'fields': 'f12,f14,f2,f3,f4,f5,f6,f7,f8,f9,f10,f13,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152,f152,f167,f168,f169,f170,f171,f172,f173,f174,f175,f176,f177,f178,f179,f180,f181,f182,f183,f184,f185,f186,f187,f188,f189,f190,f191,f192,f193,f194,f195,f196,f197,f198,f199,f200,f201,f202,f203,f204,f205,f206,f207,f208,f209,f210,f211,f212,f213,f214,f215,f216,f217,f218,f219,f220,f221,f222,f223,f224,f225,f226,f227,f228,f229,f230,f231,f232,f233,f234,f235,f236,f237,f238,f239,f240,f241,f242,f243,f244,f245,f246,f247,f248,f249,f250,f251,f252,f253,f254,f255,f256,f257,f258,f297,f298,f299,f300,f301,f302,f303,f304,f305,f306,f307,f308,f309,f310,f311,f312,f313,f314,f315,f316,f317,f318,f319,f320,f321,f322,f323,f324,f325,f326,f327,f328,f329,f330,f331,f332,f333,f334,f335,f336,f337,f338,f339,f340,f341,f342,f343,f344,f345,fc1,fc2,fc3,fc4,fc5,fc6,fc7,主要描述',
                'ut': 'fa5fd1943c7b386f172d6893dbfba10b601e0408685e9',
                'cb': 'jQuery11230181540993757293_1710288390000'  # JSONP回调函数名
            }

            # 设置超时
            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                # 解析JSON数据
                data = response.json()

                if data and 'data' in data and 'diff' in data['data'] and len(data['data']['diff']) > 0:
                    stock_data = data['data']['diff'][0]

                    result = {
                        '指数名称': name,
                        '股票代码': code,
                        '最新价': stock_data.get('f2', ''),
                        '涨跌幅(%)': stock_data.get('f3', ''),
                        '涨跌额': stock_data.get('f4', ''),
                        '今开': stock_data.get('f5', ''),
                        '昨收': stock_data.get('f6', ''),
                        '最高': stock_data.get('f7', ''),
                        '最低': stock_data.get('f8', ''),
                        '成交量': stock_data.get('f9', ''),
                        '成交额': stock_data.get('f10', ''),
                        '更新时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    results.append(result)
                    print(f"✓ 成功获取{name}数据")
                else:
                    print(f"✗ 获取{name}数据失败：数据为空")
            else:
                print(f"✗ 获取{name}数据失败：HTTP状态码{response.status_code}")

        except requests.exceptions.Timeout:
            print(f"✗ 获取{name}数据超时")
        except requests.exceptions.RequestException as e:
            print(f"✗ 获取{name}数据出错：{str(e)}")
        except Exception as e:
            print(f"✗ 获取{name}数据出错：{str(e)}")

        # 避免请求过快
        time.sleep(0.5)

    # 保存到CSV文件
    if results:
        filename = f"stock_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            fieldnames = ['指数名称', '股票代码', '最新价', '涨跌幅(%)', '涨跌额', '今开', '昨收', '最高', '最低', '成交量', '成交额', '更新时间']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

        print(f"\n✓ 数据已保存到 {filename}")
        print("\n今日A股行情概览：")
        print("-" * 80)
        for r in results:
            print(f"{r['指数名称']:8s} 最新价: {r['最新价']:>8s}  涨跌幅: {r['涨跌幅(%)']:>6s}%  涨跌额: {r['涨跌额']:>8s}")
        print("-" * 80)
    else:
        print("\n✗ 未获取到任何数据")

if __name__ == "__main__":
    print("开始获取A股实时行情数据...")
    print("=" * 80)
    get_stock_data()
