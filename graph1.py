import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# Список обласних центрів України у зворотному порядку
cities = [
    "Ужгород", "Львів", "Рівне", "Тернопіль", "Луцьк", "Чернівці", "Хмельницький", "Вінниця", "Житомир",
    "Київ", "Чернігів", "Полтава", "Кропивницький", "Умань", "Одеса", "Ізмаїл", "Миколаїв",
    "Херсон", "Сімферопіль", "Запоріжжя", "Дніпро", "Донецьк", "Луганськ", "Харків"
]

# Відстані між основними центрами (в км)
distances = {
    ("Ужгород", "Львів"): 260,
    ("Львів", "Рівне"): 210, ("Львів", "Тернопіль"): 130,
    ("Рівне", "Луцьк"): 75, ("Рівне", "Хмельницький"): 200, ("Рівне", "Житомир"): 160,
    ("Тернопіль", "Луцьк"): 170, ("Тернопіль", "Хмельницький"): 110, ("Тернопіль", "Чернівці"): 140,
    ("Чернівці", "Хмельницький"): 190,
    ("Хмельницький", "Вінниця"): 120,
    ("Житомир", "Київ"): 140,
    ("Житомир", "Вінниця"): 130,
    ("Вінниця", "Умань"): 160,
    ("Київ", "Чернігів"): 150, ("Київ", "Полтава"): 340, ("Київ", "Кропивницький"): 300, ("Київ", "Умань"): 210,
    ("Умань", "Кропивницький"): 160, ("Умань", "Одеса"): 280, ("Умань", "Миколаїв"): 270,
    ("Одеса", "Ізмаїл"): 230, ("Одеса", "Миколаїв"): 130,
    ("Кропивницький", "Полтава"): 210, ("Кропивницький", "Дніпро"): 250, ("Кропивницький", "Миколаїв"): 200,
    ("Миколаїв", "Херсон"): 60,
    ("Херсон", "Сімферопіль"): 290, ("Херсон", "Запоріжжя"): 200,
    ("Запоріжжя", "Дніпро"): 80,
    ("Дніпро", "Донецьк"): 250,
    ("Полтава", "Дніпро"): 190, ("Полтава", "Харків"): 140,
    ("Харків", "Дніпро"): 220, ("Харків", "Донецьк"): 300,
    ("Донецьк", "Луганськ"): 150
}

# Координати обласних центрів
positions = {
    "Ужгород": (35, 350), "Львів": (85, 400), "Рівне": (150, 550), "Тернопіль": (130, 350),
    "Луцьк": (100, 530), "Чернівці": (140, 230), "Хмельницький": (200, 340), "Вінниця": (230, 300),
    "Житомир": (240, 490),
    "Київ": (300, 500), "Чернігів": (340, 600), "Полтава": (450, 450), "Кропивницький": (380, 300),
    "Умань": (290, 400), "Одеса": (290, 200), "Ізмаїл": (260, 100), "Миколаїв": (350, 220),
    "Херсон": (410, 205), "Сімферопіль": (450, 50), "Запоріжжя": (525, 200), "Дніпро": (500, 280),
    "Донецьк": (650, 390), "Луганськ": (700, 410), "Харків": (600, 470)
}


# Алгоритм Дейкстри
def dekstra_shortest_path(graph, source, target):
    return nx.shortest_path(graph, source=source, target=target, weight='weight')


# Створення графу
G = nx.Graph()

# Додавання вершин
for city in cities:
    G.add_node(city)

# Додавання ребер з вагами
for (city1, city2), distance in distances.items():
    G.add_edge(city1, city2, weight=distance)



# Аналіз графу
num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()
degree_centrality = nx.degree_centrality(G)
average_degree = sum(dict(G.degree()).values()) / num_nodes
print(f"Кількість вершин: {num_nodes}")
print(f"Кількість ребер: {num_edges}")
print("Ступінь вершин:")
for city, degree in dict(G.degree()).items():
    print(f"{city}: {degree}")
    
# Алгоритми пошуку
start_node = "Ужгород"
end_node = "Полтава"

# DFS
def dfs_iterative(graph, start_vertex):
    visited = set()
    visited_order = []  # Список для зберігання порядку відвіданих вершин
    # Використовуємо стек для зберігання вершин
    stack = [start_vertex]
    while stack:
        # Вилучаємо вершину зі стеку
        vertex = stack.pop()  
        if vertex not in visited:
            visited_order.append(vertex)
            # Відвідуємо вершину
            visited.add(vertex)
            # Додаємо сусідні вершини до стеку
            stack.extend(reversed(list(graph[vertex])))
    return visited_order

#BFS
def bfs_recursive(graph, queue, visited=None, visited_order=None):
    # Перевіряємо, чи існує множина відвіданих вершин, якщо ні, то ініціалізуємо нову
    if visited is None:
        visited = set()
    if visited_order is None:
        visited_order = []
    # Якщо черга порожня, завершуємо рекурсію
    if not queue:
        return visited_order
    # Вилучаємо вершину з початку черги
    vertex = queue.popleft()
    # Перевіряємо, чи відвідували раніше дану вершину
    if vertex not in visited:
        # Якщо не відвідували, додаємо вершину до списку відвіданих
        visited_order.append(vertex)
        # Додаємо вершину до множини відвіданих вершин.
        visited.add(vertex)
        # Додаємо невідвіданих сусідів даної вершини в кінець черги.
        queue.extend(set(graph.neighbors(vertex)) - visited)
    # Рекурсивний виклик функції з тією ж чергою та множиною відвіданих вершин
    return bfs_recursive(graph, queue, visited, visited_order)


dfs_path2 = dfs_iterative(G, start_node)            
dfs_path = list(nx.dfs_edges(G, source=start_node))
dfs_path = [start_node] + [v for u, v in dfs_path]

# BFS
bfs_path2 = bfs_recursive(G, deque([start_node]))
bfs_path = list(nx.bfs_edges(G, source=start_node))
bfs_path = [start_node] + [v for u, v in bfs_path]

print("\nШлях DFS:")
print(" -> ".join(dfs_path))
print("\nШлях DFS2:")
print(" -> ".join(dfs_path2))

print("\nШлях BFS:")
print(" -> ".join(bfs_path))
print("\nШлях BFS:")
print(" -> ".join(bfs_path2))

# Порівняння шляхів
dfs_path_set = set(dfs_path)
bfs_path_set = set(bfs_path)

print("\nВершини у шляху DFS, яких немає у шляху BFS:")
print(dfs_path_set - bfs_path_set)

print("\nВершини у шляху BFS, яких немає у шляху DFS:")
print(bfs_path_set - dfs_path_set)

shortest_path = dekstra_shortest_path(G, start_node, end_node)
print(f"Найкоротший шлях від {start_node} до {end_node}: {shortest_path}")

# Візуалізація графу
plt.figure(figsize=(15, 10))
nx.draw_networkx_nodes(G, positions, node_size=500, node_color='skyblue')
nx.draw_networkx_edges(G, positions, width=2)
nx.draw_networkx_labels(G, positions, font_size=10, font_family='sans-serif')

# Додавання ваг ребер
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, positions, edge_labels=edge_labels)

plt.title("Граф міжнародних(М-) автомобільних доріг між основними центрами України з відстанню між ними")
plt.show()