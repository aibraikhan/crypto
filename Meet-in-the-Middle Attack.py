import time
import random

# Проверка наличия библиотеки для графиков
try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

# --- 1. Реализация ГИБРИДНОЙ криптографии (Сложение + XOR) ---
# Мы меняем алгоритм, чтобы ключи K1 и K2 нельзя было поменять местами.
# Это гарантирует, что программа найдет именно РЕАЛЬНЫЕ ключи.

def text_to_numbers(text):
    return tuple(ord(c) for c in text)

def numbers_to_text(numbers):
    return "".join(chr(n) for n in numbers)

# Слой 1: Арифметическое сложение (использует K1)
def encrypt_layer_1(data_tuple, k1):
    # Просто прибавляем ключ. Не делаем % 256, чтобы сохранить уникальность больших ключей.
    return tuple(x + k1 for x in data_tuple)

def decrypt_layer_1(data_tuple, k1):
    # Обратная операция - вычитание
    return tuple(x - k1 for x in data_tuple)

# Слой 2: Операция XOR (использует K2)
def encrypt_layer_2(data_tuple, k2):
    return tuple(x ^ k2 for x in data_tuple)

def decrypt_layer_2(data_tuple, k2):
    return tuple(x ^ k2 for x in data_tuple)

# Двойное шифрование: Сначала Плюс, потом XOR
def double_encrypt(data_tuple, k1, k2):
    step1 = encrypt_layer_1(data_tuple, k1)
    step2 = encrypt_layer_2(step1, k2)
    return step2

# --- 2. Алгоритм Полного перебора (Brute Force) ---
def attack_brute_force(p_tuple, c_tuple, max_key):
    # Ищем k1 и k2, которые превратят P в C
    for k1 in range(max_key):
        for k2 in range(max_key):
            # Проверяем: если зашифровать P, получится ли C?
            if double_encrypt(p_tuple, k1, k2) == c_tuple:
                return k1, k2
    return None

# --- 3. Алгоритм Meet-in-the-Middle ---
def attack_mitm(p_tuple, c_tuple, max_key):
    middle_table = {}
    
    # Этап 1: Идем СЛЕВА (от P к середине)
    # Используем encrypt_layer_1 (Сложение)
    for k1 in range(max_key):
        mid_val = encrypt_layer_1(p_tuple, k1)
        middle_table[mid_val] = k1
        
    # Этап 2: Идем СПРАВА (от C к середине)
    # Используем decrypt_layer_2 (XOR)
    for k2 in range(max_key):
        dec_val = decrypt_layer_2(c_tuple, k2)
        
        # ВСТРЕЧА ПОСЕРЕДИНЕ
        if dec_val in middle_table:
            # Нашли совпадение!
            found_k1 = middle_table[dec_val]
            return found_k1, k2
    return None

# --- 4. Проведение эксперимента ---
def run_experiment():
    print("Подготовка данных...")
    
    # Текст для шифрования
    full_text = "ANOTHER METAPHOR, IN MY OPINION, BETTER CONVEYS THE ESSENCE OF THE FUTURE BUSTLING ACTIVITY OF THE UNIVERSAL MARKET, MARKETS WHERE THEY SELL EVERYTHING FROM BUILDING MATERIALS TO WOODEN MALLETS FOR PLAYING BALLS, THE FOUNDATION OF HUMAN SOCIETY, AND I BELIEVE THAT THIS NEW MARKET WILL EVENTUALLY BECOME THE CENTRAL DEPARTMENT STORE OF THE WHOLE WORLD."
    P_tuple = text_to_numbers(full_text) 

    print(f"{'BITS':<6} | {'KEY SPACE':<10} | {'BRUTE FORCE (sec)':<18} | {'MITM (sec)':<10}")
    print("-" * 60)

    # Размеры ключей (битность)
    bit_sizes = [8, 10, 12, 13, 14] 
    
    bf_times = []
    mitm_times = []
    
    for n in bit_sizes:
        space_size = 2**n
        
        # 1. Генерируем "Настоящие" ключи
        real_k1 = random.randint(0, space_size - 1)
        real_k2 = random.randint(0, space_size - 1)
        
        # Шифруем текст гибридным методом
        C_tuple = double_encrypt(P_tuple, real_k1, real_k2)
        
        # 2. Запускаем Полный перебор
        start = time.time()
        bf_k1, bf_k2 = attack_brute_force(P_tuple, C_tuple, space_size)
        bf_time = time.time() - start
        bf_times.append(bf_time)
        
        # 3. Запускаем MITM
        start = time.time()
        mitm_k1, mitm_k2 = attack_mitm(P_tuple, C_tuple, space_size)
        mitm_time = time.time() - start
        mitm_times.append(mitm_time)
        
        print(f"{n:<6} | {space_size:<10} | {bf_time:<18.5f} | {mitm_time:<10.5f}")
        
        # --- ПРОВЕРКА НА СОВПАДЕНИЕ ---
        print(f"   [Real] Загадано: k1={real_k1}, k2={real_k2}")
        print(f"   [BF]   Найдено:  k1={bf_k1}, k2={bf_k2}")
        print(f"   [MITM] Найдено:  k1={mitm_k1}, k2={mitm_k2}")
        
        if (bf_k1 == real_k1 and bf_k2 == real_k2) and (mitm_k1 == real_k1 and mitm_k2 == real_k2):
             print("   УСПЕХ: Ключи полностью совпали!\n")
        else:
             print("   СТРАННО: Ключи разные.\n")

    # --- 5. Построение графика ---
    if HAS_MATPLOTLIB:
        plt.figure(figsize=(10, 6))
        plt.plot(bit_sizes, bf_times, label='Brute Force (O(2^2n))', marker='o', color='red')
        plt.plot(bit_sizes, mitm_times, label='Meet-in-the-Middle (O(2^n))', marker='o', color='green')
        
        plt.title('Сравнение эффективности атак (Гибридное шифрование)')
        plt.xlabel('Длина ключа (бит)')
        plt.ylabel('Время выполнения (сек)')
        plt.yscale('log')
        plt.grid(True, which="both", ls="-")
        plt.legend()
        plt.show()

if __name__ == "__main__":
    run_experiment()