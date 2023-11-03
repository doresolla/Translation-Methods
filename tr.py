import random
import matplotlib.pyplot as plt
import networkx as nx
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
                    #if self.endings.count(word[0]) > 1 or
                    try:
                        word = self.fold(self,  word)
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
                Node(word, parent = parent_node)
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

    def fold(self, word, replace = None):
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
        G = nx.DiGraph(directed = False)
        G.add_node('H')
        G.add_nodes_from(self.VT)
        print(self.Rules)
        loc = nx.spring_layout(G)
        labels_edges = {}

        for term in self.Rules.keys():
            for value in self.Rules[term]:
                if len(value) == 1:
                    #если конечный символ (a,b)
                   if value in self.VN:
                       edge = ('H', term)
                       if labels_edges.get(edge) != None:
                          labels_edges[edge] = labels_edges[edge] + ',' + value
                       else:
                          labels_edges[edge] = value
                       G.add_edge('H', term)
                    #если терминальный символ
                   else:
                        #метка для такого ребра не нужна
                       G.add_edge(value, term)
                   #G.add_edge(value, term)
                elif len(value) == 2:
                    edge = (value[0], term)
                    if labels_edges.get(edge) != None:
                        labels_edges[edge] = labels_edges[edge] +','+ value[1]
                    else:
                        labels_edges[edge] = value[1]
                    G.add_edge(value[0], term)
        print(labels_edges)

        plt.figure()
        nx.draw_networkx_edge_labels(G, loc, edge_labels=labels_edges, font_color="red")
       # nx.draw(G, with_labels=True, connectionstyle='arc3, rad = 0.1')
        nx.draw(G, with_labels=True)
        #plt.axis('off')
        plt.show()


class graph:
    def DrawGraph(self):

        edges = [['A', 'B'], ['B', 'C'], ['B', 'D']]
        G = nx.DiGraph()
        G.add_edges_from(edges)
        pos = nx.spring_layout(G)
        plt.figure()
        nx.draw(
            G, pos, edge_color='black', width=1, linewidths=1,
            node_size=500, node_color='pink', alpha=0.9,
            labels={node: node for node in G.nodes()}
        )
        nx.draw_networkx_edge_labels(
            G, pos,
            edge_labels={('A', 'B'): 'AB',
                         ('B', 'C'): 'BC',
                         ('B', 'D'): 'BD'},
            font_color='red'
        )
        plt.axis('off')
        plt.show()

