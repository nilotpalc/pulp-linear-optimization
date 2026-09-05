# Common LP/MILP Problem Patterns

A catalogue of ready-to-adapt PuLP templates for the most frequent problem types.

---

## Table of Contents
1. [Product Mix / Resource Allocation](#1-product-mix--resource-allocation)
2. [Transportation Problem](#2-transportation-problem)
3. [Assignment Problem](#3-assignment-problem)
4. [Blending / Diet Problem](#4-blending--diet-problem)
5. [Knapsack Problem (Binary)](#5-knapsack-problem-binary)
6. [Shift Scheduling](#6-shift-scheduling)
7. [Facility Location](#7-facility-location)

---

## 1. Product Mix / Resource Allocation

**Scenario**: Decide how many units of each product to produce to maximize profit,
given limited resources (machine hours, raw materials, labour).

```python
import pulp

products   = ["A", "B", "C"]
profit     = {"A": 25, "B": 30, "C": 15}       # profit per unit
resources  = ["Machine", "Labour", "Material"]
usage      = {                                   # resource per unit
    ("A", "Machine"): 2, ("B", "Machine"): 4, ("C", "Machine"): 3,
    ("A", "Labour"):  3, ("B", "Labour"):  2, ("C", "Labour"):  5,
    ("A", "Material"):1, ("B", "Material"):2, ("C", "Material"):2,
}
capacity   = {"Machine": 240, "Labour": 270, "Material": 150}

prob = pulp.LpProblem("Product_Mix", pulp.LpMaximize)
x = pulp.LpVariable.dicts("units", products, lowBound=0)

prob += pulp.lpSum(profit[p] * x[p] for p in products)

for r in resources:
    prob += (pulp.lpSum(usage[p, r] * x[p] for p in products) <= capacity[r],
             f"Cap_{r}")

prob.solve(pulp.PULP_CBC_CMD(msg=False))
print(f"Max profit: {pulp.value(prob.objective):.2f}")
for p in products:
    print(f"  Produce {x[p].varValue:.1f} units of {p}")
```

---

## 2. Transportation Problem

**Scenario**: Ship goods from multiple suppliers to multiple customers at minimum
total cost.

```python
import pulp

suppliers = ["S1", "S2"]
customers = ["C1", "C2", "C3"]
supply    = {"S1": 300, "S2": 500}
demand    = {"C1": 200, "C2": 300, "C3": 250}
cost      = {("S1","C1"): 2, ("S1","C2"): 3, ("S1","C3"): 1,
             ("S2","C1"): 5, ("S2","C2"): 4, ("S2","C3"): 8}

prob = pulp.LpProblem("Transport", pulp.LpMinimize)
x = pulp.LpVariable.dicts("ship", [(s,c) for s in suppliers for c in customers],
                           lowBound=0)

prob += pulp.lpSum(cost[s,c] * x[s,c] for s in suppliers for c in customers)

for s in suppliers:
    prob += pulp.lpSum(x[s,c] for c in customers) <= supply[s], f"Supply_{s}"
for c in customers:
    prob += pulp.lpSum(x[s,c] for s in suppliers) >= demand[c], f"Demand_{c}"

prob.solve(pulp.PULP_CBC_CMD(msg=False))
print(f"Min cost: {pulp.value(prob.objective):.2f}")
for s in suppliers:
    for c in customers:
        if x[s,c].varValue > 0:
            print(f"  {s} -> {c}: {x[s,c].varValue:.0f}")
```

---

## 3. Assignment Problem

**Scenario**: Assign workers to tasks (one-to-one) to minimize total cost/time.

```python
import pulp

workers = ["Alice", "Bob", "Carol"]
tasks   = ["T1", "T2", "T3"]
cost    = {("Alice","T1"):9, ("Alice","T2"):2, ("Alice","T3"):7,
           ("Bob",  "T1"):3, ("Bob",  "T2"):6, ("Bob",  "T3"):3,
           ("Carol","T1"):5, ("Carol","T2"):8, ("Carol","T3"):1}

prob = pulp.LpProblem("Assignment", pulp.LpMinimize)
x = pulp.LpVariable.dicts("assign", cost.keys(), cat="Binary")

prob += pulp.lpSum(cost[k] * x[k] for k in cost)

for w in workers:
    prob += pulp.lpSum(x[w,t] for t in tasks) == 1, f"Worker_{w}"
for t in tasks:
    prob += pulp.lpSum(x[w,t] for w in workers) == 1, f"Task_{t}"

prob.solve(pulp.PULP_CBC_CMD(msg=False))
for w in workers:
    for t in tasks:
        if x[w,t].varValue == 1:
            print(f"  {w} -> {t}  (cost: {cost[w,t]})")
```

---

## 4. Blending / Diet Problem

**Scenario**: Mix ingredients to meet nutritional requirements at minimum cost.

```python
import pulp

ingredients = ["Wheat", "Rice", "Corn"]
nutrients   = ["Protein", "Fat", "Carbs"]
cost_per_kg = {"Wheat": 0.6, "Rice": 0.35, "Corn": 0.2}
content     = {                          # nutrient per kg of ingredient
    ("Wheat","Protein"): 0.12, ("Rice","Protein"): 0.08, ("Corn","Protein"): 0.09,
    ("Wheat","Fat"):     0.02, ("Rice","Fat"):     0.01, ("Corn","Fat"):     0.04,
    ("Wheat","Carbs"):   0.70, ("Rice","Carbs"):   0.80, ("Corn","Carbs"):   0.72,
}
min_req = {"Protein": 0.10, "Fat": 0.015, "Carbs": 0.60}  # min fraction in blend

prob = pulp.LpProblem("Blend", pulp.LpMinimize)
x = pulp.LpVariable.dicts("kg", ingredients, lowBound=0)

prob += pulp.lpSum(cost_per_kg[i] * x[i] for i in ingredients)
prob += pulp.lpSum(x[i] for i in ingredients) == 1, "Total_1kg"

for n in nutrients:
    prob += (pulp.lpSum(content[i,n] * x[i] for i in ingredients) >= min_req[n],
             f"Min_{n}")

prob.solve(pulp.PULP_CBC_CMD(msg=False))
print(f"Min cost per kg: {pulp.value(prob.objective):.4f}")
for i in ingredients:
    print(f"  {i}: {x[i].varValue*100:.1f}%")
```

---

## 5. Knapsack Problem (Binary)

**Scenario**: Select a subset of items to maximize value without exceeding capacity.

```python
import pulp

items    = ["Laptop", "Camera", "Watch", "Book", "Headphones"]
value    = {"Laptop": 800, "Camera": 400, "Watch": 300, "Book": 50, "Headphones": 150}
weight   = {"Laptop": 3.0, "Camera": 1.5, "Watch": 0.2, "Book": 0.5, "Headphones": 0.4}
capacity = 5.0  # kg

prob = pulp.LpProblem("Knapsack", pulp.LpMaximize)
x = pulp.LpVariable.dicts("take", items, cat="Binary")

prob += pulp.lpSum(value[i]  * x[i] for i in items)
prob += pulp.lpSum(weight[i] * x[i] for i in items) <= capacity, "Weight"

prob.solve(pulp.PULP_CBC_CMD(msg=False))
print(f"Max value: {pulp.value(prob.objective):.0f}")
selected = [i for i in items if x[i].varValue == 1]
print(f"Pack: {selected}")
```

---

## 6. Shift Scheduling

**Scenario**: Assign staff to shifts to meet demand at minimum labour cost, each
worker works at most one shift per day.

```python
import pulp

shifts   = ["Morning", "Afternoon", "Night"]
workers  = [f"W{i}" for i in range(1, 6)]
demand   = {"Morning": 2, "Afternoon": 3, "Night": 2}   # min workers needed
wage     = {"Morning": 15, "Afternoon": 18, "Night": 22} # hourly rate

prob = pulp.LpProblem("Scheduling", pulp.LpMinimize)
x = pulp.LpVariable.dicts("assign",
                           [(w, s) for w in workers for s in shifts],
                           cat="Binary")

prob += pulp.lpSum(wage[s] * x[w,s] for w in workers for s in shifts)

# Meet demand per shift
for s in shifts:
    prob += pulp.lpSum(x[w,s] for w in workers) >= demand[s], f"Demand_{s}"

# Each worker works at most one shift
for w in workers:
    prob += pulp.lpSum(x[w,s] for s in shifts) <= 1, f"OneShift_{w}"

prob.solve(pulp.PULP_CBC_CMD(msg=False))
print(f"Min labour cost: {pulp.value(prob.objective):.2f}")
for s in shifts:
    assigned = [w for w in workers if x[w,s].varValue == 1]
    print(f"  {s}: {assigned}")
```

---

## 7. Facility Location

**Scenario**: Decide which facilities to open (binary) and how much to ship from
each to each customer to minimise total cost.

```python
import pulp

facilities = ["F1", "F2", "F3"]
customers  = ["C1", "C2", "C3", "C4"]
open_cost  = {"F1": 1000, "F2": 1500, "F3": 800}
ship_cost  = {("F1","C1"):2,("F1","C2"):3,("F1","C3"):4,("F1","C4"):5,
              ("F2","C1"):4,("F2","C2"):1,("F2","C3"):2,("F2","C4"):3,
              ("F3","C1"):5,("F3","C2"):4,("F3","C3"):1,("F3","C4"):2}
demand     = {"C1":100,"C2":200,"C3":150,"C4":120}
capacity   = {"F1":300,"F2":350,"F3":400}
M = max(capacity.values())

prob = pulp.LpProblem("FacilityLocation", pulp.LpMinimize)
y = pulp.LpVariable.dicts("open", facilities, cat="Binary")
x = pulp.LpVariable.dicts("ship",
                           [(f,c) for f in facilities for c in customers],
                           lowBound=0)

prob += (pulp.lpSum(open_cost[f]*y[f] for f in facilities) +
         pulp.lpSum(ship_cost[f,c]*x[f,c] for f in facilities for c in customers))

for c in customers:
    prob += pulp.lpSum(x[f,c] for f in facilities) >= demand[c], f"Dem_{c}"
for f in facilities:
    prob += pulp.lpSum(x[f,c] for c in customers) <= capacity[f]*y[f], f"Cap_{f}"

prob.solve(pulp.PULP_CBC_CMD(msg=False))
opened = [f for f in facilities if y[f].varValue == 1]
print(f"Open facilities: {opened}")
print(f"Total cost: {pulp.value(prob.objective):.2f}")
```
