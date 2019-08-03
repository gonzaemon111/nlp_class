# -*- coding: utf-8 -*-
"""
A simple implementation of CKY parser
-- extended to allow multiple parses

@author: yoshihiko
"""

from collections import defaultdict
import nltk

## Sample sentences
elephant_s = 'I shot an elephant in my pajamas'
elephant_t = nltk.word_tokenize(elephant_s)
dog_s = 'My dog chased a cat for fun'
dog_t = nltk.word_tokenize(dog_s)
time_s = 'time flies like an arrow'
time_t = nltk.word_tokenize(time_s)

## Sample grammar
grammar = nltk.grammar.CFG.fromstring("""
    S -> NP VP
    NP -> Det N | Det NP | NP PP | N N | 'I' | 'time'
    VP -> V NP | V NP PP | V PP | VP PP | VP ADV
    Det -> 'a' | 'an' | 'my' | 'My'
    N -> 'elephant' | 'pajamas' | 'time' | 'flies' | 'arrow' | 'dog' | 'cat' | 'fun'
    V -> 'shot' | 'flies' | 'like' | 'chased' | 'time'
    PP -> P N | P NP
    P -> 'for' | 'in' | 'like'
""")

## CKY parsing (initialization + table build_up)
# In turn, this table simulates a n by (n+1) matrix, 
# where n is number of tokens.      
def init_wfst(tokens, grammar):
    wfst = defaultdict(list)
    for i in range(len(tokens)):
        wfst[(i,i+1)] = [(p.lhs(), ((i,i), seq), ((i+1,i+1), seq)) 
        for seq, p in \
        enumerate(grammar.productions(rhs=tokens[i]))]
    return wfst

def build_wfst(tokens, wfst, grammar, verbose=True):
    if verbose:
        print("[building wfst]")
    num_tokens = len(tokens)
    # Dictionary for storing rules. Notice that the key is RHS of a rule
    rule_d = dict((p.rhs(), p.lhs()) for p in grammar.productions())
    #
    for span in range(2, num_tokens+1): # j-axis
        for start in range(num_tokens-span+1): # i-axis
            for div in range(1, span): # go for each left-right combination
                r1_l = wfst[(start, start+div)]
                r2_l = wfst[(start+div, start+span)]
                for i, r1 in enumerate(r1_l):
                    for j, r2 in enumerate(r2_l):
                        if r1 and r2 and (r1[0], r2[0]) in rule_d:
                            wfst[(start, start+span)].append((rule_d[(r1[0], r2[0])], 
                                                         ((start, start+div), i), 
                                                         ((start+div, start+span), j)))
                    if verbose:
                        print(start, start+span, wfst[(start, start+span)])
    return wfst

# just for displaying WFST table
def show_wfst(tokens, wfst):
    num_tokens = len(tokens)
    for i in range(num_tokens+1):
        for j in range(i+1, num_tokens+1):
            print(i, j, wfst[(i,j)], '-',)
        print

## Build NLTK tree from WFST table
def build_trees(tokens, wfst):
    return [build_tree_(tokens, root, wfst) for root in wfst[(0, len(tokens))]]

def build_tree(tokens, wfst):
    return build_tree_(tokens, wfst[(0, len(tokens))], wfst)

def build_tree_(tokens, node, wfst):
    symbol, (lspan, lseq), (rspan, rseq) = node
    if pre_terminal_node(lspan, rspan):
        return nltk.tree.Tree(str(symbol), 
                              children=[tokens[lspan[0]]])
    else:
        return nltk.tree.Tree(str(symbol), 
                              children=[build_tree_(tokens,wfst[lspan][lseq],wfst), 
                                        build_tree_(tokens,wfst[rspan][rseq],wfst)])

def pre_terminal_node(l, r):
    return (l[0] == l[1]) and (l[0] + 1 == r[0])
 
## CKY Parser
def parse(tokens, grammar, verbose=True):
    wfst = init_wfst(tokens, grammar)
    if verbose: 
        print('[init wfst]')
        show_wfst(tokens, wfst)
    wfst = build_wfst(tokens, wfst, grammar, verbose)
    if verbose:
        print('[completed wfst]')
        show_wfst(tokens, wfst)
    return build_trees(tokens, wfst)