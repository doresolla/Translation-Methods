import random
import matplotlib.pyplot as plt
import networkx as nx
# import pygraphviz as pgv
from networkx.drawing.nx_agraph import to_agraph
import my_networkx as my_nx
from anytree import Node, RenderTree


class translator:
    Rules = {}
    VN, VT = [], []
    target_symbol = 's'
    endings = []
    EPS = chr(1)

    def Read(self, filename):
        f = open(filename)
        lines = f.readlines()
        index1 = lines[0].find('{')
        index2 = lines[0].find('}')
        self.VT = lines[0][index1 + 1: index2].split(',')
        line = lines[0][index2 + 1:]
        index1 = line.find('{')
        index2 = line.find('}')
        self.VN = line[index1 + 1: index2].split(',')
        self.target_symbol = line[len(line) - 3]
        print('VT :', self.VT)
        print('VN :', self.VN)
        print('Целевой символ :', self.target_symbol)
        for i in range(2, len(lines)):
            lines[i] = lines[i].strip('\n')
            if lines[i] == "P:":
                continue
            term = lines[i][:lines[i].find('-')]
            if '|' in lines[i]:
                self.Rules[term] = lines[i][lines[i].find('-->') + 3:].split('|')
                if lines[i].endswith('|'):
                    self.Rules[term].append(self.EPS)
            else:
                self.Rules[term] = lines[i][lines[i].find('-->') + 3]
            try:
                self.endings.extend(self.Rules[term])
            except:
                print("Ошибка")
            res = '|'.join(value for value in self.Rules[term])
            print(term, '-->', res)

    def Write(self):
        index, length = 0, 0
        iterations = 0
        replacement = ''
        output = self.target_symbol
        print(output, end='')
        while (index < len(output)):
            if iterations > 30:
                break
            if output[index] in self.VT:
                replacement = random.choice(self.Rules[output[index]])
                if replacement == self.EPS:
                    replacement = ''
                output = output.replace(output[index], replacement, 1)
                print(' -->', output, end='')
                iterations += 1
            else:
                index += 1
        if (iterations > 30):
            print('\nЧисло итераций превысило 30')
        else:
            print(f'\nЧисло итераций {iterations}')
        return output

    def IsIn(self, word):
        family_tree = TreeNode.build_family_tree(TreeNode, word)
        # вывод дерева
        TreeNode.dfs(TreeNode, family_tree)
        paths = list(TreeNode.findS(TreeNode, family_tree))
        if len(paths) > 0:
            print(*paths, sep='\n')
            print('Цепочка принадлежит грамматике')
        else:
            print("Цепочка не принадлежит грамматике")




    def GetKeyByValue(value):
        for key in translator.Rules.keys():
            if value in translator.Rules[key]:
                return key
        else:
            raise ValueError('Нет такого значения')

    # Варианты на что можно свернуть нулевой, первый или первые 2 символа
    def GetListOfKeys(self, value):
        vars = []

        for key in translator.Rules.keys():
            if value != '':
                if value[0] in translator.Rules[key] or value[:2] in translator.Rules[key]:
                    vars.append(key)
                if translator.EPS in translator.Rules[key] and value[0] in self.VN:
                    vars.append(key)
            else:
                if translator.EPS in translator.Rules[key]:
                    vars.append(key)
        return vars

    # свёртка по заданному варианту
    def fold(self, word, replace=None):
        result = ''
        if replace != None:
            begin = translator.Rules[replace]
            for val in begin:
                if word.startswith(val):
                    result = replace + word[len(val):]
                    break
                elif val == translator.EPS and word[0] in self.VN:
                    result = replace + word
                    break
            total = 0
            for term in self.VT:
                total += result.count(term)
                if total > 1:
                    return word
            else:
                return result
        else:
            if word[:2] in translator.endings:
                word = translator.GetKeyByValue(word[:2]) + word[2:]
            else:
                word = translator.GetKeyByValue(word[0]) + word[1:]
            return word

    def DrawGraph(self):
        G = nx.DiGraph(directed=True)
        G.add_node('H')
        G.add_nodes_from(self.VT)

        labels_edges = {}
        # добавление ребер и меток к ним
        for term in self.Rules.keys():
            for value in self.Rules[term]:
                if len(value) == 1:
                    # если конечный символ (a,b)
                    if value in self.VN:
                        edge = ('H', term)
                        if labels_edges.get(edge) != None:
                            labels_edges[edge] = labels_edges[edge] + ',' + value
                        else:
                            labels_edges[edge] = value
                        G.add_edge('H', term)
                    # если терминальный символ
                    else:
                        # метка для такого ребра не нужна
                        G.add_edge(value, term)
                    # G.add_edge(value, term)
                elif len(value) == 2:
                    edge = (value[0], term)
                    if labels_edges.get(edge) != None:
                        labels_edges[edge] = labels_edges[edge] + ',' + value[1]
                    else:
                        labels_edges[edge] = value[1]
                    G.add_edge(value[0], term)

        for edge in G.edges():
            if edge[0] == edge[1]:
                self.LoopGraph(self, G.edges(), labels_edges)
                return
        curved_edges = [edge for edge in G.edges() if edge[::-1] in G.edges() and edge[::-1] != edge]
        straight_edges = list(set(G.edges() - set(curved_edges)))
        circle_edges = [edge for edge in G.edges() if edge == edge[::-1]]

        pos = nx.spring_layout(G, seed=5)
        fig, ax = plt.subplots()

        nx.draw_networkx_nodes(G, pos, ax=ax)
        nx.draw_networkx_labels(G, pos, ax=ax)
        labels_curved = {edge: labels_edges[edge] for edge in labels_edges.keys() if edge in curved_edges}
        labels_straight = {edge: labels_edges[edge] for edge in labels_edges.keys() if edge in straight_edges}

        # прямые ребра
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=straight_edges)
        # загнутые ребра
        arc_rad = 0.25
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=curved_edges, connectionstyle=f'arc3, rad = {arc_rad}',
                               arrows=True)

        # метки для загнутых ребер
        my_nx.my_draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=labels_curved, rotate=False, rad=arc_rad)
        # метки для прямых ребер
        nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=labels_straight, rotate=False)

        plt.axis('off')
        plt.show()

        fig.savefig("диаграмма состояний.png", bbox_inches='tight', pad_inches=0)

    def LoopGraph(self, edges, labels_edges):
        G = nx.MultiDiGraph()

        # add edges
        for edge in edges:
            if edge[0] == edge[1]:
                G.add_edge(edge[0], edge[1], color='red')
            else:
                G.add_edge(edge[0], edge[1])

        # print(G.edges(data=True))
        G.graph['edge'] = {'arrowsize': '0.6', 'splines': 'curved'}
        G.graph['graph'] = {'scale': '3'}

        A = to_agraph(G)

        A.graph_attr['strict'] = True
        A.graph_attr['rankdir'] = 'LR'
        A.layout('dot')

        # set edge labels
        for pair in labels_edges:
            edge = A.get_edge(pair[0], pair[1])
            edge.attr['label'] = str(labels_edges[pair]) + "  "

        A.draw('диаграмма состояний (петля).png')


class TreeNode:
    IsIn = False
    def __init__(self, data):
        self.data = data
        self.children = []

    def build_family_tree(self, data):
        root = TreeNode(data)
        vars = translator.GetListOfKeys(translator, data)
        if vars is None:
            return
        for var in vars:
            newword = translator.fold(translator, data, var)
            if newword == 'S':
                self.IsIn = True
            child = self.build_family_tree(self, newword)
            root.children.append(child)
            # self.build_family_tree(newword)

        return root

    def dfs(self, node, level=0):
        indent = " " * level * 4
        print(indent + str(node.data))
        for child in node.children:
            self.dfs(self, child, level + 1)

    def findS(self, node):
        if node.children != []:
            for child in node.children:
                yield from ([node.data] + arr for arr in self.findS(self, child))
        #если лист дерева
        else:
            if node.data == 'S':
                yield [node.data]
