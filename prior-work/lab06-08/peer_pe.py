"""Comparable-company P/E analysis.

Edit only the INPUTS section.  Values are per share in the same currency.
This is an equity-multiple analysis: cash and debt are intentionally not used.
"""

from statistics import median


# ================================ INPUTS =================================
# Use None when an input is unavailable.  Diluted EPS must be positive for P/E.
TARGET = {
    "name": "Joby Aviation",
    "ticker": "JOBY",
    "price": 6.69,  # Sept. 1, 2026 regular-session close; Stock Analysis historical table.
    "diluted_eps": -1.13,
}

# Add one dictionary per peer.  A peer with a duplicate ticker/name is kept only
# once, and a peer matching the target ticker/name is excluded.
PEERS = [
    {"name": "Archer Aviation", "ticker": "ACHR", "price": 5.56, "diluted_eps": -0.99},
    {"name": "Eve Air Mobility", "ticker": "EVEX", "price": 2.20, "diluted_eps": -0.70},
]
# ===========================================================================


def identifier(company):
    """Return a case-insensitive key, preferring ticker to company name."""
    ticker = str(company.get("ticker") or "").strip().casefold()
    name = str(company.get("name") or "").strip().casefold()
    return ticker or name


def label(company):
    """Return a readable peer label."""
    name = str(company.get("name") or "Unnamed peer").strip()
    ticker = str(company.get("ticker") or "").strip()
    return f"{name} ({ticker})" if ticker else name


def positive_number(value):
    """Return True only for a numeric value strictly above zero."""
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def format_price(value):
    return f"${value:.2f}"


def prepare_peers():
    """Exclude target, remove duplicates, and retain a reason for every row."""
    target_id = identifier(TARGET)
    seen = set()
    prepared = []

    for peer in PEERS:
        peer_id = identifier(peer)
        row = {"peer": peer, "status": "usable", "pe": None}
        if not peer_id:
            row["status"] = "not meaningful (missing ticker and name)"
        elif peer_id == target_id:
            row["status"] = "excluded (matches target)"
        elif peer_id in seen:
            row["status"] = "excluded (duplicate peer)"
        else:
            seen.add(peer_id)
            price = peer.get("price")
            eps = peer.get("diluted_eps")
            if not positive_number(price) or not positive_number(eps):
                row["status"] = (
                    "not meaningful (price and diluted EPS must both be positive)"
                )
            else:
                row["pe"] = price / eps
        prepared.append(row)
    return prepared


def print_peer_table(rows):
    print("Peer P/E")
    if not rows:
        print("No peers entered.")
        return
    for row in rows:
        peer = row["peer"]
        if row["pe"] is None:
            print(f"- {label(peer)}: {row['status']}")
        else:
            print(f"- {label(peer)}: {row['pe']:.6f}x")


def target_eps_is_usable():
    return positive_number(TARGET.get("diluted_eps"))


def print_full_estimate(multiples):
    print("\nImplied target prices")
    if not multiples:
        print("No usable peers.")
        return None
    if not target_eps_is_usable():
        print("Not meaningful: target diluted EPS must be positive.")
        return None

    target_eps = TARGET["diluted_eps"]
    low_multiple = min(multiples)
    median_multiple = median(multiples)
    high_multiple = max(multiples)
    median_price = median_multiple * target_eps

    if len(multiples) == 1:
        print("One usable peer: reference estimate only; no range.")
        print(f"Reference P/E: {median_multiple:.6f}x")
        print(f"Reference implied price: {format_price(median_price)}")
    else:
        print(f"Minimum P/E: {low_multiple:.6f}x; implied price: {format_price(low_multiple * target_eps)}")
        print(f"Median P/E: {median_multiple:.6f}x; implied price: {format_price(median_price)}")
        print(f"Maximum P/E: {high_multiple:.6f}x; implied price: {format_price(high_multiple * target_eps)}")
    return median_price


def print_peer_removals(rows, full_median_price):
    print("\nPeer-removal check")
    usable_rows = [row for row in rows if row["pe"] is not None]
    if not usable_rows:
        print("No usable peers; no removal estimates.")
        return
    if full_median_price is None:
        print("Not meaningful: full-peer target estimate is unavailable.")
        return

    for row in usable_rows:
        remaining = [other["pe"] for other in usable_rows if other is not row]
        if not remaining:
            print(f"- Remove {label(row['peer'])}: no estimate (no peers remain).")
            continue
        remaining_price = median(remaining) * TARGET["diluted_eps"]
        change = remaining_price - full_median_price
        print(
            f"- Remove {label(row['peer'])}: remaining median-implied price "
            f"{format_price(remaining_price)}; change {change:+.2f}"
        )


def main():
    rows = prepare_peers()
    print(f"Target: {label(TARGET)}")
    print_peer_table(rows)
    multiples = [row["pe"] for row in rows if row["pe"] is not None]
    full_median_price = print_full_estimate(multiples)
    print_peer_removals(rows, full_median_price)


if __name__ == "__main__":
    main()
