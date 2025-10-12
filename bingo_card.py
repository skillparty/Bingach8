"""
Módulo para generar cartillas de bingo aleatorias
"""

import random

class BingoCard:
    """Clase para representar y generar una cartilla de bingo"""
    
    def __init__(self, card_id=None):
        """
        Inicializa una cartilla de bingo con números aleatorios
        
        Args:
            card_id: ID único para la cartilla (opcional)
        """
        self.card_id = card_id
        self.numbers = self.generate_card()
        self.marked = set()  # Conjunto de números marcados
        
    def generate_card(self):
        """
        Genera una cartilla de bingo de 5x5 con números aleatorios
        Columnas: B(1-15), I(16-30), N(31-45), G(46-60), O(61-75)
        Pero adaptada para 90 números del bingo español
        
        Returns:
            Lista de listas con los números de la cartilla
        """
        # Cartilla de 5 columnas x 3 filas (formato bingo español tradicional)
        card = []
        
        # Dividir los 90 números en 9 columnas (10 números por columna)
        columns = []
        for col in range(9):
            start = col * 10 + 1
            end = start + 10
            # Seleccionar 3 números aleatorios de cada rango de 10
            column_numbers = random.sample(range(start, end), 3)
            column_numbers.sort()
            columns.append(column_numbers)
        
        # Organizar en 3 filas, cada fila con 5 números
        # Cada fila debe tener exactamente 5 números y 4 espacios vacíos
        for row_idx in range(3):
            row = []
            # Seleccionar 5 columnas aleatorias para esta fila
            selected_cols = random.sample(range(9), 5)
            selected_cols.sort()
            
            for col_idx in range(9):
                if col_idx in selected_cols:
                    row.append(columns[col_idx][row_idx])
                else:
                    row.append(None)  # Espacio vacío
            
            card.append(row)
        
        return card
    
    def mark_number(self, number):
        """
        Marca un número en la cartilla si existe
        
        Args:
            number: Número a marcar
            
        Returns:
            True si el número estaba en la cartilla, False si no
        """
        # Buscar el número en la cartilla
        for row in self.numbers:
            if number in row:
                self.marked.add(number)
                return True
        return False
    
    def is_marked(self, number):
        """Verifica si un número está marcado"""
        return number in self.marked
    
    def check_line(self):
        """
        Verifica si se completó una línea (fila completa)
        
        Returns:
            True si hay al menos una línea completa, False si no
        """
        for row in self.numbers:
            # Obtener solo los números válidos de la fila (sin None)
            valid_numbers = [num for num in row if num is not None]
            # Verificar si todos los números válidos están marcados
            if all(num in self.marked for num in valid_numbers):
                return True
        return False
    
    def check_bingo(self):
        """
        Verifica si se completó toda la cartilla (BINGO)
        
        Returns:
            True si todos los números están marcados, False si no
        """
        # Obtener todos los números válidos de la cartilla
        all_numbers = []
        for row in self.numbers:
            all_numbers.extend([num for num in row if num is not None])
        
        # Verificar si todos están marcados
        return all(num in self.marked for num in all_numbers)
    
    def get_numbers(self):
        """Retorna la lista de números de la cartilla"""
        return self.numbers
    
    def get_marked_numbers(self):
        """Retorna el conjunto de números marcados"""
        return self.marked
    
    def to_dict(self):
        """Convierte la cartilla a un diccionario para serialización"""
        return {
            'card_id': self.card_id,
            'numbers': self.numbers,
            'marked': list(self.marked)
        }
    
    @classmethod
    def from_dict(cls, data):
        """Crea una cartilla desde un diccionario"""
        card = cls(card_id=data.get('card_id'))
        card.numbers = data['numbers']
        card.marked = set(data.get('marked', []))
        return card
    
    def __str__(self):
        """Representación en string de la cartilla para debug"""
        result = f"Cartilla ID: {self.card_id}\n"
        for i, row in enumerate(self.numbers):
            row_str = []
            for num in row:
                if num is None:
                    row_str.append("  ")
                elif num in self.marked:
                    row_str.append(f"[{num:2d}]")
                else:
                    row_str.append(f" {num:2d} ")
            result += " ".join(row_str) + "\n"
        return result


def generate_unique_cards(num_cards):
    """
    Genera múltiples cartillas únicas
    
    Args:
        num_cards: Número de cartillas a generar
        
    Returns:
        Lista de cartillas BingoCard
    """
    cards = []
    for i in range(num_cards):
        card = BingoCard(card_id=i)
        cards.append(card)
    return cards


if __name__ == "__main__":
    # Test del generador de cartillas
    print("=== Test de generador de cartillas ===\n")
    
    # Generar una cartilla
    card = BingoCard(card_id=1)
    print(card)
    
    # Marcar algunos números
    print("\nMarcando números: 5, 17, 23, 45, 67, 89")
    card.mark_number(5)
    card.mark_number(17)
    card.mark_number(23)
    card.mark_number(45)
    card.mark_number(67)
    card.mark_number(89)
    
    print("\nCartilla después de marcar:")
    print(card)
    
    print(f"\n¿Tiene línea? {card.check_line()}")
    print(f"¿Tiene BINGO? {card.check_bingo()}")
    
    # Generar múltiples cartillas
    print("\n=== Generando 3 cartillas ===")
    cards = generate_unique_cards(3)
    for i, c in enumerate(cards):
        print(f"\nCartilla {i+1}:")
        print(c)
