from __future__ import annotations

_SIDES = ("buy", "sell")


def _check_side(side: str) -> str:
    side = side.lower()
    if side not in _SIDES:
        raise ValueError("side must be 'buy' or 'sell'")
    return side


def slippage(expected_price: float, fill_price: float, side: str) -> float:
    """Slippage per unit, in price terms.

    Positive means the fill was worse than expected: paying more on a buy,
    or receiving less on a sell. Negative means price improvement.
    """
    side = _check_side(side)
    return fill_price - expected_price if side == "buy" else expected_price - fill_price


def slippage_bps(expected_price: float, fill_price: float, side: str) -> float:
    """Slippage as basis points of the expected price (1 bp = 0.01%)."""
    if expected_price <= 0:
        raise ValueError("expected_price must be positive")
    return slippage(expected_price, fill_price, side) / expected_price * 10_000


def net_pnl(
    entry_price: float,
    exit_price: float,
    qty: float,
    side: str = "buy",
    slippage_bps_per_leg: float = 0.0,
    brokerage_per_order: float = 0.0,
    charges_pct: float = 0.0,
) -> float:
    """Net P&L of one round trip after slippage, brokerage and percentage charges.

    side is the direction of the OPENING trade: 'buy' for a long, 'sell' for a short.
    slippage_bps_per_leg is applied against you on each of the two legs.
    brokerage_per_order is a flat amount per order (two orders in a round trip).
    charges_pct is a percentage of traded value (entry + exit) for all other
    charges; set it from your own broker's current charge sheet, because
    statutory rates change and are not built into this package.
    """
    side = _check_side(side)
    if qty <= 0:
        raise ValueError("qty must be positive")
    adj = slippage_bps_per_leg / 10_000
    if side == "buy":
        entry_fill = entry_price * (1 + adj)
        exit_fill = exit_price * (1 - adj)
        gross = (exit_fill - entry_fill) * qty
    else:
        entry_fill = entry_price * (1 - adj)
        exit_fill = exit_price * (1 + adj)
        gross = (entry_fill - exit_fill) * qty
    traded_value = (entry_fill + exit_fill) * qty
    return gross - 2 * brokerage_per_order - traded_value * charges_pct / 100
