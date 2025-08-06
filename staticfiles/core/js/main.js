// core/static/core/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    fetchCourses();
    fetchStatusUpdates();
    setupWebSocket(); // Настройка Web Sockets
});

function fetchCourses() {
    fetch('/api/courses/')
        .then(response => response.json())
        .then(courses => {
            const container = document.getElementById('courses-container');
            container.innerHTML = ''; // Очистка контейнера
            courses.forEach(course => {
                const courseElement = document.createElement('div');
                courseElement.classList.add('course-card');
                courseElement.innerHTML = `
                    <h3>${course.title}</h3>
                    <p>${course.description}</p>
                    <p>Преподаватель: ${course.teacher.user.username}</p>
                    <a href="/courses/${course.id}/">Подробнее</a>
                `;
                container.appendChild(courseElement);
            });
        })
        .catch(error => console.error('Ошибка при получении курсов:', error));
}

function fetchStatusUpdates() {
    fetch('/api/status-updates/')
        .then(response => response.json())
        .then(updates => {
            const container = document.getElementById('status-updates-container');
            container.innerHTML = '';
            updates.forEach(update => {
                const updateElement = document.createElement('div');
                updateElement.innerHTML = `
                    <p><strong>${update.user.username}</strong>: ${update.content}</p>
                `;
                container.appendChild(updateElement);
            });
        })
        .catch(error => console.error('Ошибка при получении статусов:', error));
}


function setupWebSocket() {
    const user = "{{ user.username }}"; 
    const ws_protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const socket = new WebSocket(
        ws_protocol + '://' + window.location.host + '/ws/notifications/' + user + '/'
    );

    socket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const message = data.message;
        
        // Отображение уведомления
        const notificationsContainer = document.getElementById('notifications-container');
        const notificationElement = document.createElement('p');
        notificationElement.textContent = `Новое уведомление: ${message}`;
        notificationsContainer.appendChild(notificationElement);
        
        console.log('Получено сообщение WebSocket:', message);
    };

    socket.onclose = function(e) {
        console.error('Socket закрыт неожиданно');
    };
}