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


def is_between(a, b, c):
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


# функция, проверяющая связность графа
def is_connected(graph):
    if not nx.is_connected(graph):
        print("Граф связный")
        print(nx.is_connected(graph))
        return False
    return True


# функция, проверяющая планарность графа
def is_planar(graph):
    if not planarity.is_planar(graph):
        print("Граф планарный")
        print(planarity.is_planar(graph))
        return False
    return True


# функция, проверяющая наличие листьев в графе
def has_graph_leaves(graph):
    nod = list(graph.nodes)
    for i in range(len(nod)):
        if graph.degree(nod[i]) == 1:
            print("Есть листья")
            print("True")
            return False
    return True


# функция, проверяющая наличие шарниров в графе
def has_graph_hinges(graph):
    directed_graph = nx.Graph(graph)
    for i in range(len(directed_graph.nodes)):
        directed_graph = nx.Graph(graph)
        directed_graph.remove_node(i + 1)
        if not nx.is_connected(directed_graph):
            print("Есть шарниры")
            print("True")
            return False
    return True


# функция, рисующая дополнительное изображение графа
def picture(G):
    # для начала надо выбрать способ "укладки" графа. Их много, возьмём для начала такой:
    pos = nx.spring_layout(G)
    plt.figure(facecolor='white')
    ax = plt.axes()
    ax.set_facecolor("white")
    # рисуем узлы, задаём размер узла
    nx.draw_networkx_nodes(G, pos, node_color='#0000FF', node_size=1500)
    # рисуем рёбра
    nx.draw_networkx_edges(G, pos, edge_color='#000000')
    # Добавим ещё подписи к узлам
    nx.draw_networkx_labels(G, pos, font_size=25, font_family='Arial', font_color='#000000')
    # по умолчанию график будет снабжён осями с координатами, здесь они бессмысленны, так что отключаем
    plt.axis('off')
    pylab.show()


def check(graph, nodes_pos):
    is_match = True
    if is_match:
        # проверка на имена вершин
        is_match = ver_shins(graph)
    if is_match:
        # проверка графа на связность
        is_match = is_connected(graph)
    if is_match:
        # проверка графа на планарность
        is_match = is_planar(graph)
    if is_match:
        # проверка на наличие листьев в графе
        is_match = has_graph_leaves(graph)
    if is_match:
        # проверка на наличие шарниров в графе
        is_match = has_graph_hinges(graph)
    if is_match:
        # рисовка графа
        picture(graph)
        # поиск всех граней графа
        rr = find_the_lines(graph, nodes_pos)
        # проверка граней посредством теоремы Гринберга
        grinberg_theorem(rr)


# функция, проверяющая порядок вершин в графе
def ver_shins(G):
    old = G.nodes
    old2 = max(old)
    old3 = sum(old)
    old4 = 0
    for i in range(1, old2 + 1):
        old4 = old4 + i
    if old3 != old4:
        print("Порядок вершин верный")
        print("False")
        return False
    return True


