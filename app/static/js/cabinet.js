// Дата
document.addEventListener('DOMContentLoaded', () => {
    const datetimeInput = document.getElementById('datetime');
    const now = new Date();
    const localDatetime = now.toISOString().slice(0, 16); // Формат для datetime-local
    datetimeInput.setAttribute('min', localDatetime);
});

// Автоматичне встановлення дати на день вперед
document.addEventListener('DOMContentLoaded', () => {
    const datetimeInput = document.getElementById('datetime');
    if (datetimeInput) {
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1); // Наступний день
        const isoString = tomorrow.toISOString();
        datetimeInput.value = isoString.slice(0, 16); // Формат YYYY-MM-DDTHH:mm
    }
});


// Завантаження лікарів
document.addEventListener('DOMContentLoaded', function () {
    fetch('/get-doctors')
        .then(response => response.json())
        .then(doctors => {
            const doctorSelect = document.getElementById('doctor');
            const doctorSelectEdit = document.getElementById('doctor-edit');

            // Додаємо лікарів до обох випадаючих списків
            doctors.forEach(doctor => {
                // Для першого списку
                const option1 = document.createElement('option');
                option1.value = doctor.id;
                option1.textContent = doctor.full_name;
                doctorSelect.appendChild(option1);

                // Для другого списку
                const option2 = document.createElement('option');
                option2.value = doctor.id;
                option2.textContent = doctor.full_name;
                doctorSelectEdit.appendChild(option2);
            });
        })
        .catch(error => console.error('Помилка завантаження лікарів:', error));
});

