import socket
import threading
import heapq
import json

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
        pq = [(0, inicio)]
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


def manejar_cliente(conn, addr, grafo):
    print(f"Conexión desde {addr}")
    data = conn.recv(1024).decode('utf-8')
    mensaje = json.loads(data)
    
    if mensaje['type'] == 'arista':
        origen = mensaje['origen']
        destino = mensaje['destino']
        peso = mensaje['peso']
        grafo.agregar_arista(origen, destino, peso)
        print(f"Arista agregada: {origen} -> {destino} con peso {peso}")
    
    elif mensaje['type'] == 'ruta':
        inicio = mensaje['inicio']
        fin = mensaje['fin']
        ruta, distancia = grafo.ruta_mas_corta(inicio, fin)
        respuesta = {'ruta': ruta, 'distancia': distancia}
        conn.send(json.dumps(respuesta).encode('utf-8'))
    
    conn.close()

def servidor_tcp(grafo, puerto=65432):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', puerto))
    server_socket.listen(5)
    print(f"Servidor escuchando en puerto {puerto}...")
    
    while True:
        conn, addr = server_socket.accept()
        cliente_thread = threading.Thread(target=manejar_cliente, args=(conn, addr, grafo))
        cliente_thread.start()

def cliente_tcp(mensaje, puerto=65432):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', puerto))
    client_socket.send(json.dumps(mensaje).encode('utf-8'))
    
    if mensaje['type'] == 'ruta':
        data = client_socket.recv(1024).decode('utf-8')
        respuesta = json.loads(data)
        print(f"Ruta: {respuesta['ruta']}, Distancia: {respuesta['distancia']}")
    
    client_socket.close()

if __name__ == "__main__":
    grafo = Grafo()

    servidor_thread = threading.Thread(target=servidor_tcp, args=(grafo,))
    servidor_thread.start()

    cliente_tcp({'type': 'arista', 'origen': 'A', 'destino': 'B', 'peso': 1})
    cliente_tcp({'type': 'arista', 'origen': 'B', 'destino': 'C', 'peso': 2})
    cliente_tcp({'type': 'arista', 'origen': 'A', 'destino': 'C', 'peso': 4})
    cliente_tcp({'type': 'arista', 'origen': 'C', 'destino': 'D', 'peso': 1})

    cliente_tcp({'type': 'ruta', 'inicio': 'A', 'fin': 'D'})