# функция, ищущая все грани графа
def find_the_lines(graph, nodes_pos):

    edges = list(graph.edges)

    directed_graph = nx.DiGraph(graph)

    cycles = sorted(nx.simple_cycles(directed_graph))

    # Удаление элементарных путей длиной <= 2
    i = 0
    while i < len(cycles):

        if len(cycles[i]) == 2 or len(cycles[i]) == 1:
            cycles.pop(i)
        else:
            i += 1

    # print(cycles)

    i = 0
    # проходим по всем простым циклам графа
    while i < len(cycles):
        # изначально ставим флаг "это грань" в положение правды
        is_line = True
        # проходим по всем вершинам простого цикла (полигона)
        for node_of_polygon in cycles[i]:
            count_of_neighbour_by_cycle = 0
            # проходим по всем ребрам графа
            for edge in edges:
                # ищем ребра инцидентные данной вершине простого цикла
                if (edge[0] == node_of_polygon or edge[1] == node_of_polygon) and is_line:
                    # пробуем найти для найденного ребра другую вершину, смежную с текущей
                    try:
                        cycles[i].index(edge[0])
                        cycles[i].index(edge[1])
                        count_of_neighbour_by_cycle += 1
                        if count_of_neighbour_by_cycle >= 3:
                            is_line = False
                        # при успешном поиске ничего не происходит, в ином случае (когда текущая вершина простого цикла
                        # смежна с вершиной, не принадлежащей циклу) выскакивает предупреждение ValueError,
                        # которое мы обрабатываем
                    except ValueError:
                        # определяем с какой стороны ребра стояла наша вершина, чужую вершину записываем в переменную
                        # foreign_node
                        if node_of_polygon == edge[0]:
                            foreign_node = edge[1]
                        else:
                            foreign_node = edge[0]

                        polygon = []
                        # заносим в переменную полигон координаты вершин текущего простого цикла (многоугольника)
                        for j in cycles[i]:
                            polygon.append(nodes_pos[j - 1])

                        # получаем координаты "чужой" вершины
                        foreign_node_pos = nodes_pos[foreign_node - 1]

                        # Реализуем проверку трассировкой луча из "чужой" точки
                        # изначально предполагаем, что "чужая" точка находится вне полигона, т.е.
                        # не разрушает грань на части
                        in_polygon = False
                        # в x и y хранятся соответствующие координаты "чужой" точки
                        x = foreign_node_pos[0]
                        y = foreign_node_pos[1]
                        for j in range(len(polygon)):
                            # в xp и yp содержатся координаты некоторой точки полигона
                            xp = polygon[j][0]
                            yp = polygon[j][1]
                            # в xp_prev и yp_prev содержатся координаты точки полигона, предшествующей точке
                            # с координатами xp и yp
                            xp_prev = polygon[j - 1][0]
                            yp_prev = polygon[j - 1][1]
                            # "испускание луча" при условии, что "чужая" точка лежит между двумя рассматриваемыми
                            # точками полигона (одна точка полигона выше, другая - ниже)
                            # для того, чтобы точка лежала внутри полигона (многоугольника, образованного циклом),
                            # необходимо, чтобы количество пересечений луча было нечетным
                            if ((yp <= y < yp_prev) or (yp_prev <= y < yp)) and (x > (xp_prev - xp) * (y - yp) / (yp_prev - yp) + xp):
                                in_polygon = not in_polygon
                        # если точка оказалась лежащей внутри полигона - тогда она разбивает данный цикл на другие
                        # грани, и он, соответственно, не является гранью
                        if in_polygon:
                            is_line = False

        if not is_line:
            cycles.pop(i)
        else:
            i += 1

    # создание результирующего списка
    result = cycles.copy()

    i = 0
    while i < len(cycles):
        # Сортировка каждого оставшегося простого цикла (который уже является гранью) в лексикографическом порядке
        # (т.е. если цикл изначально представлен как [2, 4, 1], то он будет записан как [1, 2, 4]
        cycles[i] = sorted(cycles[i])
        i += 1

    # удаление повторяющихся простых циклов (граней) в результирующем списке с сохранением порядка вершин
    i = 0
    while i < len(cycles):
        j = 0
        while j < len(cycles):
            if cycles[i] == cycles[j] and i != j:
                result.pop(j)
                cycles.pop(j)
            else:
                j += 1
        i += 1

    # поиск и добавление внешней грани
    current_degree = 0
    nodes = list(graph.nodes)
    nodes_of_outer_line = []
    nodes_degree = []

    for i in range(len(nodes)):
        nodes_degree.append(graph.degree(nodes[i]))

    for k in range(len(nodes_degree)):
        for i in range(len(cycles)):
            for j in range(len(cycles[i])):
                if nodes[k] == cycles[i][j]:
                    current_degree += 1
        if current_degree < nodes_degree[k]:
            nodes_of_outer_line.append(nodes[k])
        current_degree = 0

    graph_copy = nx.Graph(directed_graph)
    current_nodes = list(graph_copy.nodes)
    r = 0

    for k in range(len(current_nodes)):
        for i in range(len(nodes_of_outer_line)):
            if current_nodes[k] == nodes_of_outer_line[i]:
                r = r + 1
        if r != 1:
            graph_copy.remove_node(current_nodes[k])
        r = 0

    directed_graph_copy = graph_copy.to_directed()
    current_cycles = sorted(nx.simple_cycles(directed_graph_copy))  # простые циклы текущего графа
    outer_line = []  # список с вершинами внешней грани

    for k in range(len(current_cycles)):
        if len(nodes_of_outer_line) == len(current_cycles[k]):
            for i in range(len(current_cycles[k])):
                a = sorted(current_cycles[k])
                b = sorted(nodes_of_outer_line)
                if a[i] == b[i]:
                    outer_line = current_cycles[k]
                    break
    if outer_line:
        result.append(outer_line)

    # print(result)

    return result


