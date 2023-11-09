import tr


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tr.translator.Read(tr.translator, "rules1.txt")
    family_tree = tr.TreeNode.build_family_tree(tr.TreeNode, 'baba')

    tr.TreeNode.dfs(tr.TreeNode, family_tree)

    # tr.translator.DrawGraph(tr.translator)
    #
    # for i in range(5):
    #     print(i+1, end = ')')
    #     word = tr.translator.Write(tr.translator)
    #     tr.translator.IsIn(tr.translator, word)



# tr.translator.GetParentAndChidren(tr.translator, word)
# check = input("Введите цепочку\n")
# tr.translator.IsIn(tr.translator, check)
