import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt

class GrafoConVentana:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Generador de Grafos")

        self.numero_vertices = 0
        self.tabla_adyacencia = []

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.label = tk.Label(self.frame, text="Ingrese el número de vértices:")
        self.label.pack()

        self.entry = tk.Entry(self.frame)
        self.entry.pack()

        self.boton = tk.Button(self.frame, text="Aceptar", command=self.crear_tabla)
        self.boton.pack()

        self.root.mainloop()

    def crear_tabla(self):
        try:
            self.numero_vertices = int(self.entry.get())
            if self.numero_vertices <= 0:
                raise ValueError("El número de vértices debe ser mayor que cero.")
        except ValueError:
            tk.messagebox.showerror("Error", "Por favor, ingrese un número entero válido mayor que cero.")
            return

        self.tabla_adyacencia = [[0] * self.numero_vertices for _ in range(self.numero_vertices)]

        self.frame.destroy()

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.entries = []
        for i in range(self.numero_vertices):
            row_entries = []
            for j in range(self.numero_vertices):
                label = tk.Label(self.frame, text=f"{i} -> {j}: ")
                label.grid(row=i, column=2*j)
                entry = tk.Entry(self.frame)
                entry.grid(row=i, column=2*j+1)
                row_entries.append(entry)
            self.entries.append(row_entries)

        self.boton = tk.Button(self.frame, text="Crear Grafo", command=self.crear_grafo)
        self.boton.grid(row=self.numero_vertices, columnspan=2)

    def crear_grafo(self):
        try:
            for i in range(self.numero_vertices):
                for j in range(self.numero_vertices):
                    value = self.entries[i][j].get()
                    if value.isdigit():
                        valor = int(value)
                        if valor not in [0, 1]:
                            raise ValueError(f"El valor en la celda ({i}, {j}) debe ser 0 o 1.")
                        self.tabla_adyacencia[i][j] = valor
                    else:
                        raise ValueError(f"El valor en la celda ({i}, {j}) debe ser un número entero.")
        except ValueError as e:
            tk.messagebox.showerror("Error", str(e))
            return

        # Convertir la tabla de adyacencia en una lista de aristas
        aristas = []
        for i in range(self.numero_vertices):
            for j in range(i+1, self.numero_vertices):
                if self.tabla_adyacencia[i][j] != 0:
                    aristas.append((i, j))

        # Crear el grafo a partir de la lista de aristas
        grafo = nx.Graph()
        grafo.add_edges_from(aristas)

        # Mostrar el grafo
        self.mostrar_grafo(grafo)

        # Mostrar información del grafo
        self.mostrar_informacion_grafo(grafo)

    def mostrar_grafo(self, grafo):
        plt.figure(figsize=(6, 6))
        nx.draw(grafo, with_labels=True)
        plt.show()

    def mostrar_informacion_grafo(self, grafo):
        # Verificar si el grafo es euleriano
        es_euleriano = nx.is_eulerian(grafo)
        print("El grafo es euleriano:", es_euleriano)

        # Encontrar el recorrido euleriano
        if es_euleriano:
            recorrido_euleriano = list(nx.eulerian_circuit(grafo))
            print("Recorrido euleriano:", recorrido_euleriano)

        # Grados de cada vértice
        grados = grafo.degree()
        print("Grados de cada vértice:", grados)

        # Diámetro del grafo
        diametro = nx.diameter(grafo)
        print("Diámetro del grafo:", diametro)

        # Verificar si el grafo contiene un circuito hamiltoniano
        es_hamiltoniano, ciclo_hamiltoniano = self.verificar_hamiltoniano(grafo)
        print("El grafo es hamiltoniano:", es_hamiltoniano)
        if es_hamiltoniano:
            print("Ciclo hamiltoniano:", ciclo_hamiltoniano)

        # Búsqueda en anchura
        recorrido_anchura = list(nx.bfs_edges(grafo, source=0))
        print("Recorrido en anchura:", recorrido_anchura)

        # Búsqueda en profundidad
        recorrido_profundidad = list(nx.dfs_edges(grafo, source=0))
        print("Recorrido en profundidad:", recorrido_profundidad)

    def verificar_hamiltoniano(self, grafo):
        for nodo in grafo.nodes():
            ciclo = self.hallar_ciclo(grafo, nodo, nodo, [], set())
            if ciclo:
                return True, ciclo
        return False, []

    def hallar_ciclo(self, grafo, nodo_inicial, nodo_actual, camino, visitados):
        visitados.add(nodo_actual)
        camino.append(nodo_actual)
        if len(camino) == len(grafo.nodes()):
            return camino
        for vecino in grafo.neighbors(nodo_actual):
            if vecino not in visitados:
                ciclo = self.hallar_ciclo(grafo, nodo_inicial, vecino, camino[:], visitados.copy())
                if ciclo:
                    return ciclo
        return None

if __name__ == "__main__":
    GrafoConVentana()
