# Lab 5: Static Code Analysis — Issues and Fixes

**File analysed:** `radio_schedule.py`  
**Tools used:** Pylint, Bandit, and Flake8

The following issues were identified in the original program. The line numbers refer to the original version of `radio_schedule.py`.

| Issue | Type / Severity | Original line(s) | Description | Fix Approach |
|---|---|---|---|---|
| SQL injection risk (Bandit B608) | Security — Medium | 12 | SQL queries were constructed using string formatting. Unexpected input could change the query and potentially cause SQL injection. | Replaced string formatting with parameterized SQL queries using placeholders and a tuple of values. |
| Unsafe use of `eval()` (Bandit B307, Pylint W0123) | Security — Medium | 22 | `eval()` executes Python expressions and can execute unsafe code if the input is malicious. | Replaced `eval()` with an AST-based expression evaluator that allows only selected arithmetic operations and comparisons. |
| Broad exception handling (Pylint W0718) | Code quality | 23 | Catching every `Exception` can hide unexpected errors and make debugging difficult. | Replaced the broad exception handler with specific exceptions relevant to parsing and evaluating the permitted expressions. |
| Hardcoded password (Bandit B105) | Security — Low | 6 | A studio password was stored directly in the source code, where anyone with access to the file could read it. | Removed the unused hardcoded password from the program. |
| Global variable usage (Pylint W0603) | Code quality | 7, 11 | The `booked_minutes` variable was modified through a global statement, creating unnecessary shared state. | Removed the global counter and its global statement. |
| Incorrect function naming (Pylint C0103) | Code quality | 10, 16, 20, 27, 32 | Function names such as `addSlot` and `slotLabel` did not follow Python's snake_case naming convention. | Renamed functions to `add_slot`, `slot_label`, `overlap_free`, `morning_shows`, and `remove_slot`. |
| Missing documentation strings (Pylint C0114, C0116) | Code quality | 1, 10, 16, 20, 27, 32, 36 | The module and functions did not have documentation strings explaining their purpose. | Added a module docstring and appropriate function docstrings. |
| Lines exceeding the recommended length (Pylint C0301, Flake8 E501) | Formatting | 5, 12, 28 | Several lines exceeded the tools' configured line-length limits, making the code harder to read. | Split long statements across multiple lines. |
| Multiple statements on one line (Pylint C0321, Flake8 E701) | Formatting | 28 | More than one statement appeared on the same line, reducing readability. | Separated statements onto individual lines and formatted the code consistently. |
| Regular string formatting (Pylint C0209) | Code quality | 12, 17 | Regular string formatting was used where an f-string was suggested. | Used an f-string where appropriate and parameterized SQL for database operations. |

## Verification

After fixing the issues, the program was executed successfully and all three tools were rerun.

- **Pylint:** 10.00/10.
- **Bandit:** No issues identified.
- **Flake8:** No formatting violations reported.

The before-and-after reports are saved separately in the `Lab-5` folder.
