---
name: pulp-linear-optimization
description: >
  Use this skill whenever the user wants to solve a Linear Programming (LP) or
  Mixed-Integer Linear Programming (MILP) problem using Python and the PuLP
  library. Trigger on: "optimize", "linear programming", "LP problem",
  "maximize profit", "minimize cost", "subject to constraints", "allocation
  problem", "scheduling optimization", "resource planning", "blending problem",
  "transportation problem", "assignment problem", "PuLP", "pulp solver", or any
  problem that involves optimizing an objective function subject to linear
  constraints. Even if the user doesn't say "PuLP" explicitly, use this skill
  whenever they describe a situation that sounds like a linear or integer
  optimization problem.
---

# PuLP Linear Optimization Skill

A step-by-step guide for formulating and solving Linear Programming (LP) and
Mixed-Integer Linear Programming (MILP) problems using Python's **PuLP** library
inside VS Code with GitHub Copilot.

---

## 1. Quick Reference — Skill Map

| Task | Where to look |
|---|---|
| Installing PuLP & solvers | §2 — Setup |
| Formulating the problem | §3 — Problem Formulation |
| Building the PuLP model | §4 — Code Template |
| Common problem types | `references/problem-patterns.md` |
| Sensitivity / post-solve analysis | `references/post-solve.md` |
| Debugging infeasible models | `references/debugging.md` |
| Copilot prompt examples | `references/copilot-prompts.md` |
| Ready-to-run example scripts | `scripts/` |

---

## 2. Setup

### Install PuLP
```bash
pip install pulp
```

### Solvers bundled with PuLP (no extra install needed)
- **CBC** — default open-source solver (handles LP + MILP)
- **GLPK** — optional, install via `pip install glpk` or system package

### Optional commercial solvers (better for large problems)
```bash
# HiGHS (recommended free alternative — fast, modern)
pip install highspy

# Gurobi (requires license)
# CPLEX (requires license)
```

### Verify installation
```python
import pulp
print(pulp.listSolvers(onlyAvailable=True))
```

---

## 3. Problem Formulation Checklist

Before writing code, answer these four questions:

1. **Decision Variables** — What are you choosing? (quantities, yes/no, schedules)
2. **Objective Function** — Maximize or Minimize what? (profit, cost, time)
3. **Constraints** — What limits apply? (capacity, budget, non-negativity, logical rules)
4. **Variable Types** — Continuous (`LpContinuous`), Integer (`LpInteger`), or Binary (`LpBinary`)?

> 💡 *Tip for Copilot*: Write the math first as a comment block — Copilot will then suggest the PuLP code to match it.

---

## 4. Core Code Template

```python
import pulp

# ── 1. Create the problem ──────────────────────────────────────────────────
prob = pulp.LpProblem(name="my_problem", sense=pulp.LpMaximize)
# Use pulp.LpMinimize to minimize instead

# ── 2. Define decision variables ───────────────────────────────────────────
# Continuous variable (default): lowBound=0 enforces non-negativity
x1 = pulp.LpVariable("x1", lowBound=0, cat="Continuous")
x2 = pulp.LpVariable("x2", lowBound=0, cat="Continuous")

# Integer variable
y = pulp.LpVariable("y", lowBound=0, cat="Integer")

# Binary variable (0 or 1)
z = pulp.LpVariable("z", cat="Binary")

# Dict of variables (useful for indexed problems)
items = ["A", "B", "C"]
x = pulp.LpVariable.dicts("x", items, lowBound=0, cat="Continuous")

# ── 3. Objective function ──────────────────────────────────────────────────
prob += 5 * x1 + 4 * x2, "Objective"

# ── 4. Constraints ─────────────────────────────────────────────────────────
prob += 6 * x1 + 4 * x2 <= 24, "Resource_A"
prob += x1 + 2 * x2 <= 6,  "Resource_B"

# ── 5. Solve ───────────────────────────────────────────────────────────────
solver = pulp.PULP_CBC_CMD(msg=True)   # CBC is the default
status = prob.solve(solver)

# ── 6. Read results ────────────────────────────────────────────────────────
print(f"Status      : {pulp.LpStatus[prob.status]}")
print(f"Objective   : {pulp.value(prob.objective):.4f}")

for var in prob.variables():
    print(f"  {var.name} = {var.varValue:.4f}")
```

### Status codes
| `prob.status` | Meaning |
|---|---|
| 1 | **Optimal** — solution found |
| 0 | **Not solved** |
| -1 | **Infeasible** — no feasible solution exists |
| -2 | **Unbounded** — objective can go to ∞ |
| -3 | **Undefined** |

---

## 5. Key PuLP Patterns

### Summation over a set (most common in practice)
```python
# sum of x[i] * cost[i] for all i
prob += pulp.lpSum(x[i] * cost[i] for i in items)
```

### Indexed constraints
```python
# Each item's allocation cannot exceed its capacity
for i in items:
    prob += x[i] <= capacity[i], f"Cap_{i}"
```

### Big-M trick (linking binary and continuous variables)
```python
M = 1000  # Large constant
prob += x <= M * z, "BigM_upper"   # if z=0 then x=0
```

### Choosing a solver explicitly
```python
# CBC (default, always available)
prob.solve(pulp.PULP_CBC_CMD(msg=False))

# HiGHS (faster for large LPs)
prob.solve(pulp.HiGHS_CMD(msg=False))

# GLPK
prob.solve(pulp.GLPK_CMD(msg=False))
```

---

## 6. Workflow in VS Code with GitHub Copilot

1. **Comment-driven development** — Write a comment block describing the math;
   Copilot will generate the matching PuLP code.
2. **Prompt patterns** — See `references/copilot-prompts.md` for ready-made
   Copilot chat prompts for common problem types.
3. **Problem patterns** — See `references/problem-patterns.md` for full worked
   examples: transportation, assignment, blending, scheduling.
4. **Debugging** — If you get Infeasible or Unbounded, see `references/debugging.md`.
5. **Post-solve analysis** — Sensitivity analysis and shadow prices: see
   `references/post-solve.md`.

---

## 7. When to Use Integer / Binary Variables

| Situation | Variable type |
|---|---|
| Quantities that must be whole numbers (units, people) | `LpInteger` |
| Yes/No decisions (open a facility, assign a worker) | `LpBinary` |
| Continuous flow (liquid, money, fractions allowed) | `LpContinuous` |

> ⚠️ Adding integer variables converts an LP to a MILP. Solve time can increase
> significantly. Start with continuous relaxation to validate the model.

---

## 8. Quick Debugging Checklist

- `Infeasible` → constraints are contradictory; check bounds and RHS values
- `Unbounded` → objective can grow forever; add an upper bound constraint
- All variables = 0 → check that objective coefficients have the right sign
- Unexpected result → print all constraints: `print(prob)`
- See `references/debugging.md` for a full diagnostic workflow
