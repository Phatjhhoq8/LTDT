import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def draw_graph():
    global G, graph_type
    G.clear()
    try:
        edges = input_text.get("1.0", tk.END).strip().split("\n")
        num_nodes = int(node_count_entry.get().strip()) 
        for i in range(1, num_nodes+1): G.add_node(i)
        for edge in edges:
            parts = edge.split()
            if len(parts) < 2: continue
            u, v = map(int, parts[:2])
            w = float(parts[2]) if len(parts) > 2 else 1.0  
            if graph_type.get() == "undirected":
                G.add_edge(u, v, weight=w)
            else:
                G.add_edge(u, v, weight=w)
        update_graph_display()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Định dạng đầu vào không hợp lệ!\n{e}")

selected_node = None
pos = {}

def update_graph_display():
    global pos
    ax.clear()

    if not pos:
        pos = nx.spring_layout(G)

    if graph_type.get() == "directed":
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', ax=ax, 
                connectionstyle='arc3,rad=0.2', arrows=True, arrowstyle='-|>',node_size=1000)
    else:
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', ax=ax, arrows=False,node_size=1000)

    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', ax=ax)

    canvas.mpl_connect("button_press_event", on_click)
    canvas.mpl_connect("motion_notify_event", on_drag)
    canvas.mpl_connect("button_release_event", on_release)

    canvas.draw()

def on_click(event):
    global selected_node
    if event.inaxes is None:
        return
    for node, (x, y) in pos.items():
        if abs(x - event.xdata) < 0.05 and abs(y - event.ydata) < 0.05:
            selected_node = node
            break

def on_drag(event):
    global selected_node
    if selected_node is not None and event.inaxes:
        pos[selected_node] = (event.xdata, event.ydata)
        update_graph_display()

def on_release(event):
    global selected_node
    selected_node = None
def deg():
    n = int(node_count_entry.get().strip())
    degree_info = ""
    if graph_type.get() == "undirected":
        for i in range(1, n + 1):
            degree = G.degree(i)
            degree_info += f"Nút {i} có bậc là: {degree}\n"
    else:
        for i in range(1, n + 1):
            out_degree = G.out_degree(i)
            in_degree = G.in_degree(i)
            degree_info += f"Nút {i} có bậc ra là: {out_degree} và bậc vào là: {in_degree}\n"
    return degree_info
def neighbour():
    n = int(node_count_entry.get().strip())
    neighbour_info = ""
    for i in range(1, n + 1):
        neighbors = list(G.neighbors(i))
        neighbour_info += f"Nút {i} kề với các đỉnh: {', '.join(map(str, neighbors))}\n"
    return neighbour_info
def graph_info():
    messagebox.showinfo("Thông tin đồ thị :",f"""Thông tin của đồ thị:\nBậc của các đỉnh là:\n{deg()}\nCác đỉnh kề với nó là:\n  {neighbour()}""")

def bfs():
    try:
        start = int(start_node_entry.get())
        visited = list(nx.bfs_tree(G, start).nodes)
        messagebox.showinfo("Duyệt BFS", f"Thứ tự duyệt: {' -> '.join(map(str, visited))}")
    except:
        messagebox.showerror("Lỗi", "Vui lòng nhập đỉnh hợp lệ!")

def dfs():
    try:
        start = int(start_node_entry.get())
        visited = list(nx.dfs_tree(G, start).nodes)
        messagebox.showinfo("Duyệt DFS", f"Thứ tự duyệt: {' -> '.join(map(str, visited))}")
    except:
        messagebox.showerror("Lỗi", "Vui lòng nhập đỉnh hợp lệ!")

def check_cycle():
    try:
        cycle = nx.find_cycle(G, orientation='ignore')
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=10, font_weight="bold")
        cycle_edges = [tuple(cycle[i][:2]) for i in range(len(cycle))]
        messagebox.showinfo("Chu trình", f"Đồ thị có chu trình: {cycle_edges}")
        nx.draw_networkx_edges(G, pos, edgelist=cycle_edges, edge_color='r', width=2)
        plt.show()
    except nx.NetworkXNoCycle:
        messagebox.showinfo("Chu trình", "Đồ thị không có chu trình")

def find_connected_components():
    components = list(nx.connected_components(G)) if graph_type.get() == "undirected" else list(nx.strongly_connected_components(G))
    messagebox.showinfo("Thành phần liên thông", f"Các thành phần: {components}")

def add_placeholder(entry, placeholder_text):
    entry.insert(0, placeholder_text)
    entry.bind("<FocusIn>", lambda event: clear_placeholder(entry, placeholder_text))
    entry.bind("<FocusOut>", lambda event: restore_placeholder(entry, placeholder_text))

def clear_placeholder(entry, placeholder_text):
    if entry.get() == placeholder_text:
        entry.delete(0, tk.END)
        entry.config(fg="black")

def restore_placeholder(entry, placeholder_text):
    if not entry.get():
        entry.insert(0, placeholder_text)
        entry.config(fg="gray")
