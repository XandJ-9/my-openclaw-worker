"""
报告生成器
"""

from datetime import datetime


class StockReporter:
    """股票报告生成器"""

    def generate_index_report(self, stocks, stats):
        """
        生成指数行情报告

        Args:
            stocks: 指数数据字典
            stats: 统计数据

        Returns:
            str: Markdown格式的报告
        """
        report = f"""# A股指数行情报告

**报告时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**市场状态：** {stats['market_status']}

---

## 主要指数表现

| 指数名称 | 代码 | 当前点位 | 昨日收盘 | 涨跌额 | 涨跌幅 | 成交额(亿元) |
|---------|------|---------|---------|--------|--------|------------|
"""

        for code, stock in stocks.items():
            if 'error' not in stock:
                report += f"| {stock['name']} | {stock['code']} | {stock['current']:.2f} | {stock['yesterday']:.2f} | {stock['change']:+.2f} | {stock['change_percent']:+.2f}% | {stock['amount']/100000000:.2f} |\n"

        report += f"""
---

## 市场情绪

- **平均涨跌幅：** {stats['avg_change_percent']:+.2f}%
- **上涨家数：** {stats['up_stocks']}
- **下跌家数：** {stats['down_stocks']}
- **市场活跃度：** {stats['total_amount']/100000000:.2f}亿元

---

## 操作建议

"""

        if stats['market_status'] == '上涨':
            report += "- 市场表现强劲，建议关注强势板块和龙头个股。\n- 可适当增加仓位，但注意控制风险。\n- 关注成交量变化，放量上涨更具持续性。"
        elif stats['market_status'] == '下跌':
            report += "- 市场调整，建议控制仓位，等待企稳信号。\n- 可关注超跌板块和个股的反弹机会。\n- 避免追涨杀跌，保持理性投资。"
        else:
            report += "- 市场震荡，建议观望为主。\n- 可关注结构性机会。\n- 保持合理仓位，灵活应对。"

        report += f"""

---

**数据来源：** 腾讯财经API
"""

        return report

    def generate_summary(self, stocks):
        """
        生成简要摘要

        Args:
            stocks: 指数数据字典

        Returns:
            str: 简要摘要
        """
        summary_lines = []
        summary_lines.append("=" * 60)
        summary_lines.append("A股市场数据摘要")
        summary_lines.append("=" * 60)

        for code, stock in stocks.items():
            if 'error' not in stock:
                color = "红" if stock['change'] >= 0 else "绿"
                summary_lines.append(
                    f"{stock['name']}: {stock['current']:.2f} ({stock['change']:+.2f} / {stock['change_percent']:+.2f}%)"
                )

        summary_lines.append("=" * 60)

        return "\n".join(summary_lines)

    def generate_quick_quote(self, stock_info):
        """
        生成快速行情显示

        Args:
            stock_info: 股票数据字典

        Returns:
            str: 快速行情文本
        """
        if 'error' in stock_info:
            return f"❌ {stock_info['error']}"

        lines = []
        lines.append(f"📊 {stock_info['name']} ({stock_info['code']})")
        lines.append(f"   现价: {stock_info['current']:.2f} 元")
        lines.append(f"   涨跌: {stock_info['change']:+.2f} ({stock_info['change_pct']:+.2f}%)")
        lines.append(f"   开盘: {stock_info['open']:.2f} | 最高: {stock_info['high']:.2f} | 最低: {stock_info['low']:.2f}")
        lines.append(f"   成交量: {stock_info['volume']:,} 手 | 成交额: {stock_info['amount']:.2f} 万")

        return "\n".join(lines)
