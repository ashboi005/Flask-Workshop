const apiUrl = 'http://127.0.0.1:5000/api/todos'; 

// Fetch and display to-dos
const fetchTodos = async () => {
    try {
        const response = await fetch(apiUrl);
        const todos = await response.json();

        const todoList = document.getElementById('todo-list');
        todoList.innerHTML = ''; 

        todos.forEach(todo => {
            const listItem = document.createElement('li');
            listItem.textContent = `${todo.task} - ${todo.description}`;
            todoList.appendChild(listItem);
        });
    } catch (error) {
        console.error('Error fetching todos:', error);
    }
};

// Add a new to-do
const addTodo = async () => {
    const task = document.getElementById('task').value;
    const description = document.getElementById('description').value;

    try {
        const response = await fetch('http://127.0.0.1:5000/api/todo', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                task,
                description,
            }),
        });

        if (response.ok) {
            fetchTodos(); // Re-fetch the list to update it
        } else {
            console.error('Error adding task:', response.statusText);
        }
    } catch (error) {
        console.error('Error adding task:', error);
    }
};

document.getElementById('add-task-btn').addEventListener('click', addTodo);

// Fetch to-dos when the page loads
window.onload = fetchTodos;
