import streamlit as st
import pandas as pd
import subprocess
from datetime import datetime, date
from tasks import load_tasks, save_tasks, filter_tasks_by_priority, filter_tasks_by_category, generate_unique_id

def run_unit_tests():
    result = subprocess.run(
        ["pytest", "-v", "tests/test_basic.py"],
        capture_output=True, 
        text=True
    )
    return result.stdout, result.stderr

def run_advanced_tests():
    result = subprocess.run(
        ["pytest", "-v", "tests/test_advanced.py",
        "--cov=tasks", "--cov-report=term-missing",
        "--html=report.html", "--self-contained-html"],
        capture_output=True, 
        text=True
    )
    return result.stdout, result.stderr

def run_bdd_tests():
    result = subprocess.run(
        ["pytest", "-v", "tests/feature/steps/test_add_steps.py"],
        capture_output=True, 
        text=True
    )
    return result.stdout, result.stderr

def main():
    st.title("To-Do Application")
    
    # Load existing tasks
    tasks = load_tasks()
    
    # Sidebar for adding new tasks
    st.sidebar.header("Add New Task")
    
    # new category creation
    existing_categories = list(set([task["category"] for task in tasks]))
    st.sidebar.subheader("Categories")
    new_category = st.sidebar.text_input("Add New Category")

    if new_category and new_category not in existing_categories:
        existing_categories.append(new_category)
        st.sidebar.success(f"Added category: {new_category}")

    # Task creation form
    with st.sidebar.form("new_task_form"):
        task_title = st.text_input("Task Title", max_chars=100)
        task_description = st.text_area("Description", max_chars=1000)
        task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        task_category = st.selectbox("Category", existing_categories + ["Work", "School", "Personal", "Other"])
        task_due_date = st.date_input("Due Date")
        submit_button = st.form_submit_button("Add Task")
        task_color = st.color_picker("Task Color", "#ffffff")
        
        if submit_button and task_title:
            new_task = {
                "id": generate_unique_id(tasks),
                "title": task_title,
                "description": task_description,
                "priority": task_priority,
                "category": task_category,
                "due_date": task_due_date.strftime("%Y-%m-%d"),
                "completed": False,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "color": task_color
            }
            tasks.append(new_task)
            save_tasks(tasks)
            st.sidebar.success("Task added successfully!")

    # Main area to display tasks
    st.header("Your Tasks")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        filter_category = st.selectbox("Filter by Category", ["All"] + list(set([task["category"] for task in tasks])))
    with col2:
        filter_priority = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
    
    show_completed = st.checkbox("Show Completed Tasks")
    
    # Advanced filters
    with st.expander("Advanced Filters"):
        start_date = st.date_input("Start Due Date", value=date(2025, 1, 1))
        end_date = st.date_input("End Due Date", value=date(2025, 12, 31))
    
    # Apply filters
    filtered_tasks = tasks.copy()
    if filter_category != "All":
        filtered_tasks = filter_tasks_by_category(filtered_tasks, filter_category)
    if filter_priority != "All":
        filtered_tasks = filter_tasks_by_priority(filtered_tasks, filter_priority)
    if not show_completed:
        filtered_tasks = [task for task in filtered_tasks if not task["completed"]]

    filtered_tasks = [
        task for task in filtered_tasks
        if start_date <= datetime.strptime(task["due_date"], "%Y-%m-%d").date() <= end_date
    ]

    # Display tasks
    for task in filtered_tasks:
        task_color = task.get("color", "#ffffff")
        with st.container():
            st.markdown(
                f"""
                <div style="background-color:{task_color}; padding:10px; border-radius:8px;">
                """,
                unsafe_allow_html=True
            )
            with st.form(f"task_form_{task['id']}"):
                col1, col2 = st.columns([4, 1])
                with col1:
                    if task["completed"]:
                        st.markdown(f"~~**{task['title']}**~~")
                    else:
                        st.markdown(f"**{task['title']}**")
                    st.write(task["description"])
                    st.caption(f"Due: {task['due_date']} | Priority: {task['priority']} | Category: {task['category']}")
                with col2:
                    complete_button = st.form_submit_button("Complete" if not task["completed"] else "Undo")
                    delete_button = st.form_submit_button("Delete")

                if complete_button:
                    for t in tasks:
                        if t["id"] == task["id"]:
                            t["completed"] = not t["completed"]
                            save_tasks(tasks)
                            st.rerun()

                if delete_button:
                    tasks = [t for t in tasks if t["id"] != task["id"]]
                    save_tasks(tasks)
                    st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)
    
    # Button to run unit tests
    if st.sidebar.button("Run Unit Tests"):
        st.sidebar.write("Running unit tests...")
        stdout, stderr = run_unit_tests()
        st.sidebar.text_area("Test Output", stdout + "\n" + stderr, height=400)
    
    # Button to run advanced tests
    if st.sidebar.button("Run Advanced Tests"):
        st.sidebar.write("Running advanced tests...")
        stdout, stderr = run_advanced_tests()
        st.sidebar.text_area("Test Output", stdout + "\n" + stderr, height=400)

    # Button to run bdd tests
    if st.sidebar.button("Run BDD Tests"):
        st.sidebar.write("Running BDD tests...")
        stdout, stderr = run_bdd_tests()
        st.sidebar.text_area("Test Output", stdout + "\n" + stderr, height=400)

if __name__ == "__main__":
    main()