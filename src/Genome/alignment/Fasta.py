"""
Process Fasta and Fastq format and return the sequence
"""
class Fasta():
    def readFasta(self, fastaFile):
        genome = ''
        with open(fastaFile, 'r') as f:
            for line in f:
                # ignore header line with genome information
                if not line[0] == '>':
                    genome += line.rstrip()
        return genome

    def readFastq(self, fastqFile):
        sequences = []
        qualities = []
        with open(fastqFile) as fh:
            while True:
                fh.readline()  # skip name line
                seq = fh.readline().rstrip()  # read base sequence
                fh.readline()  # skip placeholder line
                qual = fh.readline().rstrip() # base quality line
                if len(seq) == 0:
                    break
                sequences.append(seq)
                qualities.append(qual)
        return sequences, qualities

    def reverseComplement(self, s):
        complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'N': 'N'}
        t = ''
        for base in s:
            t = complement[base] + t
        return t

    def naive(self, pat, genome, errs=0):
        m1 = self.findPattern(pat, genome, errs)
        revcomp = self.reverseComplement(pat)
        if pat != revcomp:
            o2 = self.findPattern(revcomp, genome, errs)
        else:
            o2 = []
        return m1,o2


    def findPattern(self, pat, genome, errs=0):
        occurrences = []
        for i in range(len(genome) - len(pat) + 1):  # loop over alignments
            bad = 0
            for j in range(len(pat)):  # loop over characters
                if genome[i+j] != pat[j]:  # compare characters
                    bad += 1
            if bad <= errs:
                occurrences.append(i)  # enough chars matched; record
        return occurrences
