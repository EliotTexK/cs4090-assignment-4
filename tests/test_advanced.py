import pytest
import json
import os
from unittest import mock
from tasks import (
    load_tasks, save_tasks, generate_unique_id,
    filter_tasks_by_priority, filter_tasks_by_category,
    filter_tasks_by_completion, search_tasks, get_overdue_tasks
)

@pytest.fixture
def sample_tasks():
    return [
        {
            "id": 1,
            "title": "Buy groceries",
            "description": "Milk, Eggs, Bread",
            "priority": "High",
            "category": "Personal",
            "due_date": "2025-04-01",
            "completed": False
        },
        {
            "id": 2,
            "title": "Finish project",
            "description": "Complete app development",
            "priority": "Medium",
            "category": "Work",
            "due_date": "2025-05-01",
            "completed": True
        }
    ]

def test_generate_unique_id(sample_tasks):
    assert generate_unique_id(sample_tasks) == 3
    assert generate_unique_id([]) == 1

@pytest.mark.parametrize("priority,expected_count", [
    ("High", 1),
    ("Medium", 1),
    ("Low", 0)
])
def test_filter_by_priority(sample_tasks, priority, expected_count):
    filtered = filter_tasks_by_priority(sample_tasks, priority)
    assert len(filtered) == expected_count

@pytest.mark.parametrize("category,expected_count", [
    ("Personal", 1),
    ("Work", 1),
    ("School", 0)
])
def test_filter_by_category(sample_tasks, category, expected_count):
    filtered = filter_tasks_by_category(sample_tasks, category)
    assert len(filtered) == expected_count

def test_filter_by_completion(sample_tasks):
    assert len(filter_tasks_by_completion(sample_tasks, completed=True)) == 1
    assert len(filter_tasks_by_completion(sample_tasks, completed=False)) == 1

@pytest.mark.parametrize("query,expected_count", [
    ("groceries", 1),
    ("project", 1),
    ("meeting", 0),
])
def test_search_tasks(sample_tasks, query, expected_count):
    result = search_tasks(sample_tasks, query)
    assert len(result) == expected_count

@mock.patch("tasks.datetime")
def test_get_overdue_tasks(mock_datetime, sample_tasks):
    mock_datetime.now.return_value = mock.Mock(strftime=lambda fmt: "2025-04-15")
    overdue = get_overdue_tasks(sample_tasks)
    assert len(overdue) == 1
    assert overdue[0]["title"] == "Buy groceries"

@mock.patch("builtins.open", new_callable=mock.mock_open, read_data='[]')
def test_load_tasks_reads_file(mock_file):
    tasks = load_tasks("dummy.json")
    assert isinstance(tasks, list)
    mock_file.assert_called_with("dummy.json", "r")

@mock.patch("builtins.open", new_callable=mock.mock_open)
def test_save_tasks_writes_file(mock_file, sample_tasks):
    save_tasks(sample_tasks, "dummy.json")
    mock_file.assert_called_with("dummy.json", "w")
    handle = mock_file()
    handle.write.assert_called()
