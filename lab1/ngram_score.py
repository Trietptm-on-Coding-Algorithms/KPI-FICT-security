from math import log10

quadgrams = r'E:\Study\Универ\4-й курс\Безопасность\lab1\english_quadgrams.txt'
trigrams = r'E:\Study\Универ\4-й курс\Безопасность\lab1\english_trigrams.txt'


class ngram_score(object):
    def __init__(self, ngramfile, sep=' '):
        ''' load a file containing ngrams and counts, calculate log probabilities '''
        self.ngrams = {}
        for line in open(ngramfile, 'r'):
            key, count = line.split(sep)
            self.ngrams[key] = int(count)
        self.L = len(key)
        self.N = sum(list(self.ngrams.values()))
        # calculate log probabilities
        for key in list(self.ngrams.keys()):
            self.ngrams[key] = log10(float(self.ngrams[key]) / self.N)
        self.floor = log10(0.01 / self.N)

    def score(self, text):
        ''' compute the score of text '''
        score = 0
        ngrams = self.ngrams.__getitem__
        flattened_text = text.replace(' ', '')
        for i in range(len(flattened_text) - self.L + 1):
            if flattened_text[i:i + self.L] in self.ngrams:
                score += ngrams(flattened_text[i:i + self.L])
            else:
                score += self.floor
        return score
