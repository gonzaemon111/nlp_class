# -*- coding: utf-8 -*-
"""
Sample tiny rule sets for developing a pcky parser

@author: yoshihiko
"""
#
import nltk

## Sample sentences from nltk
t1_s = 'I saw the man with my telescope' 
t1_t = nltk.word_tokenize(t1_s)
t2_s = 'the boy saw Jack with Bob under the table with a telescope'
t2_t = nltk.word_tokenize(t2_s)
pierre_t = ['Pierre', 'Vinken', ',', '61', 'years', 'old', ',', 'will', 'join', 'the', 'board', 'as', 'a', 'nonexecutive', 'director', 'Nov.', '29', '.']

### Toy pcfg1 from nltk
toy_pcfg1 = nltk.PCFG.fromstring(
    """
    S -> NP VP [1.0]
    NP -> Det N [0.5] | NP PP [0.25] | 'John' [0.1] | 'I' [0.15]
    Det -> 'the' [0.8] | 'my' [0.2]
    N -> 'man' [0.5] | 'telescope' [0.5]
    VP -> VP PP [0.1] | V NP [0.7] | V [0.2]
    V -> 'ate' [0.35] | 'saw' [0.65]
    PP -> P NP [1.0]
    P -> 'with' [0.61] | 'under' [0.39]
    """
)

### Toy pcfg2 from nltk
toy_pcfg2 = nltk.PCFG.fromstring(
    """
    S    -> NP VP         [1.0]
    VP   -> V NP          [.59]
    VP   -> V             [.40]
    VP   -> VP PP         [.01]
    NP   -> Det N         [.41]
    NP   -> Name          [.28]
    NP   -> NP PP         [.31]
    PP   -> P NP          [1.0]
    V    -> 'saw'         [.21]
    V    -> 'ate'         [.51]
    V    -> 'ran'         [.27]
    V    -> 'table'       [.01]
    N    -> 'boy'         [.11]
    N    -> 'cookie'      [.12]
    N    -> 'table'       [.13]
    N    -> 'telescope'   [.14]
    N    -> 'hill'        [.5]
    Name -> 'Jack'        [.52]
    Name -> 'Bob'         [.48]
    P    -> 'with'        [.61]
    P    -> 'under'       [.39]
    Det  -> 'the'         [.41]
    Det  -> 'a'           [.31]
    Det  -> 'my'          [.28]
    """
)

### My grammar to check the handling of unary rules
my_grammar = nltk.PCFG.fromstring("""
    S -> NP VP [.90] | NP_ VP_ [.05] | VP_ [.05]
    NP_ -> NP [1.0]
    NP -> N [0.25] | N NP [0.25] | Det NP [.35] | NP PP [.15] 
    VP_ -> VP [1.0]
    VP -> V [.2] | VP NP [.3] | VP NP_PP [.2] | VP PP [.15] | VP ADV [.15]
    NP_PP -> NP PP [1.0]
    Det -> 'a' [.4] | 'an' [.4] | 'my' [.1] | 'My' [.1]
    N -> 'I' [.2] | 'elephant' [.1] | 'pajamas' [.1] | 'time' [.1] | 'flies' [.1] | 'arrow' [.1] | 'dog' [.1] | 'cat' [.1] | 'fun' [.1] 
    V -> 'shot' [.2] | 'flies' [.2] | 'like' [.2] | 'chased' [.2] | 'time' [.2]
    PP -> P NP [1.0]
    P -> 'for' [.4] | 'in' [.4] | 'like' [.2]
""")

my_grammar2 = nltk.PCFG.fromstring("""
    S -> NP_ VP_ [.95] | VP_ [.05]
    NP_ -> NP [1.0]
    NP -> N [0.25] | N NP [0.25] | Det NP [.35] | NP PP [.15] 
    VP_ -> VP [1.0]
    VP -> VP_ [0.1]| V [0.1] | VP NP [.3] | VP NP_PP [.2] | VP PP [.15] | VP ADV [.15]
    NP_PP -> NP PP [1.0]
    Det -> 'a' [.4] | 'an' [.4] | 'my' [.1] | 'My' [.1]
    N -> 'I' [.2] | 'elephant' [.1] | 'pajamas' [.1] | 'time' [.1] | 'flies' [.1] | 'arrow' [.1] | 'dog' [.1] | 'cat' [.1] | 'fun' [.1] 
    V -> 'shot' [.2] | 'flies' [.2] | 'like' [.2] | 'chased' [.2] | 'time' [.2]
    PP -> P NP [1.0]
    P -> 'for' [.4] | 'in' [.4] | 'like' [.2]
""")

### Sample sentences for my grammar
elephant_s = 'I shot an elephant in my pajamas'
elephant_t = nltk.word_tokenize(elephant_s)
dog_s = 'My dog chased a cat for fun'
dog_t = nltk.word_tokenize(dog_s)
time_s = 'time flies like an arrow'
time_t = nltk.word_tokenize(time_s)