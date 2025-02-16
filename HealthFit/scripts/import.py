import psycopg2
import csv

# Подключение к базе данных
conn = psycopg2.connect(
    dbname="HealthFitDB",
    user="postgres",
    password="kilona57",
    host="postgres",
    port="5432"
)
cur = conn.cursor()
context = cur.execute('select * from base_exercise')
if not context:

    # Открытие CSV-файла
    with open('data/base_mealgroups.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Пропуск заголовков
        for row in reader:
            cur.execute(
                "INSERT INTO base_mealgroups (id, group_name) VALUES (%s, %s)",
                row
            )
    with open('data/base_recipes.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Пропуск заголовков
        for row in reader:
            cur.execute(
                "INSERT INTO base_recipes (id, recipe_name, preparation_time, number_of_portions, weight_portion, kcal_per_100g, protein_per_100g, fat_per_100g, carb_per_100g, image, group_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                row
            )
    with open('data/base_ingredients.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Пропуск заголовков
        for row in reader:
            cur.execute(
                "INSERT INTO base_ingredients (id, ingredient_name, gramming, recipe_id) VALUES (%s, %s, %s, %s)",
                row
            )

    with open('data/base_cookingsteps.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Пропуск заголовков
        for row in reader:
            cur.execute(
                "INSERT INTO base_cookingsteps (id, step, recipe_id) VALUES (%s, %s, %s)",
                row
            )

    with open('data/base_products.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Пропуск заголовков
        for row in reader:
            cur.execute(
                "INSERT INTO base_products (id, products_name, protein_per_100g, fat_per_100g, carb_per_100g, kcal_per_100g) VALUES (%s, %s, %s, %s, %s, %s)",
                row
            )

    with open('data/base_exercise.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Пропуск заголовков
        for row in reader:
            cur.execute(
                "INSERT INTO base_exercise (id, name, description, muscle_group, difficulty, demonstration_video, demonstration_video_2, calories, equipment) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                row
            )

    # Сохранение изменений и закрытие соединения
    conn.commit()
cur.close()
conn.close()