def transGraph(state):
    global G, graph_type
    G = nx.Graph() if state == "undirected" else nx.DiGraph()
    graph_type.set(state)
def shortest_path(state):
    try:
        start = int(start_node_entry.get())
        end = int(end_node_entry.get())
        if state=="dijkstra":
            path = nx.dijkstra_path(G, source=start, target=end, weight='weight')
            length = nx.dijkstra_path_length(G, source=start, target=end, weight='weight')
            messagebox.showinfo(f"Đường đi ngắn nhất từ {start} đến {end}", 
                                f"Đường đi ngắn nhất: {' -> '.join(map(str, path))}\nĐộ dài đường đi: {length}")
        elif state=="bellman":
            lengths, paths = nx.single_source_bellman_ford(G, start, weight='weight')
            if end in paths:
                path = paths[end]
                length = lengths[end]
                messagebox.showinfo(f"Đường đi ngắn nhất từ {start} đến {end}",
                                    f"Đường đi ngắn nhất: {' -> '.join(map(str, path))}\nĐộ dài đường đi: {length}")
            else:
                messagebox.showerror("Lỗi", "Không có đường đi giữa các đỉnh này.")
        elif state=="floyd":
            dist_matrix = nx.floyd_warshall(G, weight='weight')
            if end in dist_matrix[start]:
                length = dist_matrix[start][end]
                messagebox.showinfo(f"Đường đi ngắn nhất từ {start} đến {end}",
                                    f"Độ dài đường đi: {length}")
            else:
                messagebox.showerror("Lỗi", "Không có đường đi giữa các đỉnh này.")
    except nx.NetworkXNoPath:
        messagebox.showerror("Lỗi", "Không có đường đi giữa các đỉnh này.")
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập đúng số đỉnh.")
root = tk.Tk()
root.title("Graph Editor")
root.geometry("1000x600")
root.configure(bg="#f5f5f5")

G = nx.Graph()
graph_type = tk.StringVar(value="undirected")

main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

left_frame = tk.Frame(main_frame, width=300, bg="#f0f0f0", padx=10, pady=10)
left_frame.pack(side=tk.LEFT, fill=tk.Y)
right_frame = tk.Frame(main_frame, bg="#ffffff", padx=10, pady=10)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

graph_type_frame = tk.Frame(left_frame, bg="#f0f0f0")
graph_type_frame.pack(pady=5)
tk.Radiobutton(graph_type_frame, text="Vô hướng", variable=graph_type, value="undirected", bg="#f0f0f0",command=lambda: transGraph("undirected")).pack(side=tk.LEFT)
tk.Radiobutton(graph_type_frame, text="Có hướng", variable=graph_type, value="directed", bg="#f0f0f0",command=lambda: transGraph("directed")).pack(side=tk.LEFT)

tk.Label(left_frame, text="Số đỉnh:", bg="#f0f0f0").pack(anchor="w")
node_count_entry = tk.Entry(left_frame, fg="gray")
node_count_entry.pack(fill=tk.X)
add_placeholder(node_count_entry, "Nhập số đỉnh")

tk.Label(left_frame, text="Dữ liệu đồ thị:", bg="#f0f0f0").pack(anchor="w")
input_text = tk.Text(left_frame, height=5)
input_text.pack(fill=tk.X)


draw_button = tk.Button(left_frame, text="Vẽ đồ thị", command=draw_graph, bg="#00ceff", fg="white")
draw_button.pack(fill=tk.X, pady=5)

tk.Label(left_frame, text="Đỉnh bắt đầu:", bg="#f0f0f0").pack(anchor="w")
start_node_entry = tk.Entry(left_frame, fg="gray")
start_node_entry.pack(fill=tk.X)
add_placeholder(start_node_entry, "Nhập đỉnh bắt đầu")
tk.Label(left_frame, text="Đỉnh kết thúc:", bg="#f0f0f0").pack(anchor="w")
end_node_entry = tk.Entry(left_frame, fg="gray")
end_node_entry.pack(fill=tk.X)
add_placeholder(end_node_entry, "Nhập đỉnh kết thúc")
buttons = [
    ("Thông tin đồ thị", graph_info),
    ("Duyệt BFS", bfs),
    ("Duyệt DFS", dfs),
    ("Tính chu trình", check_cycle),
    ("Thành phần liên thông", find_connected_components),
    ("Đường đi ngắn nhất trên đồ thị(Dijkstra)",lambda:shortest_path("dijkstra")),
    ("Đường đi ngắn nhất trên đồ thị(Bellman Ford)",lambda:shortest_path("bellman")),
    ("Đường đi ngắn nhất trên đồ thị(Floyd Warshall)",lambda:shortest_path("floyd"))
]

for text, command in buttons:
    btn = tk.Button(left_frame, text=text, command=command, bg="#00ceff", fg="white", padx=10, pady=5, border=0)
    btn.pack(fill=tk.X, pady=2)

fig, ax = plt.subplots(figsize=(5, 4))
canvas = FigureCanvasTkAgg(fig, master=right_frame)
canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)

root.mainloop()
