# -*- coding: utf-8 -*-
import nltk
import inspect
TRAIN_DATA_COUNT = 50

train_data = {}

def pcky_create(tree):
    for a_tree in tree:
        lhs = a_tree.lhs()
        rhs = a_tree.rhs()
        if str(lhs) in train_data:
            all_count = 0.0

            for train_data_value in train_data[str(lhs)]:
                z = train_data_value.values()
                all_count += z[0]['count']

                for a_rhs in rhs:
                    if a_rhs in train_data_value:
                        if train_data_value.get(a_rhs) != None :
                            train_data_value.values()[0]['count'] = train_data_value.values()[0]['count'] + 1
                            all_count += 1
                            train_data_value.values()[0]['prob'] = train_data_value.values()[0]['count'] / all_count
        else:
            train_data[str(lhs)] = []
            for a_rhs in rhs:
                train_data[str(lhs)].append({ a_rhs: { 'count': 1.0, 'prob': 1.0/len(rhs) } })

if __name__ == "__main__":
    nltk_datas = nltk.corpus.treebank.parsed_sents()

    for x in range(0, TRAIN_DATA_COUNT):
        nltk_datas[x].chomsky_normal_form()
        pcky_create(nltk_datas[x].productions())

    print(train_data)
