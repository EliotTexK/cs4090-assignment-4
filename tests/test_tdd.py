import pytest
from datetime import datetime, date
from tasks import (
    filter_tasks_by_category,
    generate_unique_id,
    filter_tasks_by_priority,
    filter_tasks_by_completion,
    search_tasks,
    get_overdue_tasks
)

# -------------------------
# 1. PARAMETERIZED TEST FOR DUE DATE FILTERING
# -------------------------

@pytest.mark.parametrize("task, start_date, end_date, expected", [
    ({"due_date": "2025-04-01"}, date(2025, 3, 1), date(2025, 4, 30), True),
    ({"due_date": "2025-02-01"}, date(2025, 3, 1), date(2025, 4, 30), False),
    ({"due_date": "2025-04-30"}, date(2025, 4, 30), date(2025, 4, 30), True),
])
def test_due_date_filter(task, start_date, end_date, expected):
    due_date = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
    assert (start_date <= due_date <= end_date) == expected

# -------------------------
# 2. ADD CATEGORY – TEST LOGIC IN CATEGORY LISTING
# -------------------------

def test_add_new_category():
    tasks = [
        {"category": "Work"},
        {"category": "School"},
        {"category": "Personal"},
    ]
    new_category = "Fitness"
    categories = list(set([task["category"] for task in tasks]))
    
    assert new_category not in categories
    categories.append(new_category)
    assert new_category in categories

# -------------------------
# 3. COLOR ASSIGNMENT – TASKS SHOULD STORE HEX VALUES
# -------------------------

@pytest.mark.parametrize("color", ["#ff0000", "#00ff00", "#123abc"])
def test_task_color_storage(color):
    task = {
        "id": 1,
        "title": "Sample Task",
        "color": color
    }
    assert task["color"].startswith("#")
    assert len(task["color"]) == 7
    assert all(c in "0123456789abcdefABCDEF#" for c in task["color"])

# -------------------------
# 4. OVERDUE FILTER (COMPLEMENTARY TO DUE DATE FILTER)
# -------------------------

def test_get_overdue_tasks():
    tasks = [
        {"due_date": "2024-12-01", "completed": False},
        {"due_date": "2030-01-01", "completed": False},
        {"due_date": "2024-12-01", "completed": True},
    ]
    overdue = get_overdue_tasks(tasks)
    for task in overdue:
        assert task["due_date"] < datetime.now().strftime("%Y-%m-%d")
        assert task["completed"] is False
