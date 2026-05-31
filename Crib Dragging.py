import time
import random

# --- 1. Реализация гибридного тройного шифрования ---
MOD = 256

def encrypt_L1(data, k1): return tuple((x + k1) % MOD for x in data)
def decrypt_L1(data, k1): return tuple((x - k1) % MOD for x in data)

def encrypt_L2(data, k2): return tuple(x ^ k2 for x in data)
def decrypt_L2(data, k2): return tuple(x ^ k2 for x in data)

def encrypt_L3(data, k3): return tuple((x + k3) % MOD for x in data)
def decrypt_L3(data, k3): return tuple((x - k3) % MOD for x in data)

def triple_encrypt(p_tuple, k1, k2, k3):
    return encrypt_L3(encrypt_L2(encrypt_L1(p_tuple, k1), k2), k3)

# Функция для полной расшифровки тройного шифра
def triple_decrypt(c_tuple, k1, k2, k3):
    return decrypt_L1(decrypt_L2(decrypt_L3(c_tuple, k3), k2), k1)

# --- 2. Алгоритм Полного перебора (Brute Force) ---
def attack_brute_force(p_tuple, c_tuple, max_key):
    for k1 in range(max_key):
        for k2 in range(max_key):
            for k3 in range(max_key):
                if triple_encrypt(p_tuple, k1, k2, k3) == c_tuple:
                    return k1, k2, k3
    return None

# --- 3. Атака «Разделяй и побеждай» (Meet-in-the-Middle) ---
def attack_divide_conquer(p_tuple, c_tuple, max_key):
    table = {}
    
    # СЛЕВА: 1 шаг (K1)
    for k1 in range(max_key):
        mid_val = encrypt_L1(p_tuple, k1)
        table[mid_val] = k1
        
    # СПРАВА: 2 шага (K3 и K2)
    for k2 in range(max_key):
        for k3 in range(max_key):
            dec_val = decrypt_L2(decrypt_L3(c_tuple, k3), k2)
            
            if dec_val in table:
                found_k1 = table[dec_val]
                return found_k1, k2, k3
    return None

# --- 4. Проведение эксперимента ---
def run_experiment():
    print("Анализ тройного шифрования (Divide and Conquer vs Brute Force)\n")
    
    P_tuple = (10, 42, 250, 15) 

    print(f"{'BITS':<6} | {'KEY SPACE (3 keys)':<18} | {'BRUTE FORCE (s)':<16} | {'MITM (s)':<10}")
    print("-" * 65)

    bit_sizes = [4, 5, 6, 7] 
    
    for n in bit_sizes:
        space_size = 2**n 
        total_space = space_size**3 
        
        real_k1 = random.randint(0, space_size - 1)
        real_k2 = random.randint(0, space_size - 1)
        real_k3 = random.randint(0, space_size - 1)
        
        C_tuple = triple_encrypt(P_tuple, real_k1, real_k2, real_k3)
        
        # 1. Замер Полного перебора
        start = time.time()
        bf_keys = attack_brute_force(P_tuple, C_tuple, space_size)
        bf_time = time.time() - start
        
        # 2. Замер Divide and Conquer
        start = time.time()
        mitm_keys = attack_divide_conquer(P_tuple, C_tuple, space_size)
        mitm_time = time.time() - start
        
        print(f"{n:<6} | 2^{n*3} = {total_space:<10} | {bf_time:<16.5f} | {mitm_time:<10.5f}")
        
        # --- БЛОК ВЫВОДА И ПРОВЕРКИ КЛЮЧЕЙ ---
        print(f"   [Real] Загадано: k1={real_k1}, k2={real_k2}, k3={real_k3}")
        print(f"   [BF]   Найдено:  k1={bf_keys[0]}, k2={bf_keys[1]}, k3={bf_keys[2]}")
        print(f"   [MITM] Найдено:  k1={mitm_keys[0]}, k2={mitm_keys[1]}, k3={mitm_keys[2]}")
        
        # Криптографическая проверка: расшифровываем текст найденными ключами
        if bf_keys and mitm_keys:
            check_bf = triple_decrypt(C_tuple, bf_keys[0], bf_keys[1], bf_keys[2])
            check_mitm = triple_decrypt(C_tuple, mitm_keys[0], mitm_keys[1], mitm_keys[2])
            
            if check_bf == P_tuple and check_mitm == P_tuple:
                print("   ✅ УСПЕХ: Найденные ключи корректно расшифровывают исходный текст!\n")
            else:
                print("   ❌ ОШИБКА: Ключи не подходят.\n")

if __name__ == "__main__":
    run_experiment()