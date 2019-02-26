import random


with open('/usr/share/dict/words') as wordsfile:
    wordlist = wordsfile.read().split('\n')


def make_password():
    passwd = random.choice(wordlist)
    while len(passwd) < 20:
        passwd = '{} {}'.format(passwd, random.choice(wordlist))
    return passwd
