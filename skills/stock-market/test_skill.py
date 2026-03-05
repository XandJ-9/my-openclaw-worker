"""
测试股票行情技能
"""

import sys
import os

# 添加技能目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from __init__ import StockMarketSkill


def test_index_quote():
    """测试指数行情查询"""
    print("=" * 60)
    print("测试1: 查询A股指数行情")
    print("=" * 60)

    skill = StockMarketSkill()
    result = skill.get_index_quote()

    print(result['table'])
    print("\n" + result['summary'])
    print("\n" + result['report'][:500] + "...")

    return result


def test_stock_quote():
    """测试个股行情查询"""
    print("\n" + "=" * 60)
    print("测试2: 查询个股行情")
    print("=" * 60)

    skill = StockMarketSkill()

    # 测试贵州茅台
    print("\n查询: 600519 贵州茅台")
    result = skill.get_stock_quote('600519')
    print(result['formatted'])

    # 测试闻泰科技
    print("\n查询: 600718 闻泰科技")
    result = skill.get_stock_quote('600718')
    print(result['formatted'])

    return result


def test_quick_quote():
    """测试快速查询"""
    print("\n" + "=" * 60)
    print("测试3: 快速查询个股行情")
    print("=" * 60)

    skill = StockMarketSkill()

    quote = skill.quick_quote('000001')
    print(quote)

    return quote


def test_daily_report():
    """测试每日报告生成"""
    print("\n" + "=" * 60)
    print("测试4: 生成每日复盘报告")
    print("=" * 60)

    skill = StockMarketSkill()
    result = skill.generate_daily_report()

    print(result['report'])

    return result


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("股票行情技能测试")
    print("=" * 60)

    try:
        test_index_quote()
        test_stock_quote()
        test_quick_quote()
        test_daily_report()

        print("\n" + "=" * 60)
        print("[OK] 所有测试完成!")
        print("=" * 60)

    except Exception as e:
        print(f"\n[ERROR] 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
