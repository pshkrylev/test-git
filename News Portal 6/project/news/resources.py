# 1. Создание двух пользователей
user1 = User.objects.create_user('john_doe')
user2 = User.objects.create_user('jane_smith')

# 2. Создание двух объектов Author, связанных с пользователями
author1 = Author.objects.create(user=user1, rating=0)
author2 = Author.objects.create(user=user2, rating=0)

# 3. Добавление 4 категорий в модель Category
category1 = Category.objects.create(name='Спорт')
category2 = Category.objects.create(name='Политика')
category3 = Category.objects.create(name='Образование')
category4 = Category.objects.create(name='Технологии')

# 4. Добавление 2 статей и 1 новости
post1 = Post.objects.create(
    author=author1,
    type='article',
    title='Основы Python для начинающих',
    text='Python - это высокоуровневый язык программирования с динамической типизацией...',
    rating=0
)

post2 = Post.objects.create(
    author=author2,
    type='article',
    title='Искусственный интеллект в образовании',
    text='Применение AI в современных образовательных процессах открывает новые возможности...',
    rating=0
)

post3 = Post.objects.create(
    author=author1,
    type='news',
    title='Новая версия Django 5.0',
    text='Вышла новая версия популярного веб-фреймворка Django 5.0 с множеством улучшений...',
    rating=0
)

# 5. Присвоение категорий
PostCategory.objects.create(post=post1, category=category3)  # Образование
PostCategory.objects.create(post=post1, category=category4)  # Технологии (2 категории)

PostCategory.objects.create(post=post2, category=category3)  # Образование
PostCategory.objects.create(post=post2, category=category1)  # Спорт

PostCategory.objects.create(post=post3, category=category4)  # Технологии

# 6. Создание как минимум 4 комментариев
comment1 = Comment.objects.create(
    post=post1,
    user=user1,
    text='Отличная статья для новичков!',
    rating=0
)

comment2 = Comment.objects.create(
    post=post1,
    user=user2,
    text='Спасибо, очень полезно!',
    rating=0
)

comment3 = Comment.objects.create(
    post=post2,
    user=user1,
    text='Интересная тема, хотелось бы больше деталей',
    rating=0
)

comment4 = Comment.objects.create(
    post=post3,
    user=user2,
    text='Ура, давно ждал эту новость!',
    rating=0
)

# 7. Применение like() и dislike() для корректировки рейтингов
# Лайки/дизлайки к статьям/новостям
post1.like()   # +1
post1.like()   # +1
post1.dislike()  # -1 (итого: рейтинг = 1)

post2.like()   # +1
post2.like()   # +1
post2.like()   # +1 (итого: рейтинг = 3)

post3.like()   # +1
post3.dislike()  # -1 (итого: рейтинг = 0)

# Лайки/дизлайки к комментариям
comment1.like()   # +1
comment1.like()   # +1
comment1.dislike()  # -1 (итого: рейтинг = 1)

comment2.like()   # +1
comment2.like()   # +1 (итого: рейтинг = 2)

comment3.like()   # +1
comment3.dislike()  # -1 (итого: рейтинг = 0)

comment4.like()   # +1
comment4.like()   # +1
comment4.like()   # +1 (итого: рейтинг = 3)

# 8. Обновление рейтингов авторов
author1.update_rating()
author2.update_rating()

# 9. Вывод username и рейтинга лучшего пользователя
best_author = Author.objects.order_by('-rating').first()
print(f"Лучший пользователь: {best_author.user.username}, рейтинг: {best_author.rating}")

# 10. Вывод информации о лучшей статье (по рейтингу)
best_post = Post.objects.order_by('-rating').first()
print(f"\nЛучшая статья:")
print(f"Дата добавления: {best_post.created_at}")
print(f"Автор: {best_post.author.user.username}")
print(f"Рейтинг: {best_post.rating}")
print(f"Заголовок: {best_post.title}")
print(f"Превью: {best_post.preview()}")

# 11. Вывод всех комментариев к лучшей статье
print(f"\nКомментарии к статье '{best_post.title}':")
comments = Comment.objects.filter(post=best_post).order_by('-created_at')
for comment in comments:
    print(f"Дата: {comment.created_at}")
    print(f"Пользователь: {comment.user.username}")
    print(f"Рейтинг: {comment.rating}")
    print(f"Текст: {comment.text}")
    print("-" * 40)

# Дополнительные проверки
print(f"\nСтатистика:")
print(f"Авторы: {Author.objects.count()}")
print(f"Категории: {Category.objects.count()}")
print(f"Посты: {Post.objects.count()}")
print(f"Комментарии: {Comment.objects.count()}")