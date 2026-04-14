import time
from glyph.trees import AVLTree
from glyph.heaps import MinHeap
from glyph.lists import SkipList
from glyph.tables import HashTable, BloomFilter
from glyph.linear import Stack, Queue
from glyph.utils import Style, colorize

def header(text):
    print("\n" + colorize(" " + text + " ", Style.B_BLUE + Style.RED + Style.BOLD).center(80, "="))

def test_everything():
    # 1. Árbol AVL
    header("TEST 1: ÁRBOL AVL (BALANCEO AUTOMÁTICO)")
    avl = AVLTree()
    for x in [10, 20, 30, 40, 50, 25]:
        print(f"Insertando {x}...")
        avl.insert(x)
    avl.show()

    # 2. Min Heap
    header("TEST 2: MIN HEAP (BASADO EN ARREGLO)")
    heap = MinHeap()
    for x in [50, 10, 40, 20, 5, 30]:
        heap.insert(x)
    heap.show()

    # 3. SkipList (Quad-Nodes)
    header("TEST 3: SKIPLIST (ESTRUCTURA PROBABILÍSTICA)")
    sk = SkipList(p=0.5)
    for x in [1, 10, 5, 20, 15, 30, 25]:
        sk.insert(x)
    sk.show()

    # 4. Hash Table & Bloom Filter
    header("TEST 4: TABLAS Y FILTROS")
    ht = HashTable(size=5)
    ht.insert("User1", "Paris")
    ht.insert("User2", "ITAM")
    ht.insert("User3", "Data Science") # Forzando colisiones
    ht.show()

    bf = BloomFilter(size=15)
    bf.insert("python")
    bf.contains("python")
    bf.contains("java")

    # 5. Estructuras Lineales
    header("TEST 5: PILA Y COLA")
    s = Stack()
    for x in ['A', 'B', 'C']: s.push(x)
    s.show()
    
    print("\n")
    q = Queue()
    for x in [1, 2, 3, 4]: q.enqueue(x)
    q.show()

if __name__ == "__main__":
    test_everything()
    print("\n" + colorize(" TODAS LAS PRUEBAS COMPLETADAS CON ÉXITO ", Style.B_GREEN))