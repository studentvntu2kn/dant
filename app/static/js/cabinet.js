// Дата
document.addEventListener('DOMContentLoaded', () => {
    const datetimeInput = document.getElementById('datetime');
    const now = new Date();
    const localDatetime = now.toISOString().slice(0, 16); // Формат для datetime-local
    datetimeInput.setAttribute('min', localDatetime);
});

// Переключення кнопок сповіщення
document.querySelectorAll('.toggle-btn').forEach(button => {
    button.addEventListener('click', async () => {
        const notificationType = button.getAttribute('data-type');
        const currentStatus = button.getAttribute('data-status');
        const newStatus = currentStatus === 'enabled' ? 'disabled' : 'enabled';

        // Оновлення класів кнопки на фронтенді до відповіді сервера
        button.setAttribute('data-status', newStatus);
        button.textContent = newStatus === 'enabled' ? 'Включено' : 'Виключено';

        if (newStatus === 'enabled') {
            button.classList.remove('disabled');
            button.classList.add('enabled');
        } else {
            button.classList.remove('enabled');
            button.classList.add('disabled');
        }

        try {
            const response = await fetch(`/cabinet/toggle-notification`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ type: notificationType, status: newStatus })
            });

            const data = await response.json();
            if (!data.success) {
                // Якщо сервер повертає помилку, скасуємо локальні зміни
                button.setAttribute('data-status', currentStatus);
                button.textContent = currentStatus === 'enabled' ? 'Включено' : 'Виключено';

                if (currentStatus === 'enabled') {
                    button.classList.remove('disabled');
                    button.classList.add('enabled');
                } else {
                    button.classList.remove('enabled');
                    button.classList.add('disabled');
                }

                alert('Помилка: ' + data.message);
            }
        } catch (error) {
            // Якщо виникла помилка, скасувати локальні зміни
            button.setAttribute('data-status', currentStatus);
            button.textContent = currentStatus === 'enabled' ? 'Включено' : 'Виключено';

            if (currentStatus === 'enabled') {
                button.classList.remove('disabled');
                button.classList.add('enabled');
            } else {
                button.classList.remove('enabled');
                button.classList.add('disabled');
            }

            console.error('Помилка запиту:', error);
        }
    });
});

// Модальне вікно
const openModalBtn = document.getElementById('openEditModal');
const closeModalBtn = document.getElementById('closeModal');
const modal = document.getElementById('editModal');

// Відкриття модального вікна
openModalBtn.addEventListener('click', () => {
    modal.style.display = 'block';
});

// Закриття модального вікна
closeModalBtn.addEventListener('click', () => {
    modal.style.display = 'none';
});

// Закриття модального вікна при кліку поза його межами
window.addEventListener('click', (event) => {
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});

