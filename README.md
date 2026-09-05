# PuLP Linear Optimization

A practical GitHub Copilot skill and reference repository for modeling and
solving linear programming (LP) and mixed-integer linear programming (MILP)
problems in Python with [PuLP](https://coin-or.github.io/pulp/).

It includes a concise modeling guide, prompt patterns for Copilot, debugging
notes, post-solve analysis guidance, and runnable examples.

## Requirements

- Python 3.9 or later
- `pulp`
- `pandas` for the included example reports

Install the Python dependencies:

```powershell
python -m pip install pulp pandas
```

PuLP includes the CBC solver used by the examples. To check available solvers:

```powershell
python -c "import pulp; print(pulp.listSolvers(onlyAvailable=True))"
```

## Run the Examples

From the repository root, run either example:

```powershell
python scripts/example_product_mix.py
python scripts/example_transportation.py
```

`example_product_mix.py` maximizes profit while respecting machine, labor, and
material capacity constraints. Its output includes the production plan, slack,
and shadow prices.

`example_transportation.py` minimizes shipping cost subject to supply and
demand constraints. Its output lists non-zero shipping routes and the total
cost.

## Model a Problem

Start each optimization problem by identifying:

1. **Decision variables**: the quantities or yes/no choices to make.
2. **Objective**: the profit, cost, time, or other value to maximize or
   minimize.
3. **Constraints**: capacity, demand, budget, assignment, and business-rule
   limits.
4. **Variable types**: continuous, integer, or binary.

A minimal PuLP model looks like this:

```python
import pulp

model = pulp.LpProblem("my_problem", pulp.LpMaximize)
x = pulp.LpVariable("x", lowBound=0)
y = pulp.LpVariable("y", lowBound=0)

model += 5 * x + 4 * y, "Profit"
model += 6 * x + 4 * y <= 24, "Resource_A"
model += x + 2 * y <= 6, "Resource_B"

model.solve(pulp.PULP_CBC_CMD(msg=False))
print(pulp.LpStatus[model.status])
print(pulp.value(model.objective))
```

Use `pulp.LpMinimize` for cost-minimization models. For indexed decisions,
prefer `pulp.LpVariable.dicts()` and `pulp.lpSum()`.

## Use with GitHub Copilot

Describe the math in a comment before generating code. Include the decision
variables, objective, constraints, and whether any decisions must be integers
or binary. The prompt examples in [references/copilot-prompts.md](references/copilot-prompts.md)
provide starting points for common optimization tasks.

For a new model, validate the formulation in this order:

1. Solve its continuous version first when practical.
2. Confirm the solver status is `Optimal` before interpreting values.
3. Review every decision variable and constraint slack.
4. Add integer or binary restrictions only where the real-world decision
   requires them.

## Repository Contents

| Path | Purpose |
| --- | --- |
| [SKILL.md](SKILL.md) | Core PuLP modeling guide and solver reference. |
| [scripts/example_product_mix.py](scripts/example_product_mix.py) | Profit-maximizing product mix example. |
| [scripts/example_transportation.py](scripts/example_transportation.py) | Cost-minimizing transportation example. |
| [references/problem-patterns.md](references/problem-patterns.md) | Patterns for transportation, assignment, blending, and scheduling. |
| [references/debugging.md](references/debugging.md) | Workflow for infeasible, unbounded, and unexpected models. |
| [references/post-solve.md](references/post-solve.md) | Slack, shadow-price, and post-solve analysis guidance. |
| [references/copilot-prompts.md](references/copilot-prompts.md) | Ready-to-adapt Copilot prompts. |

## Common Solver Outcomes

| Status | Meaning | Next step |
| --- | --- | --- |
| `Optimal` | A best feasible solution was found. | Review values and constraint activity. |
| `Infeasible` | The constraints cannot all be satisfied. | Check bounds, demand, capacities, and contradictory rules. |
| `Unbounded` | The objective can improve without limit. | Add missing limits or bounds. |
| `Not Solved` | No solution was obtained. | Check solver availability and model diagnostics. |

See [references/debugging.md](references/debugging.md) for a structured
diagnostic process.