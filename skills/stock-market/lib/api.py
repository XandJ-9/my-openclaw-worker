"""
腾讯财经API封装
"""

import requests
import re


class TencentAPI:
    """腾讯财经API"""

    BASE_URL = "http://qt.gtimg.cn/q="

    def __init__(self):
        self.session = requests.Session()

    def get_stock_data(self, stock_code):
        """
        获取股票数据

        Args:
            stock_code: 股票代码，支持 sh600718、600718、sh600718、600718 等

        Returns:
            dict: 股票数据字典，包含错误信息或数据
        """
        # 标准化股票代码
        stock_code = self._normalize_code(stock_code)

        url = f"{self.BASE_URL}{stock_code}"

        try:
            response = self.session.get(url, timeout=5)
            response.encoding = 'gbk'

            if response.status_code != 200:
                return {'error': f"HTTP {response.status_code}"}

            # 返回格式: v_sh600745="闻泰科技~17.23~17.15~17.28~..."
            data = response.text.split('"')[1]
            values = data.split('~')

            stock_info = {
                'name': values[1],  # 股票名称
                'code': stock_code,  # 股票代码
                'open': float(values[2]),  # 开盘价
                'pre_close': float(values[3]),  # 昨日收盘
                'current': float(values[4]),  # 当前价格
                'high': float(values[5]),  # 最高价
                'low': float(values[6]),  # 最低价
                'volume': int(values[8]),  # 成交量
                'amount': float(values[9]),  # 成交额
                'date': values[30],  # 日期
                'time': values[31],  # 时间
            }

            change = stock_info['current'] - stock_info['pre_close']
            change_pct = (change / stock_info['pre_close']) * 100 if stock_info['pre_close'] != 0 else 0

            stock_info['change'] = change
            stock_info['change_pct'] = change_pct

            return stock_info

        except Exception as e:
            return {'error': str(e)}

    def get_index_data(self, index_code):
        """
        获取指数数据

        Args:
            index_code: 指数代码，如 sh000001、sz399001 等

        Returns:
            dict: 指数数据字典
        """
        return self.get_stock_data(index_code)

    def get_multi_index_data(self, index_codes):
        """
        批量获取指数数据

        Args:
            index_codes: 指数代码列表

        Returns:
            dict: 指数数据字典 {code: data}
        """
        results = {}
        for code in index_codes:
            results[code] = self.get_index_data(code)
        return results

    def _normalize_code(self, code):
        """
        标准化股票代码

        Args:
            code: 原始股票代码

        Returns:
            str: 标准化后的股票代码
        """
        code = str(code).strip().upper()

        # 如果已经是标准格式，直接返回
        if code.startswith('SH') or code.startswith('SZ'):
            return code.lower()

        # 如果没有前缀，添加前缀
        if len(code) == 6:
            if code.startswith('6'):
                return f"sh{code}"
            else:
                return f"sz{code}"
        else:
            # 保留原样
            return code
