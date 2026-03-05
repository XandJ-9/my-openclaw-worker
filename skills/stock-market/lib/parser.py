"""
数据解析器
"""

import re
from datetime import datetime


class StockParser:
    """股票数据解析器"""

    def parse_response(self, response_text):
        """
        解析API响应文本

        Args:
            response_text: API返回的文本

        Returns:
            dict: 解析后的数据字典
        """
        stocks = {}
        pattern = r'v_(\w+)="([^"]+)"'

        matches = re.findall(pattern, response_text)

        for match in matches:
            code = match[0]
            data = match[1].split('~')
            stocks[code] = {
                "name": data[1],  # 指数名称
                "code": data[2],  # 指数代码
                "current": float(data[3]),  # 当前价格
                "yesterday": float(data[4]),  # 昨日收盘
                "open": float(data[5]),  # 开盘价
                "high": float(data[6]),  # 最高价
                "low": float(data[7]),  # 最低价
                "volume": int(data[8]),  # 成交量
                "amount": float(data[9]),  # 成交额
                "bid": float(data[10]),  # 买一价
                "ask": float(data[11]),  # 卖一价
                "date": data[12],  # 日期
                "time": data[13],  # 时间
                "change": float(data[14]),  # 涨跌额
                "change_percent": float(data[15]),  # 涨跌幅
            }

        return stocks

    def format_table(self, stocks):
        """
        格式化输出表格

        Args:
            stocks: 股票数据字典

        Returns:
            str: 格式化后的表格字符串
        """
        lines = []
        lines.append("=" * 60)
        lines.append(f"{'指数名称':<15} {'代码':<10} {'当前':<10} {'涨跌额':<10} {'涨跌幅':<10} {'成交量':<15}")
        lines.append("=" * 60)

        for code, stock in stocks.items():
            name = stock['name']
            code_num = stock['code']
            current = stock['current']
            change = stock['change']
            change_percent = stock['change_percent']
            volume = stock['volume']

            # 判断涨跌颜色
            color = "红" if change >= 0 else "绿"
            change_str = f"{change:+.2f}"
            change_percent_str = f"{change_percent:+.2f}%"

            lines.append(f"{name:<15} {code_num:<10} {current:<10.2f} {change_str:<10} {change_percent_str:<10} {volume:<15}")

        lines.append("=" * 60)

        return "\n".join(lines)

    def format_quote(self, stock_info):
        """
        格式化单个股票行情

        Args:
            stock_info: 股票数据字典

        Returns:
            str: 格式化后的行情文本
        """
        if 'error' in stock_info:
            return f"获取失败: {stock_info['error']}"

        lines = []
        lines.append("=" * 26)
        lines.append(f"[行情] {stock_info['name']} ({stock_info['date']} {stock_info['time']})")
        lines.append("=" * 26)
        lines.append(f"[现价] {stock_info['current']:.2f} 元")
        lines.append(f"[涨跌] {stock_info['change']:+.2f} 元 ({stock_info['change_pct']:+.2f}%)")
        lines.append(f"[开盘] {stock_info['open']:.2f}")
        lines.append(f"[最高] {stock_info['high']:.2f}")
        lines.append(f"[最低] {stock_info['low']:.2f}")
        lines.append(f"[昨收] {stock_info['pre_close']:.2f}")
        lines.append(f"[成交量] {stock_info['volume']:,} 手")
        lines.append(f"[成交额] {stock_info['amount']:.2f} 万")
        lines.append("=" * 26)

        return "\n".join(lines)

    def calculate_statistics(self, stocks):
        """
        计算统计数据

        Args:
            stocks: 股票数据字典

        Returns:
            dict: 统计数据
        """
        stats = {
            "market_status": "上涨" if stocks.get('sh000001', {}).get('change', 0) > 0 else
                            "下跌" if stocks.get('sh000001', {}).get('change', 0) < 0 else "震荡",
            "avg_change": 0,
            "avg_change_percent": 0,
            "up_stocks": 0,
            "down_stocks": 0,
            "total_volume": 0,
            "total_amount": 0,
        }

        # 计算平均涨跌和涨跌幅
        total_change = 0
        total_change_percent = 0
        up_count = 0
        down_count = 0

        for code, stock in stocks.items():
            total_change += stock.get('change', 0)
            total_change_percent += stock.get('change_percent', 0)
            if stock.get('change', 0) > 0:
                up_count += 1
            elif stock.get('change', 0) < 0:
                down_count += 1

        stats['avg_change'] = total_change / len(stocks) if stocks else 0
        stats['avg_change_percent'] = total_change_percent / len(stocks) if stocks else 0
        stats['up_stocks'] = up_count
        stats['down_stocks'] = down_count
        stats['total_volume'] = stocks.get('sh000001', {}).get('volume', 0)
        stats['total_amount'] = stocks.get('sh000001', {}).get('amount', 0)

        return stats
