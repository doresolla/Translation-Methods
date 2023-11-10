import tr


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tr.translator.Read(tr.translator, "rules1.txt")


    tr.translator.DrawGraph(tr.translator)

    for i in range(5):
        print(i+1, end = ')')
        word = tr.translator.Write(tr.translator)
       # tr.translator.IsIn(tr.translator, word)
        family_tree = tr.TreeNode.build_family_tree(tr.TreeNode, word)
        # вывод дерева
        tr.TreeNode.dfs(tr.TreeNode, family_tree)
        try:
            paths = tr.TreeNode.findS(tr.TreeNode, family_tree)
            print(*paths, sep='\n')
            for path in paths:
                if 'S' in path:
                    print('Цепочка принадлежит грамматике')
                    break
        except:
            raise Exception






# tr.translator.GetParentAndChidren(tr.translator, word)
# check = input("Введите цепочку\n")
# tr.translator.IsIn(tr.translator, check)
