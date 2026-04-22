// Configure your API Gateway endpoint URL here
const API_URL = 'https://<YOUR_API_ID>.execute-api.us-east-1.amazonaws.com/Prod/todos';

const taskInput = document.getElementById('task-input');
const addTaskBtn = document.getElementById('add-task-btn');
const taskList = document.getElementById('task-list');

// Fetch and display all tasks
async function getTasks() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const tasks = await response.json();
        taskList.innerHTML = ''; // Clear existing list
        tasks.forEach(task => {
            const li = document.createElement('li');
            li.textContent = task.task;
            li.dataset.id = task.id;
            if (task.completed) {
                li.classList.add('completed');
            }

            const deleteBtn = document.createElement('button');
            deleteBtn.textContent = 'Delete';
            deleteBtn.classList.add('delete-btn');
            deleteBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                deleteTask(task.id);
            });

            const completeBtn = document.createElement('button');
            completeBtn.textContent = task.completed ? 'Undo' : 'Complete';
            completeBtn.classList.add('complete-btn');
            completeBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                toggleComplete(task.id, !task.completed);
            });
            
            li.appendChild(completeBtn);
            li.appendChild(deleteBtn);
            taskList.appendChild(li);
        });
    } catch (error) {
        console.error('Error fetching tasks:', error);
        alert('Failed to fetch tasks. Please check the console for more details.');
    }
}

// Add a new task
async function addTask() {
    const taskText = taskInput.value.trim();
    if (taskText === '') {
        alert('Please enter a task.');
        return;
    }

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ task: taskText }),
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        taskInput.value = '';
        getTasks(); // Refresh the list
    } catch (error) {
        console.error('Error adding task:', error);
        alert('Failed to add task. Please check the console for more details.');
    }
}

// Delete a task
async function deleteTask(id) {
    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        getTasks(); // Refresh the list
    } catch (error) {
        console.error('Error deleting task:', error);
        alert('Failed to delete task. Please check the console for more details.');
    }
}

// Toggle task completion status
async function toggleComplete(id, completed) {
    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ completed: completed }),
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        getTasks(); // Refresh the list
    } catch (error) {
        console.error('Error updating task:', error);
        alert('Failed to update task. Please check the console for more details.');
    }
}

// Event Listeners
addTaskBtn.addEventListener('click', addTask);
taskInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        addTask();
    }
});

// Initial load
document.addEventListener('DOMContentLoaded', getTasks);
