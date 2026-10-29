# Algo trading platform: architecture notes

A reference for the broker layer and order layer of an algo trading website: login, session, order endpoints, tagging, rate limits, risk controls. Written around the Kite Connect API; the same layer design applies to other broker APIs.

Maintained by [Brandzivio](https://brandzivio.com), a software company in Gurugram, India.

> Software design only, not investment or legal advice. Backtest results describe the past and are not a promise of future returns. Licences and compliance stay with the business running the platform.

## Components

- **Strategy builder**: rule-based entry and exit conditions, parameters and position sizing, saved and versioned per user.
- **Backtester**: replays historical candles against a strategy and reports trades, drawdown and returns, with slippage, brokerage and statutory charges modelled.
- **Paper trading**: runs a strategy on live quotes with simulated fills and no real orders.
- **Order layer**: the only code allowed to send orders. Tags each order, enforces rate limits, keeps an audit log.
- **Risk controls**: per-strategy and per-day loss limits, order-size limits, a kill switch.

The same strategy code backtests, paper trades and goes live, so results are comparable.

## Kite Connect login and order flow

| Step | Kite Connect behaviour | What the broker layer does |
|---|---|---|
| Login | User is sent to the Kite login page with the API key; Kite redirects back with a short-lived `request_token` | Starts the login per client and captures `request_token` on the registered redirect URL |
| Session | `POST /session/token` with `api_key`, `request_token` and a SHA-256 checksum of api_key, request_token and api_secret | Builds the checksum on the server, stores the `access_token` encrypted against the client |
| Token expiry | `access_token` expires at 6 AM the next day unless invalidated earlier | Schedules the daily re-login prompt and pauses live strategies for clients whose token has lapsed |
| Order | `POST /orders/:variety` (regular, amo, co, iceberg) | Sends orders only from the order layer after risk checks, never straight from a strategy |
| Tag | Optional order tag, alphanumeric, up to 20 characters, returned in the order book | Writes a compact strategy and version tag so every order traces to the exact rule set |

Check Zerodha's current documentation and support pages for order-rate limits and static-IP requirements before launch; they change.

## Order tags

[`order-tag.ts`](order-tag.ts) builds a tag that stays inside the 20-character alphanumeric limit and maps back to a strategy version in your own audit log.

## Full guide

Build custom, white-label or subscribe, cost and phasing, and what Brandzivio delivers in each project: [algo trading software development guide](https://brandzivio.com/solutions/algo-trading-website-development). Related: [trading app development service](https://brandzivio.com/services/trading-app-development).

MIT licensed.
