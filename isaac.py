def xor(val1, val2):
    res = ""
    tabk = ["" for i in range(len(val1))]
    for i in range(len(val1)):
        v1 = val1[i:i + 1]
        v2 = val2[i:i + 1]

        tabk[i] = "0" if v1 == v2 else "1"

    for i in tabk:
        res += i
    return res


def or_logic(val1, val2):
    res = ""
    tabk = ["" for i in range(len(val1))]
    for i in range(len(val1)):
        v1 = val1[i:i + 1]
        v2 = val2[i:i + 1]

        tabk[i] = "1" if v1 == "1" or v2 == "1" else "0"

    for i in tabk:
        res += i
    return res


def and_logic(val1, val2):
    res = ""
    tabk = [""] * len(val1)
    for i in range(len(val1)):
        v1 = val1[i:i + 1]
        v2 = val2[i:i + 1]
        tabk[i] = "1" if v1 == "1" and v2 == "1" else "0"
    res = "".join(tabk)
    return res


def permut(val, k):
    res = ""
    tabk = [0] * len(val)

    for i in range(len(val)):
        id = k[i:i + 1]
        vid = int(id)
        tabk[i] = val[vid]
        res += tabk[i]

    return res


def inverse_permut(k):
    res = ""
    tabk = [0] * len(k)

    for i in range(len(k)):
        id = k[i:i + 1]
        vid = int(id)
        tabk[vid] = str(i)

    res = ''.join(tabk)
    return res


def shift(val, order, left):
    res = ""
    tabk = [""] * len(val)
    s = -1 if left else 1
    for i in range(len(val)):
        v1 = val[i:i + 1]
        o = order
        j = i
        while o > 0:
            if j + s < 0:
                j = len(val) - 1
            elif j + s >= len(val):
                j = 0
            else:
                j = j + s
            o -= 1
        tabk[j] = v1
    res = "".join(tabk)
    return res


def generate_key(key, perm_func, left_shift_order, right_shift_order):
    res = ""
    new_key = permut(key, perm_func)
    key1 = new_key[0:4]
    key2 = new_key[4:8]
    new_key1 = xor(key1, key2)
    new_key2 = and_logic(key1, key2)
    shifted_new_key1 = shift(new_key1, left_shift_order, True)
    shifted_new_key2 = shift(new_key2, right_shift_order, False)
    res = shifted_new_key1 + "," + shifted_new_key2
    return res


def round_D_encrypt(val, perm_func, key):
    res = ""
    permuted_val = permut(val, perm_func)
    res = xor(permuted_val, key)
    return res


def round_G_encrypt(right_half_val, left_half_val, key):
    res = ""
    function_result = or_logic(left_half_val, key)
    res = xor(right_half_val, function_result)
    return res


def round_G_decrypt(right_half_val, perm_func, key):
    res = ""
    inverse_permuted_key = inverse_permut(perm_func)
    result_after_xor = xor(right_half_val, key)
    res = permut(result_after_xor, inverse_permuted_key)
    return res


def round_D_decrypt(right_half_val, left_half_val, key):
    res = ""
    function_result = or_logic(left_half_val, key)
    res = xor(right_half_val, function_result)
    return res

def main():
    print("********ALGORITHME DE FREISNEL CIPHER*********")
    key = input("Donnez une clé K de longueur 8: ")
    while len(key) < 8:
        key = input("La taille de la clé doit être de longueur 8: ")
    h = input("Donnez la fonction H de permutation: ")
    while len(h) < 8:
        h = input("La taille doit être de longueur 8: ")
    decg = int(input("Entrez l'ordre de décalage à gauche: "))
    while decg <= 0:
        decg = int(input("L'ordre doit être supérieur à 0: "))
    decd = int(input("Entrez l'ordre de décalage à droite: "))
    while decd <= 0:
        decd = int(input("L'ordre doit être supérieur à 0: "))
    kgen = generate_key(key, h, decg, decd)
    n = input("Entrez la valeur N ou C à traiter: ")
    while len(n) < 8:
        n = input("La taille doit être de longueur 8: ")
    choix = -1
    while choix != 1 and choix != 2:
        choix = int(input("Voulez-vous chiffrer ou dechiffrer? (1 pour dechiffrer et 2 pour chiffrer): "))
    p = input("Entrez la permutation P de 4 bits: ")
    while len(p) < 4:
        p = input("La taille doit être de longueur 4: ")
    keyc = input("Entrez la clé de permutation pour l'opération de chiffrement ou déchiffrement: ")
    while len(keyc) < 8:
        keyc = input("La taille doit être de longueur 8: ")
    tkey = kgen.split(",")
    if choix == 2:
        pn = permut(n, keyc)
        g0 = pn[:4]
        d0 = pn[4:8]
        d1 = round_D_encrypt(g0, p, tkey[0])
        g1 = round_G_encrypt(d0, g0, tkey[0])
        d2 = round_D_encrypt(g1, p, tkey[1])
        g2 = round_G_encrypt(d1, g1, tkey[1])
        c = g2 + d2
        ikey = inverse_permut(keyc)
        res = permut(c, ikey)
        print("La valeur chiffrée est :", res)
    else:
        pn = permut(n, keyc)
        g2 = pn[:4]
        d2 = pn[4:8]
        g1 = round_G_decrypt(d2, p, tkey[1])
        d1 = round_D_decrypt(g2, g1, tkey[1])
        g0 = round_G_decrypt(d1, p, tkey[0])
        d0 = round_D_decrypt(g1, g0, tkey[0])
        Nd = g0 + d0
        ikey = inverse_permut(keyc)
        res = permut(Nd, ikey)
        print("La valeur déchiffrée est :", res)

main()