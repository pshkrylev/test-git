/* ========================================
   СКРИПТЫ ДЛЯ РАБОТЫ С ОТКЛИКАМИ
   ======================================== */

document.addEventListener('DOMContentLoaded', function() {

    // Фильтр откликов без перезагрузки
    const filterSelect = document.querySelector('#response-filter');
    if (filterSelect) {
        filterSelect.addEventListener('change', function() {
            const postId = this.value;
            if (postId) {
                window.location.href = `/responses/my/?post=${postId}`;
            } else {
                window.location.href = '/responses/my/';
            }
        });
    }

    // Подтверждение принятия отклика
    const acceptButtons = document.querySelectorAll('.btn-accept');
    acceptButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (!confirm('Принять этот отклик? После принятия автор получит уведомление.')) {
                e.preventDefault();
            }
        });
    });

    // Подтверждение удаления отклика
    const deleteResponseButtons = document.querySelectorAll('.btn-delete-response');
    deleteResponseButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (!confirm('Удалить этот отклик? Это действие нельзя отменить.')) {
                e.preventDefault();
            }
        });
    });

    // Анимация для новых откликов
    const newResponses = document.querySelectorAll('.response-new');
    newResponses.forEach(response => {
        response.style.animation = 'fadeIn 0.5s ease-out';
        setTimeout(() => {
            response.classList.remove('response-new');
        }, 500);
    });
});