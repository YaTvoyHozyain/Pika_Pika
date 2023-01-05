import networkx as nx
import planarity
from matplotlib import pyplot as plt
from itertools import compress, product
import pylab
import pygame
from itertools import zip_longest
import time


def func_chunk_itertools(lst):
    i_ = iter(lst)
    return list(zip_longest(i_, i_))


def isBetween(a, b, c):
    crossproduct = (c[1] - a[1]) * (b[0] - a[0]) - (c[0] - a[0]) * (b[1] - a[1])
    if abs(crossproduct) > 1000:
        return False
    dotproduct = (c[0] - a[0]) * (b[0] - a[0]) + (c[1] - a[1]) * (b[1] - a[1])
    if dotproduct < 0:
        return False
    squaredlengthba = (b[0] - a[0]) * (b[0] - a[0]) + (b[1] - a[1]) * (b[1] - a[1])
    if dotproduct > squaredlengthba:
        return False
    return True


def graf(G, edges):
    n = 10000
    t1 = n * n
    print("Ввести рёбра сразу, нажмите 6?")
    # nn = int(input())
    nn = 6
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


def svy_zn(G):
    print("Граф связный")
    print(nx.is_connected(G))
    if not nx.is_connected(G):
        return False
    return True
# -1


def pla_nar(G):
    print("Граф планарный")
    print(planarity.is_planar(G))
    if not planarity.is_planar(G):
        return False
    return True
# -2


def li_st(G):
    print("Есть листья")
    nod = list(G.nodes)
    for i in range(len(nod)):
        if G.degree(nod[i]) == 1:
            print("True")
            return False
    print("False")
    return True
# -3


def sharn(G):
    print("Есть шарниры")
    H = nx.DiGraph(G)
    tiil = sorted(nx.simple_cycles(H))
    for j in range(len(tiil)):
        if len(tiil[j]) == len(G.nodes):
            print("False")
            return True
    print("True")
    return False
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


def proverki(G):
    t = True
    if t:
        # проверка на имена вершин
        t = ver_shins(G)
    if t:
        # проверка графа на связность
        t = svy_zn(G)
    if t:
        # проверка графа на планарность
        t = pla_nar(G)
    if t:
        # проверка на наличие листьев
        t = li_st(G)
    if t:
        # проверка на шарниры
        t = sharn(G)
    if t:
        # рисовка графа
        # picture(G)
        # все грани графа
        rr = grani(G)
        # проверка граней
        pruffs(rr)


def ver_shins(G):
    print("Порядок вершин верный")
    old = G.nodes
    old2 = max(old)
    old3 = sum(old)
    old4 = 0
    for i in range(1, old2 + 1):
        old4 = old4 + i
    if old3 != old4:
        print("False")
        return False
    print("True")
    return True
# -5


