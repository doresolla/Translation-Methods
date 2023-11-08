import random
import matplotlib.pyplot as plt
import networkx as nx
import pygraphviz as pgv
from networkx.drawing.nx_agraph import to_agraph
import my_networkx as my_nx
from anytree import Node, RenderTree


class translator:
    Rules = {}
    VN, VT = [], []
    target_symbol = 's'
    endings = []

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
        print('len(lines) = ', len(lines))
        for i in range(2, len(lines)):
            lines[i] = lines[i].strip('\n')
            if lines[i] == "P:":
                continue
            term = lines[i][:lines[i].find('-')]
            if '|' in lines[i]:
                self.Rules[term] = lines[i][lines[i].find('-->') + 3:].split('|')
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
        if word == "":
            print("word is null")
            return False
        else:
            print(f"Операция свёртки: \n {word}", end="")
            try:
                p = self.GetParentAndChidren(word)
                print(RenderTree(p))
                word = self.fold(self, word)
                print(f" <-- {word}", end="")
            except:
                print("\nЦепочка не принадлежит грамматике")
                return False
            while any(elem in word for elem in self.VN):
                for index in range(len(word)):
                    # if self.endings.count(word[0]) > 1 or
                    try:
                        word = self.fold(self, word)
                    except:
                        print("\nЦепочка не принадлежит грамматике")
                        return False
                    print(f" <-- {word}", end='')
                    if (word == self.target_symbol):
                        print("\nЦепочка принадлежит грамматике")
                        return True
            else:
                print("\nЦепочка не принадлежит грамматике")
                return False

    def GetParentAndChidren(self, word):
        parent_node = Node(word)
        vars = self.GetListOfKeys(self, word)
        if vars == []:
            return None
        elif len(vars) >= 1:
            for i in range(len(vars)):
                # варианты (дети текущего узла)
                word = self.fold(self, word, vars[i])
                word = vars[i] + word[len(vars[i]):]
                Node(word, parent=parent_node)
                while 'S' not in parent_node.leaves:
                    self.GetParentAndChidren(self, word)
        #  print(RenderTree(parent_node))
        return parent_node

    def GetKeyByValue(value):
        for key in translator.Rules.keys():
            if value in translator.Rules[key]:
                return key
        else:
            raise ValueError('Нет такого значения')

    def GetListOfKeys(self, value):
        vars = []
        for key in translator.Rules.keys():
            if value[0] in translator.Rules[key] or value[:2] in translator.Rules[key]:
                vars.append(key)
            elif ' ' in translator.Rules[key]:
                vars.append(key)
        return vars

    def fold(self, word, replace=None):
        if replace != None:
            begin = translator.Rules[replace]
            for val in begin:
                if word.startswith(val):
                    word = replace + word[len(val):]
                    return word
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
                self.LoopGraph(self,G.edges(), labels_edges)
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

        #print(G.edges(data=True))
        G.graph['edge'] = {'arrowsize': '0.6', 'splines': 'curved'}
        G.graph['graph'] = {'scale': '3'}

        A = to_agraph(G)

        A.graph_attr['strict'] = True
        A.graph_attr['rankdir']='LR'
        A.layout('dot')

        # set edge labels
        for pair in labels_edges:
            edge = A.get_edge(pair[0], pair[1])
            edge.attr['label'] = str(labels_edges[pair]) + "  "

        A.draw('диаграмма состояний (петля).png')
