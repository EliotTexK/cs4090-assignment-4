# Test Results and Metrics

Run tests to see test results.

As for metrics: read the test code, and run with coverage. It's the only real way to understand what the tests are measuring.
It would be silly to make tests for the tests.

# Bug Summary

## Bug Report 1:

### Application crashes when entering a very long task title or description

- Severity: High

- Environment: Streamlit, Latest version as of report

### Steps to Reproduce:

1. Open the app.

2. Add a new task with a title or description longer than several hundred characters.

3. Click "Add Task".

- Expected Result: The task is added, or input is truncated/sanitized gracefully.

- Actual Result: The app crashes or becomes unresponsive.

- Root Cause: Unbounded input length overwhelms the UI or storage logic.

### Suggested Fix:

- Add maximum length validation to inputs (e.g., st.text_input(..., max_chars=100)).

- Consider truncating text for display.

## Bug Report 2:

### Task ID generation using len(tasks) + 1 can lead to duplicate IDs

- Severity: Critical

- Environment: All environments using app.py

### Steps to Reproduce:

1. Add several tasks.

2. Delete one or more tasks.

3. Add a new task.

- Expected Result: Every task has a unique ID.

- Actual Result: A new task may reuse an ID that was just deleted.

- Root Cause: ID is generated using len(tasks) + 1, which doesn't account for deletions.

### Suggested Fix:

- Use generate_unique_id(tasks) from tasks.py which computes the max existing ID and adds 1.

## Bug Report 3:

### Pressing "Complete" and "Delete" buttons rapidly in succession causes inconsistent task state

- Severity: Medium

- Environment: Streamlit, under normal use with fast user interaction

### Steps to Reproduce:

1. View a task in the main area.

2. Rapidly click both "Complete" and "Delete" buttons for the same task.

3. Expected Result: One action is processed cleanly (preferably Delete).

Actual Result:

- Task disappears without saving its updated state,

- UI reruns with stale or duplicate state,

- App may behave unpredictably.

Root Cause: Streamlit handles both buttons independently, and simultaneous rerun events can clash.

### Suggested Fix:

- Use a st.form() to group actions per task.

## Evidence of Fixes:

I implemented all "suggested fixes", which you can see in the diffs.

# Reports of TDD, BDD, and Property-based testing

Run pytest with `"--html=report.html", "--self-contained-html"`

Then, open the generated `report.html` with a browser.

# Lessons Learned

1. There are many ways to test.

2. Property-based testing is very thorough.

3. pytest.ini is a godsend for organizing your test files.

4. Coverage is not a sufficient metric, but it's not completely useless.

5. TDD can catch bugs before you even write the code.

6. TDD can't catch everything.