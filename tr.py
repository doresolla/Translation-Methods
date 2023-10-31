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
                length = len(self.Rules[output[index]])
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
                word = self.fold(self, word)
                print(f" <-- {word}", end="")
            except:
                print("\nЦепочка не принадлежит грамматике")
                return False
            while any(elem in word for elem in self.VN):
                for index in range(len(word)):
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



    def GetParentAndChidren(self, replace, word):
        parent_node = Node(word)
        child_Nodes = []
        vars = self.GetListOfKeys(replace)
        if len(vars) > 1:
            for i in range(len(vars)):
                # варианты (дети текущего узла)
                child_Nodes.append(Node(vars[i] + word[1:]))
            parent_node.children = child_Nodes
        print(RenderTree(parent_node))
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
            if value in translator.Rules[key]:
                vars.append(key)
        return vars

    def fold(self, word):
        if word[:2] in self.endings:
            word = self.GetKeyByValue(word[:2]) + word[2:]
        else:
            word = self.GetKeyByValue(word[0]) + word[1:]
        return word


    def DrawGraph(self):
        G = nx.DiGraph(directed = True)
        pos = nx.spring_layout
        G.add_node('H')
        G.add_nodes_from(self.VT)
        print(self.Rules)
        edges = []
        labels_edges = {}

        for term in self.Rules.keys():
            for value in self.Rules[term]:
                edges.append([value, term])
                if len(value) == 1:
                    #если конечный символ (a,b)
                    if value in self.VN:
                        edge = ('H', term)
                        labels_edges[edge] = value
                        G.add_edge('H', term)
                    #если терминальный символ
                    else:
                        #метка для такого ребра не нужна
                        G.add_edge(value, term)
                else:
                    edge = (value[0], term)
                    labels_edges[edge] = value[1]
                    G.add_edge(value[0], term)
        print(labels_edges)
    #    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels_edges)
        nx.draw(G, with_labels=True, connectionstyle='arc3, rad = 0.1')
        plt.axis('off')
        plt.show()

