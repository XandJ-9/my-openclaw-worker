"""
示例：查询A股指数行情
"""

from lib.api import TencentAPI
from lib.parser import StockParser
from lib.reporter import StockReporter


def main():
    # 初始化API和解析器
    api = TencentAPI()
    parser = StockParser()
    reporter = StockReporter()

    # 主要指数代码
    index_codes = [
        'sh000001',  # 上证指数
        'sz399001',  # 深证成指
        'sz399006',  # 创业板指
        'sz399005',  # 中小板指
    ]

    print("正在获取A股指数行情...")
    print("=" * 60)

    # 获取数据
    stocks = parser.parse_response(api.get_multi_index_data(index_codes))

    # 格式化输出
    print(parser.format_table(stocks))

    # 生成摘要
    print("\n" + parser.generate_summary(stocks))

    # 生成报告
    stats = parser.calculate_statistics(stocks)
    print("\n" + reporter.generate_index_report(stocks, stats))


if __name__ == "__main__":
    main()
