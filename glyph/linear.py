class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop() if self.items else None

    def show(self):
        visualize_stack(self.items)

class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        return self.items.pop(0) if self.items else None

    def show(self):
        visualize_queue(self.items)

def visualize_stack(elements):
    """Visualiza una pila verticalmente."""
    if not elements:
        print("Pila vacía")
        return
    
    width = max(len(str(e)) for e in elements) + 4
    print(" TOP ".center(width, " "))
    print("▼".center(width, " "))
    for e in reversed(elements): # El último entra es el primero sale
        print(f"| {str(e).center(width-4)} |")
        print("+" + "-"*(width-2) + "+")

def visualize_queue(elements):
    """Visualiza una cola horizontalmente con entrada y salida."""
    if not elements:
        print("Cola vacía")
        return
    
    body = " | ".join(str(e) for e in elements)
    border = "-" * (len(body) + 4)
    print(f"SALIDA <---  {body}  <--- ENTRADA")
    print(f"             {border}")