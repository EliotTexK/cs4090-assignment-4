import pytest
from hypothesis import given, strategies as st, assume
from datetime import date
from tasks import (
    filter_tasks_by_priority,
    filter_tasks_by_category,
    filter_tasks_by_completion,
    generate_unique_id,
    save_tasks,
    load_tasks,
    search_tasks
)

# Strategy for generating task dictionaries
@st.composite
def task_dict(draw):
    return {
        "id": draw(st.integers(min_value=0, max_value=1000000)),
        "title": draw(st.text(min_size=1, max_size=100)),
        "description": draw(st.text(max_size=1000)),
        "priority": draw(st.sampled_from(["Low", "Medium", "High"])),
        "category": draw(st.text(min_size=1, max_size=20)),
        "due_date": draw(st.dates(min_value=date(2000, 1, 1), max_value=date(2100, 1, 1)).map(str)),
        "completed": draw(st.booleans()),
        "created_at": draw(st.datetimes().map(lambda d: d.strftime("%Y-%m-%d %H:%M:%S"))),
        "color": draw(st.from_regex(r"^#[0-9a-fA-F]{6}$"))
    }

@given(st.lists(task_dict()))
def test_filter_by_priority_preserves_priority(tasks):
    for priority in ["Low", "Medium", "High"]:
        filtered = filter_tasks_by_priority(tasks, priority)
        assert all(task["priority"] == priority for task in filtered)

@given(st.lists(task_dict()))
def test_filter_by_category_preserves_category(tasks):
    categories = {task["category"] for task in tasks}
    for category in categories:
        filtered = filter_tasks_by_category(tasks, category)
        assert all(task["category"] == category for task in filtered)

@given(st.lists(task_dict()))
def test_filter_by_completion(tasks):
    completed_tasks = filter_tasks_by_completion(tasks, completed=True)
    assert all(task["completed"] for task in completed_tasks)
    not_completed_tasks = filter_tasks_by_completion(tasks, completed=False)
    assert all(not task["completed"] for task in not_completed_tasks)

@given(st.lists(task_dict()))
def test_generate_unique_id_is_unique(tasks):
    ids = [task["id"] for task in tasks]
    new_id = generate_unique_id(tasks)
    assert new_id not in ids

@given(st.lists(task_dict()), st.text(min_size=1, max_size=10))
def test_search_tasks_returns_relevant_matches(tasks, query):
    results = search_tasks(tasks, query)
    for task in results:
        in_title = query.lower() in task["title"].lower()
        in_description = query.lower() in task["description"].lower()
        assert in_title or in_description