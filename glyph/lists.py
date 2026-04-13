import random
from .utils import Style, colorize

class QuadNode:
    def __init__(self, val=None):
        self.val = val
        self.next = None
        self.prev = None
        self.up = None
        self.down = None

class SkipList:
    def __init__(self, max_levels=16, p=0.5): # Dejamos un default alto pero flexible
        self.max_levels = max_levels
        self.p = p
        self.head = QuadNode(float('-inf'))
        self.top_head = self.head
        self.current_height = 1 # Niveles reales creados

    def _find_position(self, val):
        curr = self.top_head
        while True:
            while curr.next and curr.next.val <= val:
                curr = curr.next
            if curr.down:
                curr = curr.down
            else:
                return curr

    def insert(self, val):
        node = self._find_position(val)
        if node.val == val: return

        # Nivel base
        new_node = QuadNode(val)
        new_node.next = node.next
        new_node.prev = node
        if node.next: node.next.prev = new_node
        node.next = new_node

        curr_base = new_node
        lvl = 0
        temp_ptr = node
        
        while random.random() < self.p and lvl < self.max_levels - 1:
            lvl += 1
            # Si el volado pide un nivel que no hemos construido, lo creamos
            if lvl >= self.current_height:
                new_head = QuadNode(float('-inf'))
                self.top_head.up = new_head
                new_head.down = self.top_head
                self.top_head = new_head
                self.current_height += 1
            
            # Subir por la izquierda hasta encontrar un nodo con 'up'
            while temp_ptr.prev and not temp_ptr.up:
                temp_ptr = temp_ptr.prev
            
            temp_ptr = temp_ptr.up
            up_node = QuadNode(val)
            up_node.next = temp_ptr.next
            up_node.prev = temp_ptr
            if temp_ptr.next: temp_ptr.next.prev = up_node
            temp_ptr.next = up_node
            
            up_node.down = curr_base
            curr_base.up = up_node
            curr_base = up_node

    def show(self):
        layers = []
        curr_h = self.head
        while curr_h:
            layer = []
            curr_n = curr_h.next
            while curr_n:
                layer.append(curr_n.val)
                curr_n = curr_n.next
            
            # SOLO agregamos la capa si tiene datos
            if layer:
                layers.append(layer)
            curr_h = curr_h.up
        
        # Si todas están vacías (lista vacía), al menos mostramos la base
        if not layers:
            layers = [[]]
            
        from .lists import visualize_skiplist
        visualize_skiplist(layers)

def visualize_skiplist(layers):
    if not layers:
        print(colorize("SkipList vacía", Style.RED))
        return

    # 1. Alineación vertical pro
    all_nodes = sorted(list(set(node for layer in layers for node in layer)))
    cell_w = max(len(str(n)) for n in all_nodes) + 4

    print(colorize("\n[ ESTRUCTURA DE SKIPLIST ]\n", Style.BOLD + Style.CYAN))

    # 2. Definición de colores por nivel
    colors = [Style.B_MAGENTA, Style.B_BLUE, Style.B_CYAN, Style.B_GREEN]
    
    # Imprimimos de la capa más alta a la más baja
    for i in reversed(range(len(layers))):
        layer_nodes = set(layers[i])
        color = colors[i % len(colors)]
        
        line = colorize(f"L{i}: ", color + Style.BOLD)
        
        for idx, node in enumerate(all_nodes):
            if node in layer_nodes:
                # Nodo presente en este nivel
                node_str = f"[{str(node).center(cell_w-2)}]"
                line += colorize(node_str, color)
            else:
                # Camino de conexión vacío
                line += colorize("-" * cell_w, Style.BLUE)
            
            if idx < len(all_nodes) - 1:
                line += colorize("→", Style.BLUE)
        
        print(line)