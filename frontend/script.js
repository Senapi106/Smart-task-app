let token = localStorage.getItem("token") || "";

// LOGIN
async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const res = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password })
    });

    const data = await res.json();

    if (data.access_token) {
        token = data.access_token;
        localStorage.setItem("token", token);

        alert("Login successful");
        getTasks();
    } else {
        alert("Login failed");
    }
}

// LOGOUT
function logout() {
    localStorage.removeItem("token");
    token = "";
    document.getElementById("taskList").innerHTML = "";
    alert("Logged out");
}

// CREATE TASK
async function createTask() {
    const title = document.getElementById("taskTitle").value;

    await fetch("http://127.0.0.1:5000/tasks", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({ title })
    });

    document.getElementById("taskTitle").value = "";
    getTasks();
}

// GET TASKS
async function getTasks() {
    if (!token) return;

    const res = await fetch("http://127.0.0.1:5000/tasks", {
        headers: {
            "Authorization": "Bearer " + token
        }
    });

    const tasks = await res.json();

    const list = document.getElementById("taskList");
    list.innerHTML = "";

    tasks.forEach(task => {
        const li = document.createElement("li");

        li.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center;">
                
                <span style="${task.completed ? 'text-decoration: line-through; color: gray;' : ''}">
                    ${task.title}
                </span>

                <div>
                    <input type="checkbox" 
                        ${task.completed ? "checked" : ""} 
                        onchange="toggleTask(${task.id}, this.checked)">

                    <button onclick="deleteTask(${task.id})">❌</button>
                </div>

            </div>
        `;

        list.appendChild(li);
    });
}

// DELETE TASK
async function deleteTask(taskId) {
    await fetch(`http://127.0.0.1:5000/tasks/${taskId}`, {
        method: "DELETE",
        headers: {
            "Authorization": "Bearer " + token
        }
    });

    getTasks();
}

// TOGGLE TASK
async function toggleTask(taskId, completed) {
    await fetch(`http://127.0.0.1:5000/tasks/${taskId}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({ completed })
    });

    getTasks();
}

// AUTO LOAD
if (token) {
    getTasks();
}