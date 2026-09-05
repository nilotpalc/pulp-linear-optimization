# Post-Solve Analysis with PuLP

## 1. Reading Variable Values

```python
# After prob.solve()
for var in prob.variables():
    print(f"{var.name}: {var.varValue}")

# Or by name
print(x["A"].varValue)
```

---

## 2. Objective Value

```python
print(f"Optimal objective: {pulp.value(prob.objective)}")
```

---

## 3. Shadow Prices (Dual Values)

Shadow prices tell you how much the objective would improve if a constraint's
RHS were relaxed by one unit. **Available for LP only (not MILP).**

```python
# After solving an LP (no integer variables)
for name, constraint in prob.constraints.items():
    print(f"{name}: shadow price = {constraint.pi:.4f}, "
          f"slack = {constraint.slack:.4f}")
```

- `constraint.pi` — shadow price (dual value)
- `constraint.slack` — amount of slack (0 = binding constraint)

---

## 4. Sensitivity / Ranging

PuLP does not natively expose ranging (how much a coefficient can change before
the basis changes). For full sensitivity analysis use one of:

**Option A — use `scipy.optimize.linprog` for the ranging, keep PuLP for modelling**

**Option B — export to LP file and parse**
```python
prob.writeLP("model.lp")   # human-readable LP file
prob.writeMPS("model.mps") # MPS format for external solvers
```

**Option C — use HiGHS solver and its Python API directly**
```python
import highspy
# HiGHS exposes full ranging through its own Python API
```

---

## 5. Checking Constraint Status

```python
for name, c in prob.constraints.items():
    status = "BINDING" if abs(c.slack) < 1e-6 else f"slack={c.slack:.2f}"
    print(f"{name}: {status}")
```

---

## 6. Exporting Results to DataFrame

```python
import pandas as pd

results = pd.DataFrame([
    {"variable": v.name, "value": v.varValue}
    for v in prob.variables()
])
print(results)
results.to_csv("results.csv", index=False)
```

---

## 7. Printing the Full Model (for debugging)

```python
print(prob)   # prints objective + all constraints in math notation
```

---

## 8. Re-solving After Changes

PuLP models are mutable — you can add/remove constraints and re-solve:

```python
# Add a new constraint
prob += x["A"] <= 50, "New_Cap_A"
prob.solve()

# Remove a named constraint
del prob.constraints["New_Cap_A"]
prob.solve()
```
