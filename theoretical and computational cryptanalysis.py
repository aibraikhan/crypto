import random
import collections
import math
import matplotlib.pyplot as plt

def entropy(data):
    freq = collections.Counter(data)
    total = len(data)
    H = 0
    for v in freq.values():
        p = v / total
        H -= p * math.log2(p)
    return H

print("=== ЗАДАНИЕ 1: АНАЛИЗ ГАММЫ (Вариант 4) ===")

my_p0 = 0.65
my_p1 = 0.35
gamma_var4 = ''.join(random.choices(['0', '1'], weights=[my_p0, my_p1], k=10000))

print(f"Частота нулей и единиц: {collections.Counter(gamma_var4)}")
print(f"Энтропия: {entropy(gamma_var4):.4f}")


print("\n=== ЭКСПЕРИМЕНТ И ГРАФИК ===")

probabilities_p0 = [0.5, 0.6, 0.7, 0.8]
entropies = []

for p0 in probabilities_p0:
    p1 = 1.0 - p0
    
    test_gamma = ''.join(random.choices(['0', '1'], weights=[p0, p1], k=10000))

    current_entropy = entropy(test_gamma)
    entropies.append(current_entropy)
    
    print(f"При P(0)={p0:.1f}, энтропия = {current_entropy:.4f}")

# ШАГ 3: Отрисовка графика (я написал базу для тебя)
plt.figure(figsize=(8, 5))
plt.plot(probabilities_p0, entropies, marker='o', color='b', linewidth=2)
plt.title('Зависимость энтропии от вероятности P(0)')
plt.xlabel('Вероятность генерации нуля P(0)')
plt.ylabel('Энтропия (бит на символ)')
plt.grid(True)
plt.show()


print("\n=== ЗАДАНИЕ 2: РАССТОЯНИЕ УНИКАЛЬНОСТИ ===")

key_length = 128
D = 1.3

h_bit = entropy(gamma_var4)

# Шаг 1: Посчитай общую энтропию ключа H_K (длина ключа умножить на энтропию одного бита)
H_K = key_length * h_bit

# Шаг 2: Вычисли расстояние уникальности U по формуле H_K / D
U = H_K / D

print(f"Общая энтропия ключа H(K): {H_K:.2f} бит")
print(f"Расстояние уникальности U: {U:.2f} символов")


print("\n=== ЗАДАНИЕ 3: КРИПТОАНАЛИЗ OTP (Вариант 4) ===")

c1_str = "1110001010110011"
c2_str = "1011100101011010"

c1_int = int(c1_str, 2)
c2_int = int(c2_str, 2)

xor_result_int = c1_int ^ c2_int

xor_result_str = format(xor_result_int, f'0{len(c1_str)}b')

print(f"C1:        {c1_str}")
print(f"C2:        {c2_str}")
print(f"C1 XOR C2: {xor_result_str}")
print(f"Это равносильно P1 XOR P2!")


print("\n--- Шаг 4: Вероятностный анализ (Crib Dragging) ---")
byte1_xor = int(xor_result_str[:8], 2)
byte2_xor = int(xor_result_str[8:], 2)

guess_char = ''
guess_byte = ord(guess_char)

p2_guess_1 = byte1_xor ^ guess_byte
p2_guess_2 = byte2_xor ^ guess_byte

print(f"Анализ байта 1 ({xor_result_str[:8]}):")
print(f"Если первый символ P1 был пробелом, то первый символ P2 = '{chr(p2_guess_1)}' (ASCII: {p2_guess_1})")

print(f"\nАнализ байта 2 ({xor_result_str[8:]}):")
print(f"Если второй символ P1 был пробелом, то второй символ P2 = '{chr(p2_guess_2)}' (ASCII: {p2_guess_2})")
print("\nВывод: Перебирая так частые буквы и словари, криптоаналитик восстанавливает оба текста.")