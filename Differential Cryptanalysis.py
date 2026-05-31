import matplotlib.pyplot as plt
import numpy as np
import os

# S-box (Вариант 4) переведенный в HEX
s_box = [0x1, 0xA, 0x6, 0x5, 0x9, 0x0, 0xC, 0x3, 0x4, 0xF, 0x7, 0xD, 0x2, 0xB, 0xE, 0x8]

size = 16
# Создаем пустую таблицу 16x16, заполненную нулями
ddt = [[0]*size for _ in range(size)]

# 1. Построение DDT
for dx in range(size):         # Перебираем все возможные входные разности (дельта X)
    for x in range(size):      # Перебираем все возможные входы (от 0 до 15)
        x_prime = x ^ dx       # Находим второй вход, чтобы разница между ними была dx
        
        y = s_box[x]
        y_prime = s_box[x_prime]
        
        dy = y ^ y_prime       # Находим выходную разность (дельта Y)
        
        # Записываем в таблицу: для входной разницы dx получилась выходная dy
        ddt[dx][dy] += 1

print("=== ТАБЛИЦА РАСПРЕДЕЛЕНИЯ РАЗНОСТЕЙ (DDT) ===")
print("    ", end="")
for i in range(size):
    print(f"dY{i:<2}", end="")
print("\n" + "-"*65)

for i, row in enumerate(ddt):
    print(f"dX{i:<2}|", end="")
    for val in row:
        print(f"{val:3}", end=" ")
    print()

# 2. Анализ таблицы
max_val = -1
best_dx = -1
best_dy = -1

# Ищем максимальное значение (игнорируя dx=0, dy=0, так как там всегда будет 16)
for dx in range(size):
    for dy in range(size):
        if dx == 0 and dy == 0:
            continue
        if ddt[dx][dy] > max_val:
            max_val = ddt[dx][dy]
            best_dx = dx
            best_dy = dy

probability = max_val / 16.0

print("\n=== РЕЗУЛЬТАТ АНАЛИЗА ===")
print(f"Максимальное количество повторений: {max_val} (из 16)")
print(f"Самый вероятный переход: ΔX = {best_dx} ---> ΔY = {best_dy}")
print(f"Вероятность этого перехода: {max_val}/16 = {probability:.4f} ({probability*100}%)")

# === ОТРИСОВКА И СОХРАНЕНИЕ ГРАФИКА ===
ddt_array = np.array(ddt)

plt.figure(figsize=(10, 8))
plt.imshow(ddt_array, cmap='Reds', interpolation='nearest')
plt.colorbar(label='Количество попаданий')

# Расставляем циферки в клетках
for i in range(size):
    for j in range(size):
        text_color = 'white' if ddt_array[i, j] > 4 else 'black'
        plt.text(j, i, str(ddt_array[i, j]), ha='center', va='center', color=text_color, fontsize=9)

plt.title('Тепловая карта DDT (Вариант 4)\nЯркие клетки - уязвимости к дифференциальному анализу', fontsize=14)
plt.xlabel('Выходная разность (ΔY)', fontsize=12)
plt.ylabel('Входная разность (ΔX)', fontsize=12)
plt.xticks(range(size))
plt.yticks(range(size))
plt.tight_layout()

file_name = "ddt_heatmap_var4.png"
plt.savefig(file_name, dpi=300)

print(f"\n[+] Скрипт завершен! Картинка успешно сохранена как: {os.path.abspath(file_name)}")