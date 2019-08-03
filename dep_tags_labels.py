# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 07:58:34 2019

@author: yoshihiko
"""

# the set of POS tags
_TAGS = {'NN': 3, 'IN': 4, 'NNP': 5, 'DT': 6, 'JJ': 7, 'NNS': 8, ',': 9, 'CD': 10, 'VBD': 11, '.': 12, 'RB': 13, 'CC': 14, 'VB': 15, 'TO': 16, 'VBN': 17, 'VBZ': 18, 'PRP': 19, 'VBG': 20, 'POS': 21, 'VBP': 22, '$': 23, 'MD': 24, '``': 25, "''": 26, 'PRP$': 27, ':': 28, 'WDT': 29, 'JJR': 30, 'RP': 31, 'JJS': 32, 'WRB': 33, 'WP': 34, 'RBR': 35, 'NNPS': 36, '-RRB-': 37, '-LRB-': 38, 'EX': 39, 'PDT': 40, 'RBS': 41, 'WP$': 42, '#': 43, 'UH': 44, 'LS': 45, '<unk>': 0, '<root>': 1, '<null>': 2}
# the set of dependency relations
_DEPR = {'punct': 3, 'prep': 4, 'pobj': 5, 'det': 6, 'nn': 7, 'nsubj': 8, 'amod': 9, 'root': 10, 'dobj': 11, 'advmod': 12, 'aux': 13, 'num': 14, 'conj': 15, 'cc': 16, 'poss': 17, 'dep': 18, 'xcomp': 19, 'ccomp': 20, 'number': 21, 'possessive': 22, 'mark': 23, 'rcmod': 24, 'advcl': 25, 'auxpass': 26, 'appos': 27, 'nsubjpass': 28, 'tmod': 29, 'partmod': 30, 'acomp': 31, 'pcomp': 32, 'quantmod': 33, 'npadvmod': 34, 'neg': 35, 'prt': 36, 'infmod': 37, 'parataxis': 38, 'mwe': 39, 'expl': 40, 'iobj': 41, 'csubj': 42, 'predet': 43, 'preconj': 44, 'discourse': 45, 'cop': 46, 'csubjpass': 47, '<unk>': 0, '<root>': 1, '<null>': 2}