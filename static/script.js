const API_BASE = '';

// Управление вкладками
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const tab = btn.dataset.tab;
        
        // Убираем активный класс у всех кнопок и контента
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        
        // Добавляем активный класс выбранным элементам
        btn.classList.add('active');
        document.getElementById(tab).classList.add('active');
        
        // Загружаем данные для выбранной вкладки
        loadTabData(tab);
    });
});

// Загрузка данных для вкладки
function loadTabData(tab) {
    switch(tab) {
        case 'students':
            loadStudents();
            break;
        case 'teachers':
            loadTeachers();
            break;
        case 'schedule':
            loadSchedule();
            break;
        case 'grades':
            loadGrades();
            break;
        case 'retakes':
            loadRetakes();
            break;
        case 'payments':
            loadPayments();
            break;
        case 'instructions':
            loadInstructions();
            break;
    }
}

// Утилиты
function showLoading() {
    document.getElementById('loading').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loading').classList.add('hidden');
}

function showError(message) {
    const errorDiv = document.getElementById('error-message');
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
    setTimeout(() => {
        errorDiv.classList.add('hidden');
    }, 5000);
}

async function fetchAPI(url) {
    try {
        showLoading();
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        return await response.json();
    } catch (error) {
        showError(`Ошибка: ${error.message}`);
        throw error;
    } finally {
        hideLoading();
    }
}

// Загрузка студентов
async function loadStudents() {
    try {
        const data = await fetchAPI(`${API_BASE}/students`);
        renderList('students-list', data, (student) => `
            <div class="data-card">
                <h3>${student.first_name} ${student.last_name}</h3>
                <div class="field">
                    <span class="field-label">ID:</span>
                    <span class="field-value">${student.id}</span>
                </div>
                <div class="field">
                    <span class="field-label">Группа:</span>
                    <span class="field-value">${student.group}</span>
                </div>
                <div class="field">
                    <span class="field-label">Факультет:</span>
                    <span class="field-value">${student.faculty}</span>
                </div>
                <div class="field">
                    <span class="field-label">Email:</span>
                    <span class="field-value">${student.email}</span>
                </div>
                <div class="field">
                    <span class="field-label">Баланс:</span>
                    <span class="field-value">${student.balance} ₽</span>
                </div>
            </div>
        `);
    } catch (error) {
        document.getElementById('students-list').innerHTML = '<div class="empty-state">Не удалось загрузить данные</div>';
    }
}

// Загрузка преподавателей
async function loadTeachers() {
    try {
        const data = await fetchAPI(`${API_BASE}/teachers`);
        renderList('teachers-list', data, (teacher) => `
            <div class="data-card">
                <h3>${teacher.first_name} ${teacher.last_name}</h3>
                <div class="field">
                    <span class="field-label">ID:</span>
                    <span class="field-value">${teacher.id}</span>
                </div>
                <div class="field">
                    <span class="field-label">Должность:</span>
                    <span class="field-value">${teacher.position}</span>
                </div>
                <div class="field">
                    <span class="field-label">Кафедра:</span>
                    <span class="field-value">${teacher.department}</span>
                </div>
                <div class="field">
                    <span class="field-label">Email:</span>
                    <span class="field-value">${teacher.email}</span>
                </div>
            </div>
        `);
    } catch (error) {
        document.getElementById('teachers-list').innerHTML = '<div class="empty-state">Не удалось загрузить данные</div>';
    }
}

// Загрузка расписания
async function loadSchedule() {
    try {
        const group = document.getElementById('schedule-group').value;
        const teacherId = document.getElementById('schedule-teacher').value;
        let url = `${API_BASE}/schedule`;
        const params = new URLSearchParams();
        if (group) params.append('group', group);
        if (teacherId) params.append('teacher_id', teacherId);
        if (params.toString()) url += '?' + params.toString();
        
        const data = await fetchAPI(url);
        renderList('schedule-list', data, (item) => `
            <div class="data-card">
                <h3>${item.subject || 'Предмет'}</h3>
                <div class="field">
                    <span class="field-label">Группа:</span>
                    <span class="field-value">${item.group || 'N/A'}</span>
                </div>
                <div class="field">
                    <span class="field-label">Преподаватель ID:</span>
                    <span class="field-value">${item.teacher_id || 'N/A'}</span>
                </div>
                <div class="field">
                    <span class="field-label">День/Время:</span>
                    <span class="field-value">${item.day || 'N/A'} ${item.time || ''}</span>
                </div>
            </div>
        `);
    } catch (error) {
        document.getElementById('schedule-list').innerHTML = '<div class="empty-state">Не удалось загрузить данные</div>';
    }
}

// Загрузка оценок
async function loadGrades() {
    try {
        const studentId = document.getElementById('grade-student').value;
        let url = `${API_BASE}/grade`;
        if (studentId) url += `?student_id=${studentId}`;
        
        const data = await fetchAPI(url);
        renderList('grades-list', data, (grade) => `
            <div class="data-card">
                <h3>Оценка #${grade.id}</h3>
                <div class="field">
                    <span class="field-label">Студент ID:</span>
                    <span class="field-value">${grade.student_id || 'N/A'}</span>
                </div>
                <div class="field">
                    <span class="field-label">Предмет:</span>
                    <span class="field-value">${grade.subject || 'N/A'}</span>
                </div>
                <div class="field">
                    <span class="field-label">Оценка:</span>
                    <span class="field-value"><strong>${grade.grade || 'N/A'}</strong></span>
                </div>
                <div class="field">
                    <span class="field-label">Дата:</span>
                    <span class="field-value">${grade.date || 'N/A'}</span>
                </div>
            </div>
        `);
    } catch (error) {
        document.getElementById('grades-list').innerHTML = '<div class="empty-state">Не удалось загрузить данные</div>';
    }
}

