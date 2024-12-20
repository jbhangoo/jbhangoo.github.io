from alignment.BoyerMoore import BoyerMoore
  
def boyer_moore(p, p_bm, t):
    """ Do Boyer-Moore matching """
    i = 0
    occurrences = []
    while i < len(t) - len(p) + 1:
        shift = 1
        mismatched = False
        for j in range(len(p)-1, -1, -1):
            if p[j] != t[i+j]:
                skip_bc = p_bm.bad_character_rule(j, t[i+j])
                skip_gs = p_bm.good_suffix_rule(j)
                shift = max(shift, skip_bc, skip_gs)
                mismatched = True
                break
        if not mismatched:
            occurrences.append(i)
            skip_gs = p_bm.match_skip()
            shift = max(shift, skip_gs)
        i += shift
    return occurrences

p ='GCGTATGC'
t ='TATTGGCTATACGGTT'
p = 'TAT'
p,t = 'TATATTAT', 'TATATTATACTTATATTATATTATATGA'

bm = BoyerMoore(p)
m =  boyer_moore(p, bm, t)
print(m)