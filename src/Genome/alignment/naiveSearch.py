from alignment.Fasta import Fasta

fasta = Fasta()

"""
p = 'CCC'
ten_as = 'AAAAAAAAAA'
t = ten_as + 'CCC' + ten_as + 'GGG' + ten_as
occurrences = fasta.naive(p, t)
print(occurrences)

p = 'CGCG'
t = ten_as + 'CGCG' + ten_as + 'CGCG' + ten_as
occurrences = fasta.naive(p, t)
print(occurrences)

print(fasta.naive('ACTTTA', 'ACTTACTTGATAAAGT', 2))
"""

phix_genome = fasta.readFasta('data/lambda_virus.fa')
o1,o2 = fasta.naive('AGGAGGTT', phix_genome, 2)
if len(o1) > 0:
    print('%s: offset of leftmost occurrence: %d' % ('pat', min(o1)))
    print('# occurrences: %d' % len(o1))
if len(o2) > 0:
    print('%s: offset of leftmost occurrence: %d' % ("REV-pat", min(o2)))
    print('# occurrences: %d' % len(o2))
