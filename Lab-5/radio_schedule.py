
"""Manage a simple radio show schedule."""

import ast
import operator
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute(
    "CREATE TABLE slots ("
    "id INTEGER PRIMARY KEY, show TEXT, host TEXT, "
    "start_hour INTEGER, minutes INTEGER)"
)


def add_slot(show, host, start_hour, minutes):
    """Add a radio show to the schedule."""
    conn.execute(
        "INSERT INTO slots (show, host, start_hour, minutes) "
        "VALUES (?, ?, ?, ?)",
        (show, host, start_hour, minutes),
    )


def slot_label(show, host):
    """Return a label describing the show and its host."""
    return f"{show} hosted by {host}"


def overlap_free(formula):
    """Safely evaluate a basic arithmetic comparison."""
    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Lt: operator.lt,
        ast.LtE: operator.le,
        ast.Gt: operator.gt,
        ast.GtE: operator.ge,
        ast.Eq: operator.eq,
        ast.NotEq: operator.ne,
    }

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in allowed_operators:
            return allowed_operators[type(node.op)](
                evaluate(node.left), evaluate(node.right)
            )
        if isinstance(node, ast.Compare) and len(node.ops) == 1:
            operation = allowed_operators.get(type(node.ops[0]))
            if operation is None:
                raise ValueError("Unsupported comparison")
            return operation(
                evaluate(node.left), evaluate(node.comparators[0])
            )
        raise ValueError("Unsupported expression")

    try:
        expression = ast.parse(formula, mode="eval")
        return bool(evaluate(expression))
    except (SyntaxError, ValueError, TypeError, ZeroDivisionError):
        return False


def morning_shows():
    """Return shows scheduled before noon."""
    total = conn.execute(
        "SELECT SUM(minutes) FROM slots"
    ).fetchone()[0]

    if total and total > 0:
        return [
            row[0]
            for row in conn.execute(
                "SELECT show FROM slots WHERE start_hour < 12"
            )
        ]
    return []


def remove_slot(slot_id):
    """Remove a scheduled show by its ID."""
    conn.execute("DELETE FROM slots WHERE id = ?", (slot_id,))


def main():
    """Run a short demonstration of the radio schedule."""
    add_slot("Sunrise Beats", "Vik", 7, 60)
    add_slot("Midday Talk", "Anu", 13, 45)
    print(slot_label("Sunrise Beats", "Vik"))
    print(overlap_free("7 + 1 <= 13"), morning_shows())
    remove_slot(2)


if __name__ == "__main__":
    main()
