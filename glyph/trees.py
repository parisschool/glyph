from .utils import Style, colorize

class AVLNode:
    def __init__(self, val, papa=None):
        self.val = val
        self.left = None
        self.right = None
        self.papa = papa
        self.fe = 0  # Factor de equilibrio

class AVLTree:
    def __init__(self):
        self.root = None
        self.count = 0

    def insert(self, val):
        if self.root is None:
            self.root = AVLNode(val)
            self.count += 1
            return
        
        curr = self.root
        parent = None
        while curr:
            parent = curr
            if val < curr.val:
                curr = curr.left
            elif val > curr.val:
                curr = curr.right
            else:
                return # Valor duplicado
        
        new_node = AVLNode(val, papa=parent)
        if val < parent.val:
            parent.left = new_node
        else:
            parent.right = new_node
            
        self.count += 1
        self._balance_insert(new_node)

    def _balance_insert(self, n):
        padre = n.papa
        while padre:
            if n == padre.left:
                padre.fe -= 1
            else:
                padre.fe += 1

            if padre.fe == 0:
                break
            elif padre.fe in (2, -2):
                self._rebalance(padre)
                break
            else:
                n = padre
                padre = padre.papa

    def _rebalance(self, node):
        if node.fe == 2:
            if node.right.fe >= 0:
                self._rotate_left(node)
            else:
                self._rotate_right(node.right)
                self._rotate_left(node)
        elif node.fe == -2:
            if node.left.fe <= 0:
                self._rotate_right(node)
            else:
                self._rotate_left(node.left)
                self._rotate_right(node)

    def _rotate_left(self, nodo):
        hijo_der = nodo.right
        tatara = nodo.papa

        nodo.right = hijo_der.left
        if hijo_der.left:
            hijo_der.left.papa = nodo

        hijo_der.papa = tatara
        if tatara is None:
            self.root = hijo_der
        elif tatara.left == nodo:
            tatara.left = hijo_der
        else:
            tatara.right = hijo_der

        hijo_der.left = nodo
        nodo.papa = hijo_der

        if hijo_der.fe == 0:
            nodo.fe = 1
            hijo_der.fe = -1
        else:
            nodo.fe = 0
            hijo_der.fe = 0

    def _rotate_right(self, nodo):
        hijo_izq = nodo.left
        tatara = nodo.papa

        nodo.left = hijo_izq.right
        if hijo_izq.right:
            hijo_izq.right.papa = nodo

        hijo_izq.papa = tatara
        if tatara is None:
            self.root = hijo_izq
        elif tatara.right == nodo:
            tatara.right = hijo_izq
        else:
            tatara.left = hijo_izq

        hijo_izq.right = nodo
        nodo.papa = hijo_izq

        if hijo_izq.fe == 0:
            nodo.fe = -1
            hijo_izq.fe = 1
        else:
            nodo.fe = 0
            hijo_izq.fe = 0

    def delete(self, dato):
        actual = self.root
        encontrado = False
        while actual and not encontrado:
            if dato == actual.val:
                encontrado = True
            elif dato < actual.val:
                actual = actual.left
            else:
                actual = actual.right
        
        if not encontrado: return

        if actual.left and actual.right:
            sucesor = actual.right
            while sucesor.left:
                sucesor = sucesor.left
            actual.val = sucesor.val
            actual = sucesor

        hijo = actual.left if actual.left else actual.right
        padre_aux = actual.papa
        vino_de_izq = (padre_aux and actual == padre_aux.left)

        if hijo:
            hijo.papa = padre_aux
        
        if padre_aux is None:
            self.root = hijo
        elif actual == padre_aux.left:
            padre_aux.left = hijo
        else:
            padre_aux.right = hijo
        
        self.count -= 1
        if padre_aux:
            self._balance_delete(padre_aux, vino_de_izq)

    def _balance_delete(self, padre, de_izq):
        para = False
        while padre and not para:
            if de_izq:
                padre.fe += 1
            else:
                padre.fe -= 1

            if padre.fe in (1, -1):
                para = True
            elif padre.fe in (2, -2):
                self._rebalance(padre)
                nuevo_tope = padre.papa
                if nuevo_tope and nuevo_tope.fe != 0:
                    para = True
                padre = nuevo_tope
            
            if padre and not para:
                abuelo = padre.papa
                if abuelo:
                    de_izq = (padre == abuelo.left)
                padre = abuelo

    def show(self):
        """Usa el visualizador  de abajo"""
        from .trees import visualize_bst
        visualize_bst(self.root)

