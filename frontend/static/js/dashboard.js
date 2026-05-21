async function loadDashboard() {
    const res = await apiFetch('/dashboard/');
    if (!res) return;

    const data = await res.json();

    document.getElementById('total-tasks').textContent = data.total_tasks;
    document.getElementById('todo-tasks').textContent = data.todo;
    document.getElementById('inprogress-tasks').textContent = data.in_progress;
    document.getElementById('done-tasks').textContent = data.done;
    document.getElementById('overdue-tasks').textContent = data.overdue;
    document.getElementById('total-projects').textContent = data.total_projects;

    const tbody = document.getElementById('recent-tasks-body');
    if (data.recent_tasks.length === 0) {
        tbody.innerHTML = `<tr><td colspan="4" class="empty-state">No tasks yet</td></tr>`;
        return;
    }

    tbody.innerHTML = data.recent_tasks.map(task => `
        <tr>
            <td>${task.title}</td>
            <td><span class="badge badge-${task.status}">${task.status.replace('_', ' ')}</span></td>
            <td><span class="badge badge-${task.priority}">${task.priority}</span></td>
            <td class="${isOverdue(task.deadline, task.status) ? 'badge-overdue' : ''}">
                ${formatDate(task.deadline)}
                ${isOverdue(task.deadline, task.status) ? ' ⚠️' : ''}
            </td>
        </tr>
    `).join('');
}

document.addEventListener('DOMContentLoaded', loadDashboard);