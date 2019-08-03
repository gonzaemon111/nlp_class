# -*- coding: utf-8 -*-
"""
cky2.py: A simple implementation of (not probabilistic) CKY parser
-- Assignment: 
    add some lines of code to accommodate unary rules

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
grammar_cnf = nltk.grammar.CFG.fromstring("""
    S -> NP VP
    NP -> Det N | Det NP | NP PP | N N | 'I' | 'time'
    VP -> V NP | V PP | VP PP | VP ADV
    Det -> 'a' | 'an' | 'my' | 'My'
    N -> 'elephant' | 'pajamas' | 'time' | 'flies' | 'arrow' | 'dog' | 'cat' | 'fun'
    V -> 'shot' | 'flies' | 'like' | 'chased' | 'time'
    PP -> P N | P NP
    P -> 'for' | 'in' | 'like'
""")

## Sample grammar
# u-nary rules are now allowed
# NP_ and VP_ are intentionally introduced to make sure that 
# unary rules are properly handled
grammar = nltk.grammar.CFG.fromstring("""
    S -> NP_ VP_ | VP_
    NP_ -> NP
    NP -> N | N NP | Det NP | NP PP 
    VP_ -> VP
    VP -> V | VP NP | VP NP_PP | VP PP | VP ADV
    NP_PP -> NP PP
    Det -> 'a' | 'an' | 'my' | 'My'
    N -> 'I' | 'elephant' | 'pajamas' | 'time' | 'flies' | 'arrow' | 'dog' | 'cat' | 'fun'
    V -> 'shot' | 'flies' | 'like' | 'chased' | 'time'
    PP -> P NP
    P -> 'for' | 'in' | 'like'
""")

## some utilities
# extract unary rules from the grammar
def extract_unary_rules(grammar):
    return filter(lambda x: len(x.rhs())==1, grammar.productions())

# check duplicated trees
import itertools
def check_same_trees(trees):
    tt = list(itertools.combinations(trees, 2))
    print('Number of tree combinations:', len(tt))
    duplicate = False
    for t1, t2 in tt:
        if t1 == t2:
            print('same tree!', t1)
            duplicate = True
    if not duplicate:
        print('No same trees')

# draw multiples trees in a window
def draw_trees(trees):
    nltk.draw.tree.draw_trees(*trees)

# just for displaying WFST table
def show_wfst(tokens, wfst):
    num_tokens = len(tokens)
    for i in range(num_tokens+1):
        for j in range(i+1, num_tokens+1):
            print(i, j, wfst[(i,j)], '-',)
        print

## CKY parsing (initialization + table build_up)
# a well-formed substring table (wfst) is implemented by a n times (n+1) matrix, 
# where n is the number of tokens of a sentence

# initialize a wfst table w.r.t. input tokens and the grammar
def init_wfst(tokens, grammar):
    wfst = defaultdict(list)
    for i in range(len(tokens)):
        # -1 specially indicates a lexical rule
        wfst[(i,i+1)] = [(p.lhs(), ((i,i+1), -1))
        for seq, p in \
        enumerate(grammar.productions(rhs=tokens[i]))]
    # handling unary rules
    #
    # Add around 20 lines of code
    #
    return wfst

# develop the wfst by CKY algorithm
def build_wfst(tokens, wfst, grammar, verbose=True):
    if verbose:
        print("[building wfst]")
    num_tokens = len(tokens)
    #
    # Dictionary for storing rules. Notice that the key is RHS of a rule
    rule_d = dict((p.rhs(), p.lhs()) for p in grammar.productions())
    #
    # CKY main loop
#    history = []
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
            # handling unary rules for start ~ start+span
            #
            # Add around 20 lines of code (almost same as above place)
            #
            if verbose:
                print(start, start+span, wfst[(start, start+span)])
    return wfst

## build NlTK trees from an WFST table
def build_trees(tokens, wfst):
    return [build_tree_(tokens, root, wfst) for root in wfst[(0, len(tokens))]]

def build_tree_(tokens, node, wfst):
    unary = False
    if len(node) == 3: # binary branch
        symbol, (lspan, lseq), (rspan, rseq) = node
    else: # unary branch
        symbol, (lspan, lseq) = node
        unary = True
    if pre_terminal_node(lseq):
        return nltk.tree.Tree(str(symbol), 
                              children=[tokens[lspan[0]]])
    elif unary:
        return nltk.tree.Tree(str(symbol), 
                              children=[build_tree_(tokens,wfst[lspan][lseq],wfst)]) 
    else:
        return nltk.tree.Tree(str(symbol), 
                              children=[build_tree_(tokens,wfst[lspan][lseq],wfst), 
                                        build_tree_(tokens,wfst[rspan][rseq],wfst)])

def pre_terminal_node(lseq):
    return lseq == -1
   
## CKY Parser
def parse(tokens, grammar, verbose=True):
    wfst = init_wfst(tokens, grammar)
    if verbose: 
        print('[init wfst]')
        show_wfst(tokens, wfst)
    wfst = build_wfst(tokens, wfst, grammar, verbose)
    trees = build_trees(tokens, wfst)
    if verbose:
        print('[completed wfst]')
        show_wfst(tokens, wfst)
        print('Found', len(trees), 'trees')
        check_same_trees(trees)
    return trees