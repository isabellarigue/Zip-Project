def counting_sort(symbs):
    """
    Trie la liste 'symbs' en utilisant le tri par comptage.
    symbs (list): Liste des symboles à trier.
    """
    freqs = {}  # Dictionnaire pour stocker les fréquences de chaque symbole
    index = {}  # Dictionnaire pour stocker les indices de début de chaque symbole dans le tableau trié
    
    # Calculer la fréquence de chaque symbole
    for a in symbs:
        if a in freqs:
            freqs[a] += 1
        else:
            freqs[a] = 1

    # Calculer les indices de début pour chaque symbole trié
    i = 0
    sorted_symbs = sorted(freqs.keys())  # Trie les symboles par ordre croissant
    for item in sorted_symbs:
        index[item] = i
        i += freqs[item]

    # Réorganisation des symboles dans la liste
    k = 0
    while k < len(symbs):
        symb = symbs[k]
        # Vérifie si le symbole est déjà à la bonne position
        if k >= index[symb] and k < (index[symb] + freqs[symb]):
            k += 1  # Passe au symbole suivant
        else:
            # Trouve un symbole mal placé et échange les deux
            for i in range(index[symb], (index[symb] + freqs[symb])):
                if symbs[i] != symb:
                    symbs[i], symbs[k] = symbs[k], symbs[i]
                    break
    return symbs


def correspondance_func(tab, n):
    """Fonction de correspondance pour obtenir le critère de tri."""
    return tab[n]


def counting_sort_arrays(arrays, n, correspondance_func):
    """Trie les tableaux en fonction de la position 'n' choisie."""
    freqs = {}  # Fréquences de chaque symbole
    index = {}  # Indices de début pour chaque symbole trié
    
    # Calcul des fréquences basées sur l'élément à la position n de chaque tableau
    for array in arrays:
        symb = array[n]
        if symb in freqs:
            freqs[symb] += 1
        else:
            freqs[symb] = 1

    # Calcul des indices de début pour chaque symbole trié
    i = 0
    sorted_symbs = sorted(freqs.keys())
    for item in sorted_symbs:
        index[item] = i
        i += freqs[item]

    # Réorganisation des tableaux dans la liste
    k = 0
    while k < len(arrays):
        symb = correspondance_func(arrays[k], n)
        if k >= index[symb] and k < (index[symb] + freqs[symb]):
            k += 1
        else:
            # Trouver un tableau mal placé et échanger
            for i in range(index[symb], (index[symb] + freqs[symb])):
                if len(arrays[i]) > n and arrays[i][n] != symb:
                    arrays[i], arrays[k] = arrays[k], arrays[i]
                    break
    return arrays


def correspondance_func1(index, shift, text, n):
    """ Obtenir le symbole correspondant à la rotation. """
    return text[(index + shift) % n]


def burrows_wheeler_transform(text, correspondance_func1):
    """
    Réalise la transformation de Burrows-Wheeler sur le texte donné.
    text (str): Le texte à transformer.
    correspondance_func1 (function): Fonction pour obtenir le caractère correspondant.
    """
    bwt_marker = chr(256)  # Marqueur de fin pour le texte
    text += bwt_marker  # Ajoute le marqueur au texte

    n = len(text)
    rotations = list(range(n))  # Liste des indices pour les rotations implicites

    def counting_sort_rotations(rotations, shift):
        """Trie les rotations en fonction du caractère au décalage spécifié."""
        max_char = 257  # Intervalle de caractères
        count = [0] * max_char

        # Fréquence des caractères à la position de décalage
        for index in rotations:
            symbol = ord(correspondance_func1(index, shift, text, n))
            count[symbol] += 1

        # Calcul des positions initiales
        for i in range(1, max_char):
            count[i] += count[i - 1]

        # Trie les rotations en fonction du caractère
        sorted_rotations = [0] * n
        for i in range(n - 1, -1, -1):
            index = rotations[i]
            symbol = ord(correspondance_func1(index, shift, text, n))
            count[symbol] -= 1
            sorted_rotations[count[symbol]] = index

        return sorted_rotations

    # Trie des rotations en fonction de chaque caractère
    for shift in reversed(range(n)):
        rotations = counting_sort_rotations(rotations, shift)

    # Construction du résultat à partir de la dernière colonne
    bwt_result = ''.join(text[(index - 1) % n] for index in rotations)

    return bwt_result


def bwt_decode(bwt_result):
    """
    Décodage de la transformation de Burrows-Wheeler.
    bwt_result (str): Texte encodé avec la transformation de Burrows-Wheeler.
    """
    last_column = list(bwt_result)
    first_column = sorted(last_column)
    n = len(last_column)

    next_index = [0] * n  # Positions de chaque caractère dans la première colonne
    
    # Comptage des occurrences pour le mappage
    count = {}
    for i in range(n):
        char = last_column[i]
        if char not in count:
            count[char] = 0
        next_index[i] = count[char]
        count[char] += 1

    # Indexation pour les positions correctes dans la première colonne
    count = {}
    for i in range(n):
        char = first_column[i]
        if char not in count:
            count[char] = 0
        next_index[i] = count[char]
        count[char] += 1

    # Reconstruit la chaîne originale
    current_index = bwt_result.index(chr(256))  # Trouver le marqueur de fin
    original_string = []
    for _ in range(n):
        original_string.append(last_column[current_index])
        current_index = next_index[current_index]

    original_string.reverse()  # La chaîne originale est construite de la fin vers le début
    
    return ''.join(original_string).rstrip(chr(256))  # Retirer le marqueur de fin




###### Test ######
symbs = [3, 5, 5, 3, 2, 3]
symbs2 = counting_sort(symbs)
print(symbs2)

arrays = [[3, 4, 6, 4, 9], [1, 1, 3, 1, 6], [6, 4, 6, 4, 3]]
arrays2 = counting_sort_arrays(arrays, 3, correspondance_func)
print(arrays2)

result = burrows_wheeler_transform("simili.", correspondance_func1)
print(result.replace(chr(256), ''))  
original_text = bwt_decode(result)
print(original_text) 
