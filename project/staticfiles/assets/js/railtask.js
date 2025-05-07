// Update task status

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.complete-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', function () {
            const status = this.checked ? 'completed' : 'in_progress';
            const taskId = this.dataset.id;
            const url = `/tasks/update-status/${taskId}?status=${status}`;

            fetch(url)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Serverdan xatolik qaytdi');
                    }
                    return response.json();
                })
                .then(data => {
                    console.log(`Vazifa holati: ${data.status}`);
                })
                .catch(error => {
                    console.error('Xatolik:', error);
                    alert('Vazifa holatini yangilashda muammo yuz berdi');
                });
        });
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const editButtons = document.querySelectorAll('.edit-task');
    editButtons.forEach(function (btn) {
        btn.addEventListener('click', function () {
            const taskId = this.getAttribute('data-id');
            fetch(`/tasks/${taskId}/`)
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    // Formani to'ldirish
                    document.getElementById('editTaskName').value = data.title;
                    document.getElementById('editTaskDescription').value = data.description;
                    document.getElementById('editTaskDeadline').value = data.deadline;

                    // Muhimlik darajasi
                    document.getElementById("editTaskDegree").value = data.degree;

                    // Ijrochilar
                    const performersSelect = document.getElementById('editTaskPerformers');
                    [...performersSelect.options].forEach(opt => {
                        opt.selected = data.performers.includes(parseInt(opt.value));
                    });

                    // Forma action-ni o'zgartirish
                    document.querySelector('#editTasks form').action = `/tasks/edit/${taskId}/`;
                })
                .catch(error => {
                    console.error('Xatolik:', error);
                });
        });
    });
});
