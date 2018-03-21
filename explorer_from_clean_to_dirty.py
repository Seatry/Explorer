#Задача поиска списка пользовательских адресов соответствующих адресу из БД

names = ["федеральный округ", "городской округ", "республика", "респ", "район", "микрорайон", "жилой массив", "садовое товарищество",
         "область", "россия", "поселок городского типа", "дом", "р-н", "пр-зд", "пл-ка", "кв-л", "б-р", "пр-кт"]
delimeters = [" ", ".", "," ]
keyWords = ["пл", "ул", "г", "д", "пгт", "гор", "с",  "тер", "снт", "дп", "кп", "мкр", "б", "м", "бол", "мал", "обл" ]

def deleteKeyWords(s) :
     for key in keyWords:
        for delimeter in delimeters:
            s = s.replace(key+delimeter, '')
     for name in names:
         s = s.replace(name, '')
     s = s.replace('ё', 'е')
     return s

class Symbol:
    LETTER = 0,
    NUMBER = 1,
    DELIMITER = 2

def correctMeaning(meaning, correct, ind) :
    if meaning != correct :
        meaning = correct
        ind = 0
    return ind, meaning

def makeGramm(s, i, trigramms, ind):
    trigramms.add(s[i-ind:i+1])
    if ind < 1 :
        ind += 1
    return ind

def makeToken(meaning, tokens, trigrammsL):
    if meaning == Symbol.LETTER and len(trigrammsL) != 0:
        tokens.append(trigrammsL.copy())
        trigrammsL.clear()

def gramming(s) :
    meaning = Symbol.LETTER
    tokens = list()
    trigrammsL = set()
    trigrammsN = set()
    ind = 0
    for i, c in enumerate(s):
        if c.isalpha():
            s = s[i:len(s)]
            break
    s = s.lower()
    s = deleteKeyWords(s)
    for i, c in enumerate(s) :
        if c.isalpha() :
            if meaning == Symbol.NUMBER:
                break
            ind, meaning = correctMeaning(meaning, Symbol.LETTER, ind)
            ind = makeGramm(s, i, trigrammsL, ind)
        elif c.isdigit() :
            makeToken(meaning, tokens, trigrammsL)
            ind, meaning = correctMeaning(meaning, Symbol.NUMBER, ind)
            ind = makeGramm(s, i, trigrammsN, ind)
        elif c != '|'  :
            makeToken(meaning, tokens, trigrammsL)
            if c != '-' and meaning == Symbol.NUMBER:
                break
            meaning = Symbol.DELIMITER
        else:
            break
    makeToken(meaning, tokens, trigrammsL)
    return tokens, trigrammsN

def ratio(tokenSearched, tgrSearchedN, tokenBased, tgrBasedN, results, strBased):
    similar = True
    indexes = list()
    for tokenB in tokenBased:
        found = False
        for i, tokenS in enumerate(tokenSearched):
            cross = len(set.intersection(tokenS,tokenB))
            rate = cross / (len(tokenS) + len(tokenB) - cross)
            if rate >= 0.65 and indexes.count(i) == 0:
                indexes.append(i)
                found = True
                break
        if not found:
            similar = False
            break

    crossN = len(set.intersection(tgrSearchedN, tgrBasedN))
    if len(tgrBasedN) == 0 and len(tgrSearchedN) != 0:
        step_rateN = 0
    elif len(tgrSearchedN) == 0:
        step_rateN = 1
    else:
        step_rateN = crossN / (len(tgrBasedN) + len(tgrSearchedN) - crossN)

    if similar and step_rateN == 1:
        results.add(strBased)

    return results

def search(base, tokenSearched, tgrSearchedN) :
    results = set()
    for strBased in base:
        tokenBased, tgrBasedN = gramming(strBased)
        results = ratio(tokenSearched, tgrSearchedN, tokenBased, tgrBasedN, results, strBased)
    return results

def main() :
    with open("search_addr.txt", "r") as addrs, open("result1_1.txt", "w") as out :
        for strSearched in addrs :
            tokensSearched, tgrSearchedN = gramming(strSearched)
            with open("kazan2.txt", "r") as base :
                results = search(base, tokensSearched, tgrSearchedN)
                if len(results) == 0:
                    out.writelines("Ничего не найдено" + '| ' + strSearched + '\n')
                else:
                    for result in results:
                        out.writelines(result )
            out.writelines('\n')

main()
