let editingProjectId = null;
let selectedProjectId = null;

async function loadProjects() {
    const res = await apiFetch('/projects/');
    if (!res) return;

    const projects = await res.json();
    const grid = document.getElementById('projects-grid');

    if (projects.length === 0) {
        grid.innerHTML = `<div class="empty-state"><p>🗂️ No projects yet</p></div>`;
        return;
    }

    grid.innerHTML = projects.map(p => `
        <div class="project-card">
            <h3>${p.name}</h3>
            <p>${p.description || 'No description'}</p>
            <div class="project-meta">
                <span>📅 ${formatDate(p.deadline)}</span>
                <span>👥 ${p.members.length} members</span>
            </div>
            <div class="members-list">
                ${p.members.map(m => `<span class="member-tag">${m.name}</span>`).join('')}
            </div>
            <div class="project-actions" style="margin-top:12px">
                ${isAdmin() ? `
                    <button class="btn btn-sm btn-primary" onclick="openEditModal(${JSON.stringify(p).replace(/"/g, '&quot;')})">Edit</button>
                    <button class="btn btn-sm btn-outline" onclick="openAddMember(${p.id})">+ Member</button>
                    <button class="btn btn-sm btn-danger" onclick="deleteProject(${p.id})">Delete</button>
                ` : ''}
            </div>
        </div>
    `).join('');
}

function openProjectModal() {
    editingProjectId = null;
    document.getElementById('modal-title').textContent = 'New Project';
    document.getElementById('project-name').value = '';
    document.getElementById('project-desc').value = '';
    document.getElementById('project-deadline').value = '';
    document.getElementById('project-error').textContent = '';
    document.getElementById('project-modal').style.display = 'flex';
}

function openEditModal(project) {
    editingProjectId = project.id;
    document.getElementById('modal-title').textContent = 'Edit Project';
    document.getElementById('project-name').value = project.name;
    document.getElementById('project-desc').value = project.description || '';
    document.getElementById('project-deadline').value = project.deadline ? project.deadline.split('T')[0] : '';
    document.getElementById('project-error').textContent = '';
    document.getElementById('project-modal').style.display = 'flex';
}

function closeProjectModal() {
    document.getElementById('project-modal').style.display = 'none';
}

async function saveProject() {
    const name = document.getElementById('project-name').value.trim();
    const description = document.getElementById('project-desc').value.trim();
    const deadline = document.getElementById('project-deadline').value;
    const errorEl = document.getElementById('project-error');

    if (!name) {
        errorEl.textContent = 'Project name required';
        return;
    }

    const body = { name, description, deadline: deadline || null };
    const url = editingProjectId ? `/projects/${editingProjectId}` : '/projects/';
    const method = editingProjectId ? 'PUT' : 'POST';

    const res = await apiFetch(url, {
        method,
        body: JSON.stringify(body)
    });

    if (!res) return;
    const data = await res.json();

    if (!res.ok) {
        errorEl.textContent = data.error || 'Something went wrong';
        return;
    }

    closeProjectModal();
    loadProjects();
}

async function deleteProject(id) {
    if (!confirm('Delete this project? All tasks will be deleted too!')) return;

    const res = await apiFetch(`/projects/${id}`, { method: 'DELETE' });
    if (res && res.ok) loadProjects();
}

async function openAddMember(projectId) {
    selectedProjectId = projectId;

    // Load all users
    const res = await apiFetch('/auth/users');
    if (!res) return;
    const users = await res.json();

    const select = document.getElementById('member-select');
    select.innerHTML = users
        .filter(u => u.role === 'member')
        .map(u => `<option value="${u.id}">${u.name} (${u.email})</option>`)
        .join('');

    document.getElementById('member-error').textContent = '';
    document.getElementById('member-modal').style.display = 'flex';
}

function closeMemberModal() {
    document.getElementById('member-modal').style.display = 'none';
}

async function addMember() {
    const userId = document.getElementById('member-select').value;
    const errorEl = document.getElementById('member-error');

    const res = await apiFetch(`/projects/${selectedProjectId}/members`, {
        method: 'POST',
        body: JSON.stringify({ user_id: parseInt(userId) })
    });

    if (!res) return;
    const data = await res.json();

    if (!res.ok) {
        errorEl.textContent = data.error || 'Something went wrong';
        return;
    }

    closeMemberModal();
    loadProjects();
}

document.addEventListener('DOMContentLoaded', loadProjects);