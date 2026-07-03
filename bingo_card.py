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
        Genera una cartilla de bingo de 9 columnas x 3 filas (formato bingo español tradicional)
        que cumple con las reglas oficiales:
        - Cada fila contiene exactamente 5 números y 4 espacios vacíos.
        - Cada columna contiene al menos un número (evita columnas vacías).
        - Los números en cada columna están ordenados de menor a mayor de arriba a abajo.
        - Un total de exactamente 15 números.
        
        Returns:
            Lista de listas con los números de la cartilla (None para espacios vacíos)
        """
        # Bucle de reintento hasta que encontremos una distribución válida de celdas
        while True:
            # 1. Decidir cuántos números colocar por columna.
            # Cada una de las 9 columnas debe tener al menos 1 número, y máximo 3 (debido a las 3 filas).
            # Total de números en la cartilla = 15.
            col_counts = [1] * 9  # Comenzamos con 1 número en cada una de las 9 columnas (quedan 6 por distribuir)
            
            # Distribuir los 6 números restantes aleatoriamente sin exceder el máximo de 3 por columna
            extra_pool = list(range(9))
            random.shuffle(extra_pool)
            extras_added = 0
            for col_idx in extra_pool:
                if extras_added < 6:
                    add = random.randint(1, 2)
                    if col_counts[col_idx] + add <= 3:
                        if extras_added + add <= 6:
                            col_counts[col_idx] += add
                            extras_added += add
                        else:
                            needed = 6 - extras_added
                            if col_counts[col_idx] + needed <= 3:
                                col_counts[col_idx] += needed
                                extras_added += needed
            
            # Verificar si logramos distribuir exactamente 15 celdas
            if sum(col_counts) != 15:
                continue
                
            # 2. Intentar asignar las filas de las columnas asegurando exactamente 5 números por fila
            # Representamos la matriz de celdas activas: 3 filas x 9 columnas
            grid = [[False] * 9 for _ in range(3)]
            row_counts = [0, 0, 0]
            
            # Buscaremos una solución válida usando Backtracking de forma muy rápida
            def solve(col):
                if col == 9:
                    # Condición de éxito: todas las filas deben tener exactamente 5 números
                    return all(r == 5 for r in row_counts)
                
                count = col_counts[col]
                # Todas las combinaciones posibles de filas para este recuento de columna (1, 2 o 3 celdas ocupadas)
                import itertools
                combos = list(itertools.combinations(range(3), count))
                random.shuffle(combos)  # Aleatorizar para variar las cartillas
                
                for combo in combos:
                    # Validar si al agregar estas filas superamos el límite de 5 números por fila
                    if any(row_counts[r] >= 5 for r in combo):
                        continue
                    
                    # Colocar
                    for r in combo:
                        grid[r][col] = True
                        row_counts[r] += 1
                        
                    if solve(col + 1):
                        return True
                        
                    # Deshacer (Backtrack)
                    for r in combo:
                        grid[r][col] = False
                        row_counts[r] -= 1
                        
                return False
            
            # Si encontramos una distribución de celdas válida, procedemos a llenarla con números
            if solve(0):
                card = [[None] * 9 for _ in range(3)]
                for col in range(9):
                    # Asignar los rangos oficiales de números para cada columna en el bingo español:
                    # Columna 1 (0): 1-9 (9 números)
                    # Columnas 2-8 (1-7): decenas completas (ej. Col 2: 10-19, Col 3: 20-29, etc.)
                    # Columna 9 (8): 80-90 (11 números)
                    if col == 0:
                        start_num = 1
                        end_num = 9
                    elif col == 8:
                        start_num = 80
                        end_num = 90
                    else:
                        start_num = col * 10
                        end_num = start_num + 9
                        
                    # Obtener números ordenados únicos para esta columna
                    num_needed = col_counts[col]
                    column_numbers = random.sample(range(start_num, end_num + 1), num_needed)
                    column_numbers.sort()
                    
                    # Colocar en la cartilla
                    placed = 0
                    for row in range(3):
                        if grid[row][col]:
                            card[row][col] = column_numbers[placed]
                            placed += 1
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