def grinberg_theorem(rr):
    is_not_error = True
    print("")
    print("Все грани графа")
    rr.sort(key=len)
    print(rr)
    rr0, loi, loi2 = [], [], []
    for i in range(len(rr)):
        rr0.append(len(rr[i]) - 2)  # print(rr0)
    if sum(rr0) % 2 != 0:
        print("Невозможно разделить на 2 половины")
        is_not_error = False
        print("Error")
        print("Граф не удовлетворяет теореме Гринберга")
        print("")
    if is_not_error:
        if sum(rr0) % 2 == 0:  # even sum
            for selectors in product([0, 1], repeat=len(rr0)):
                if sum(compress(rr0, selectors)) == sum(rr0) // 2:
                    loi = list(compress(rr0, selectors))
                    loi2 = list(
                        compress(rr0, (not s for s in selectors)))  # print(loi, loi2)  # print(sum(loi), sum(loi2))
                    break
        else:
            is_not_error = False
    print("")
    print("Части графа")
    print(loi, "  ",loi2)
    print("")
    if is_not_error:
        fk, fk1, fk2, fk10, fk20, b = 0, 0, 0, 0, 0, 0
        max_k = max(rr0)
        for k in range(1, max_k + 1):
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


def main(edges, nodes_position):
    t0 = time.perf_counter()
    # создание графа
    graph = nx.Graph(edges)
    # обязатедбные вещи
    check(graph, nodes_position)
    t1 = time.perf_counter()
    print(t1 - t0)


