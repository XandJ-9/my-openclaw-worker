"""
示例：查询个股行情
"""

from lib.api import TencentAPI
from lib.parser import StockParser


def main():
    # 初始化API和解析器
    api = TencentAPI()
    parser = StockParser()

    # 示例股票代码
    stock_codes = [
        '600718',  # 闻泰科技
        '000001',  # 平安银行
        '600519',  # 贵州茅台
    ]

    print("正在获取A股个股行情...")
    print("=" * 60)

    for code in stock_codes:
        print(f"\n查询: {code}")
        print("-" * 40)

        # 获取股票数据
        stock_info = api.get_stock_data(code)

        # 格式化输出
        print(parser.format_quote(stock_info))

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
