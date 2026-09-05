"""
example_transportation.py
=========================
Ready-to-run PuLP example: Transportation Problem
Minimize total shipping cost from suppliers to customers.

Run: python example_transportation.py
"""

import pulp
import pandas as pd


def solve_transportation():
    # ── Data ──────────────────────────────────────────────────────────────────
    suppliers = ["Mumbai", "Delhi", "Chennai"]
    customers = ["Bangalore", "Hyderabad", "Pune", "Kolkata"]

    supply = {"Mumbai": 300, "Delhi": 500, "Chennai": 400}
    demand = {"Bangalore": 250, "Hyderabad": 350, "Pune": 200, "Kolkata": 300}

    # Cost per unit shipped (₹)
    cost = {
        ("Mumbai",  "Bangalore"): 4,  ("Mumbai",  "Hyderabad"): 3,
        ("Mumbai",  "Pune"):      2,  ("Mumbai",  "Kolkata"):   6,
        ("Delhi",   "Bangalore"): 5,  ("Delhi",   "Hyderabad"): 4,
        ("Delhi",   "Pune"):      3,  ("Delhi",   "Kolkata"):   2,
        ("Chennai", "Bangalore"): 1,  ("Chennai", "Hyderabad"): 2,
        ("Chennai", "Pune"):      5,  ("Chennai", "Kolkata"):   7,
    }

    # ── Model ─────────────────────────────────────────────────────────────────
    prob = pulp.LpProblem("Transportation", pulp.LpMinimize)

    routes = [(s, c) for s in suppliers for c in customers]
    x = pulp.LpVariable.dicts("ship", routes, lowBound=0)

    # Objective: minimize total shipping cost
    prob += pulp.lpSum(cost[s, c] * x[s, c] for s, c in routes), "Total_Cost"

    # Supply constraints
    for s in suppliers:
        prob += (
            pulp.lpSum(x[s, c] for c in customers) <= supply[s],
            f"Supply_{s}",
        )

    # Demand constraints
    for c in customers:
        prob += (
            pulp.lpSum(x[s, c] for s in suppliers) >= demand[c],
            f"Demand_{c}",
        )

    # ── Solve ─────────────────────────────────────────────────────────────────
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    # ── Results ───────────────────────────────────────────────────────────────
    print("=" * 55)
    print(f"  Status        : {pulp.LpStatus[prob.status]}")
    print(f"  Min Total Cost: ₹{pulp.value(prob.objective):,.0f}")
    print("=" * 55)

    print("\nShipment Plan (units > 0):")
    rows = []
    for s, c in routes:
        qty = x[s, c].varValue
        if qty > 0:
            rows.append({
                "From": s, "To": c,
                "Units": int(qty),
                "Unit_Cost": cost[s, c],
                "Total_Cost": int(qty) * cost[s, c],
            })
    df = pd.DataFrame(rows)
    print(df.to_string(index=False))
    print(f"\nGrand Total: ₹{df['Total_Cost'].sum():,}")

    return prob


if __name__ == "__main__":
    solve_transportation()
