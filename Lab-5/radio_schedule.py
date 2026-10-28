
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
    try:
        return eval(formula)
    except Exception:
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
