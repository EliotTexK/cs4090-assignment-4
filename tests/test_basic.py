import pytest
import os
import json
from datetime import datetime, timedelta
from tasks import (
    load_tasks, save_tasks, generate_unique_id,
    filter_tasks_by_priority, filter_tasks_by_category,
    filter_tasks_by_completion, search_tasks, get_overdue_tasks
)

TEST_FILE = "test_tasks.json"
INVALID_FILE = "tests/evil_json.json"
MISSING_FILE = "93-49n924lo9ochbPOooooHDGSlskjdhn"

@pytest.fixture
def sample_tasks():
    return [
        {
            "id": 1,
            "title": "Test Task 1",
            "description": "Description 1",
            "priority": "High",
            "category": "Work",
            "due_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "id": 2,
            "title": "Test Task 2",
            "description": "Description 2",
            "priority": "Low",
            "category": "Personal",
            "due_date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "id": 3,
            "title": "Completed Task",
            "description": "Description 3",
            "priority": "Medium",
            "category": "School",
            "due_date": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
            "completed": True,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    ]

def test_save_and_load_tasks(sample_tasks):
    save_tasks(sample_tasks, TEST_FILE)
    loaded = load_tasks(TEST_FILE)
    assert loaded == sample_tasks
    os.remove(TEST_FILE)

# Invalid JSON is gracefully handled
def test_bad_json():
    load_tasks(INVALID_FILE)

# Missing JSON file is gracefully handled
def test_missing_json():
    load_tasks(MISSING_FILE)

def test_generate_unique_id(sample_tasks):
    # Make sure the latest generated ID is incremental
    new_id = generate_unique_id(sample_tasks)
    assert new_id == 4

# Case in which no uid is provided
def test_degenerate_unique_id(sample_tasks):
    new_id = generate_unique_id(None)

def test_filter_tasks_by_priority(sample_tasks):
    # In the sample, only one high priority task was provided
    high_priority = filter_tasks_by_priority(sample_tasks, "High")
    # So, expect only one item in the result
    assert len(high_priority) == 1
    assert high_priority[0]["priority"] == "High"

def test_filter_tasks_by_category(sample_tasks):
    work_tasks = filter_tasks_by_category(sample_tasks, "Work")
    assert len(work_tasks) == 1
    assert work_tasks[0]["category"] == "Work"

def test_filter_tasks_by_completion(sample_tasks):
    completed = filter_tasks_by_completion(sample_tasks, True)
    not_completed = filter_tasks_by_completion(sample_tasks, False)
    assert len(completed) == 1
    assert len(not_completed) == 2

def test_search_tasks(sample_tasks):
    results = search_tasks(sample_tasks, "completed")
    assert len(results) == 1
    assert results[0]["title"] == "Completed Task"

def test_get_overdue_tasks(sample_tasks):
    overdue = get_overdue_tasks(sample_tasks)
    assert any(task["title"] == "Test Task 2" for task in overdue)
    assert all(task["due_date"] < datetime.now().strftime("%Y-%m-%d") for task in overdue)
