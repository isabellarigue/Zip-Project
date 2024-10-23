class HuffmanTreeNode:
    def __init__(self, symbole, nb_occur, g=None, d=None):
        self.symbole = symbole  # Symbole représenté par le nœud (ou None pour les nœuds internes)
        self.nb_occur = nb_occur  # Nombre d'occurrences du symbole
        self.g = g  # Fils gauche
        self.d = d  # Fils droit

    @staticmethod
    def merge(x, y):
        # Fusionne deux nœuds pour créer un nouveau nœud parent avec les deux nœuds enfants
        return HuffmanTreeNode(None, x.nb_occur + y.nb_occur, x, y)

    @staticmethod
    def less(x, y):
        # Compare deux nœuds en fonction de leur nombre d'occurrences
        return x.nb_occur < y.nb_occur
    
    def print_tree(self, prefix=""):
        """Affiche l'arbre de Huffman."""
        if self.symbole is not None:  # Si c'est une feuille
            print(f"{prefix} -> {self.symbole} (Freq: {self.nb_occur})")
        else:  
            self.g.print_tree(prefix + "0")  
            self.d.print_tree(prefix + "1")  

    def build_codemap_rec(self, current_code=None):
        # Génère récursivement la table de codage à partir de l'arbre
        if current_code is None:  # Initialise le code binaire accumulé lors du parcours
            current_code = []
        
        if self.symbole is not None:  # Si c'est une feuille
            return {self.symbole: current_code}
        else:  # Si ce n'est pas une feuille (un nœud interne)
            res = {}
            res.update(self.g.build_codemap_rec(current_code + [0]))  
            res.update(self.d.build_codemap_rec(current_code + [1]))  
            return res


class PQueue:
    def __init__(self, func):
        # Initialisation de la file de priorité avec une fonction de comparaison
        self.A = []
        self.compare = func

    def swap(self, i, p):
        self.A[i], self.A[p] = self.A[p], self.A[i]

    def taille(self):
        return len(self.A)

    def heap_fix_up(self, i):
        # Répare le tas en remontant
        p = (i - 1) // 2
        while p >= 0 and self.compare(self.A[i], self.A[p]):  
            self.swap(i, p)
            i = p
            p = (i - 1) // 2

    def heap_insert(self, x):
        # Insère un élément dans le tas
        self.A.append(x)
        self.heap_fix_up(self.taille() - 1)

    def heap_fix_down(self, i):
        # Répare le tas en descendant
        while 2 * i + 1 < self.taille():
            p = 2 * i + 1
            if p + 1 < self.taille() and self.compare(self.A[p + 1], self.A[p]):
                p = p + 1
            if not self.compare(self.A[p], self.A[i]):
                break
            self.swap(i, p)
            i = p

    def extract_min(self):
        # Extrait l'élément de priorité minimale
        if self.taille() == 0:
            raise ValueError("erreur : le tas est vide")
        else:
            n = self.taille()
            x = self.A[0]
            self.A[0] = self.A[n - 1]
            self.A.pop() 
            self.heap_fix_down(0)
            return x


huffman_marker = 'ª'  # Pour aider au décodage

class Huffman:
    def __init__(self, text):
        self.tree = None
        self.codes = {}
        self.text = ''.join([text, huffman_marker])  # Marqueur spécial ajouté pour delimiter la fin du texte

    def build_tree(self):
        # Crée l'arbre de Huffman à partir du texte
        symbs = {}
        for a in self.text:
            if a in symbs:
                symbs[a] += 1
            else:
                symbs[a] = 1

        pqueue = PQueue(HuffmanTreeNode.less)
        for key in symbs:
            if symbs[key] > 0:
                pqueue.heap_insert(HuffmanTreeNode(key, symbs[key]))

        # Construire l'arbre en fusionnant les nœuds jusqu'à ce qu'il reste un seul nœud
        while pqueue.taille() > 1:
            x = pqueue.extract_min()
            y = pqueue.extract_min()
            pqueue.heap_insert(HuffmanTreeNode.merge(x, y))

        self.tree = pqueue.extract_min()
        return self.tree

    def build_codemap(self):
        # Génère la table de codage à partir de l'arbre de Huffman
        self.codes = self.tree.build_codemap_rec()
        return self.codes
    
    def print_huffman_tree(self):
        # Affiche l'arbre de Huffman s'il a été construit
        if self.tree is not None:
            self.tree.print_tree()

    def encode(self):
        """Encode le texte en utilisant les codes de Huffman et renvoie une liste d'octets."""
        res = 0  
        bit_count = 0 
        output = []  # Liste d'octets pour le résultat

        for symbol in self.text:  
            code = self.codes[symbol]  # Obtenir le code binaire correspondant

            for bit in code: 
                res <<= 1  # Décale à gauche pour faire de la place au nouveau bit
                res |= bit  # Ajoute le nouveau bit au résultat
                bit_count += 1  

                if bit_count == 8: 
                    output.append(res)  # Ajouter l'octet à la liste de sortie
                    res = 0  
                    bit_count = 0  

        # Si le dernier octet n'est pas complet
        if bit_count > 0:  # S'il reste des bits
            res <<= (8 - bit_count)  # Remplit les bits restants avec des zéros
            output.append(res) 

        return output  
    
    def decode(self, res):
        """Décode les octets en utilisant l'arbre de Huffman et renvoie le texte original."""
        octets = []  
        node = self.tree  

        for byte in res:  
            for i in range(7, -1, -1):  # Lit les bits de l'octet, du plus significatif au moins
                bit = (byte >> i) & 1  # Extrait le bit correspondant
                node = node.g if bit == 0 else node.d  # Déplace dans l'arbre

                if node.symbole is not None:  # Si on atteint une feuille
                    if node.symbole == huffman_marker:  # Ignore le symbole spécial
                        return octets  
                    octets.append(node.symbole)  
                    node = self.tree 

        return octets  






###### Test ######

f = open("test.txt", 'r') #TODO add path to the file
texto_str = f.read()

huffman = Huffman(texto_str)
arbre = huffman.build_tree()
codemap = huffman.build_codemap()

cod = huffman.encode()
print("Texte codé:", cod)

decod = huffman.decode(cod)
print("Texte décodé:", decod)
