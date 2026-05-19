import os
import json
import webbrowser
from threading import Timer
from flask import Flask, render_template_string, request, jsonify, session

app = Flask(__name__)
# Use SECRET_KEY from environment when available (safer for production)
app.secret_key = os.environ.get("SECRET_KEY", "multi_user_secure_os_token_2026")

USER_DATABASE_FILE = "user_registry.json"
CONFIG_FILE = "config_dashboard.json"

# --- MULTI-USER DATA ISOLATION HANDLERS ---
def load_global_registry():
    if os.path.exists(USER_DATABASE_FILE):
        with open(USER_DATABASE_FILE, "r") as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_global_registry(data):
    with open(USER_DATABASE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_user_scoped_filename(data_type):
    """Isolates dataset storage paths dynamically using active user sessions."""
    if "user_email" in session:
        # Replaces characters unsafe for system file designations
        safe_email = session["user_email"].replace("@", "_").replace(".", "_")
        return f"user_{safe_email}_{data_type}_dashboard.json"
    # Fallback to general files if not logged in
    return f"guest_{data_type}_dashboard.json"

def load_data(filename, default_val=None):
    if default_val is None:
        default_val = []
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try: return json.load(f)
            except: return default_val
    return default_val

def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def get_config():
    # Prefer environment variable for production deployments (e.g., Render)
    env_key = os.environ.get("AI_API_KEY")
    if env_key is not None and env_key.strip() != "":
        return {"api_key": env_key}

    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            try: return json.load(f)
            except: return {"api_key": ""}
    return {"api_key": ""}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

# --- MODERNIZED GRADIENT LAYERED UI TEMPLATE ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Life Personal OS</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { 
            background: linear-gradient(135deg, #f5f0f9 0%, #e8dff5 100%); 
            font-family: 'Segoe UI', system-ui, sans-serif;
            color: #3d2c4d;
            min-height: 100vh;
            scroll-behavior: smooth;
        }
        .navbar-custom {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            border-bottom: 2px solid #e1b3ff;
            box-shadow: 0 4px 15px rgba(138, 43, 226, 0.05);
        }
        .brand-logo {
            font-weight: 800;
            background: linear-gradient(45deg, #8a2be2, #ff1493);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        /* HEADER SHORTCUT BUTTONS */
        .header-shortcut-btn {
            background: transparent;
            border: 1px solid transparent;
            border-radius: 12px;
            color: #6a4fa3;
            font-weight: 600;
            font-size: 0.9rem;
            padding: 6px 12px;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 4px;
        }
        .header-shortcut-btn:hover {
            background: #f3ebff;
            color: #4b0082;
            border-color: #dfc2ff;
        }

        /* 📝 TODO CONTAINER (PRESERVED AS REQUESTED) */
        .card-main {
            background: #ffffff;
            border: 1px solid #f0daf7;
            border-radius: 20px;
            box-shadow: 0 10px 25px rgba(138, 43, 226, 0.05);
            transition: all 0.3s ease;
        }
        .card-main:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 30px rgba(255, 20, 147, 0.08);
        }

        /* 💳 NEW UPGRADED EXPENSE TRACKER UI */
        .card-expense-lux {
            background: linear-gradient(145deg, #ffffff 0%, #fffbfd 100%);
            border: 2px solid #ffc2e0;
            border-radius: 24px;
            box-shadow: 0 12px 30px rgba(255, 20, 147, 0.05);
            transition: all 0.3s ease;
        }
        .card-expense-lux:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(255, 20, 147, 0.12);
        }
        
        /* 🤖 NEW UPGRADED NEON DARK AI TERMINAL UI */
        .card-ai-darkspace {
            background: linear-gradient(135deg, #1d0f30 0%, #0d041a 100%);
            color: #f1ebfa;
            border-radius: 26px;
            border: 1px solid #bd5eff;
            box-shadow: 0 15px 40px rgba(157, 78, 221, 0.2);
        }

        .btn-gradient-purple {
            background: linear-gradient(135deg, #9400d3 0%, #4b0082 100%);
            color: white; border: none; font-weight: 600; border-radius: 10px;
        }
        .btn-gradient-purple:hover { color: #f8f1ff; opacity: 0.9; }
        
        .btn-gradient-pink {
            background: linear-gradient(135deg, #ff1493 0%, #c71585 100%);
            color: white; border: none; font-weight: 600; border-radius: 10px;
        }
        .btn-gradient-pink:hover { color: #fff0f5; opacity: 0.9; }

        .btn-pill {
            border-radius: 30px; font-size: 0.85rem; font-weight: 600;
            transition: all 0.2s; border: 1px solid rgba(255,255,255,0.25);
        }
        .btn-pill:hover { background: #ff1493; color: white; border-color: #ff1493; }

        .completed-task { text-decoration: line-through; color: #bba2cd; }
        .form-control, .form-select { border-radius: 10px; border: 1px solid #dcd0ec; }
        .form-control:focus, .form-select:focus { border-color: #ba55d3; box-shadow: 0 0 0 0.25rem rgba(186, 85, 211, 0.25); }
        
        .ai-response-box {
            background: rgba(255, 255, 255, 0.07);
            border-left: 5px solid #ff1493;
            border-radius: 14px;
            font-size: 0.98rem;
            line-height: 1.6;
            color: #ebd9ff;
        }
        .notes-textarea {
            resize: none;
            font-size: 0.9rem;
            border: 1px dashed #dcd0ec;
            background: #fff9fe;
            border-radius: 12px;
            color: #5c4475;
        }
        .notes-textarea:focus { background: #ffffff; border-style: solid; }
        
        .user-auth-trigger {
            font-weight: 600;
            border-radius: 12px;
            border: 1px solid #ba55d3;
            color: #8a2be2;
            background: #ffffff;
            transition: all 0.2s;
        }
        .user-auth-trigger:hover { background: #ba55d3; color: white; }
    </style>
</head>
<body>

<nav class="navbar navbar-expand-lg navbar-custom sticky-top mb-4">
    <div class="container-fluid px-4">
        <span class="navbar-brand brand-logo fs-3 me-3">🔮 AI Life Personal OS</span>
        
        <div class="d-none d-md-flex align-items-center gap-2 me-auto">
            <button class="header-shortcut-btn" onclick="scrollToTarget('todoFrame')">📝 Tasks</button>
            <button class="header-shortcut-btn" onclick="scrollToTarget('expenseFrame')">💳 Expenses</button>
            <button class="header-shortcut-btn" onclick="scrollToTarget('aiFrame')">🤖 AI Terminal</button>
        </div>

        <div class="d-flex align-items-center gap-3">
            <div class="d-flex align-items-center bg-white p-1 rounded border">
                <input type="password" id="apiKeyInput" class="form-control form-control-sm border-0 shadow-none" style="width: 180px;" placeholder="🔐 Paste API Key" value="{{ config.api_key }}">
                <button class="btn btn-sm btn-gradient-purple px-2" onclick="saveApiKey()">Save Key</button>
            </div>
            
            {% if session.get('user_email') %}
                <div class="dropdown">
                    <button class="btn btn-sm user-auth-trigger dropdown-toggle px-3" type="button" id="userSettings" data-bs-toggle="dropdown" aria-expanded="false">
                        👤 {{ session.get('user_name') }}
                    </button>
                    <ul class="dropdown-menu dropdown-menu-end shadow" aria-labelledby="userSettings">
                        <li><span class="dropdown-item-text text-muted small">ID: {{ session.get('user_email') }}</span></li>
                        <li><hr class="dropdown-divider"></li>
                        <li><a class="dropdown-item text-danger fw-bold" href="#" onclick="logoutUser()">Logout Account</a></li>
                    </ul>
                </div>
            {% else %}
                <button class="btn btn-sm user-auth-trigger px-3" onclick="openAuthenticationModal()">👤 Login / Link Profile</button>
            {% endif %}
        </div>
    </div>
</nav>

<div class="container mb-5">
    {% if not session.get('user_email') %}
    <div class="alert alert-sm border-0 shadow-sm rounded-4 mb-4 text-center text-secondary bg-white p-2" style="font-size:0.9rem;">
        💡 You are viewing as a guest. Link your profile above to back up data across multiple users.
    </div>
    {% endif %}

    <div class="row g-4">
        
        <div class="col-lg-6" id="todoFrame">
            <div class="card card-main p-4 d-flex flex-column h-100">
                <h3 class="mb-3 d-flex justify-content-between align-items-center" style="color: #4b0082;">
                    <span>📝 Things/Task</span>
                    <span class="badge rounded-pill fs-6" id="taskCount" style="background-color: #8a2be2;">0</span>
                </h3>
                
                <div class="input-group mb-4">
                    <input type="text" id="newTask" class="form-control" placeholder="Deploy new life objective...">
                    <button class="btn btn-gradient-purple" onclick="addTask()">Add Task</button>
                </div>

                <ul class="list-group list-group-flush mb-4" id="todoList" style="max-height: 280px; overflow-y: auto;"></ul>
                
                <div class="mt-auto pt-3 border-top">
                    <label class="form-label fw-bold text-muted small d-flex align-items-center gap-1">📌 Task Pad Context Notes:</label>
                    <textarea id="taskNotes" class="form-control notes-textarea p-2" rows="3" placeholder="Jot down execution guidelines..." oninput="saveNotes('task')">{{ notes.task }}</textarea>
                </div>
            </div>
        </div>

        <div class="col-lg-6" id="expenseFrame">
            <div class="card card-expense-lux p-4 d-flex flex-column h-100">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h3 class="m-0" style="color: #c71585; font-weight: 700;">💳 Expense Tracker</h3>
                    <span class="badge fs-5 rounded-pill shadow-sm" id="totalExpense" style="background: linear-gradient(135deg, #ff1493, #c71585);">₹0.00</span>
                </div>

                <div class="d-flex align-items-center justify-content-end gap-2 mb-3">
                    <div class="d-flex align-items-center bg-white border px-2 py-1 rounded" style="border-color: #ffc2e0 !important;">
                        <span class="me-1">📅</span>
                        <input type="date" id="ledgerDatePicker" class="border-0 bg-transparent text-muted small" style="outline: none;" onchange="saveLedgerDate()">
                    </div>
                    <select id="currencySelector" class="form-select form-select-sm" style="width: 85px; font-weight: 600;" onchange="updateCurrencySign()">
                        <option value="₹" selected>₹ (Rs)</option>
                        <option value="$">$ (USD)</option>
                        <option value="€">€ (EUR)</option>
                        <option value="£">£ (GBP)</option>
                    </select>
                </div>
                
                <div class="row g-2 mb-3">
                    <div class="col-md-4">
                        <input type="number" id="expAmount" class="form-control" placeholder="Cost">
                    </div>
                    <div class="col-md-4">
                        <input type="text" id="expCategory" class="form-control" placeholder="Category">
                    </div>
                    <div class="col-md-4">
                        <input type="text" id="expDesc" class="form-control" placeholder="Description">
                    </div>
                </div>
                <button class="btn btn-gradient-pink w-100 mb-4 shadow-sm" onclick="addExpense()">Record Expense Log</button>

                <div class="table-responsive mb-4" style="max-height: 200px; overflow-y: auto;">
                    <table class="table align-middle table-hover">
                        <thead>
                            <tr style="color: #c71585;">
                                <th>Category</th>
                                <th>Amount</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody id="expenseTableBody"></tbody>
                    </table>
                </div>

                <div class="mt-auto pt-3 border-top">
                    <label class="form-label fw-bold text-muted small d-flex align-items-center gap-1">💰 Financial Blueprint Notes:</label>
                    <textarea id="expenseNotes" class="form-control notes-textarea p-2" rows="3" placeholder="Log savings objectives..." oninput="saveNotes('expense')">{{ notes.expense }}</textarea>
                </div>
            </div>
        </div>

    </div>

    <div class="row mt-4" id="aiFrame">
        <div class="col-12">
            <div class="card p-4 card-ai-darkspace">
                <div class="d-flex align-items-center justify-content-between mb-3 border-bottom border-secondary pb-3">
                    <h4 class="m-0 text-white d-flex align-items-center fw-bold">
                        <span class="fs-2 me-2">🤖</span> AI Assistant Workspace Workspace
                    </h4>
                </div>

                <div class="mb-4">
                    <label class="form-label text-white-50 small mb-2">✨ Ask your OS anything or query system workflows:</label>
                    <form id="aiForm" onsubmit="triggerQueryAction(event)">
                        <div class="input-group">
                            <input type="text" id="aiUserQuery" class="form-control bg-dark text-white border-secondary" style="border-radius: 12px 0 0 12px;" placeholder="Type your query or instruction prompt here...">
                            <button type="submit" class="btn btn-gradient-pink px-4" style="border-radius: 0 12px 12px 0;">Ask AI 🚀</button>
                        </div>
                    </form>
                </div>

                <div class="mb-4">
                    <p class="text-white-50 small mb-2">⚡ Quick Analytical Blueprint Macros:</p>
                    <div class="d-flex flex-wrap gap-2">
                        <button class="btn btn-outline-light btn-pill" onclick="triggerMacroAction('blueprint')">📊 Audit Budget Blueprint</button>
                        <button class="btn btn-outline-light btn-pill" onclick="triggerMacroAction('tasks')">⚡ Map Out Action Priority Plan</button>
                    </div>
                </div>
                
                <div class="p-3 ai-response-box" id="aiOutputDisplay">
                    <span class="text-white-50"><em>Standing by. Submit an open query or select a macro blueprint shortcut option...</em></span>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="modal fade" id="authModal" tabindex="-1" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content text-dark" style="border-radius:20px;">
      <div class="modal-header border-0 pb-0">
        <h5 class="modal-title fw-bold" style="color: #4b0082;">👤 User System Space Access</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body">
        <nav class="nav nav-tabs mb-3" id="authTabs" role="tablist">
          <button class="nav-link active fw-bold" id="login-tab" data-bs-toggle="tab" data-bs-target="#loginPane" type="button" role="tab">Login</button>
          <button class="nav-link fw-bold" id="register-tab" data-bs-toggle="tab" data-bs-target="#registerPane" type="button" role="tab">Sign Up</button>
        </nav>
        <div class="tab-content">
          <div class="tab-pane fade show active" id="loginPane" role="tabpanel">
             <div class="mb-3">
                 <label class="form-label small fw-bold">Account Email</label>
                 <input type="email" id="loginEmail" class="form-control" placeholder="name@example.com">
             </div>
             <div class="mb-3">
                 <label class="form-label small fw-bold">Password</label>
                 <input type="password" id="loginPass" class="form-control" placeholder="••••••••">
             </div>
             <button class="btn btn-gradient-purple w-100" onclick="performAuthentication('login')">Access Account Panel</button>
          </div>
          <div class="tab-pane fade" id="registerPane" role="tabpanel">
             <button class="btn btn-outline-danger w-100 mb-3 fw-bold d-flex align-items-center justify-content-center gap-2" onclick="performAuthentication('google')">
                 <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-google" viewBox="0 0 16 16"><path d="M15.545 6.558a9.4 9.4 0 0 1 .139 1.626c0 2.434-.87 4.492-2.384 5.885h.002C11.978 15.292 10.158 16 8 16A8 8 0 1 1 8 0c2.198 0 4.036.818 5.437 2.15l-2.138 2.138C10.207 3.238 9.214 2.765 8 2.765c-2.3 0-4.237 1.556-4.935 3.654A4.8 4.8 0 0 0 3 8c0 .416.052.822.152 1.21.698 2.098 2.635 3.654 4.935 3.654 1.31 0 2.417-.353 3.214-1.018 1.15-.956 1.742-2.433 1.742-4.143V6.56z"/></svg>
                 Sign up with Google
             </button>
             <div class="text-center text-muted small mb-2">- OR TYPE DETAILS -</div>
             <div class="mb-2">
                 <label class="form-label small fw-bold">Your Name</label>
                 <input type="text" id="regName" class="form-control form-control-sm" placeholder="John Doe">
             </div>
             <div class="mb-2">
                 <label class="form-label small fw-bold">Email Address</label>
                 <input type="email" id="regEmail" class="form-control form-control-sm" placeholder="name@example.com">
             </div>
             <div class="mb-3">
                 <label class="form-label small fw-bold">Set Password</label>
                 <input type="password" id="regPass" class="form-control form-control-sm" placeholder="••••••••">
             </div>
             <button class="btn btn-gradient-pink w-100" onclick="performAuthentication('register')">Register Account Matrix</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="modal fade" id="editModal" tabindex="-1" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content text-dark" style="border-radius:15px;">
      <div class="modal-header">
        <h5 class="modal-title">✏️ Edit Matrix Element</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body">
        <input type="hidden" id="editType">
        <input type="hidden" id="editId">
        <div id="todoEditFields">
            <input type="text" id="editTaskTitle" class="form-control">
        </div>
        <div id="expenseEditFields" class="d-none">
            <input type="number" id="editExpAmount" class="form-control mb-2" placeholder="Amount">
            <input type="text" id="editExpCategory" class="form-control mb-2" placeholder="Category">
            <input type="text" id="editExpDesc" class="form-control" placeholder="Description">
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-light" data-bs-dismiss="modal">Close</button>
        <button type="button" class="btn btn-gradient-purple" onclick="submitEdit()">Save Metrics</button>
      </div>
    </div>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
<script>
    let editModalObj;
    let authModalObj;
    let currencySign = "₹";
    let notesTimeout = null;

    document.addEventListener("DOMContentLoaded", () => {
        editModalObj = new bootstrap.Modal(document.getElementById('editModal'));
        authModalObj = new bootstrap.Modal(document.getElementById('authModal'));
        
        const today = new Date().toISOString().split('T')[0];
        const storedDate = localStorage.getItem('ledger_date') || today;
        document.getElementById('ledgerDatePicker').value = storedDate;

        refreshDashboard();
        
        document.getElementById('aiForm').addEventListener('submit', function(e) {
            e.preventDefault();
        });
    });

    function scrollToTarget(id) {
        const target = document.getElementById(id);
        if(target) {
            window.scrollTo({ top: target.offsetTop - 90, behavior: 'smooth' });
        }
    }

    function openAuthenticationModal() {
        authModalObj.show();
    }

    function performAuthentication(mode) {
        let payload = { action: mode };
        if (mode === 'login') {
            payload.email = document.getElementById('loginEmail').value.trim();
            payload.password = document.getElementById('loginPass').value;
            if(!payload.email || !payload.password) { alert("Please input all authentication credentials!"); return; }
        } else if (mode === 'register') {
            payload.name = document.getElementById('regName').value.trim();
            payload.email = document.getElementById('regEmail').value.trim();
            payload.password = document.getElementById('regPass').value;
            if(!payload.name || !payload.email || !payload.password) { alert("All fields are mandatory to build user account profiles!"); return; }
        }

        fetch('/api/auth/gateway', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        }).then(res => res.json()).then(data => {
            if(data.status === 'success') {
                authModalObj.hide();
                window.location.reload();
            } else {
                alert(data.message);
            }
        });
    }

    function logoutUser() {
        fetch('/api/auth/gateway', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ action: 'logout' })
        }).then(() => window.location.reload());
    }

    function saveLedgerDate() {
        const selectedDate = document.getElementById('ledgerDatePicker').value;
        localStorage.setItem('ledger_date', selectedDate);
    }

    // Dynamic UI currency updating handler
    function updateCurrencySign() {
        currencySign = document.getElementById('currencySelector').value;
        refreshDashboard();
    }

    function saveNotes(type) {
        clearTimeout(notesTimeout);
        const textVal = (type === 'task') ? document.getElementById('taskNotes').value : document.getElementById('expenseNotes').value;
        
        notesTimeout = setTimeout(() => {
            fetch('/api/notes', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ type: type, content: textVal })
            });
        }, 500);
    }

    function saveApiKey() {
        const key = document.getElementById('apiKeyInput').value;
        fetch('/api/config', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({api_key: key})
        }).then(() => alert("System Key Map Synced!"));
    }

    function refreshDashboard() {
        fetch('/api/todos').then(res => res.json()).then(data => {
            const list = document.getElementById('todoList');
            list.innerHTML = '';
            document.getElementById('taskCount').innerText = data.length;
            data.forEach((task, index) => {
                list.innerHTML += `
                    <li class="list-group-item d-flex justify-content-between align-items-center bg-transparent border-bottom py-2 px-1">
                        <div>
                            <input class="form-check-input me-3" type="checkbox" ${task.completed ? 'checked' : ''} onchange="toggleTodo(${index})">
                            <span class="${task.completed ? 'completed-task fw-light' : 'fw-semibold'}">${task.title}</span>
                        </div>
                        <div>
                            <button class="btn btn-sm btn-outline-secondary btn-e me-1" style="border-radius:7px; font-size:0.75rem;" onclick="openEdit('todo', ${index}, '${escape(task.title)}')">Edit</button>
                            <button class="btn btn-sm btn-outline-danger btn-e" style="border-radius:7px; font-size:0.75rem;" onclick="deleteTodo(${index})">Delete</button>
                        </div>
                    </li>`;
            });
        });

        fetch('/api/expenses').then(res => res.json()).then(data => {
            const tbody = document.getElementById('expenseTableBody');
            tbody.innerHTML = '';
            let total = 0;
            data.forEach((exp, index) => {
                total += parseFloat(exp.amount);
                tbody.innerHTML += `
                    <tr class="border-bottom">
                        <td><span class="badge bg-light text-dark border p-2">${exp.category}</span><br><small class="text-muted">${exp.description}</small></td>
                        <td class="fw-bold text-dark">${currencySign}${parseFloat(exp.amount).toFixed(2)}</td>
                        <td>
                            <button class="btn btn-sm btn-link text-secondary p-0 me-2" onclick="openEdit('expense', ${index}, '', ${exp.amount}, '${escape(exp.category)}', '${escape(exp.description)}')">Edit</button>
                            <button class="btn btn-sm btn-link text-danger p-0" onclick="deleteExpense(${index})">Delete</button>
                        </td>
                    </tr>`;
            });
            document.getElementById('totalExpense').innerText = currencySign + total.toFixed(2);
        });
    }

    function addTask() {
        const title = document.getElementById('newTask').value;
        if(!title) return;
        fetch('/api/todos', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({title: title})
        }).then(() => { document.getElementById('newTask').value = ''; refreshDashboard(); });
    }
    
    function toggleTodo(index) {
        fetch(`/api/todos/toggle/${index}`, { method: 'POST' }).then(() => refreshDashboard());
    }
    
    function deleteTodo(index) {
        fetch(`/api/todos/${index}`, { method: 'DELETE' }).then(() => refreshDashboard());
    }

    function addExpense() {
        const amount = document.getElementById('expAmount').value;
        const category = document.getElementById('expCategory').value;
        const description = document.getElementById('expDesc').value;
        if(!amount || !category) return;
        fetch('/api/expenses', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({amount: amount, category: category, description: description})
        }).then(() => {
            document.getElementById('expAmount').value = '';
            document.getElementById('expCategory').value = '';
            document.getElementById('expDesc').value = '';
            refreshDashboard();
        });
    }
    
    function deleteExpense(index) {
        fetch(`/api/expenses/${index}`, { method: 'DELETE' }).then(() => refreshDashboard());
    }

    function openEdit(type, id, title="", amount=0, category="", desc="") {
        document.getElementById('editType').value = type;
        document.getElementById('editId').value = id;
        if(type === 'todo') {
            document.getElementById('todoEditFields').classList.remove('d-none');
            document.getElementById('expenseEditFields').classList.add('d-none');
            document.getElementById('editTaskTitle').value = unescape(title);
        } else {
            document.getElementById('todoEditFields').classList.add('d-none');
            document.getElementById('expenseEditFields').classList.remove('d-none');
            document.getElementById('editExpAmount').value = amount;
            document.getElementById('editExpCategory').value = unescape(category);
            document.getElementById('editExpDesc').value = unescape(desc);
        }
        editModalObj.show();
    }

    function submitEdit() {
        const type = document.getElementById('editType').value;
        const id = document.getElementById('editId').value;
        let payload = {};
        if (type === 'todo') {
            payload = { title: document.getElementById('editTaskTitle').value };
        } else {
            payload = {
                amount: document.getElementById('editExpAmount').value,
                category: document.getElementById('editExpCategory').value,
                description: document.getElementById('editExpDesc').value
            };
        }
        fetch(`/api/edit/${type}/${id}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        }).then(() => { editModalObj.hide(); refreshDashboard(); });
    }

    function triggerQueryAction(event) {
        if(event) event.preventDefault();
        const query = document.getElementById('aiUserQuery').value;
        if (!query) return;
        executeAiEngine('custom', query);
    }

    function triggerMacroAction(macroMode) {
        executeAiEngine(macroMode, "");
    }

    function executeAiEngine(mode, customMessage) {
        const out = document.getElementById('aiOutputDisplay');
        out.innerHTML = "✨ Submitting system context matrix to AI Workspace Engine... Please wait...";
        
        fetch('/api/utility', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ mode: mode, user_query: customMessage })
        })
        .then(res => res.json())
        .then(data => {
            out.innerHTML = `✨ <strong>Response:</strong><br>${data.result}`;
        });
    }
</script>
</body>
</html>
"""
# ====================================================================
# PASTE THIS SINGLE BLOCK AT THE ABSOLUTE END OF YOUR APP.PY FILE
# ====================================================================

HEADER_SNIPPET = """
<style>
    header {
        background-color: #1e293b;
        border-bottom: 1px solid #334155;
        padding: 15px 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: sticky;
        top: 0;
        z-index: 1000;
        font-family: 'Segoe UI', sans-serif;
    }
    .header-brand {
        font-size: 1.4rem;
        font-weight: bold;
        background: linear-gradient(to right, #a855f7, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .header-nav {
        display: flex;
        gap: 25px;
        align-items: center;
    }
    .nav-item {
        color: #f8fafc;
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 1rem;
        font-weight: 500;
        transition: color 0.2s ease, transform 0.2s ease;
    }
    .nav-item:hover {
        color: #a855f7;
        transform: translateY(-1px);
    }
    .streak-container {
        background: rgba(168, 85, 247, 0.1);
        border: 1px solid #a855f7;
        padding: 6px 14px;
        border-radius: 20px;
        display: flex;
        align-items: center;
        gap: 6px;
        font-weight: 600;
        color: #f43f5e;
        box-shadow: 0 0 10px rgba(168, 85, 247, 0.15);
    }
    .streak-icon {
        width: 18px;
        height: 18px;
        animation: flame-pulse 1.5s infinite ease-in-out;
    }
    @keyframes flame-pulse {
        0%, 100% { transform: scale(1); filter: drop-shadow(0 0 2px #f43f5e); }
        50% { transform: scale(1.2); filter: drop-shadow(0 0 5px #f43f5e); }
    }
    
    @media (max-width: 768px) {
        header {
            padding: 12px 15px;
            flex-direction: column;
            gap: 12px;
        }
        .header-nav {
            gap: 15px;
            width: 100%;
            justify-content: center;
            flex-wrap: wrap;
        }
    }
</style>

<header>
    <div class="header-brand">Workspace Dashboard</div>
    <nav class="header-nav">
        <a href="#todo-section" class="nav-item">To Do List</a>
        <a href="#expense-section" class="nav-item">Expense Tracker</a>
        <a href="#ai-section" class="nav-item">AI Assistant</a>
        <div class="streak-container" title="Your daily login streak!">
            <svg class="streak-icon" viewBox="0 0 24 24" fill="#f43f5e">
                <path d="M17.66 11.57c-.77-1.42-2.12-2.42-3.66-2.92.23.94.17 1.93-.17 2.83-.43 1.15-1.3 2.03-2.42 2.49-1.21.49-2.58.37-3.69-.34.1.84.47 1.62 1.07 2.22 1.95 1.95 5.12 1.95 7.07 0 1.96-1.95 1.96-5.12.01-7.07zm-4.32-8.31c-.39-.39-1.02-.39-1.42 0-.25.26-.35.63-.26.98.54 2.13-.07 4.39-1.55 5.87-1.8 1.8-4.5 2.14-6.68.99-.41-.22-.92-.09-1.17.31-.25.4-.19.92.14 1.25 3.32 3.32 8.7 3.32 12.02 0 3.32-3.32 3.32-8.7 0-12.02l-2.6-2.38z"/>
            </svg>
            <span id="streak-days">5 Days</span>
        </div>
    </nav>
</header>
"""

FOOTER_SNIPPET = """
<style>
    footer {
        background-color: #090d16;
        border-top: 1px solid #334155;
        padding: 35px 20px;
        font-family: 'Segoe UI', sans-serif;
        margin-top: 50px;
    }
    .footer-content {
        max-width: 1200px;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 22px;
    }
    .footer-links {
        display: flex;
        gap: 30px;
    }
    .footer-links a {
        color: #94a3b8;
        text-decoration: none;
        transition: color 0.2s ease, transform 0.2s ease;
        font-size: 0.95rem;
    }
    .footer-links a:hover {
        color: #f8fafc;
        transform: translateY(-1px);
    }
    .footer-socials {
        display: flex;
        gap: 24px;
    }
    .social-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 52px;
        height: 52px;
        border-radius: 50%;
        transition: transform 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.25s ease;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        background-color: #1e293b; /* Fallback frame background */
    }
    .social-btn img {
        width: 100%;
        height: 100%;
        object-fit: contain;
        border-radius: 50%;
    }
    .social-btn:hover {
        transform: translateY(-5px);
    }
    .tg-btn:hover { box-shadow: 0 6px 16px rgba(0, 136, 204, 0.5); }
    .wa-btn:hover { box-shadow: 0 6px 16px rgba(37, 211, 102, 0.5); }
    .mail-btn:hover { box-shadow: 0 6px 16px rgba(234, 67, 53, 0.4); }
    
    .footer-copy {
        color: #64748b;
        font-size: 0.85rem;
        margin: 0;
        text-align: center;
    }
</style>

<footer>
    <div class="footer-content">
        <div class="footer-links">
            <a href="#">Contact Us</a>
            <a href="#">Privacy Policy</a>
        </div>
        <div class="footer-socials">
            <a href="https://t.me/+918262925515" target="_blank" class="social-btn tg-btn" title="Chat on Telegram">
                <img src="https://upload.wikimedia.org/wikipedia/commons/8/83/Telegram_2019_Logo.svg" alt="Telegram">
            </a>
            <a href="https://wa.me/918262925515" target="_blank" class="social-btn wa-btn" title="Chat on WhatsApp">
                <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" alt="WhatsApp">
            </a>
            <a href="mailto:yogeshdg5515@gmail.com" class="social-btn mail-btn" title="Send Email">
                <img src="https://upload.wikimedia.org/wikipedia/commons/7/7e/Gmail_icon_%282020%29.svg" alt="Gmail">
            </a>
        </div>
        <p class="footer-copy">&copy; 2026 Workspace Dashboard. All Rights Reserved.</p>
    </div>
</footer>
"""

# Dynamic injection logic to seamlessly integrate components with your HTML string asset
if "HTML_TEMPLATE" in globals():
    if "<body>" in HTML_TEMPLATE:
        HTML_TEMPLATE = HTML_TEMPLATE.replace("<body>", f"<body>{HEADER_SNIPPET}")
    if "</body>" in HTML_TEMPLATE:
        HTML_TEMPLATE = HTML_TEMPLATE.replace("</body>", f"{FOOTER_SNIPPET}</body>")
# --- BACKEND MULTI-USER SYSTEM ENDPOINTS ---
@app.route('/')
def home():
    notes_file = get_user_scoped_filename("notes")
    notes_data = load_data(notes_file, default_val={"task": "", "expense": ""})
    return render_template_string(HTML_TEMPLATE, config=get_config(), notes=notes_data)

@app.route('/api/auth/gateway', methods=['POST'])
def handle_multiuser_auth():
    data = request.json
    action = data.get('action')
    registry = load_global_registry()

    if action == 'logout':
        session.clear()
        return jsonify({"status": "success"})
    
    elif action == 'google':
        # Simulated profile payload injection matching a seamless single sign-on experience
        session['user_email'] = "google_user@gmail.com"
        session['user_name'] = "Google Integrated Explorer"
        return jsonify({"status": "success"})

    elif action == 'register':
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        if email in registry:
            return jsonify({"status": "error", "message": "Email address already linked to a registered profile!"})
        
        registry[email] = {"name": name, "password": password}
        save_global_registry(registry)
        
        session['user_email'] = email
        session['user_name'] = name
        return jsonify({"status": "success"})

    elif action == 'login':
        email = data.get('email')
        password = data.get('password')
        
        if email not in registry or registry[email]['password'] != password:
            return jsonify({"status": "error", "message": "Invalid password or profile email vector matching error!"})
        
        session['user_email'] = email
        session['user_name'] = registry[email]['name']
        return jsonify({"status": "success"})

    return jsonify({"status": "error", "message": "Invalid operations directive context."})

@app.route('/api/config', methods=['POST'])
def save_config_route():
    config = get_config()
    config['api_key'] = request.json.get('api_key', '')
    save_config(config)
    return jsonify({"status": "success"})

@app.route('/api/todos', methods=['GET', 'POST'])
def handle_todos():
    todo_file = get_user_scoped_filename("todo")
    todos = load_data(todo_file)
    if request.method == 'POST':
        todos.append({"title": request.json.get('title'), "completed": False})
        save_data(todo_file, todos)
    return jsonify(todos)

@app.route('/api/todos/toggle/<int:index>', methods=['POST'])
def toggle_todo(index):
    todo_file = get_user_scoped_filename("todo")
    todos = load_data(todo_file)
    if 0 <= index < len(todos):
        todos[index]['completed'] = not todos[index]['completed']
        save_data(todo_file, todos)
    return jsonify({"status": "success"})

@app.route('/api/todos/<int:index>', methods=['DELETE'])
def delete_todo(index):
    todo_file = get_user_scoped_filename("todo")
    todos = load_data(todo_file)
    if 0 <= index < len(todos):
        todos.pop(index)
        save_data(todo_file, todos)
    return jsonify({"status": "success"})

@app.route('/api/expenses', methods=['GET', 'POST'])
def handle_expenses():
    expense_file = get_user_scoped_filename("expense")
    expenses = load_data(expense_file)
    if request.method == 'POST':
        expenses.append({
            "amount": float(request.json.get('amount', 0)),
            "category": request.json.get('category'),
            "description": request.json.get('description', '')
        })
        save_data(expense_file, expenses)
    return jsonify(expenses)

@app.route('/api/expenses/<int:index>', methods=['DELETE'])
def delete_expense(index):
    expense_file = get_user_scoped_filename("expense")
    expenses = load_data(expense_file)
    if 0 <= index < len(expenses):
        expenses.pop(index)
        save_data(expense_file, expenses)
    return jsonify({"status": "success"})

@app.route('/api/edit/<string:type_>/<int:index>', methods=['PUT'])
def edit_entry(type_, index):
    if type_ == 'todo':
        todo_file = get_user_scoped_filename("todo")
        todos = load_data(todo_file)
        if 0 <= index < len(todos):
            todos[index]['title'] = request.json.get('title')
            save_data(todo_file, todos)
    elif type_ == 'expense':
        expense_file = get_user_scoped_filename("expense")
        expenses = load_data(expense_file)
        if 0 <= index < len(expenses):
            expenses[index]['amount'] = float(request.json.get('amount'))
            expenses[index]['category'] = request.json.get('category')
            expenses[index]['description'] = request.json.get('description')
            save_data(expense_file, expenses)
    return jsonify({"status": "success"})

@app.route('/api/notes', methods=['POST'])
def handle_notes():
    notes_file = get_user_scoped_filename("notes")
    notes_data = load_data(notes_file, default_val={"task": "", "expense": ""})
    note_type = request.json.get('type')
    content = request.json.get('content', '')
    if note_type in ['task', 'expense']:
        notes_data[note_type] = content
        save_data(notes_file, notes_data)
    return jsonify({"status": "success"})

@app.route('/api/utility', methods=['POST'])
def external_utility():
    import urllib.request
    import json
    
    req_payload = request.json
    mode = req_payload.get('mode')
    user_query = req_payload.get('user_query', '')
    
    cfg = get_config()
    api_key = cfg.get('api_key', '').strip()
    
    todo_file = get_user_scoped_filename("todo")
    expense_file = get_user_scoped_filename("expense")
    notes_file = get_user_scoped_filename("notes")
    
    todos = load_data(todo_file)
    expenses = load_data(expense_file)
    notes_data = load_data(notes_file, default_val={"task": "", "expense": ""})
    
    total_spent = sum(float(e['amount']) for e in expenses)
    pending_tasks = [t['title'] for t in todos if not t['completed']]
    completed_tasks = [t['title'] for t in todos if t['completed']]
    
    if not api_key:
        return jsonify({"result": "❌ <strong>System Warning:</strong> API authentication token required. Paste your API Key in header navigation frame above."})
    
    base_context = f"""
    Current Dashboard Data state:
    - Logged Expenses Total: {total_spent:.2f}
    - Log Matrix Entries: {[{'category': e['category'], 'amount': e['amount'], 'desc': e['description']} for e in expenses]}
    - Pending Tasks Items: {pending_tasks}
    - Finished Tasks Items: {completed_tasks}
    - User's Extra Task Pad Notes: "{notes_data.get('task', '')}"
    - User's Extra Expense Budget Notes: "{notes_data.get('expense', '')}"
    """
    
    if mode == 'blueprint':
        prompt = base_context + "\\nAction Directive: Formulate a breakdown and clear budgetary risk profile map based on the active expenses logs and financial notes."
    elif mode == 'tasks':
        prompt = base_context + "\\nAction Directive: Structure a clear prioritize order strategy map detailing how to address the pending workflow items and tasks notes efficiently."
    else:
        prompt = base_context + f"\\nUser Query: '{user_query}'\\nAction Directive: Respond to the user's specific query directly and naturally using the data context if applicable."

    # --- CLOUD API TUNNEL EXECUTION ---
    if api_key.startswith("sk-"):
        try:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            data = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant. Provide direct answers to questions without unnecessary roleplay references."},
                    {"role": "user", "content": prompt}
                ]
            }
            req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
            with urllib.request.urlopen(req) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                return jsonify({"result": res_data['choices'][0]['message']['content'].replace('\\n', '<br>')})
        except Exception as e:
            return jsonify({"result": f"❌ <strong>OpenAI Interface Error:</strong> {str(e)}"})
    else:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
            headers = {"Content-Type": "application/json"}
            data = {"contents": [{"parts": [{"text": prompt}]}]}
            
            req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
            with urllib.request.urlopen(req) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                markdown_text = res_data['candidates'][0]['content']['parts'][0]['text']
                html_text = markdown_text.replace('**', '<strong>').replace('*', '✨').replace('\\n', '<br>')
                return jsonify({"result": html_text})
                
        except urllib.error.HTTPError as e:
            if e.code == 429:
                return jsonify({"result": "⏳ <strong>Gemini Rate Limit:</strong> Free tier limit reached. Please pause for 10-15 seconds and try again! 💜"})
            else:
                return jsonify({"result": f"❌ <strong>Gemini Server Error ({e.code}):</strong> {e.reason}"})
        except Exception as e:
            return jsonify({"result": f"❌ <strong>Gemini Interface Error:</strong> {str(e)}"})

def launch_chrome():
    webbrowser.open("http://127.0.0.1:5010/")

if __name__ == '__main__':
    Timer(1, launch_chrome).start()
    app.run(port=5010, debug=False)
