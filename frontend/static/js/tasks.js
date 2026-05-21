let editingTaskId = null;
let updatingTaskId = null;

async function loadProjects() {
    const res = await apiFetch('/projects/');
    if (!res) return;
    const projects = await res.json();

    const filterSelect = document.getElementById('filter-project');
    const taskProjectSelect = document.getElementById('task-project');

    filterSelect.innerHTML = '<option value="">All Projects</option>' +
        projects.map(p => `<option value="${p.id}">${p.name}</option>`).join('');

    taskProjectSelect.innerHTML = '<option value="">Select Project</option>' +
        projects.map(p => `<option value="${p.id}">${p.name}</option>`).join('');

    return projects;
}

async function loadMembers() {
    const res = await apiFetch('/auth/users');
    if (!res) return;
    const users = await res.json();

    const assigneeSelect = document.getElementById('task-assignee');
    assigneeSelect.innerHTML = '<option value="">Unassigned</option>' +
        users.filter(u => u.role === 'member')
            .map(u => `<option value="${u.id}">${u.name}</option>`).join('');
}

async function loadTasks() {
    const projectId = document.getElementById('filter-project').value;
    const status = document.getElementById('filter-status').value;
    const priority = document.getElementById('filter-priority').value;

    let url = '/tasks/?';
    if (projectId) url += `project_id=${projectId}&`;

    const res = await apiFetch(url);
    if (!res) return;

    let tasks = await res.json();

    // Client side filtering
    if (status) tasks = tasks.filter(t => t.status === status);
    if (priority) tasks = tasks.filter(t => t.priority === priority);

    const tbody = document.getElementById('tasks-body');

    if (tasks.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" style="text-align:center;padding:32px;color:#64748b">No tasks found</td></tr>`;
        return;
    }

    tbody.innerHTML = tasks.map(task => {
        const overdue = isOverdue(task.deadline, task.status);
        return `
        <tr>
            <td>
                ${task.title}
                ${overdue ? '<span class="badge badge-overdue" style="margin-left:6px">Overdue</span>' : ''}
            </td>
            <td>${task.project_id}</td>
            <td>${task.assignee_name || '-'}</td>
            <td><span class="badge badge-${task.status}">${task.status.replace('_', ' ')}</span></td>
            <td><span class="badge badge-${task.priority}">${task.priority}</span></td>
            <td style="${overdue ? 'color:#dc2626;font-weight:600' : ''}">${formatDate(task.deadline)}</td>
            <td>
                <button class="btn btn-sm btn-outline" onclick="openStatusModal(${task.id}, '${task.status}')">Status</button>
                ${isAdmin() ? `
                    <button class="btn btn-sm btn-primary" onclick="openEditTask(${JSON.stringify(task).replace(/"/g, '&quot;')})">Edit</button>
                    <button class="btn btn-sm btn-danger" onclick="deleteTask(${task.id})">Delete</button>
                ` : ''}
            </td>
        </tr>
    `}).join('');
}

function openTaskModal() {
    editingTaskId = null;
    document.getElementById('task-modal-title').textContent = 'New Task';
    document.getElementById('task-title').value = '';
    document.getElementById('task-desc').value = '';
    document.getElementById('task-deadline').value = '';
    document.getElementById('task-error').textContent = '';
    document.getElementById('task-modal').style.display = 'flex';
}

function openEditTask(task) {
    editingTaskId = task.id;
    document.getElementById('task-modal-title').textContent = 'Edit Task';
    document.getElementById('task-title').value = task.title;
    document.getElementById('task-desc').value = task.description || '';
    document.getElementById('task-project').value = task.project_id;
    document.getElementById('task-assignee').value = task.assigned_to || '';
    document.getElementById('task-priority').value = task.priority;
    document.getElementById('task-deadline').value = task.deadline ? task.deadline.split('T')[0] : '';
    document.getElementById('task-error').textContent = '';
    document.getElementById('task-modal').style.display = 'flex';
}

function closeTaskModal() {
    document.getElementById('task-modal').style.display = 'none';
}

async function saveTask() {
    const title = document.getElementById('task-title').value.trim();
    const description = document.getElementById('task-desc').value.trim();
    const project_id = document.getElementById('task-project').value;
    const assigned_to = document.getElementById('task-assignee').value;
    const priority = document.getElementById('task-priority').value;
    const deadline = document.getElementById('task-deadline').value;
    const errorEl = document.getElementById('task-error');

    if (!title || !project_id) {
        errorEl.textContent = 'Title and project are required';
        return;
    }

    const body = {
        title, description, project_id: parseInt(project_id),
        assigned_to: assigned_to ? parseInt(assigned_to) : null,
        priority, deadline: deadline || null
    };

    const url = editingTaskId ? `/tasks/${editingTaskId}` : '/tasks/';
    const method = editingTaskId ? 'PUT' : 'POST';

    const res = await apiFetch(url, { method, body: JSON.stringify(body) });
    if (!res) return;

    const data = await res.json();
    if (!res.ok) {
        errorEl.textContent = data.error || 'Something went wrong';
        return;
    }

    closeTaskModal();
    loadTasks();
}

async function deleteTask(id) {
    if (!confirm('Delete this task?')) return;
    const res = await apiFetch(`/tasks/${id}`, { method: 'DELETE' });
    if (res && res.ok) loadTasks();
}

function openStatusModal(taskId, currentStatus) {
    updatingTaskId = taskId;
    document.getElementById('task-status').value = currentStatus;
    document.getElementById('status-modal').style.display = 'flex';
}

function closeStatusModal() {
    document.getElementById('status-modal').style.display = 'none';
}

async function updateStatus() {
    const status = document.getElementById('task-status').value;
    const res = await apiFetch(`/tasks/${updatingTaskId}`, {
        method: 'PUT',
        body: JSON.stringify({ status })
    });
    if (res && res.ok) {
        closeStatusModal();
        loadTasks();
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    await loadProjects();
    if (isAdmin()) {
        await loadMembers();
    }
    loadTasks();
});