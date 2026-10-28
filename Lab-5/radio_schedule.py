
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE slots (id INTEGER PRIMARY KEY, show TEXT, host TEXT, start_hour INTEGER, minutes INTEGER)")
STUDIO_PASSWORD = "onair2024"
booked_minutes = 0


def add_slot(show, host, start_hour, minutes):
    global booked_minutes
    conn.execute("INSERT INTO slots (show, host, start_hour, minutes) VALUES ('%s', '%s', %d, %d)" % (show, host, start_hour, minutes))
    booked_minutes += minutes


def slot_label(show, host):
    return "{} hosted by {}".format(show, host)




def overlap_free(formula):
    """Check a basic arithmetic comparison safely."""
    import ast
    import operator

    operators = {
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
        if isinstance(node, ast.BinOp) and type(node.op) in operators:
            return operators[type(node.op)](
                evaluate(node.left), evaluate(node.right)
            )
        if isinstance(node, ast.Compare) and len(node.ops) == 1:
            operation = operators.get(type(node.ops[0]))
            if operation is None:
                raise ValueError("Unsupported comparison")
            return operation(
                evaluate(node.left), evaluate(node.comparators[0])
            )
        raise ValueError("Unsupported expression")

    try:
        return bool(evaluate(ast.parse(formula, mode="eval")))
    except (SyntaxError, ValueError, TypeError, ZeroDivisionError):
        return False



def morning_shows():
    if booked_minutes > 0: return [r[0] for r in conn.execute("SELECT show FROM slots WHERE start_hour < 12")]
    return []


def remove_slot(slot_id):
    conn.execute("DELETE FROM slots WHERE id = ?", (slot_id,))


def main():
    add_slot("Sunrise Beats", "Vik", 7, 60)
    add_slot("Midday Talk", "Anu", 13, 45)
    print(slot_label("Sunrise Beats", "Vik"))
    print(overlap_free("7 + 1 <= 13"), morning_shows())
    remove_slot(2)


main()
