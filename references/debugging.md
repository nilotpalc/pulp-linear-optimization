# Debugging LP/MILP Models in PuLP

## Diagnostic Workflow

```
Solve → check status → diagnose → fix → re-solve
```

---

## Status Codes Cheatsheet

```python
import pulp
status = prob.solve()
print(pulp.LpStatus[prob.status])
# 'Optimal', 'Infeasible', 'Unbounded', 'Not Solved', 'Undefined'
```

---

## Infeasible (-1)

The constraints cannot all be satisfied simultaneously.

### Step 1 — Print the model
```python
print(prob)
```
Look for constraints that obviously conflict (e.g., `x >= 10` and `x <= 5`).

### Step 2 — Check variable bounds
```python
for v in prob.variables():
    print(f"{v.name}: lb={v.lowBound}, ub={v.upBound}")
```
Ensure `lowBound <= upBound`.

### Step 3 — Relax constraints one at a time
Comment out constraints and re-solve to find the conflicting one.

### Step 4 — Feasibility relaxation (manual)
Add slack variables with a large penalty to every constraint to find which are
violated:
```python
# Instead of: prob += expr <= rhs, "C1"
slack = pulp.LpVariable("slack_C1", lowBound=0)
prob += expr - slack <= rhs, "C1"
prob += -10000 * slack  # penalise slack in objective
```

### Common causes
- RHS values are inconsistent with supply/demand totals
- Non-negativity + equality constraints force contradiction
- Big-M value too small (MILP)

---

## Unbounded (-2)

The objective can grow to infinity — a constraint is missing.

### Fixes
- Add an upper bound on decision variables: `x = LpVariable("x", lowBound=0, upBound=1000)`
- Check that objective coefficients have the correct sign (+/-)
- Ensure all variables appear in at least one constraint

---

## Optimal but Suspicious Results

### All variables are zero
- Check objective coefficient signs: maximising with negative coefficients → zero is optimal
- Check that decision variables are correctly referenced in the objective

### Result doesn't match expectation
```python
# Print full model — compare math to your intent
print(prob)
# Check each constraint value at solution
for name, c in prob.constraints.items():
    print(f"{name}: LHS={pulp.value(c)} slack={c.slack:.4f}")
```

### MILP gives worse result than expected
- Continuous relaxation gives an upper bound — solve without integer constraints first
```python
# Temporarily relax integer constraints
for v in prob.variables():
    v.cat = "Continuous"
prob.solve()
print("LP relaxation:", pulp.value(prob.objective))
# Then restore integer constraints and re-solve
```

---

## Solver-Specific Debugging

### CBC verbose output
```python
prob.solve(pulp.PULP_CBC_CMD(msg=True))
```

### Write LP file and inspect
```python
prob.writeLP("debug_model.lp")
# Open debug_model.lp in VS Code — readable text format
```

### Time limit (prevent hanging on hard MILPs)
```python
prob.solve(pulp.PULP_CBC_CMD(msg=True, timeLimit=60))  # 60 seconds max
```

### MIP gap tolerance (accept near-optimal for large MILPs)
```python
prob.solve(pulp.PULP_CBC_CMD(msg=True, gapRel=0.01))  # accept 1% gap
```
