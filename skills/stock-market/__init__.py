"""
Stock Market Skill - 主接口
"""

from lib.api import TencentAPI
from lib.parser import StockParser
from lib.reporter import StockReporter


class StockMarketSkill:
    """股市行情数据获取技能"""

    def __init__(self):
        self.api = TencentAPI()
        self.parser = StockParser()
        self.reporter = StockReporter()

    def get_index_quote(self, index_codes=None):
        """
        获取指数行情

        Args:
            index_codes: 指数代码列表，默认为常用指数

        Returns:
            dict: 包含表格、摘要和报告的字典
        """
        if index_codes is None:
            index_codes = [
                'sh000001',  # 上证指数
                'sz399001',  # 深证成指
                'sz399006',  # 创业板指
                'sz399005',  # 中小板指
            ]

        # 获取原始数据
        raw_data = self.api.get_multi_index_data(index_codes)

        # 将字典转换为字符串格式（API返回的格式）
        response_text = ""
        for code, data in raw_data.items():
            response_text += f'v_{code}="{data.get("name", "")}~{data.get("code", "")}~{data.get("open", 0)}~{data.get("pre_close", 0)}~{data.get("current", 0)}~{data.get("high", 0)}~{data.get("low", 0)}~{data.get("volume", 0)}~{data.get("amount", 0)}~{data.get("bid", 0)}~{data.get("ask", 0)}~{data.get("date", "")}~{data.get("time", "")}~{data.get("change", 0)}~{data.get("change_percent", 0)}"\n'

        # 解析数据
        stocks = self.parser.parse_response(response_text)

        # 计算统计
        stats = self.parser.calculate_statistics(stocks)

        return {
            'table': self.parser.format_table(stocks),
            'summary': self.parser.generate_summary(stocks),
            'report': self.reporter.generate_index_report(stocks, stats),
            'stats': stats,
            'stocks': stocks
        }

    def get_stock_quote(self, stock_code):
        """
        获取个股行情

        Args:
            stock_code: 股票代码

        Returns:
            dict: 包含行情数据和格式化输出的字典
        """
        stock_info = self.api.get_stock_data(stock_code)

        return {
            'quote': stock_info,
            'formatted': self.parser.format_quote(stock_info),
            'quick': self.reporter.generate_quick_quote(stock_info)
        }

    def generate_daily_report(self, date=None):
        """
        生成每日复盘报告

        Args:
            date: 日期字符串，格式为YYYY-MM-DD

        Returns:
            dict: 包含报告和数据的字典
        """
        if date is None:
            from datetime import datetime
            date = datetime.now().strftime('%Y-%m-%d')

        # 获取主要指数数据
        index_codes = [
            'sh000001',  # 上证指数
            'sz399001',  # 深证成指
            'sz399006',  # 创业板指
            'sz399005',  # 中小板指
        ]

        stocks = self.parser.parse_response(self.api.get_multi_index_data(index_codes))
        stats = self.parser.calculate_statistics(stocks)

        report = self.reporter.generate_index_report(stocks, stats)

        return {
            'report': report,
            'stocks': stocks,
            'stats': stats,
            'date': date
        }

    def quick_quote(self, stock_code):
        """
        快速获取个股行情（简洁格式）

        Args:
            stock_code: 股票代码

        Returns:
            str: 快速行情文本
        """
        stock_info = self.api.get_stock_data(stock_code)
        return self.reporter.generate_quick_quote(stock_info)

    def format_table(self, stocks):
        """
        格式化股票表格

        Args:
            stocks: 股票数据字典

        Returns:
            str: 格式化后的表格
        """
        return self.parser.format_table(stocks)

    def format_quote(self, stock_info):
        """
        格式化股票行情

        Args:
            stock_info: 股票数据字典

        Returns:
            str: 格式化后的行情
        """
        return self.parser.format_quote(stock_info)
