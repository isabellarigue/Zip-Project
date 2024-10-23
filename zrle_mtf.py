class ListNode:
    """ Représente un nœud dans une liste chaînée. """
    def __init__(self, symb, successor):
        self.symb = symb # Le symbole stocké dans le nœud
        self.successor = successor

    def insert_front_node(self, node):
        """Insère un nœud au début de la liste."""
        node.successor = self
        return node
    
    def insert_front_symbol(self, symb, head):
        """Insère un symbole au début de la liste en créant un nouveau nœud."""
        new = ListNode(symb, None)
        new_head = self.insert_front_node(new, head)
        return new_head
    
    @staticmethod
    def insert_end_node(new, head):
        """Insère un nœud à la fin de la liste."""
        node = head
        if node is None:
            return new
        while node.successor is not None:
            node = node.successor
        node.successor = new
        return head
    
    def insert_end_symbol(self, symb):
        """Insère un symbole à la fin de la liste en créant un nouveau nœud."""
        new = ListNode(symb, None)
        new_head = self.insert_end_node(new, self)
        return new_head

    @staticmethod
    def delete_next(node):
        """Supprime le nœud suivant dans la liste. """
        if node is not None:
            node_del = node.successor
            node.successor = node.successor.successor
        return node_del
    
    def find_npi(self, symb):
        """ Trouve le nœud contenant le symbole donné, son parent, et son indice. """
        node = self  # Tête de la liste
        if node.symb == symb:
            return (node, None, 0)
        i = 1
        while node.successor is not None:
            if node.successor.symb == symb:
                return node.successor, node, i
            node = node.successor
            i += 1
        return None, None, None
    
    def find_np(self, index):
        """ Trouve le nœud à l'indice donné et son parent. """
        node = self
        if index == 0:
            return node, None #Node, parent
        i = 1
        while node.successor is not None:
            if i == index:
                return node.successor, node
            node = node.successor
            i += 1
    
    def print_list(self):
        """Affiche tous les symboles de la liste chaînée."""
        head = self
        print(head.symb)
        while head.successor is not None:
            print(head.successor.symb)
            head = head.successor

def create_list_symb(n):
    """Crée une liste chaînée de taille n, où chaque élément correspond à son indice."""
    head = ListNode(0, None)
    for i in range(1, n):
        head = head.insert_end_symbol(i)
    return head

def mtf_encode(inputs):
    """Effectue l'encodage Move-to-Front (MTF) sur les données d'entrée. """
    symbs = create_list_symb(257)
    first = True
    for symb in inputs:
        node, parent, index = symbs.find_npi(symb)
        if parent is not None:
            node = symbs.delete_next(parent)
            symbs = symbs.insert_front_node(node)
        if first:
            outputs = ListNode(index, None)
            first = False
        else:
            outputs.insert_end_symbol(index)
    return outputs

def mtf_decode(outputs):
    """ Effectue le décodage Move-to-Front (MTF) à partir de la liste encodée. """
    symbs = create_list_symb(257)
    first = True
    while outputs is not None:
        index = outputs.symb
        node, parent = symbs.find_np(index)
        if parent is not None:
            node = symbs.delete_next(parent)
            symbs = symbs.insert_front_node(node)
        if first:
            inputs = ListNode(node.symb, None)
            first = False
        else:
            inputs.insert_end_symbol(node.symb)
        outputs = outputs.successor
    return inputs

def count_digits(x):
    count = 0
    while x > 0:
        x = x // 10
        count += 1
    return count

def zrle_constant(res, zrle_one, zrle_two):
    """ Retourne la constante ZRLE appropriée."""
    if res == 1:
        return zrle_one
    elif res == 2:
        return zrle_two
    else: 
        raise ValueError("Valeur invalide")

def binary_bijective(x, zrle_one, zrle_two):
    """Encode un nombre en utilisant un système binaire bijectif modifié."""
    if x <= 0:
        return []

    coefficients = []
    q = x
    while q > 0:
        q_next = (q + 1) // 2 - 1
        a = q - 2 * q_next
        coefficients.append(zrle_constant(a, zrle_one, zrle_two))
        q = q_next

    coefficients.reverse()
    return ''.join(str(d) for d in coefficients)

def zrle_encode(symbs):
    """Effectue l'encodage ZRLE sur une liste chaînée de symboles."""
    zrle_one = 257
    zrle_two = 258

    head = symbs
    while symbs.successor is not None:
        if symbs.symb == 0:
            first_zero = symbs
            count = 1
            while symbs.successor is not None and symbs.successor.symb == 0:
                count += 1
                symbs = symbs.successor
            n = binary_bijective(count, zrle_one, zrle_two)
            first_zero.symb = n
            first_zero.successor = symbs.successor

        symbs = symbs.successor
        if symbs is None:
            break
    
    return head








###### Test ######
inputs = [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
outputs = mtf_encode(inputs)
symbs_compressesd = zrle_encode(outputs)
symbs_compressesd.print_list()
