"""
example_product_mix.py
======================
Ready-to-run PuLP example: Product Mix Optimization
Maximize profit subject to resource constraints.

Run: python example_product_mix.py
"""

import pulp
import pandas as pd


def solve_product_mix():
    # ── Data ──────────────────────────────────────────────────────────────────
    products = ["Product_A", "Product_B", "Product_C"]

    profit = {
        "Product_A": 25,
        "Product_B": 30,
        "Product_C": 15,
    }

    resources = ["Machine_Hours", "Labour_Hours", "Raw_Material"]

    # Resource consumption per unit of each product
    usage = {
        ("Product_A", "Machine_Hours"): 2,
        ("Product_B", "Machine_Hours"): 4,
        ("Product_C", "Machine_Hours"): 3,
        ("Product_A", "Labour_Hours"):  3,
        ("Product_B", "Labour_Hours"):  2,
        ("Product_C", "Labour_Hours"):  5,
        ("Product_A", "Raw_Material"):  1,
        ("Product_B", "Raw_Material"):  2,
        ("Product_C", "Raw_Material"):  2,
    }

    capacity = {
        "Machine_Hours": 240,
        "Labour_Hours":  270,
        "Raw_Material":  150,
    }

    # ── Model ─────────────────────────────────────────────────────────────────
    prob = pulp.LpProblem("Product_Mix", pulp.LpMaximize)

    x = pulp.LpVariable.dicts("units", products, lowBound=0, cat="Continuous")

    # Objective
    prob += pulp.lpSum(profit[p] * x[p] for p in products), "Total_Profit"

    # Resource constraints
    for r in resources:
        prob += (
            pulp.lpSum(usage[p, r] * x[p] for p in products) <= capacity[r],
            f"Cap_{r}",
        )

    # ── Solve ─────────────────────────────────────────────────────────────────
    solver = pulp.PULP_CBC_CMD(msg=False)
    prob.solve(solver)

    # ── Results ───────────────────────────────────────────────────────────────
    print("=" * 50)
    print(f"  Status    : {pulp.LpStatus[prob.status]}")
    print(f"  Max Profit: ${pulp.value(prob.objective):,.2f}")
    print("=" * 50)

    print("\nProduction Plan:")
    plan = []
    for p in products:
        plan.append({"Product": p, "Units": x[p].varValue, "Revenue": profit[p] * x[p].varValue})
    df_plan = pd.DataFrame(plan)
    print(df_plan.to_string(index=False))

    print("\nConstraint Analysis:")
    analysis = []
    for name, c in prob.constraints.items():
        analysis.append({
            "Constraint": name,
            "Slack": round(c.slack, 4),
            "Shadow_Price": round(c.pi, 4) if c.pi is not None else "N/A",
            "Status": "BINDING" if abs(c.slack) < 1e-6 else "slack",
        })
    df_con = pd.DataFrame(analysis)
    print(df_con.to_string(index=False))

    return prob


if __name__ == "__main__":
    solve_product_mix()