// Завантаження клінік
document.addEventListener('DOMContentLoaded', function () {
    fetch('/get-clinics')
        .then(response => response.json())
        .then(clinics => {
            const clinicSelect = document.getElementById('clinica');
            const clinicSelectEdit = document.getElementById('clinic-edit');

            clinics.forEach(clinic => {
                // Створюємо окремі <option> для кожного списку
                const option1 = document.createElement('option');
                option1.value = clinic.id;
                option1.textContent = clinic.name;
                clinicSelect.appendChild(option1);

                const option2 = document.createElement('option');
                option2.value = clinic.id;
                option2.textContent = clinic.name;
                clinicSelectEdit.appendChild(option2);
            });
        })
        .catch(error => console.error('Помилка завантаження клінік:', error));
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


// Редактування запису
document.addEventListener('DOMContentLoaded', () => {
    const editButtons = document.querySelectorAll('.edit-btn');
    const editModal = document.getElementById('editModal');
    const closeModal = document.getElementById('closeModal');
    const editForm = document.getElementById('editForm');
    const cancelBtn = document.getElementById('cancelBtn');

    const datetimeInput = document.getElementById('datetime-edit');
    const doctorSelect = document.getElementById('doctor-edit');
    const clinicSelect = document.getElementById('clinic-edit');

    // Відкриття модального вікна
    editButtons.forEach(button => {
        button.addEventListener('click', () => {
            const appointmentId = button.getAttribute('data-id');
            const appointmentDatetime = button.getAttribute('data-datetime-edit');
            const appointmentDoctor = button.getAttribute('data-doctor-edit');
            const appointmentClinic = button.getAttribute('data-clinic-edit');

            // Заповнення форми
            editForm.setAttribute('data-appointment-id', appointmentId);
            datetimeInput.value = appointmentDatetime;

            // Встановлення лікаря
            Array.from(doctorSelect.options).forEach(option => {
                option.selected = option.textContent === appointmentDoctor;
            });

            // Встановлення клініки
            Array.from(clinicSelect.options).forEach(option => {
                option.selected = option.textContent === appointmentClinic;
            });

            // Показати модальне вікно
            editModal.style.display = 'block';
        });
    });

    // Закриття модального вікна
    const closeModalWindow = () => {
        editModal.style.display = 'none';
    };

    closeModal.addEventListener('click', closeModalWindow);

    // Закриття модального вікна при кліку за межі контенту
    window.addEventListener('click', (e) => {
        if (e.target === editModal) {
            closeModalWindow();
        }
    });

    // Обробка кнопки "Скасувати"
    cancelBtn.addEventListener('click', () => {
        closeModalWindow();
    });

    // Обробка кнопки "Зберегти зміни"
    editForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const appointmentId = editForm.getAttribute('data-appointment-id');
        const datetime = datetimeInput.value;
        const doctorId = doctorSelect.value;
        const clinicId = clinicSelect.value;

        try {
            const response = await fetch(`/cabinet/edit-appointment/${appointmentId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    date: datetime,
                    doctor: doctorId,
                    clinic: clinicId,
                }),
            });

            const result = await response.json(); // Викликаємо тільки один раз

            if (response.ok) {
                const updatedAppointment = result.data;

                // Знаходимо всі елементи, які потрібно оновити
                const editButton = document.querySelector(`.edit-btn[data-id='${updatedAppointment.id}']`);
                if (editButton) {
                    // Оновлення дати в кнопці редагування
                    editButton.setAttribute('data-datetime-edit', updatedAppointment.date);
                    editButton.setAttribute('data-doctor-edit', updatedAppointment.doctor);
                    editButton.setAttribute('data-clinic-edit', updatedAppointment.clinic);

                    // Оновлення інформації у відповідному блоці
                    const appointmentInfo = editButton.closest('.appointment-card').querySelector('.appointment-info');
                    if (appointmentInfo) {
                        const infoElements = appointmentInfo.querySelectorAll('p');
                        if (infoElements.length >= 4) {
                            // Оновлюємо дані: назва, дата, лікар, клініка
                            infoElements[1].textContent = new Date(updatedAppointment.date).toLocaleString();
                            infoElements[2].textContent = `Лікар: ${updatedAppointment.doctor}`;
                            infoElements[3].textContent = `Клініка: ${updatedAppointment.clinic}`;
                        }
                    }
                }

                // Закриваємо модальне вікно
                editModal.style.display = 'none';
                alert(result.message);
            } else {
                alert(result.message || 'Помилка при збереженні даних.');
            }
        } catch (error) {
            console.error('Помилка:', error);
            alert('Сталася помилка при збереженні даних.');
        }
    });
});


// Відкриття модального вікна
document.addEventListener('DOMContentLoaded', () => {
    const editModal = document.getElementById('editModal');
    const closeModalBtn = document.getElementById('closeModal');
    const editForm = document.getElementById('editForm');

    // Перевірка, чи кнопки доступні
    const editButtons = document.querySelectorAll('.edit-btn');
    if (!editButtons.length) {
        console.error('Кнопки для редагування записів не знайдено.');
        return;
    }

    // Функція для відкриття модального вікна
    function openEditModal(event) {
        const button = event.target; // Кнопка, на яку натиснули
        const appointmentId = button.getAttribute('data-appointment-id');
        const date = button.getAttribute('data-datetime-edit');
        const doctor = button.getAttribute('data-doctor-edit');
        const clinic = button.getAttribute('data-clinic-edit');

        if (!appointmentId || !date || !doctor || !clinic) {
            console.error('Немає даних для редагування.');
            return;
        }

        // Заповнення форми
        editForm.dataset.appointmentId = appointmentId;
        editForm.querySelector('#datetime-edit').value = date;

        const doctorOptions = editForm.querySelector('#doctor-edit').options;
        for (let option of doctorOptions) {
            option.selected = option.textContent === doctor;
        }

        const clinicOptions = editForm.querySelector('#clinic-edit').options;
        for (let option of clinicOptions) {
            option.selected = option.textContent === clinic;
        }

        // Відображення модального вікна
        editModal.style.display = 'block';
    }

    // Закриття модального вікна
    function closeEditModal() {
        editModal.style.display = 'none';
    }

    // Додаємо обробники подій
    editButtons.forEach(button => {
        button.addEventListener('click', openEditModal);
    });

    closeModalBtn.addEventListener('click', closeEditModal);

    // Закриття модального вікна при кліку поза ним
    window.addEventListener('click', (event) => {
        if (event.target === editModal) {
            closeEditModal();
        }
    });
});
