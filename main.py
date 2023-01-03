import networkx as nx
import planarity
from matplotlib import pyplot as plt
from itertools import compress, product
import pylab
import time


def graf(G, edges):
    n = 10000
    t1 = n * n
    print("Ввести рёбра сразу, нажмите 6?")
    nn = int(input())
    if nn != 6:
        edges = []
        print("Введите рёбра, чтобы прекратить ввод введите в одну из вершин 0, 0")
        for t in range(t1):
            print("Введите вершины v1 и v2")
            j, j1 = map(int, input().split())
            if (j > 0) and (j1 > 0):
                G.add_edge(j, j1)
            else:
                break
    else:
        G = nx.Graph(edges)
    print("Вершины")
    print(G.nodes())
    print("Рёбра")
    print(G.edges())
    return G


def mat_ritsa(G):
    print("Матрица")
    nod = G.nodes()
    edges = list(G.edges())
    n = len(nod)
    m = len(edges)
    adj = [[0] * n for _ in range(n)]
    man, ram = [], []
    for it in range(m):
        ram.append(edges[it][0])
        ram.append(edges[it][1])
        man.append(ram)
        ram = []
    print(man)
    for it in range(m):
        r = man[it][0]
        c = man[it][1]
        adj[r - 1][c - 1] = adj[c - 1][r - 1] = 1
    print([0], end='     ')
    print(sorted(nod))
    print('')
    for it in range(n):
        print([it + 1], '   ', adj[it])


def svy_zn(G):
    print("Граф связный")
    print(nx.is_connected(G))
    if not nx.is_connected(G):
        return -1
# -1

def pla_nar(G):
    print("Граф планарный")
    print(planarity.is_planar(G))
    if not planarity.is_planar(G):
        return -2
# -2

def li_st(G):
    t = 1
    print("Есть листья")
    nod = list(G.nodes)
    for i in range(len(nod)):
        if G.degree(nod[i]) == 1:
            print("Falls")
            t = -3
            break
    if t == 1:
        print("True")
    return t
# -3

def sharn(G):
    print("Есть шарниры")
    H = nx.DiGraph(G)
    tiil = sorted(nx.simple_cycles(H))
    for j in range(len(tiil)):
        if len(tiil[j]) == len(G.nodes):
            print("Falls")
            return 1
    print("True")
    return -4
# -4

def picture(G):
    # для начала надо выбрать способ "укладки" графа. Их много, возьмём для начала такой:
    pos = nx.spring_layout(G)
    plt.figure(facecolor='aqua')
    ax = plt.axes()
    ax.set_facecolor("red")
    # рисуем узлы красным цветом, задаём размер узла
    nx.draw_networkx_nodes(G, pos, node_color='#FFFF00', node_size=1500)
    # рисуем рёбра жёлтым
    nx.draw_networkx_edges(G, pos, edge_color='#8b4513')
    # Добавим ещё подписи к узлам
    nx.draw_networkx_labels(G, pos, font_size=25, font_family='Arial', font_color='#ff00ff')
    # по умолчанию график будет снабжён осями с координатами, здесь они бессмысленны, так что отключаем
    # plt.axis('off')
    pylab.show()


def dob_ver_reb(G):
    w = 100
    for t in range(w):
        print("Хотите добавить вершину или ребро?")
        print("1 - да")
        q1 = int(input())
        if q1 == 1:
            print("Введите вершины v1 и v2")
            j, j1 = map(int, input().split())
            G.add_edge(j, j1)
        else:
            break
    print("Вершины")
    print(G.nodes())
    print("Рёбра")
    print(G.edges())
    return G


def del_ver_reb(G):
    w = 100
    for t in range(w):
        print("Хотите удалить?")
        print("вершину 1, ребро 2")
        q1 = int(input())
        if q1 == 1:
            print("Введите вершину v1 ")
            j = int(input())
            G.remove_node(j)
        elif q1 == 2:
            print("Введите вершины v1 и v2")
            j, j1 = map(int, input().split())
            G.remove_edge(j, j1)
        else:
            break
    print("Вершины")
    print(G.nodes())
    print("Рёбра")
    print(G.edges())
    return G


