/* ========================================
   ФИЛЬТРАЦИЯ ОБЪЯВЛЕНИЙ
   ======================================== */

document.addEventListener('DOMContentLoaded', function() {

    // Поиск по объявлениям
    const searchInput = document.querySelector('#search-input');
    const searchButton = document.querySelector('#search-btn');

    function performSearch() {
        if (searchInput) {
            const query = searchInput.value.trim();
            const currentUrl = new URL(window.location.href);
            if (query) {
                currentUrl.searchParams.set('search', query);
            } else {
                currentUrl.searchParams.delete('search');
            }
            window.location.href = currentUrl.toString();
        }
    }

    if (searchButton) {
        searchButton.addEventListener('click', performSearch);
    }

    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
    }

    // Сортировка
    const sortSelect = document.querySelector('#sort-select');
    if (sortSelect) {
        sortSelect.addEventListener('change', function() {
            const currentUrl = new URL(window.location.href);
            currentUrl.searchParams.set('sort', this.value);
            window.location.href = currentUrl.toString();
        });
    }
});