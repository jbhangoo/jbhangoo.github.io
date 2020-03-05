"""
Use Boyer Moore algorithm to find pattern in text
First, pre process the pattern to create tables of how many positions to skip for different situations
Original Author: Ben Langmead
"""
from alignment.BoyerMooreTables import BoyerMooreTables

class BoyerMoore():
    def __init__(self, p, alphabet='ACGT'):
        self.p = p
        supportTables = BoyerMooreTables()
        # Create map from alphabet characters to integers
        self.amap = {alphabet[i]: i for i in range(len(alphabet))}
        # Make bad character rule table
        self.bad_char = supportTables.dense_bad_char_tab(p, self.amap)
        # Create good suffix rule table
        _, self.big_l, self.small_l_prime = supportTables.good_suffix_table(p)

    def bad_character_rule(self, i, c):
        '''
        Return # skips given by bad character rule at offset i
        '''
        assert c in self.amap
        assert i < len(self.bad_char)
        ci = self.amap[c]
        return i - (self.bad_char[i][ci]-1)

    def good_suffix_rule(self, i):
        """ Given a mismatch at offset i, return amount to shift
            as determined by (weak) good suffix rule. """
        length = len(self.big_l)
        assert i < length
        if i == length - 1:
            return 0
        i += 1  # i points to leftmost matching position of P
        if self.big_l[i] > 0:
            return length - self.big_l[i]
        return length - self.small_l_prime[i]

    def match_skip(self):
        '''
        Skip entire length of pattern, unless you are at the end of text t 
        '''
        return len(self.small_l_prime) - self.small_l_prime[1]

    def align(self, t):
        '''
        Step through the text. Use the pre-processed tables to jump ahead past characters that can't match
        '''
        i = 0
        occurrences = []
        while i < len(t) - len(self.p) + 1:
            shift = 1
            mismatched = False
            for j in range(len(self.p)-1, -1, -1):
                if self.p[j] != t[i+j]:
                    skip_bc = self.bad_character_rule(j, t[i+j])
                    skip_gs = self.good_suffix_rule(j)
                    shift = max(shift, skip_bc, skip_gs)
                    mismatched = True
                    break
            if not mismatched:
                occurrences.append(i)
                skip_gs = self.match_skip()
                shift = max(shift, skip_gs)
            i += shift
        return occurrences
