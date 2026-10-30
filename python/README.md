# brandzivio-trade-costs

Tiny, dependency-free helpers for backtests and paper trading:

- `slippage(expected_price, fill_price, side)` per-unit slippage (positive = worse than expected)
- `slippage_bps(expected_price, fill_price, side)` the same in basis points
- `net_pnl(entry, exit, qty, side, slippage_bps_per_leg, brokerage_per_order, charges_pct)` round-trip P&L after costs

```python
from brandzivio_trade_costs import slippage_bps, net_pnl

slippage_bps(200, 200.2, "buy")                       # 10.0 bps
net_pnl(100, 110, 10, slippage_bps_per_leg=5,
        brokerage_per_order=20, charges_pct=0.05)     # net of slippage, brokerage and charges
```

## What it deliberately does not do

- It has **no built-in tax or exchange charge rates**. Statutory rates change, so pass `charges_pct` from your own broker's current charge sheet.
- It does not model market impact, partial fills or queue position.
- A backtest result describes the past and is not a promise of future returns.

## Where it fits

Slippage, brokerage and charges are the fill-model inputs of a backtester: see [Algo Trading Software Architecture](https://brandzivio.com/solutions/algo-trading-website-development) for how the backtester, paper trading and order layer fit together. Source: [algo-trading-platform-architecture](https://github.com/brandzivio/algo-trading-platform-architecture/tree/main/python).

By [Brandzivio](https://brandzivio.com). MIT licensed.
