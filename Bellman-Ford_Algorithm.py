import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
import random

# Реализация алгоритма Беллмана-Форда
def bellman_ford(graph, start):
    # Инициализация расстояний
    vertices = graph.nodes()
    dist = {vertex: float('inf') for vertex in vertices}
    dist[start] = 0
    # Релаксация рёбер
    for _ in range(len(vertices) - 1):
        for u, v, weight in graph.edges(data=True):
            if dist[u] != float('inf') and dist[u] + weight['weight'] < dist[v]:
                dist[v] = dist[u] + weight['weight']
    # Проверка наличия циклов с отрицательными суммами весов
    for u, v, weight in graph.edges(data=True):
        if dist[u] != float('inf') and dist[u] + weight['weight'] < dist[v]:
            show_error_window("Граф содержит циклы с отрицательной суммой весов.")
            return
    return dist

# Запуск алгоритма и визуализация результатов
def run_algorithm(graph, start_vertex):
    distances = bellman_ford(graph, start_vertex)

    # Разрешает редактирование текстового поля
    result_text.config(state=tk.NORMAL)

    result_text.delete(1.0, tk.END)

    result_text.insert(tk.END, "Кратчайшие расстояния от вершины {}:\n".format(start_vertex))
    for vertex, distance in distances.items():
        result_text.insert(tk.END, "Вершина {}: {}\n".format(vertex, distance))

    # Запрещает редактирование текстового поля
    result_text.config(state=tk.DISABLED)
    save_results_to_file(distances)
    draw_graph(graph, distances, start_vertex)

 # Визуализация графа
def draw_graph(graph, distances, start_vertex):
    pos = nx.random_layout(graph, seed=random.seed())  # генерирует случайное распределение вершин графа для их позиционирования на плоскости.
    nx.draw(graph, pos, with_labels=True, node_color='skyblue', node_size=800, font_size=8,
            font_color='black', font_weight='bold', edge_color='gray')

    nx.draw_networkx_edge_labels(graph, pos, edge_labels={(u, v): str(data['weight']) for u, v, data in graph.edges(data=True)})

    nx.draw_networkx_nodes(graph, pos, nodelist=[start_vertex], node_color='limegreen', node_size=800)

    plt.title('Граф с кратчайшим путем', fontsize=12, color='darkblue')
    plt.show()

# Обработчик нажатия кнопки "Запустить алгоритм"
def on_run_button_click():
    # Получает текст из текстовых виджетов
    graph_str = graph_entry.get("1.0", tk.END)
    start_vertex = int(start_entry.get())

    # чтобы создать граф на основе введенных пользователем данных.
    graph = create_graph_from_string(graph_str)
    run_algorithm(graph, start_vertex)

# Создание графа из строки
def create_graph_from_string(graph_str):
    graph = nx.DiGraph() #встроенная функция показывает сколько вершин и ребер
    lines = graph_str.strip().split('\n') # из строки список
    for line in lines:
        u, v, weight = map(int, line.split())
        graph.add_edge(u, v, weight=weight)
    return graph  # DiGraph with x nodes and y edges

def save_results_to_file(distances):
    filename = "results.txt"
    with open(filename, 'w') as file:
        file.write("Кратчайшие расстояния:\n")
        for vertex, distance in distances.items():
            file.write("Вершина {}: {}\n".format(vertex, distance))
# Сохранен ие строки графа в файл
def save_to_file():
    graph_str = graph_entry.get("1.0", tk.END)
    filename = file_entry.get()

    with open(filename, 'w') as file:
        file.write(graph_str)

# Загрузка графа из файла
def load_from_file():
    filename = file_entry.get()

    try:
        with open(filename, 'r') as file:
            graph_str = file.read()
            graph_entry.delete("1.0", tk.END)
            graph_entry.insert(tk.END, graph_str)
    except FileNotFoundError:
        print("Файл не найден.")


def show_error_window(message):
    error_window = tk.Toplevel(root)
    error_window.title("Ошибка")

    error_label = ttk.Label(error_window, text=message, font=('Helvetica', 12), foreground='red')
    error_label.pack(padx=20, pady=20)

    ok_button = ttk.Button(error_window, text="OK", command=error_window.destroy)
    ok_button.pack(pady=10)

    error_window.focus_set()
    error_window.grab_set()
    error_window.wait_window()

# Создание основного окна
root = tk.Tk()
root.title("Bellman-Ford Algorithm")
root.geometry("500x700")
root.configure(bg='darkgray')

# Создание и размещение элементов интерфейса
style = ttk.Style()
style.configure("TButton", padding=10, relief="flat", font=('Helvetica', 10))
style.configure("TLabel", padding=5, font=('Helvetica', 10))
style.configure("TEntry", padding=5, font=('Helvetica', 10))

graph_label = ttk.Label(root, text="Введите граф (u v weight):")
graph_label.pack(pady=10)

graph_entry = tk.Text(root, height=5, width=40)
graph_entry.pack(pady=10)

start_label = ttk.Label(root, text="Введите начальную вершину:")
start_label.pack(pady=5)

start_entry = ttk.Entry(root)
start_entry.pack(pady=5)

run_button = ttk.Button(root, text="Запустить алгоритм", command=on_run_button_click)
run_button.pack(pady=10)

result_text = tk.Text(root, height=10, width=40, state=tk.DISABLED)
result_text.pack(pady=10)

file_label = ttk.Label(root, text="Имя файла:")
file_label.pack(pady=5)

file_entry = ttk.Entry(root)
file_entry.pack(pady=5)

save_button = ttk.Button(root, text="Сохранить в файл", command=save_to_file)
save_button.pack(pady=5)

load_button = ttk.Button(root, text="Загрузить из файла", command=load_from_file)
load_button.pack(pady=10)

root.mainloop()