// Загрузка пересдач
async function loadRetakes() {
    try {
        const studentId = document.getElementById('retake-student').value;
        let url = `${API_BASE}/retake`;
        if (studentId) url += `?student_id=${studentId}`;
        
        const data = await fetchAPI(url);
        renderList('retakes-list', data, (retake) => `
            <div class="data-card">
                <h3>Пересдача #${retake.id}</h3>
                <div class="field">
                    <span class="field-label">Студент ID:</span>
                    <span class="field-value">${retake.student_id || 'N/A'}</span>
                </div>
                <div class="field">
                    <span class="field-label">Предмет:</span>
                    <span class="field-value">${retake.subject || 'N/A'}</span>
                </div>
                <div class="field">
                    <span class="field-label">Дата:</span>
                    <span class="field-value">${retake.date || 'N/A'}</span>
                </div>
                <div class="field">
                    <span class="field-label">Статус:</span>
                    <span class="field-value">${retake.status || 'N/A'}</span>
                </div>
            </div>
        `);
    } catch (error) {
        document.getElementById('retakes-list').innerHTML = '<div class="empty-state">Не удалось загрузить данные</div>';
    }
}

async function loadAllRetakes() {
    try {
        const data = await fetchAPI(`${API_BASE}/retake/all`);
        renderList('retakes-list', data, (retake) => `
            <div class="data-card">
                <h3>Пересдача #${retake.id}</h3>
                <div class="field">
                    <span class="field-label">Студент ID:</span>
                    <span class="field-value">${retake.student_id || 'N/A'}</span>
                </div>
                <div class="field">
                    <span class="field-label">Предмет:</span>
                    <span class="field-value">${retake.subject || 'N/A'}</span>
                </div>
                <div class="field">
                    <span class="field-label">Дата:</span>
                    <span class="field-value">${retake.date || 'N/A'}</span>
                </div>
                <div class="field">
                    <span class="field-label">Статус:</span>
                    <span class="field-value">${retake.status || 'N/A'}</span>
                </div>
            </div>
        `);
    } catch (error) {
        document.getElementById('retakes-list').innerHTML = '<div class="empty-state">Не удалось загрузить данные</div>';
    }
}

// Загрузка платежей
async function loadPayments() {
    try {
        const studentId = document.getElementById('payment-student').value;
        let url = `${API_BASE}/payment`;
        if (studentId) url += `?student_id=${studentId}`;
        
        const data = await fetchAPI(url);
        renderList('payments-list', data, (payment) => `
            <div class="data-card">
                <h3>Платеж #${payment.id}</h3>
                <div class="field">
                    <span class="field-label">Студент ID:</span>
                    <span class="field-value">${payment.student_id || 'N/A'}</span>
                </div>
                <div class="field">
                    <span class="field-label">Сумма:</span>
                    <span class="field-value"><strong>${payment.amount || 0} ₽</strong></span>
                </div>
                <div class="field">
                    <span class="field-label">Дата:</span>
                    <span class="field-value">${payment.date || 'N/A'}</span>
                </div>
                <div class="field">
                    <span class="field-label">Статус:</span>
                    <span class="field-value">${payment.status || 'N/A'}</span>
                </div>
            </div>
        `);
    } catch (error) {
        document.getElementById('payments-list').innerHTML = '<div class="empty-state">Не удалось загрузить данные</div>';
    }
}

// Загрузка инструкций
async function loadInstructions() {
    try {
        const data = await fetchAPI(`${API_BASE}/instruction`);
        renderList('instructions-list', data, (instruction) => `
            <div class="data-card">
                <h3>${instruction.title || 'Инструкция'}</h3>
                <div class="field">
                    <span class="field-label">ID:</span>
                    <span class="field-value">${instruction.id}</span>
                </div>
                <div class="field">
                    <span class="field-label">Описание:</span>
                    <span class="field-value">${instruction.description || 'N/A'}</span>
                </div>
                <div class="field">
                    <span class="field-label">Тип:</span>
                    <span class="field-value">${instruction.type || 'N/A'}</span>
                </div>
            </div>
        `);
    } catch (error) {
        document.getElementById('instructions-list').innerHTML = '<div class="empty-state">Не удалось загрузить данные</div>';
    }
}

// Рендер списка
function renderList(containerId, data, renderItem) {
    const container = document.getElementById(containerId);
    if (!data || data.length === 0) {
        container.innerHTML = '<div class="empty-state">Данные отсутствуют</div>';
        return;
    }
    container.innerHTML = data.map(renderItem).join('');
}

// Загрузка данных при открытии вкладки "Студенты"
document.addEventListener('DOMContentLoaded', () => {
    if (document.querySelector('.tab-btn.active')) {
        const activeTab = document.querySelector('.tab-btn.active').dataset.tab;
        loadTabData(activeTab);
    }
});