def visualize_bst(root):
    lines, *_ = _build_tree_canvas(root)
    for line in lines:
        print(line)

def _build_tree_canvas(node):
    if node is None:
        return [], 0, 0, 0

    C_NODE = Style.BOLD + Style.B_GREEN
    C_BRANCH = Style.BROWN

    raw_label = str(getattr(node, 'val', getattr(node, 'data', '?')))
    label_len = len(raw_label)
    label_colored = colorize(raw_label, C_NODE)

    left_lines, left_w, left_h, left_pos = _build_tree_canvas(node.left)
    right_lines, right_w, right_h, right_pos = _build_tree_canvas(node.right)

    # Caso 1: Hoja
    if not left_lines and not right_lines:
        return [label_colored], label_len, 1, label_len // 2

    # Caso 2: Solo hijo izquierdo
    if left_lines and not right_lines:
        # Calculamos el espacio para que el padre no quede "volando"
        shift = max(label_len // 2, 1)
        first_line = " " * left_pos + colorize("_" * (left_w - left_pos - 1), C_BRANCH) + label_colored
        second_line = " " * left_pos + colorize("/", C_BRANCH) + " " * (label_len)
        
        lines = [first_line, second_line]
        for l in left_lines:
            lines.append(l + " " * label_len)
        return lines, left_w + label_len, left_h + 2, left_w + label_len // 2

    # Caso 3: Solo hijo derecho
    if not left_lines and right_lines:
        # El subguion debe conectar con el inicio del hijo
        first_line = label_colored + colorize("_" * right_pos, C_BRANCH)
        second_line = " " * (label_len + right_pos) + colorize("\\", C_BRANCH)
        
        lines = [first_line, second_line]
        for r in right_lines:
            lines.append(" " * label_len + r)
        return lines, label_len + right_w, right_h + 2, label_len // 2

    # Caso 4: Dos hijos
    if left_lines and right_lines:
        gap = 2
        right_abs_pos = left_w + gap + right_pos
        root_x = (left_pos + right_abs_pos) // 2

        # Calculamos el tamaño de los subguiones basándonos en la distancia real
        left_branch_w = root_x - left_pos - 1
        right_branch_w = right_abs_pos - root_x - label_len

        # Si los nodos chocan, ampliamos el gap
        if left_branch_w < 0 or right_branch_w < 0:
            shift = max(0 if left_branch_w >= 0 else -left_branch_w, 
                        0 if right_branch_w >= 0 else -right_branch_w)
            gap += shift * 2
            right_abs_pos = left_w + gap + right_pos
            root_x = (left_pos + right_abs_pos) // 2
            left_branch_w = root_x - left_pos - 1
            right_branch_w = right_abs_pos - root_x - label_len

        total_w = left_w + gap + right_w

        line1 = " " * (left_pos + 1) + \
                colorize("_" * left_branch_w, C_BRANCH) + \
                label_colored + \
                colorize("_" * right_branch_w, C_BRANCH)
                
        line2 = " " * left_pos + colorize("/", C_BRANCH) + \
                " " * (right_abs_pos - left_pos - 1) + \
                colorize("\\", C_BRANCH)

        lines = [line1, line2]
        for i in range(max(left_h, right_h)):
            l = left_lines[i] if i < left_h else " " * left_w
            r = right_lines[i] if i < right_h else " " * right_w
            lines.append(l + " " * gap + r)

        return lines, total_w, max(left_h, right_h) + 2, root_x + label_len // 2

class _HeapNode:
    """Convierte la lógica de índices (2i+1, 2i+2) en una estructura de nodos."""
    def __init__(self, array, index):
        self.val = array[index]
        l_idx = 2 * index + 1
        r_idx = 2 * index + 2
        
        # Recursivamente creamos los hijos si existen en el arreglo
        self.left = _HeapNode(array, l_idx) if l_idx < len(array) else None
        self.right = _HeapNode(array, r_idx) if r_idx < len(array) else None

