# -*- coding: utf-8 -*-
import requests
import csv
from datetime import datetime

def get_stock_data():
    # 新浪财经API
    codes = ['sh000001', 'sz399001', 'sz399006']
    names = ['上证指数', '深证成指', '创业板指']

    results = []

    for code, name in zip(codes, names):
        try:
            url = f"http://hq.sinajs.cn/list={code}"
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                # 解析新浪返回的数据
                # 格式：var hq_str_sh000001="上证指数,12.34,12.35,12.36,...";
                data_str = response.text.split('=')[1].strip('"').strip("'")
                parts = data_str.split(',')

                if len(parts) >= 32:
                    result = {
                        '指数名称': name,
                        '股票代码': code,
                        '最新价': parts[1],
                        '涨跌幅(%)': parts[2],
                        '涨跌额': parts[3],
                        '今开': parts[4],
                        '昨收': parts[5],
                        '最高': parts[6],
                        '最低': parts[7],
                        '成交量': parts[8],
                        '成交额': parts[9],
                        '更新时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    results.append(result)
                    print(f"[OK] {name}: 最新价={result['最新价']}, 涨跌幅={result['涨跌幅(%)']}%")
                else:
                    print(f"[ERROR] {name}: 数据格式错误")
            else:
                print(f"[ERROR] {name}: HTTP {response.status_code}")
        except Exception as e:
            print(f"[ERROR] {name}: {str(e)}")

    # 保存CSV
    if results:
        filename = f"stock_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            fieldnames = ['指数名称', '股票代码', '最新价', '涨跌幅(%)', '涨跌额', '今开', '昨收', '最高', '最低', '成交量', '成交额', '更新时间']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

        print(f"\n[OK] 数据已保存到 {filename}")
    else:
        print("\n[ERROR] 未获取到数据")

if __name__ == "__main__":
    print("开始获取A股行情...")
    print("=" * 60)
    get_stock_data()
