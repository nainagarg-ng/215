import re
import math

####feature engineering####
def entropy(domain, base=2):

    if domain == None:
        return 0
    
    entropy = 0.0

    try:
        length = len(str(domain))
    except:
        length = 0.0001

    occ = {}
    for c in domain:
        if not c in occ:
            occ[c] = 0
        occ[c] += 1

    for k, v in occ.items():
        p = float(v) / float(length)
        entropy -= p * math.log(p, base)

    return entropy


def length(domain):
    try:
        return len(domain) if (domain) else  0
    except:
        return 0
    
def number_of_vowels(domain):
    try:
        return len(re.findall("[aeiouAEIOU]", domain)) if (domain) else  0
    except:
        return 0

def number_of_consonants(domain):
    try:
        return len(re.findall("[^aeiou.AEIOU]", domain)) if (domain) else  0
    except:
        return 0

def number_of_numbers(domain):
    try:
        return len(re.findall("[0-9]", domain)) if (domain) else  0
    except:
        return 0

def number_of_specials(domain):
    try:
        return len(re.findall("[^0-9a-zA-Z]", domain))  if (domain) else  0
    except:
        return 0

####end features####