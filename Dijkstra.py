import heapq
import sys

class Grafo:
    def __init__(self):
        self.nodos = {}
    
    def agregar_arista(self, origen, destino, peso):
        if origen not in self.nodos:
            self.nodos[origen] = []
        if destino not in self.nodos:
            self.nodos[destino] = []
        self.nodos[origen].append((peso, destino))
        self.nodos[destino].append((peso, origen))
    
    def dijkstra(self, inicio):
        distancias = {nodo: float('inf') for nodo in self.nodos}
        distancias[inicio] = 0
        pq = [(0, inicio)]  # cola de prioridad
        heapq.heapify(pq)
        predecesores = {nodo: None for nodo in self.nodos}
        
        while pq:
            distancia_actual, nodo_actual = heapq.heappop(pq)
            
            if distancia_actual > distancias[nodo_actual]:
                continue
            
            for peso, vecino in self.nodos[nodo_actual]:
                distancia = distancia_actual + peso
                
                if distancia < distancias[vecino]:
                    distancias[vecino] = distancia
                    predecesores[vecino] = nodo_actual
                    heapq.heappush(pq, (distancia, vecino))
        
        return distancias, predecesores

    def ruta_mas_corta(self, inicio, fin):
        distancias, predecesores = self.dijkstra(inicio)
        ruta = []
        nodo_actual = fin
        
        while nodo_actual is not None:
            ruta.insert(0, nodo_actual)
            nodo_actual = predecesores[nodo_actual]
        
        if ruta[0] == inicio:
            return ruta, distancias[fin]
        else:
            return None, float('inf')


if __name__ == "__main__":
    grafo = Grafo()
    grafo.agregar_arista('A', 'B', 3)
    grafo.agregar_arista('B', 'C', 1)
    grafo.agregar_arista('A', 'C', 5)
    grafo.agregar_arista('C', 'D', 1)
    
    inicio = 'A'
    fin = 'D'
    ruta, distancia = grafo.ruta_mas_corta(inicio, fin)
    if ruta:
        print(f"La ruta más corta de {inicio} a {fin} es: {' -> '.join(ruta)} con una distancia de {distancia}")
    else:
        print(f"No existe una ruta de {inicio} a {fin}")
