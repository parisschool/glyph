from .utils import Style, colorize
from .trees import _build_tree_canvas

class _HeapNode:
    """Clase interna para 'engañar' al motor de árboles."""
    def __init__(self, array, index):
        self.val = array[index]
        l_idx = 2 * index + 1
        r_idx = 2 * index + 2
        self.left = _HeapNode(array, l_idx) if l_idx < len(array) else None
        self.right = _HeapNode(array, r_idx) if r_idx < len(array) else None

def visualize_heap(array):
    """Visualiza un arreglo como un árbol binario completo."""
    if not array:
        print(colorize("Heap vacío", Style.RED))
        return

    # Encabezado estético
    print(colorize("\n[ TIPO ARREGLO ]\n", Style.BOLD + Style.B_CYAN))
    indices = "  ".join(str(i).center(6) for i in range(len(array)))
    values = "  ".join(colorize(f"[{x}]".center(6), Style.B_GREEN) for x in array)
    print(indices)
    print(values)
    
    print(colorize("\n[ TIPO ÁRBOL ]\n", Style.BOLD + Style.B_CYAN))
    
    root = _HeapNode(array, 0)
    lines, *_ = _build_tree_canvas(root)
    for line in lines:
        print(line)

class MinHeap:
    """Implementación de MinHeap que usa el visualizador."""
    def __init__(self):
        self.heap = []

    def insert(self, val):
        self.heap.append(val)
        self.subir(len(self.heap) - 1)

    def subir(self, i):
        while i > 0:
            p = (i - 1) // 2
            if self.heap[i] < self.heap[p]:
                # Intercambiamos
                self.heap[i], self.heap[p] = self.heap[p], self.heap[i]
                i = p  # Seguimos subiendo desde la nueva posición del padre
            else:
                break

    def show(self):
        visualize_heap(self.heap)