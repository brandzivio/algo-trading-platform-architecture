"""Small helpers for backtests: slippage and net P&L after costs. No dependencies."""

from .costs import slippage, slippage_bps, net_pnl

__all__ = ["slippage", "slippage_bps", "net_pnl"]
__version__ = "0.1.0"
