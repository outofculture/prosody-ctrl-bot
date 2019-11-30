import random


with open('/usr/share/dict/words') as wordsfile:
    wordlist = [word for word in wordsfile.read().split('\n') if "'" not in word]


def make_password():
    return '{} {} {}'.format(random.choice(wordlist), random.choice(wordlist), random.choice(wordlist))
