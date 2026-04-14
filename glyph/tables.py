from .utils import Style, colorize

class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.count = 0

    def _hash(self, key):
        # Función de hash simple: suma de ASCII de caracteres mod size
        if isinstance(key, int):
            return key % self.size
        return sum(ord(c) for c in str(key)) % self.size

    def insert(self, key, value):
        idx = self._hash(key)
        
        # Si la llave ya existe, actualizamos el valor
        for i, (k, v) in enumerate(self.table[idx]):
            if k == key:
                self.table[idx][i] = (key, value)
                return
        
        # Si no existe, lo agregamos (Colisión si ya hay algo)
        self.table[idx].append((key, value))
        self.count += 1

    def show(self):
        visualize_hash_table(self.table)

    def search(self, key):
        # 1. Calcular en qué cubeta debería estar
        index = self._hash(key)
        bucket = self.table[index]
        
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                return bucket[i][1] # Devolvemos el valor
                
        return None # No se encontró
    
    def delete(self, key):
        # 1. Calcular el índice
        index = self._hash(key)
        bucket = self.table[index]
        
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                bucket.pop(i)
                return True # Borrado 
                
        return False # La llave no existía

    @property
    def load_factor(self):
        """Indica qué tan llena está la tabla."""
        return self.count / self.size

def visualize_hash_table(buckets):
    """
    Recibe una lista de listas (buckets).
    Ex: [[('key1', 'val1')], [], [('key2', 'val2'), ('key3', 'val3')]]
    """
    print(colorize("\n=== ESTRUCTURA DE HASH TABLE (CHAINING) ===", Style.BOLD + Style.CYAN))
    
    # Calculamos el ancho del índice para que todo esté alineado
    max_idx_len = len(str(len(buckets) - 1))

    for i, bucket in enumerate(buckets):
        idx_str = colorize(f"[{str(i).zfill(max_idx_len)}]", Style.B_YELLOW)
        
        if not bucket:
            print(f"{idx_str} -> " + colorize("None", Style.BLUE))
        else:
            # Construimos la cadena de colisiones
            chain = []
            for key, val in bucket:
                item = f"( {colorize(str(key), Style.B_GREEN)}: {val} )"
                chain.append(item)
            
            print(f"{idx_str} -> " + " -> ".join(chain))

import hashlib

class BloomFilter:
    def __init__(self, size=15, num_hashes=3):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def _get_hashes(self, item):
        """Genera múltiples índices usando diferentes sales."""
        indices = []
        for i in range(self.num_hashes):
            # Usamos MD5 con una sal diferente para cada función de hash
            hash_hex = hashlib.md5(f"{i}{item}".encode()).hexdigest()
            index = int(hash_hex, 16) % self.size
            indices.append(index)
        return indices

    def insert(self, item):
        indices = self._get_hashes(item)
        for idx in indices:
            self.bit_array[idx] = 1
        
        print(f"\nInsertando '{item}' -> Índices: {indices}")
        visualize_bloom(self.bit_array, hash_results=indices)

    def contains(self, item):
        indices = self._get_hashes(item)
        # Si TODOS los bits están en 1, "probablemente" está
        result = all(self.bit_array[idx] == 1 for idx in indices)
        
        status = colorize("POSIBLEMENTE ESTÁ", Style.B_GREEN) if result else colorize("NO ESTÁ", Style.B_RED)
        print(f"¿Contiene '{item}'? {status} (Chequeando índices: {indices})")
        return result
    
    def show(self, hash_results=None):
        """
        Visualiza el vector de bits. 
        'hash_results' puede ser una lista de índices para resaltar qué 
        bits se activaron en la última operación.
        """
        print(colorize("\n=== BLOOM FILTER (BIT VECTOR) ===", Style.BOLD + Style.CYAN))
        
        # Si el filtro es muy grande, lo cortamos para que no se vea mal en terminal
        display_size = min(len(self.bit_array), 32)
        
        indices = ""
        bits = ""
        
        for i in range(display_size):
            val = self.bit_array[i]
            indices += f" {i} ".center(5)
            
            # Lógica de colores
            if hash_results and i in hash_results:
                color = Style.B_YELLOW  # Resaltar bits recién calculados
            elif val:
                color = Style.B_GREEN   # Bit encendido
            else:
                color = Style.BLUE      # Bit apagado
                
            char = " [1] " if val else " [0] "
            bits += colorize(char.center(5), color)
        
        print(indices)
        print(bits)
        
        if len(self.bit_array) > 32:
            print(colorize(f"... (mostrando 32 de {len(self.bit_array)} bits) ...", Style.DIM))

def visualize_bloom(bit_array, hash_results=None):
    print(colorize("\n=== BLOOM FILTER (BIT VECTOR) ===", Style.BOLD + Style.CYAN))
    indices = ""
    bits = ""
    for i, val in enumerate(bit_array):
        indices += f" {i} ".center(5)
        color = Style.B_GREEN if val else Style.BLUE
        if hash_results and i in hash_results:
            color = Style.B_YELLOW #+ Style.BLACK
        char = " [1] " if val else " [0] "
        bits += colorize(char.center(5), color)
    print(indices)
    print(bits)