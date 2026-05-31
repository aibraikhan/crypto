import hashlib
import random
import string
import time
import matplotlib.pyplot as plt
import os

def random_string(length=12):
    """Генерирует случайную строку"""
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def find_collision(trunc_len):
    """Ищет коллизию для укороченного хеша MD5"""
    seen = {}
    attempts = 0
    start_time = time.time()

    while True:
        attempts += 1
        text = random_string(15)
        # Берем MD5 и отрезаем первые trunc_len символов
        hash_val = hashlib.md5(text.encode()).hexdigest()[:trunc_len]

        if hash_val in seen:
            if seen[hash_val] != text:
                elapsed_time = time.time() - start_time
                return attempts, elapsed_time
        else:
            seen[hash_val] = text

# Вариант 4: Исследовать зависимость от длины укороченного хеша (4, 5, 6 символов)
lengths_to_test = [4, 5, 6]
experiments = 5

avg_attempts = []
avg_times = []

print("=== ПОИСК КОЛЛИЗИЙ (АТАКА ДНЕЙ РОЖДЕНИЯ) ===")

for L in lengths_to_test:
    print(f"\n[~] Тестируем длину хеша: {L} символов...")
    total_att = 0
    total_time = 0

    for i in range(experiments):
        att, t = find_collision(L)
        total_att += att
        total_time += t
        print(f"    Эксперимент {i+1}: {att} попыток ({t:.4f} сек)")

    avg_a = total_att / experiments
    avg_t = total_time / experiments
    avg_attempts.append(avg_a)
    avg_times.append(avg_t)

    print(f"[*] СРЕДНЕЕ для длины {L}: {int(avg_a)} попыток ({avg_t:.4f} сек)")

# === ОТРИСОВКА И СОХРАНЕНИЕ ГРАФИКА ===
plt.figure(figsize=(10, 6))

# График количества попыток
plt.plot(lengths_to_test, avg_attempts, marker='o', color='red', linewidth=2, markersize=8)
plt.yscale('log')
plt.title('Зависимость количества попыток от длины хеша (Вариант 4)', fontsize=14)
plt.xlabel('Длина укороченного хеша (в символах)', fontsize=12)
plt.ylabel('Среднее количество попыток до коллизии (Log)', fontsize=12)
plt.grid(True, which="both", ls="--")
plt.xticks(lengths_to_test)

# Сохраняем картинку в папку со скриптом
file_name = "collision_graph_var4.png"
plt.savefig(file_name, dpi=300)

print(f"\n[+] Скрипт завершен! График успешно сохранен как: {os.path.abspath(file_name)}")