def ver_shins(G):
    print("Порядок вершин верный")
    old = G.nodes
    old2 = max(old)
    old3 = sum(old)
    old4 = 0
    for i in range(1, old2 + 1):
        old4 = old4 + i
    if old3 != old4:
        print("Falls")
        return -5
    print("True")
    return 1
# -5

def grani(G):
    nod = list(G.nodes)
    edges = list(G.edges)
    url = []
    url2 = []
    url3 = []
    print("Количество граней", 2 + len(edges) - len(nod))
    for i in range(1, len(nod) + 1):
        rr = (nx.cycle_basis(G, i))
        # print(i, " = ", rr)
        for j in range(len(rr)):
            url.append(len(rr[j]))
        # print(url)
        for j in range(len(url)):
            url2.append(rr[j])
        url2.sort(key=len)
        sas = 0
        # print("kjshgfjksdhg", url2)
        for j1 in range(len(url2)):
            for j2 in range(len(url2)):
                # print(sorted(url2[j1]), "==", sorted(url2[j2]))

                if sorted(url2[j1]) != sorted(url2[j2]):
                    sas = sas + 1
                    # print(sas)
            if sas == len(url2) - 1:
                url3.append(url2[j1])
                # print("iqweryqoertqweru", url3)
            sas = 0
        url3.sort(key=len)  # print(url3)
        url = []
    url4 = url3  # print("iqweryqoertqweru")
    for j1 in range(len(url3)):
        for j2 in range(len(url3)):
            if sorted(url3[j1]) == sorted(url4[j2]) and j1 != j2:
                url4[j2] = [0]  # print(url4)
    url5 = []
    for j1 in range(len(url4)):
        if url4[j1] != [0]:
            url5.append(url4[j1])
    url5.sort(key=len)  # print(url5)
    ilm = []  # выбрать deg(v) - 1 минимальных граней в которых есть эта вершина и взять максимальный
    for po in range(len(url5)):
        ilm.append(len(url5[po]))  # print(max(ilm))
    nudez = []
    url6 = []
    for j0 in range(len(nod)):
        nudez.append(G.degree(nod[j0]))  # print(nod)  # print(nudez)
    oikl = 0
    oikl2 = []
    url7 = []
    for j1 in range(len(nudez)):
        for j2 in range(len(url5)):
            for j3 in range(len(url5[j2])):
                if nod[j1] == url5[j2][j3]:
                    oikl = oikl + 1
                    oikl2.append(j2)
        for yq in range(nudez[j1] - 1):
            url6.append(url5[oikl2[yq]])  # print(oikl2)
        gg1 = max(ilm)   # print(gg1)  # print(oikl2[0])  # print(url5)
        if len(oikl2) > 1:
            if len(url5[oikl2[len(oikl2) - 1]]) != gg1:
                url6.append(url5[oikl2[nudez[j1] - 1]])
        url7 = url7 + url6
        url6 = []
        oikl = 0
        oikl2 = []  # print(url7)
    for j1 in range(len(url7)):
        for j2 in range(len(url7)):
            if url7[j1] == url7[j2] and j1 != j2:
                url7[j2] = [0]  # print(url7)
    url8 = []
    for j1 in range(len(url7)):
        if url7[j1] != [0]:
            url8.append(url7[j1])  # print(url8)
    for j1 in range(len(nudez)):
        for j2 in range(len(url8)):
            for j3 in range(len(url8[j2])):
                if nod[j1] == url8[j2][j3]:
                    oikl = oikl + 1  # print(oikl, " != ", nudez[j1], "->", nod[j1])
        if oikl != nudez[j1]:
            oikl2.append(nod[j1])
        oikl = 0  # print(oikl2)
    H = nx.Graph(G)
    t1 = list(H.nodes)
    r = 0
    for j1 in range(len(t1)):
        for j2 in range(len(oikl2)):
            if t1[j1] == oikl2[j2]:
                r = r + 1
        if r != 1:
            H.remove_node(t1[j1])
        r = 0
    H = H.to_directed()
    yap = sorted(nx.simple_cycles(H))
    yap2 = []
    for j1 in range(len(yap)):
        if len(oikl2) == len(yap[j1]):
            for j2 in range(len(yap[j1])):
                a = sorted(yap[j1])
                b = sorted(oikl2)
                if a[j2] == b[j2]:
                    yap2 = yap[j1]
                    break
    url8.append(yap2)  # print(url8)
    return url8


