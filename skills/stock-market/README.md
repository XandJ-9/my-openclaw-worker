# Stock Market Skill - 股市行情数据获取技能

使用腾讯财经API获取A股市场行情数据，支持指数、个股查询和复盘报告生成。

## 功能

1. **指数行情查询**
   - 上证指数 (sh000001)
   - 深证成指 (sz399001)
   - 创业板指 (sz399006)
   - 中小板指 (sz399005)

2. **个股行情查询**
   - 支持任意A股个股
   - 自动识别上海/深圳交易所
   - 支持多种代码格式

3. **复盘报告生成**
   - 自动生成Markdown格式报告
   - 包含市场情绪统计
   - 基础操作建议

## 安装

```bash
# 进入技能目录
cd skills/stock-market

# 使用uv安装依赖
uv add requests
```

## 使用方法

### Python代码示例

```python
from __init__ import StockMarketSkill

# 初始化技能
skill = StockMarketSkill()

# 1. 获取指数行情
result = skill.get_index_quote()
print(result['table'])
print(result['summary'])
print(result['report'])

# 2. 查询个股行情
result = skill.get_stock_quote('600519')  # 贵州茅台
print(result['formatted'])

# 3. 快速查询
quote = skill.quick_quote('600718')
print(quote)

# 4. 生成每日复盘报告
report = skill.generate_daily_report()
print(report['report'])
```

### 命令行示例

```bash
# 查询指数行情
python examples/index_quote.py

# 查询个股行情
python examples/stock_quote.py
```

## API文档

### StockMarketSkill 类

#### get_index_quote(index_codes=None)

获取指数行情数据。

**参数:**
- `index_codes`: 指数代码列表（可选）

**返回:**
- `table`: 表格格式数据
- `summary`: 简要摘要
- `report`: Markdown格式报告
- `stats`: 统计数据
- `stocks`: 原始数据

#### get_stock_quote(stock_code)

获取个股行情数据。

**参数:**
- `stock_code`: 股票代码

**返回:**
- `quote`: 原始数据
- `formatted`: 格式化行情
- `quick`: 快速行情

#### generate_daily_report(date=None)

生成每日复盘报告。

**参数:**
- `date`: 日期字符串（可选，默认为今天）

**返回:**
- `report`: Markdown格式报告
- `stocks`: 指数数据
- `stats`: 统计数据
- `date`: 报告日期

#### quick_quote(stock_code)

快速获取个股行情（简洁格式）。

**参数:**
- `stock_code`: 股票代码

**返回:**
- `str`: 快速行情文本

## 数据源

- **API**: 腾讯财经 (http://qt.gtimg.cn/q=)
- **编码**: GBK
- **延迟**: 5-15秒

## 注意事项

1. 仅在交易时间（9:30-15:00）有实时数据
2. 周末/节假日可能无数据
3. API对请求频率有限制
4. 数据可能包含延迟

## 文件结构

```
stock-market/
├── SKILL.md              # 技能说明
├── README.md             # 使用文档
├── requirements.txt      # 依赖列表
├── __init__.py           # 主接口
├── lib/
│   ├── __init__.py
│   ├── api.py            # API封装
│   ├── parser.py         # 数据解析
│   └── reporter.py       # 报告生成
└── examples/
    ├── index_quote.py    # 指数查询示例
    └── stock_quote.py    # 个股查询示例
```

## 依赖

- Python 3.7+
- requests >= 2.31.0

## 许可证

MIT
