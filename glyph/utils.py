class Style:
    # Colores básicos
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BROWN = '\033[0;33m'
    
    # Estilos de texto
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    B_RED = '\033[91m'
    B_GREEN = '\033[92m'
    B_YELLOW = '\033[93m'
    B_BLUE = '\033[94m'
    B_MAGENTA = '\033[95m'
    B_CYAN = '\033[96m'
    
    # Reset (Obligatorio para dejar de pintar)
    END = '\033[0m'

def colorize(text, color_code):
    """Envuelve el texto en el color y lo resetea al final."""
    return f"{color_code}{text}{Style.END}"