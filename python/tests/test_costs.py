import math
import pytest
from brandzivio_trade_costs import slippage, slippage_bps, net_pnl


def test_slippage_buy_and_sell():
    assert slippage(100, 100.5, "buy") == pytest.approx(0.5)
    assert slippage(100, 99.5, "sell") == pytest.approx(0.5)
    assert slippage(100, 99.8, "buy") == pytest.approx(-0.2)  # price improvement


def test_slippage_bps():
    assert slippage_bps(200, 200.2, "buy") == pytest.approx(10.0)


def test_net_pnl_no_costs_matches_gross():
    assert net_pnl(100, 110, 10) == pytest.approx(100.0)
    assert net_pnl(100, 90, 10, side="sell") == pytest.approx(100.0)


def test_net_pnl_costs_reduce_result():
    base = net_pnl(100, 110, 10)
    with_costs = net_pnl(100, 110, 10, slippage_bps_per_leg=5, brokerage_per_order=20, charges_pct=0.05)
    assert with_costs < base
    # brokerage only: two orders
    assert net_pnl(100, 110, 10, brokerage_per_order=20) == pytest.approx(60.0)


def test_validation():
    with pytest.raises(ValueError):
        slippage(100, 100, "hold")
    with pytest.raises(ValueError):
        net_pnl(100, 110, 0)
    with pytest.raises(ValueError):
        slippage_bps(0, 1, "buy")