def pruffs(rr):
    print("Все грани графа")
    rr.sort(key=len)
    print(rr)
    rr0, loi, loi2 = [], [], []
    for i in range(len(rr)):
        rr0.append(len(rr[i]) - 2)  # print(rr0)
    if sum(rr0) % 2 != 0:
        print("Невозможно разделить на 2 графа")
        print("Error")
    if sum(rr0) % 2 == 0:  # even sum
        for selectors in product([0, 1], repeat=len(rr0)):
            if sum(compress(rr0, selectors)) == sum(rr0) // 2:
                loi = list(compress(rr0, selectors))
                loi2 = list(compress(rr0, (not s for s in selectors)))  # print(loi, loi2)  # print(sum(loi), sum(loi2))
                break
    else:
        # это попытка вывода ошибки
        # raise ValueError("Can't partition into two parts with equal sums for {rr0!r}".format(**vars()))
        print("Error")
    fk, fk1, fk2, fk10, fk20, b = 0, 0, 0, 0, 0, 0
    maxk = max(rr0)
    for k in range(1, maxk + 1):
        for i in range(len(loi)):
            if loi[i] == k:
                fk1 = fk1 + 1
        for i in range(len(loi2)):
            if loi2[i] == k:
                fk2 = fk2 + 1
        for i in range(len(rr0)):
            if rr0[i] == k:
                fk = fk + 1
        if fk1 + fk2 == fk:
            print("При k = ", k + 2)
            print("fk1 + fk2 = fk")
            print(fk1, " + ", fk2, " = ", fk)
            print("Congate")
            fk10 = fk1 * k + fk10
            fk20 = fk2 * k + fk20
            fk1, fk2, fk = 0, 0, 0
        else:
            print("При k = ", k + 2)
            print("fk1 + fk2 = fk")
            print(fk1, " + ", fk2, " = ", fk)
            print("Error")
            b = b + 1
    print("fk10 = fk20")
    print(fk10, " = ", fk20)
    if fk10 != fk20:
        print("Error")
        b = b + 1
    else:
        print("Congate")
    if b != 0:
        print("Граф не удовлетворяет теореме Гринберга")
    else:
        print("Граф гамильтонов")


t0 = time.perf_counter()
# edges = [(1, 2), (3, 2), (3, 4), (1, 4), (1, 5), (5, 2), (5, 3), (4, 5), (1, 6), (6, 2), (7, 2), (7, 3), (3, 8), (8, 4),
# (4, 9), (9, 1)]
edges = [(10, 5), (10, 4), (1, 2), (1, 6), (2, 3), (2, 8), (8, 3), (4, 3), (4, 5), (1, 5), (2, 6), (3, 6), (5, 6), (3, 7),
(7, 4), (7, 9), (9, 8)]
# edges = [(1, 2), (2, 3), (4, 3), (4, 6), (5, 6), (1, 5), (1, 7), (7, 8), (8, 4)]
# edges = [(1, 2), (1, 9), (1, 10), (2, 3), (2, 8), (3, 4), (3, 7), (4, 6), (4, 5), (4, 7), (5, 10), (5, 6), (6, 7),
# (7, 9), (7, 8), (8, 9), (9, 10)]
# edges = [(2, 1), (2, 3), (2, 5), (2, 6), (2, 7), (2, 8), (4, 1), (4, 3), (4, 5),
# (4, 6), (4, 7), (4, 8), (1, 5), (3, 6), (7, 8)]
# edges = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8),
# (1, 10), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8),
# (9, 10), (10, 3), (10, 4), (10, 5), (10, 6), (10, 7), (10, 8)]

G = nx.Graph()
# создание графа
G = graf(G, edges)
# проверка на имена вершин
vers = ver_shins(G)
# матрица графа
mat_ritsa(G)
# проверка графа на связность
svy = svy_zn(G)
# проверка графа на планарность
pla = pla_nar(G)
# проверка на наличие листьев
lst = li_st(G)
# проверка на шарниры
sha = sharn(G)
# рисовка графа
picture(G)
# добавление вершин и рёбер
G = dob_ver_reb(G)
# удаление вершин и рёбер
G = del_ver_reb(G)
# все грани графа
rr = grani(G)
# проверка граней
pruffs(rr)
t1 = time.perf_counter()
print(t1 - t0)