def grani(G):
    nod = list(G.nodes)
    edges = list(G.edges)
    url = []
    url2 = []
    url3 = []
    # print("Количество граней", 2 + len(edges) - len(nod))
    for i in range(1, len(nod) + 1):
        rr = (nx.cycle_basis(G, nod[i-1]))  # print(i, " = ", rr)
        for j in range(len(rr)):
            url.append(len(rr[j]))  # print(url)
        for j in range(len(url)):
            url2.append(rr[j])
        # url2.sort(key=len)
        sas = 0  # print("kjshgfjksdhg", url2)
        for j1 in range(len(url2)):
            for j2 in range(len(url2)):
                # print(sorted(url2[j1]), "==", sorted(url2[j2]))
                if sorted(url2[j1]) != sorted(url2[j2]):
                    sas = sas + 1  # print(sas)
            if sas == len(url2) - 1:
                url3.append(url2[j1])  # print("iqweryqoertqweru", url3)
            sas = 0
        for i in range(len(url3) - 1):
            if len(url3[i]) > len(url3[i + 1]):
                tau = url3[i]
                url3[i] = url3[i + 1]
                url3[i + 1] = tau
                i = -1
        # print(url3)
        url3.sort(key=len)  # print(url3)
        # print(url3)
        url = []  # print(url3)
    url4 = url3  # print("iqweryqoertqweru")
    for j1 in range(len(url3)):
        for j2 in range(len(url3)):
            if sorted(url3[j1]) == sorted(url4[j2]) and j1 != j2:
                url4[j2] = [0]  # print(url4)
    url5 = []
    for j1 in range(len(url4)):
        if url4[j1] != [0]:
            url5.append(url4[j1])
    url5.sort(key=len)
    # for po in range(len(url5)):
    #     if url5[po] == [2, 3, 4, 5, 1]:
    #         url5[po] = [0]
    # print(url5)
    ilm = []  # выбрать deg(v) - 1 минимальных граней в которых есть эта вершина и взять максимальный
    for po in range(len(url5)):
        ilm.append(len(url5[po]))  # print(max(ilm))
    nudez = []
    url6 = []
    for j0 in range(len(nod)):
        nudez.append(G.degree(nod[j0]))

    # print(nod)
    # print(nudez)
    oikl2 = []
    url7 = []
    for j1 in range(len(nudez)):
        for j2 in range(len(url5)):
            for j3 in range(len(url5[j2])):
                if nod[j1] == url5[j2][j3]:
                    oikl2.append(j2)
        for yq in range(nudez[j1] - 1):
            url6.append(url5[oikl2[yq]])
        # print(url6)
        # print(oikl2)
        gg1 = max(ilm)  # print(gg1)  # print(oikl2[0])  # print(url5)
        if len(oikl2) > 1:
            if len(url5[oikl2[len(oikl2) - 1]]) != gg1:
                url6.append(url5[oikl2[nudez[j1] - 1]])  # print(url6)
        url7 = url7 + url6
        # print(url7)
        url6 = []
        oikl2 = []  # print(url7)
    oikl = 0
    for j1 in range(len(url7)):
        for j2 in range(len(url7)):
            if url7[j1] == url7[j2] and j1 != j2:
                url7[j2] = [0]  # print(url7)
    url8 = []
    for j1 in range(len(url7)):
        if url7[j1] != [0]:
            url8.append(url7[j1])
    url8.sort(key=len)  # print(url8)
    url10 = []
    for j in range(len(url8)):
        url10.append(len(url8[j]))  # print(url10)
    ttre = []
    for j in range(len(url10) - 1):
        if url10[j] < url10[j + 1]:
            ttre.append(url8[j + 1])   # print(ttre)
    ttre1 = []
    ttre2 = []
    for j in range(len(ttre)):
        ttre1.append(sum(ttre[j]))
        ttre2.append(len(ttre[j]))  # print(ttre1)  print(ttre2)
    ttre3 = []
    for j in range(len(ttre)):
        ttre3.append(ttre1[j] // ttre2[j])  # print(ttre3)
    hight = []
    t = 0
    url9 = []
    if len(url8) >= 2 + len(edges) - len(nod):
        for j1 in range(len(url8) - 1 - len(edges) + len(nod)):
            find = min(ttre3)
            ttre3.remove(min(ttre3))
            for j in range(len(ttre1)):
                if ttre1[j] // ttre2[j] == find:
                    hight.append(ttre[j])  # print(hight)
        for j2 in range(len(url8)):
            for j3 in range(len(hight)):
                if url8[j2] != hight[j3]:
                    t = t + 1
            if t == len(hight):
                url9.append(url8[j2])
            t = 0
    else:
        url9 = url8  # print(url9)

    for j1 in range(len(nudez)):
        for j2 in range(len(url9)):
            for j3 in range(len(url9[j2])):
                if nod[j1] == url9[j2][j3]:
                    oikl = oikl + 1  # print(oikl, " != ", nudez[j1], "->", nod[j1])
        if oikl < nudez[j1]:
            oikl2.append(nod[j1])
        oikl = 0
    # print(oikl2)
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
    # print(oikl2)
    # print(yap2)
    url9.append(yap2)  # print(url8)
    return url9


def pruffs(rr):
    t = True
    print("")
    # print("Все грани графа")
    rr.sort(key=len)
    # print(rr)
    rr0, loi, loi2 = [], [], []
    for i in range(len(rr)):
        rr0.append(len(rr[i]) - 2)  # print(rr0)
    if sum(rr0) % 2 != 0:
        print("Невозможно разделить на 2 половины")
        t = False
        print("Error")
        print("Граф не удовлетворяет теореме Гринберга")
        print("")
    if t:
        if sum(rr0) % 2 == 0:  # even sum
            for selectors in product([0, 1], repeat=len(rr0)):
                if sum(compress(rr0, selectors)) == sum(rr0) // 2:
                    loi = list(compress(rr0, selectors))
                    loi2 = list(compress(rr0, (not s for s in selectors)))  # print(loi, loi2)  # print(sum(loi), sum(loi2))
                    break
        else:
            t = False
    if t:
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
                print("")
                fk10 = fk1 * k + fk10
                fk20 = fk2 * k + fk20
                fk1, fk2, fk = 0, 0, 0
            else:
                print("При k = ", k + 2)
                print("fk1 + fk2 = fk")
                print(fk1, " + ", fk2, " = ", fk)
                print("Error")
                print("")
                b = b + 1
        print("Сумма половин графа")
        print("fk10 = fk20")
        print(fk10, " = ", fk20)
        if fk10 != fk20:
            print("Error")
            print("")
            b = b + 1
        else:
            print("Congate")
            print("")
        if b != 0:
            print("Граф не удовлетворяет теореме Гринберга")
            print("")
        else:
            print("Граф гамильтонов")
            print("")


def main(edges):
    t0 = time.perf_counter()
    G = nx.Graph()
    # создание графа
    G = graf(G, edges)
    # обязатедбные вещи
    proverki(G)
    t1 = time.perf_counter()
    print(t1 - t0)


def vis():
    W, H = 800, 600
    pygame.init()
    sc = pygame.display.set_mode((W, H), pygame.RESIZABLE)
    pygame.display.set_caption("Гамильтоновы графы")
    # pygame.display.set_icon(pygame.image.load("asd.bmp"))
    clock = pygame.time.Clock()
    FPS = 60
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    YELLOW = (239, 228, 176)
    f_sys = pygame.font.SysFont('arial', 36)
    sc_text = f_sys.render('Для проверки графа нажмите ENTER', True, RED, YELLOW)
    pos = sc_text.get_rect(center=(W//2, 40))
    sc.fill(WHITE)
    sc.blit(sc_text, pos)
    pygame.display.flip()
    poos2 = []
    poos3 = []
    running = True
    nbsd = True
    blc = []
    blc2 = True
    yel = []
    x, y = x2, y2 = 0, 0
    unn = False
    unn2 = False
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False # обнуляем первое смещение (при повторном вызове ниже)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    nodes = []
                    nodes2 = []
                    edges = []
                    yel2 = []
                    for i in range(len(poos2)):
                        nodes2.append(i+1)
                    for i in range(len(nodes2)):
                        for j in range(len(blc)):
                            if i == blc[j]:
                                blc2 = False
                        if blc2:
                            nodes.append(nodes2[i])
                        blc2 = True
                    for i in range(len(poos3)):
                        for o in range(len(yel)):
                            if i == yel[o]:
                                poos3[i] = [(0, 0), (0, 0)]
                    for i in range(len(poos3)):
                        for j in range(len(poos2)):
                            if poos3[i][0] == poos2[j]:
                                yel2.append(j + 1)
                            if poos3[i][1] == poos2[j]:
                                yel2.append(j + 1)
                    nodes2 = nodes
                    nodes = []
                    for i in range(len(nodes2)):
                        nodes.append(i + 1)
                    edges2 = yel2
                    yel2 = []
                    for i in range(len(edges2)):
                        for j in range(len(nodes2)):
                            if edges2[i] == nodes2[j]:
                                yel2.append(j + 1)
                    edges2 = list(func_chunk_itertools(yel2))
                    for i in range(len(edges2)):
                        if edges2[i][0] != edges2[i][1]:
                            edges.append(edges2[i])
                    edges2 = edges
                    edges = []
                    for i in range(len(edges2)):
                        for j in range(len(edges2)):
                            if edges2[i] == edges2[j] and j != i:
                                edges2[j] = 0
                    for i in range(len(edges2)):
                        if edges2[i] != 0:
                            edges.append(edges2[i])
                    main(edges)
            for i in range(len(poos2)):  # перерисовываем вершины
                for j in range(len(blc)):
                    if i == blc[j]:
                        blc2 = False
                if blc2:
                    pygame.draw.circle(sc, BLUE, poos2[i], 15)
                    pygame.display.update()
                blc2 = True
            pressed = pygame.mouse.get_pressed()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i in range(len(poos2)):  # рисуем вершины по нажатию
                    if event.button == 2 and abs(poos2[i][0] - mouse_x) < 30 and abs(poos2[i][1] - mouse_y) < 30:
                        nbsd = False
                if nbsd and event.button == 2:  # рисуем вершины по нажатию
                    pygame.draw.circle(sc, BLUE, (mouse_x, mouse_y), 15)
                    poos2.append((mouse_x, mouse_y))
                    pygame.display.update()
                nbsd = True
                if event.button == 1:  # рисуем рёбра по нажатию
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    x = mouse_x
                    y = mouse_y
                    for i in range(len(poos2)):
                        jjpo = True
                        for j in range(len(blc)):
                            if i == blc[j]:
                                jjpo = False
                        if jjpo or blc == []:
                            if abs(poos2[i][0] - x) < 15 and abs(poos2[i][1] - y) < 15:
                                x = poos2[i][0]
                                y = poos2[i][1]
                                unn2 = True
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if event.button == 3:   # удаляем по нажатию
                    for i in range(len(poos2)):
                        if abs(poos2[i][0] - mouse_x) < 15 and abs(poos2[i][1] - mouse_y) < 15:
                            pygame.draw.circle(sc, YELLOW, (poos2[i][0], poos2[i][1]), 15)
                            blc.append(i)
                            for j in range(len(poos3)):
                                if poos3[j][0] == poos2[i] or poos3[j][1] == poos2[i]:
                                    pygame.draw.line(sc, YELLOW, poos3[j][0], poos3[j][1], 3)
                                    yel.append(j)
                            pygame.display.update()
                    for i in range(len(poos3)):
                         if isBetween(poos3[i][0], poos3[i][1], (mouse_x, mouse_y)):
                            pygame.draw.line(sc, YELLOW, poos3[i][0], poos3[i][1], 3)
                            yel.append(i)
                            pygame.display.update()
            if pressed[0]:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                x2 = mouse_x
                y2 = mouse_y
                unn = True
            if event.type == pygame.MOUSEBUTTONUP:
                if unn and unn2:
                    for i in range(len(poos2)):
                        if abs(poos2[i][0] - x2) < 15 and abs(poos2[i][1] - y2) < 15:
                            for j in range(len(blc)):
                                if i == blc[j]:
                                    blc2 = False
                            if blc2:
                                pygame.draw.line(sc, BLACK, (x, y), (poos2[i][0], poos2[i][1]), 3)
                                poos3.append([(x, y), (poos2[i][0], poos2[i][1])])
                                pygame.display.update()
                                unn = False
                                unn2 = False
                            blc2 = True
    sc.fill(WHITE)
    pygame.quit()


vis()
