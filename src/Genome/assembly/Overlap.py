from src.Genome import Levenshtein

class Overlap():
    def __init__(self, fastqFile, k):
        '''
        Store reads from the FASTQ file into a list
        Also build a dictionary that maps every k-mer to all reads that contain it
        :param fastqFile:   Input file
        :param k:           Fragment size
        '''
        self.k = k
        self.readsContaining = {}
        with open(fastqFile) as fh:
            self.reads = []
            while True:
                fh.readline()  # skip name line
                read = fh.readline().rstrip()  # read base sequence
                slen = len(read)
                if slen == 0:
                    break
                self.reads.append(read)
                fh.readline()  # skip placeholder line
                fh.readline().rstrip() # skip base quality line

                for i in range(slen-k+1):
                    kmer = read[i:i+k]
                    if kmer not in self.readsContaining:
                        self.readsContaining[kmer] = set()
                    self.readsContaining[kmer].add(read)

    def getOverlaps(self, errors=2):
        '''
        Use the kmer index to find all pairs of reads that overlap
        For each read, extract the length k prefix (kmer), then process every read that is indexed by it.
        Then compare the two reads to see if they actually overlap  -- within the allowed number of edits
        Repeat this process for the length k suffix k-mer.

        :param errors:  Maximum number of edit errors to allow in an overlap between reads
        :return:        Overlap dictionary where some suffix of the key overlaps some prefix of its value
        '''
        overlaps = {}
        for read in self.reads:
            pref = read[:self.k].strip()
            if len(pref) == 0:
                continue
            for candidate in self.readsContaining[pref]:
                if read != candidate:
                    # The candidate has the prefix somewhere inside it. Find that spot
                    # If everything after that point matches the beginning of the read, this is an overlap
                    startpoint = candidate.rfind(pref)
                    overlap_length = len(candidate) - startpoint
                    a = candidate[startpoint:]
                    b = read[:overlap_length]
                    mismatch = Levenshtein.distance(a, b)
                    if mismatch <= errors:
                        if candidate not in overlaps:
                            overlaps[candidate] = set()
                        overlaps[candidate].add((read, overlap_length))

            suff = read[-self.k:].strip()
            if len(suff) == 0:
                continue
            for candidate in self.readsContaining[suff]:
                if read != candidate:
                    # The candidate has the suffix somewhere inside it. Find that spot
                    # If everything after that point matches the beginning of the read, this is an overlap
                    startpoint = candidate.rfind(suff)
                    overlap_length = len(candidate) - startpoint
                    a = candidate[startpoint:]
                    b = read[:overlap_length]
                    mismatch = Levenshtein.distance(a, b)
                    if mismatch <= errors:
                        if read not in overlaps:
                            overlaps[read] = set()
                        overlaps[read].add((candidate, overlap_length))
        return overlaps

    def getOverlapSize(self, a, b, min_length=3):
        """
        Return length of longest suffix of 'a' matching
        a prefix of 'b' that is at least 'min_length'
        characters long.  If no such overlap exists,
        return 0.
        """
        start = 0  # start all the way at the left
        while True:
            start = a.find(b[:min_length], start)  # look for b's prefix in a
            if start == -1:  # no more occurrences to right
                return 0
            # found occurrence; check for full suffix/prefix match
            if b.startswith(a[start:]):
                return len(a) - start
            start += 1  # move just past previous match