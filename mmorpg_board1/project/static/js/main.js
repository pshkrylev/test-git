/* ========================================
   MMORPG BOARD - ОСНОВНОЙ JS
   ======================================== */

// Ждём загрузки DOM
document.addEventListener('DOMContentLoaded', function() {

    // Автоматическое скрытие сообщений через 5 секунд
    const messages = document.querySelectorAll('.alert');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => {
                if (message.parentNode) {
                    message.remove();
                }
            }, 300);
        }, 5000);
    });

    // Подтверждение удаления
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (!confirm('Вы уверены, что хотите удалить?')) {
                e.preventDefault();
            }
        });
    });

    // Подсветка активной категории
    const currentUrl = window.location.href;
    const categoryLinks = document.querySelectorAll('.category-list a');
    categoryLinks.forEach(link => {
        if (link.href === currentUrl) {
            link.classList.add('active');
        }
    });

    // Счётчик символов в тексте
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        const maxLength = textarea.getAttribute('maxlength');
        if (maxLength) {
            const counter = document.createElement('small');
            counter.style.display = 'block';
            counter.style.textAlign = 'right';
            counter.style.color = '#718096';
            counter.style.marginTop = '5px';
            counter.innerHTML = `0 / ${maxLength}`;
            textarea.parentNode.insertBefore(counter, textarea.nextSibling);

            textarea.addEventListener('input', function() {
                const remaining = this.value.length;
                counter.innerHTML = `${remaining} / ${maxLength}`;

                if (remaining > maxLength * 0.9) {
                    counter.style.color = '#e53e3e';
                } else {
                    counter.style.color = '#718096';
                }
            });

            textarea.dispatchEvent(new Event('input'));
        }
    });

    // Переключение видимости пароля
    const passwordFields = document.querySelectorAll('input[type="password"]');
    passwordFields.forEach(field => {
        const toggle = document.createElement('button');
        toggle.type = 'button';
        toggle.innerHTML = '👁️';
        toggle.style.position = 'absolute';
        toggle.style.right = '10px';
        toggle.style.top = '50%';
        toggle.style.transform = 'translateY(-50%)';
        toggle.style.background = 'none';
        toggle.style.border = 'none';
        toggle.style.cursor = 'pointer';

        const wrapper = document.createElement('div');
        wrapper.style.position = 'relative';
        field.parentNode.insertBefore(wrapper, field);
        wrapper.appendChild(field);
        wrapper.appendChild(toggle);

        toggle.addEventListener('click', function() {
            const type = field.getAttribute('type') === 'password' ? 'text' : 'password';
            field.setAttribute('type', type);
            toggle.innerHTML = type === 'password' ? '👁️' : '🙈';
        });
    });
});