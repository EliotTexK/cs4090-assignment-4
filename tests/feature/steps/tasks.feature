

Feature: Task management

  Scenario: Loading tasks from a file
    Given I have a list of sample tasks
    When I load the tasks from the file
    Then I should get all the saved tasks

  Scenario: Saving a new task
    Given the task list is empty
    When I add a new task
    Then the file should contain one task

  Scenario: Filtering by category
    Given I have a list of sample tasks
    When I filter tasks by the 'Work' category
    Then I should only get tasks in the 'Work' category

  Scenario: Filtering by priority
    Given I have a list of sample tasks
    When I filter tasks by 'High' priority
    Then I should only get tasks with 'High' priority

  Scenario: Generating a unique ID
    Given I have a list of sample tasks
    When I generate a unique ID
    Then I should receive a unique ID greater than all existing task IDs
