WORD_SCORES = [0, 0, 0.1, 0.1, 0.2, 0.3, 0.5, 0.8, 1, 1.2, 1.5, 2, 2.5, 3.2]

def content_score(text):
	"""Computes a score intended to correlate with the amount of
	information conveyed by a block of prose."""

	score = 0
	word_counts = {}	# keep track of the words seen so we can penalise repetitiveness
	for w in text.lower().split(' '):
		try:
			wscore = WORD_SCORES[len(w)]
		except IndexError:
			wscore = WORD_SCORES[-1]
		
		wc = word_counts.get(w, 1)
		score += wscore / wc
		word_counts[w] = wc + 1

	return score


class StringAttributeScorer(object):
	def __init__(self, target, max_score):
		self.target = target
		self.max_score = max_score

	def get_score(self, inst):
		try:
			s = content_score(getattr(inst, self.name))
		except AttributeError:
			return 0
		
		return min(s, self.target)/float(self.target) * self.max_score


class HasAttributeScorer(object):
	def __init__(self, score):
		self.score = score

	def get_score(self, inst):
		if getattr(inst, self.name, None):
			return self.score
		return 0


class DeclarativeScoreSystem(type):
	def __init__(cls, name, bases, dict):
		scorers = []
		for n in dict:
			if hasattr(n, 'get_score'):
				s = dict[n]
				s.name = n
				scorers.append(s)
				del(dict[n])
		dict['scorers'] = scorers 
		return type.__init__(self, cls, bases, dict)


class ObjectScorer(object):
	__metaclass__ = DeclarativeScoreSystem

	def get_score(self, inst):
		return sum([s.get_score(inst) for s in self.scorers])

