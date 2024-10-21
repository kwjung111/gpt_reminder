// static/js/main.js

document.addEventListener('DOMContentLoaded', function() {
    // 완료 토글
    const toggleButtons = document.querySelectorAll('.toggle-complete');
    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const todoId = this.getAttribute('data-id');
            fetch(`/toggle_todo/${todoId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert('완료 상태를 변경할 수 없습니다.');
                }
            });
        });
    });

    // 삭제 버튼
    const deleteButtons = document.querySelectorAll('.delete-todo');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const todoId = this.getAttribute('data-id');
            if (confirm('정말 이 To-Do를 삭제하시겠습니까?')) {
                fetch(`/delete_todo/${todoId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        location.reload();
                    } else {
                        alert('삭제할 수 없습니다.');
                    }
                });
            }
        });
    });

    // 툴팁 초기화
    $('[data-toggle="tooltip"]').tooltip()
});
