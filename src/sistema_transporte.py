import heapq

class SistemaTransporteInteligente:
    def __init__(self):
        # 1. BASE DE CONOCIMIENTO (Reglas de conexión y costos)
        # Representa: "Si existe una ruta de X a Y, el tiempo estimado es T"
        # g(n): Costo real del trayecto
        self.grafo = {
            'Portal Norte': {'Calle 100': 10, 'Suba': 15},
            'Calle 100': {'Portal Norte': 10, 'Calle 72': 5, 'Héroes': 3},
            'Suba': {'Portal Norte': 15, 'Calle 100': 8},
            'Héroes': {'Calle 100': 3, 'Calle 72': 4, 'Calle 26': 10},
            'Calle 72': {'Calle 100': 5, 'Héroes': 4, 'Jiménez': 12},
            'Calle 26': {'Héroes': 10, 'Jiménez': 6},
            'Jiménez': {'Calle 72': 12, 'Calle 26': 6, 'Portal Sur': 15},
            'Portal Sur': {'Jiménez': 15}
        }

        # 2. HEURÍSTICA (Conocimiento a priori)
        # h(n): Estimación de tiempo "en línea recta" hasta el Portal Sur
        self.heuristica = {
            'Portal Norte': 45,
            'Calle 100': 30,
            'Suba': 40,
            'Héroes': 25,
            'Calle 72': 20,
            'Calle 26': 15,
            'Jiménez': 10,
            'Portal Sur': 0
        }

    def obtener_vecinos(self, nodo):
        return self.grafo.get(nodo, {})

    def busqueda_a_estrella(self, inicio, destino):
        # Priority Queue: (f_score, g_score, nodo_actual, camino)
        # f(n) = g(n) + h(n)
        open_set = []
        heapq.heappush(open_set, (self.heuristica[inicio], 0, inicio, [inicio]))
        
        visitados = {} # Nodo: g_score mínimo encontrado

        print(f"\n--- Iniciando búsqueda desde {inicio} hasta {destino} ---")

        while open_set:
            f, g, actual, camino = heapq.heappop(open_set)

            # Si llegamos al destino, retornamos el resultado
            if actual == destino:
                return camino, g

            # Si ya visitamos este nodo con un costo menor, lo ignoramos
            if actual in visitados and visitados[actual] <= g:
                continue
            
            visitados[actual] = g

            # Explorar conexiones (Reglas de la Base de Conocimiento)
            for vecino, costo_tramo in self.obtener_vecinos(actual).items():
                nuevo_g = g + costo_tramo
                nuevo_f = nuevo_g + self.heuristica.get(vecino, 999)
                
                nuevo_camino = camino + [vecino]
                heapq.heappush(open_set, (nuevo_f, nuevo_g, vecino, nuevo_camino))

        return None, float('inf')

# --- BLOQUE PRINCIPAL PARA EJECUCIÓN ---
if __name__ == "__main__":
    sistema = SistemaTransporteInteligente()
    
    # Definir puntos de prueba
    punto_a = 'Suba'
    punto_b = 'Calle brayan'
    
    ruta, tiempo = sistema.busqueda_a_estrella(punto_a, punto_b)
    
    print("-" * 50)
    if ruta:
        print(f"✅ ¡RUTA ENCONTRADA!")
        print(f"📍 Trayecto: {' -> '.join(ruta)}")
        print(f"⏱️ Tiempo total estimado: {tiempo} minutos")
    else:
        print("❌ No se encontró una ruta válida.")
    print("-" * 50)