def vis():
    print("")
    print("ЛКМ - добавить ребро")
    print("Колёсико - Добавить вершину")
    print("ПКМ - удалить ребро или вершину")
    print("")

    # установка ширины и высоты действующего окна
    weight, height = 800, 600

    # инициализация класса
    pygame.init()
    # создание рабочего окна
    sc = pygame.display.set_mode((weight, height), pygame.RESIZABLE)
    pygame.display.set_caption("Гамильтоновы графы")
    # pygame.display.set_icon(pygame.image.load("asd.bmp"))
    clock = pygame.time.Clock()
    fps = 60

    black_color = (0, 0, 0)
    white_color = (255, 255, 255)
    blue_color = (0, 0, 255)
    red_color = (255, 0, 0)
    yellow_color = (239, 228, 176)

    # установка шрифта
    f_sys = pygame.font.SysFont('arial', 36)
    # вывод надписи
    sc_text = f_sys.render('Для проверки графа нажмите ENTER', True, red_color, yellow_color)
    pos = sc_text.get_rect(center=(weight // 2, 40))


# заполнение рабочего окна белым цветом
    sc.fill(white_color)
    sc.blit(sc_text, pos)
    pygame.display.flip()

    # инициализация необходимых переменных
    nodes_position = []  # список координат вершин
    edges_position = []  # список координат ребер

    is_running = True
    flag_1 = True
    blc = []
    blc2 = True
    yel = []
    x, y = x2, y2 = 0, 0
    unn = False
    unn2 = False
    while is_running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False  # обнуляем первое смещение (при повторном вызове ниже)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    nodes = []
                    nodes2 = []
                    edges = []
                    yel2 = []
                    for i in range(len(nodes_position)):
                        nodes2.append(i + 1)
                    for i in range(len(nodes2)):
                        for j in range(len(blc)):
                            if i == blc[j]:
                                blc2 = False
                        if blc2:
                            nodes.append(nodes2[i])
                        blc2 = True
                    for i in range(len(edges_position)):
                        for o in range(len(yel)):
                            if i == yel[o]:
                                edges_position[i] = [(0, 0), (0, 0)]
                    for i in range(len(edges_position)):
                        for j in range(len(nodes_position)):
                            if edges_position[i][0] == nodes_position[j]:
                                yel2.append(j + 1)
                            if edges_position[i][1] == nodes_position[j]:
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
                    if edges:
                        print("")
                        print("")
                        print("")
                        main(edges, nodes_position)
                    else:
                        print("нет рёбер")
            for i in range(len(nodes_position)):  # перерисовываем вершины
                for j in range(len(blc)):
                    if i == blc[j]:
                        blc2 = False
                if blc2:
                    pygame.draw.circle(sc, blue_color, nodes_position[i], 15)
                    pygame.display.update()
                blc2 = True
            pressed = pygame.mouse.get_pressed()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i in range(len(nodes_position)):  # рисуем вершины по нажатию
                    if event.button == 2 and abs(nodes_position[i][0] - mouse_x) < 30 and abs(
                            nodes_position[i][1] - mouse_y) < 30:
                        flag_1 = False
                if flag_1 and event.button == 2:  # рисуем вершины по нажатию
                    pygame.draw.circle(sc, blue_color, (mouse_x, mouse_y), 15)
                    nodes_position.append((mouse_x, mouse_y))
                    pygame.display.update()
                flag_1 = True
                if event.button == 1:  # рисуем рёбра по нажатию
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    x = mouse_x
                    y = mouse_y
                    for i in range(len(nodes_position)):
                        flag_2 = True
                        for j in range(len(blc)):
                            if i == blc[j]:
                                flag_2 = False
                        if flag_2 or blc == []:
                            if abs(nodes_position[i][0] - x) < 15 and abs(nodes_position[i][1] - y) < 15:
                                x = nodes_position[i][0]
                                y = nodes_position[i][1]
                                unn2 = True
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if event.button == 3:  # удаляем по нажатию
                    for i in range(len(nodes_position)):
                        if abs(nodes_position[i][0] - mouse_x) < 15 and abs(nodes_position[i][1] - mouse_y) < 15:
                            pygame.draw.circle(sc, yellow_color, (nodes_position[i][0], nodes_position[i][1]), 15)
                            blc.append(i)
                            for j in range(len(edges_position)):
                                if edges_position[j][0] == nodes_position[i] or edges_position[j][1] == nodes_position[
                                    i]:
                                    pygame.draw.line(sc, yellow_color, edges_position[j][0], edges_position[j][1], 3)
                                    yel.append(j)
                            pygame.display.update()
                    for i in range(len(edges_position)):
                        if is_between(edges_position[i][0], edges_position[i][1], (mouse_x, mouse_y)):
                            pygame.draw.line(sc, yellow_color, edges_position[i][0], edges_position[i][1], 3)
                            yel.append(i)
                            pygame.display.update()
            if pressed[0]:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                x2 = mouse_x
                y2 = mouse_y
                unn = True
            if event.type == pygame.MOUSEBUTTONUP:
                if unn and unn2:
                    for i in range(len(nodes_position)):
                        if abs(nodes_position[i][0] - x2) < 15 and abs(nodes_position[i][1] - y2) < 15:
                            for j in range(len(blc)):
                                if i == blc[j]:
                                    blc2 = False
                            if blc2:
                                pygame.draw.line(sc, black_color, (x, y), (nodes_position[i][0], nodes_position[i][1]),
                                                 3)
                                edges_position.append([(x, y), (nodes_position[i][0], nodes_position[i][1])])
                                pygame.display.update()
                                unn = False
                                unn2 = False
                            blc2 = True
    sc.fill(white_color)
    pygame.quit()


vis()
