from app import db, create_app

# Создаём экземпляр приложения
app = create_app()

# Устанавливаем контекст приложения и создаём базу данных
with app.app_context():
    db.create_all()

print("База данных успешно создана!")
