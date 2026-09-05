# GitHub Copilot Prompt Examples for PuLP

Use these prompts in Copilot Chat (Ctrl+I or the Chat panel) to get high-quality
PuLP code generated for you.

---

## General Scaffolding Prompt

```
Using Python PuLP, create a linear programming model to [describe your problem].
Decision variables: [list them]
Objective: [maximize/minimize] [what]
Constraints:
  - [constraint 1]
  - [constraint 2]
Include CBC solver, print status, objective value, and all variable values.
```

---

## Prompt: Product Mix

```
Using PuLP, solve a product mix LP:
- Products: A, B, C
- Profit per unit: A=25, B=30, C=15
- Resource constraints (Machine ≤ 240h, Labour ≤ 270h, Material ≤ 150kg)
- Resource usage per unit: provided in a dict called `usage`
Maximize profit. Print which constraints are binding.
```

---

## Prompt: Transportation

```
Write a PuLP transportation problem:
- 2 suppliers with supply limits, 3 customers with demand requirements
- Shipping cost matrix as a dict
- Minimize total shipping cost
- After solving, display shipment flows > 0 in a readable table format
```

---

## Prompt: Binary / Knapsack

```
PuLP knapsack problem:
- Items with name, value, weight stored in a list of dicts
- Knapsack capacity = 10 kg
- Binary decision: take item or leave it
- Maximize total value
Print selected items and total weight used.
```

---

## Prompt: Sensitivity Analysis

```
After solving this PuLP LP model, print a sensitivity report showing:
- Each constraint name
- Whether it is binding (slack ≈ 0)
- The shadow price (dual value) using constraint.pi
Format as a pandas DataFrame and save to sensitivity.csv
```

---

## Prompt: Refactor Existing Model

```
Refactor this PuLP model to:
1. Use LpVariable.dicts instead of individual variables
2. Use lpSum with generator expressions
3. Add named constraints with descriptive strings
4. Print a summary table using pandas after solving
[paste your existing code]
```

---

## Prompt: Debugging

```
This PuLP model returns status 'Infeasible'. Help me debug it:
1. Print the full model using print(prob)
2. Check each constraint's slack value
3. Identify which constraints are most likely conflicting
4. Suggest how to add elastic constraints (with penalty slacks) to find the issue
[paste your model code]
```

---

## Copilot Inline Comment Patterns

Use these as inline comments — Copilot will autocomplete the PuLP code:

```python
# Create a minimization LP problem called "Cost_Model"

# Define binary variable 'open_warehouse' for each warehouse in warehouse_list

# Objective: minimize sum of (fixed_cost * open + unit_cost * ship) over all routes

# Constraint: total demand at each customer must be met

# Constraint: each warehouse can only ship if it is open (Big-M)

# Solve with CBC, suppress output, print status and optimal cost
```
