from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktTrainer
from nltk.stem import WordNetLemmatizer
from collections import OrderedDict
from itertools import islice

lemmatizer = WordNetLemmatizer()

def clean_text(text):

	stop_words = set(stopwords.words('english'))
	pcts = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
	text = text.lower()
	tokens = word_tokenize(text)

	words = [w for w in tokens if w not in stop_words]
	words = [w for w in words if w not in pcts]

	return words


def score_words(text):

	unique = []
	imp_words = clean_text(text)
	score = {}
	
	for w in imp_words:
		#print(w)
		w = lemmatizer.lemmatize(w)
		if w not in unique:
			unique.append(w)
			score[w] = 1

		elif w in unique:
			score[w] += 1

	return [score, unique]

def score_sentences(text, word_scores, unique):

	trainer = PunktTrainer()
	trainer.INCLUDE_ALL_COLLOCS = True
	trainer.train(text)
	sent_score = {}
	
	sent_tokenizer = PunktSentenceTokenizer(trainer.get_params())
	sentences = sent_tokenizer.tokenize(text.lower())

	for s in sentences:
		words = clean_text(s)
		sent_score[s] = 0

		for w in words:
			w = lemmatizer.lemmatize(w)
			if w in unique:
				sent_score[s] += word_scores[w]

	return sent_score


def similarity_score(t, s):

	tt = clean_text(t)
	st = clean_text(s)
	count = 0

	for w in st:
		if w in tt:
			count += 1

	ratio = count / len(tt)

	return ratio


def rank_sentences(text, sentence_scores, title="", n=7):

	final_sentences = []

	trainer = PunktTrainer()
	trainer.INCLUDE_ALL_COLLOCS = True
	trainer.train(text)	
	sent_tokenizer = PunktSentenceTokenizer(trainer.get_params())

	for s in sentence_scores:
		if title == "":
			break
		else:
			sentence_scores[s] *= (1 + similarity_score(title, s))

	sc = sentence_scores.copy()
	sc = OrderedDict(sorted(sc.items(), key=lambda t: t[1], reverse=True))
	ordered_sents = dict(islice(sc.items(), n))

	proper_sentences = sent_tokenizer.tokenize(text)

	for s in proper_sentences:
		if s.lower() in ordered_sents:
			final_sentences.append(s)

	return final_sentences


def summarize(text, title="", n=7):

	word_scores, unique_words = score_words(text)
	sentence_scores = score_sentences(text, word_scores, unique_words)
	final_sentences = rank_sentences(text, sentence_scores, title, n)

	return final_sentences





















"""
senti = '''The U.S. Supreme Court struck down a Minnesota law Thursday that prohibited voters [from wearing political buttons and apparel] when they cast ballots.

In a 7-2 decision, the high court revoked a century-old Minnesota law that barred voters from wearing politically affiliated clothing at polling places.

The ban covered all articles of clothing and accessories that contained a political insignia or message. Violators were subject to a fine or petty misdemeanor charge.

Clothing that speaks to an issue on the ballot or promotes a group with recognizable political views are also banned. Examples include a National Rifle Association T-shirt or one with the text of the Second Amendment.

The state said its approach preserved order and decorum at polling places and helped prevent voter intimidation.

The challengers, citing the First Amendment, said [the law is too vague – that] the state should not be able to prohibit such a broad swath of politically expressive clothing.

Chief Justice John Roberts, writing for the court, said Minnesota’s law was vague and open to confusion at times, and noted it must be guided by workable and objective standards.

“Without them, an election judge’s own politics may shape his views on what counts as ‘political.’ And if voters experience or witness episodes of unfair or inconsistent enforcement of the ban, the State’s interest in maintaining a polling place free of distraction and disruption would be undermined by the very measure intended to further it,” Roberts wrote.

Most states have laws restricting what voters can wear when they cast ballots, but Minnesota’s law was one of the broadest. It barred voters from casting a ballot while wearing clothing with the name of a candidate or political party. Also not allowed: clothing that references an issue on the ballot or promotes a group with recognizable political views. Delaware, Kansas, Montana, New Jersey, New York, South Carolina, Tennessee, Texas and Vermont all have similar laws to Minnesota’s. South Carolina also has a restriction, but it applies only to what can be worn inside the polling place by candidates themselves, not voters.

“Minnesota, like other states, has sought to strike the balance in a way that affords the voter the opportunity to exercise his civic duty in a setting removed from the clamor and din of electioneering,” Roberts wrote. “While that choice is generally worthy of our respect, Minnesota has not supported its good intentions with a law capable of reasoned application.”

Roberts noted the broad definition of the law could ban a t-shirt that simply said “Vote!” or a t-shirt saying “Support our Troops” or “#MeToo.”

Justice Sonia Sotomayor, joined by Stephen Breyer in the dissenting opinion, argued there was no evidence the Minnesota statute was interpreted or applied in an unreasonable manner.

“There is no evidence that any individual who refused to remove a political item has been prohibited from voting, and respondents maintain that no one has been referred for prosecution for violating the provision,” Sotomayor wrote.

The case was brought to the court by Andrew Cilek, who went to a polling place in 2010 wearing a shirt with a Tea Party logo and the words “Don’t Tread on Me” on it, as well as a button with the words “Please I.D. Me,” a reference to legislation then under discussion in Minnesota that would have required residents to show photo identification to vote. The legislation ultimately didn’t become law.

Election workers initially stopped Mr. Cilek from casting a ballot, telling him he must remove his t-shirt and button. [He changed his shirt a few times – to others deemed unacceptable by the poll workers, and after taking down his name and address for potential prosecution], they eventually let him vote.

“If you showed 20 election judges various logos and T-shirts and asked them if they were allowed under the statute, you’d get 20 different answers,” Cilek said.

The Supreme Court has previously backed some restrictions on voters’ free speech rights at the polls. In 1992, the court upheld a Tennessee statute prohibiting the display or distribution of campaign materials within 100 feet of a polling place.
'''

title = '''U.S. Supreme Court strikes down Minnesota dress code for voters'''

if __name__ == "__main__":

	fst = summarize(senti, n=9)
	for s in fst:
		print(s)
		print('--------------------------------------------------------------------')

"""

# print(senti)
	



""" 

dt = {"ts": 10, "te":23, "tr":3, "td": 9, "ty": 11, "tt":2, "tf":7}

>>> dt

{'ts': 10, 'te': 23, 'tr': 3, 'td': 9, 'ty': 11, 'tt': 2, 'tf': 7}

>>> dc = OrderedDict(sorted(dt.items(), key=lambda t: t[1], reverse=True))

>>> dc

OrderedDict([('te', 23), ('ty', 11), ('ts', 10), ('td', 9), ('tf', 7), ('tr', 3), ('tt', 2)])

ds = dict(islice(dc.items(), 4))

>>> ds

{'te': 23, 'ty': 11, 'ts': 10, 'td': 9}





"""

