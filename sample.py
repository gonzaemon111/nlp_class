# coding: UTF-8

from collections import defaultdict
from itertools import product

from lxml import etree

example_sentence = "astronomers saw stars with ears"

grammar_text = """S→NP VP:1.0
PP→P NP:1.0
VP→V NP:0.7
VP→VP PP:0.3
NP→NP PP:0.4
P→with:1.0
V→saw:1.0
NP→astronomers:0.1
NP→ears:0.18
NP→saw:0.04
NP→stars:0.18
NP→telescope:0.1"""

class CKY:
    def __init__(self, grammar_text):
        self.grammar_dict = defaultdict(set)
        for line in grammar_text.split("\n"):
            rule, p = line.split(":")
            l, r = rule.split("→")
            self.grammar_dict[r].add((l, float(p)))

        self.cky_array = None

    def _init_cky_array(self, length):
        self.cky_array = [[[] for _ in range(length)]
                          for i in range(length)]
        return self.cky_array

    def parse(self, text):
        words = text.split()
        self.length = len(words)
        self._init_cky_array(self.length)

        for i, word in enumerate(words):
            for l, p in self.grammar_dict[word]:
                self.cky_array[i][i].append((l, word, p))
        
        # 対角成分の1つ右,2つ右,...と処理を回すループ
        for d in range(1, self.length):
            
            # 斜め下に進んでいくループ
            # i,jでどのセルを処理対象とするか決める
            for i in range(self.length - d):
                j = i + d
                
                # セルの中身を埋めるループ
                for k in range(i, j):

                    # 右辺の可能な組み合わせを列挙してる
                    for a, b in product(
                            range(len(self.cky_array[i][k])),
                            range(len(self.cky_array[k+1][j]))):

                        # 辞書のキーを作る
                        s = "{0} {1}".format(
                            self.cky_array[i][k][a][0],
                            self.cky_array[k+1][j][b][0])
                        
                        # キーに合致する文法をぜんぶ出す
                        for l,p in self.grammar_dict[s]:

                            # セルに中身を入れる
                            self.cky_array[i][j].append(
                                (l, ((i,k,a), (k+1,j,b)), p))

        # parseの最後
        return self._gen_xml_etree_list()

    def _traverse_tree(self, index=(0,0,0)):
        # 構文木を辿る
        i,j,k = index
        node = self.cky_array[i][j][k]
        elem = etree.Element(node[0])
        child = node[1]
        p = node[2]
        elem.attrib["p"] = str(p)

        if type(child) == str:
            elem.text = child
            return elem
        else:
            l, r = child
            elem.append(self._traverse_tree(index=l))            
            elem.append(self._traverse_tree(index=r))
            return elem

    def _gen_xml_etree_list(self):
        # 再帰呼出しを開始する
        lst = []
        for i, s in enumerate(self.cky_array[0][self.length - 1]):
            if s[0] != "S":
                pass
            else:
                # etreeのまま返すことにしよう...
                lst.append(self._traverse_tree((0,4,i)))
        return lst

def main():
    cky = CKY(grammar_text)
    lst = cky.parse(example_sentence)
    for xml_tree in lst:
        p = 1
        for elem in xml_tree.iter():
            p *= float(elem.attrib["p"])
        print(p)
        print(
            etree.tostring(xml_tree, pretty_print=True).decode())

if __name__ == "__main__":
    main()