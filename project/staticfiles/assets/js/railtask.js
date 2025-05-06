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
