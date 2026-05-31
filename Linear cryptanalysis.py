import matplotlib.pyplot as plt
import numpy as np
import os

def dot_product(val, mask):
    # Вычисляет XOR-сумму битов результата логического AND
    res = val & mask
    return bin(res).count('1') % 2

def build_lat(sbox):
    size = len(sbox)
    lat = [[0]*size for _ in range(size)]

    for alpha in range(size):
        for beta in range(size):
            matches = 0
            for x in range(size):
                if dot_product(x, alpha) == dot_product(sbox[x], beta):
                    matches += 1
            lat[alpha][beta] = matches - (size // 2)
    return lat

# Вариант 4
s_box_v4 = [0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD, 0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2]

# Строим таблицу
my_lat = build_lat(s_box_v4)

print("ТАБЛИЦА ЛИНЕЙНЫХ АППРОКСИМАЦИЙ (LAT)")
print("    ", end="")
for i in range(16):
    print(f"b{i:<2}", end=" ")
print("\n" + "-"*65)

for i, row in enumerate(my_lat):
    print(f"a{i:<2}|", end="")
    for val in row:
        print(f"{val:3}", end=" ")
    print()

max_abs_val = -1
best_alpha = -1
best_beta = -1

for alpha in range(16):
    for beta in range(16):
        if alpha == 0 and beta == 0:
            continue
        
        current_abs = abs(my_lat[alpha][beta])
        if current_abs > max_abs_val:
            max_abs_val = current_abs
            best_alpha = alpha
            best_beta = beta

real_val = my_lat[best_alpha][best_beta]

print("\nРЕЗУЛЬТАТ АНАЛИЗА")
print(f"Максимальное отклонение: {real_val} (по модулю {max_abs_val})")
print(f"Найдено в координатах: alpha (вход) = {best_alpha}, beta (выход) = {best_beta}")

# === ОТРИСОВКА И СОХРАНЕНИЕ ГРАФИКА ===
lat_array = np.array(my_lat)

plt.figure(figsize=(10, 8))
plt.imshow(lat_array, cmap='coolwarm', interpolation='nearest')
plt.colorbar(label='Значение отклонения (V)')

for i in range(16):
    for j in range(16):
        text_color = 'black' if abs(lat_array[i, j]) < 3 else 'white'
        plt.text(j, i, str(lat_array[i, j]), ha='center', va='center', color=text_color, fontsize=9)

plt.title('Тепловая карта LAT (Вариант 4)\nЯркие клетки - уязвимости S-блока', fontsize=14)
plt.xlabel('Выходная маска (beta)', fontsize=12)
plt.ylabel('Входная маска (alpha)', fontsize=12)
plt.xticks(range(16))
plt.yticks(range(16))
plt.tight_layout()

# Вместо вывода на экран сохраняем в картинку высокого качества (300 dpi)
file_name = "lat_heatmap_var4.png"
plt.savefig(file_name, dpi=300)

print(f"\n[+] Скрипт завершен! Картинка успешно сохранена как: {os.path.abspath(file_name)}")