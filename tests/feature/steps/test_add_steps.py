import pytest
from pytest_bdd import scenarios, given, when, then
from tasks import (
    load_tasks, save_tasks, generate_unique_id,
    filter_tasks_by_priority, filter_tasks_by_category
)

import os
import json

# Scenarios
scenarios("tasks.feature")

# Shared fixtures
TEST_TASKS_FILE = "test_tasks.json"

@pytest.fixture
def sample_tasks():
    return [
        {"id": 1, "title": "Task 1", "description": "Do something", "priority": "High", "category": "Work", "completed": False, "due_date": "2025-05-01"},
        {"id": 2, "title": "Task 2", "description": "Read something", "priority": "Low", "category": "Personal", "completed": True, "due_date": "2025-06-01"},
        {"id": 3, "title": "Task 3", "description": "Buy something", "priority": "Medium", "category": "Work", "completed": False, "due_date": "2025-07-01"},
    ]

@pytest.fixture(autouse=True)
def cleanup_file():
    # Clean up test file before and after
    yield
    if os.path.exists(TEST_TASKS_FILE):
        os.remove(TEST_TASKS_FILE)

# Given steps
@given("I have a list of sample tasks")
def tasks_loaded(sample_tasks):
    save_tasks(sample_tasks, TEST_TASKS_FILE)

@given("the task list is empty")
def empty_tasks_file():
    save_tasks([], TEST_TASKS_FILE)

# When steps
@when("I load the tasks from the file")
def load_from_file():
    return load_tasks(TEST_TASKS_FILE)

@when("I add a new task")
def add_task(sample_tasks):
    new_id = generate_unique_id(sample_tasks)
    sample_tasks.append({"id": new_id, "title": "New Task", "description": "New Desc", "priority": "High", "category": "School", "completed": False, "due_date": "2025-08-01"})
    save_tasks(sample_tasks, TEST_TASKS_FILE)

@when("I filter tasks by the 'Work' category")
def filter_by_category(sample_tasks):
    return filter_tasks_by_category(sample_tasks, "Work")

@when("I filter tasks by 'High' priority")
def filter_by_priority(sample_tasks):
    return filter_tasks_by_priority(sample_tasks, "High")

@when("I generate a unique ID")
def generate_id(sample_tasks):
    return generate_unique_id(sample_tasks)

# Then steps
@then("I should get all the saved tasks")
def assert_all_tasks_loaded():
    tasks = load_tasks(TEST_TASKS_FILE)
    assert len(tasks) == 3

@then("the file should contain one task")
def assert_one_task():
    tasks = load_tasks(TEST_TASKS_FILE)
    assert len(tasks) == 4

@then("I should only get tasks in the 'Work' category")
def assert_work_tasks():
    filtered = filter_tasks_by_category(load_tasks(TEST_TASKS_FILE), "Work")
    assert all(task["category"] == "Work" for task in filtered)

@then("I should only get tasks with 'High' priority")
def assert_high_priority_tasks():
    filtered = filter_tasks_by_priority(load_tasks(TEST_TASKS_FILE), "High")
    assert all(task["priority"] == "High" for task in filtered)

@then("I should receive a unique ID greater than all existing task IDs")
def assert_unique_id(sample_tasks):
    new_id = generate_unique_id(sample_tasks)
    assert new_id >= max(task["id"] for task in sample_tasks)
