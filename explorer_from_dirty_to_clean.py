#Задача поиска адреса пользователя в БД

keyWords = ["федеральный округ", "городской округ", "республика", "респ", "район",
                                "р-н", "жилой массив", "садовое товарищество", "область", "россия"]

def deleteKeyWords(s) :
    for key in keyWords :
        s = s.replace(key, '')
    s = s.replace("большая", "б.")
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
    if ind < 2 :
        ind += 1
    return ind

def gramming(s) :
    meaning = Symbol.LETTER
    ind = 0
    trigramms = set()
    #for i, c in enumerate(s):
        #if c.isalpha():
           # s = s[i:len(s)]
           # break
    s = s.lower()
    s = deleteKeyWords(s)
    for i, c in enumerate(s) :
        if c.isalpha() :
            ind, meaning = correctMeaning(meaning, Symbol.LETTER, ind)
            ind = makeGramm(s, i, trigramms, ind)
        elif c.isdigit() :
            ind, meaning = correctMeaning(meaning, Symbol.NUMBER, ind)
            ind = makeGramm(s, i, trigramms, ind)
        elif (c != '|') :
            meaning = Symbol.DELIMITER;
        else:
            break
    return trigramms

def ratio(tgrSearched, tgrBased, rate, result, strBased) :
    cross = len(set.intersection(tgrSearched, tgrBased))
    step_rate = cross / (len(tgrBased) + len(tgrSearched) - cross)
    if rate < step_rate :
        rate = step_rate
        result = strBased
    return rate, result

def search(base, tgrSearched) :
    rate = 0.0
    result = "Ничего не найдено\n"
    for strBased in base:
        tgrBased = gramming(strBased)
        rate, result = ratio(tgrSearched, tgrBased, rate, result, strBased)
        if rate == 1.0 :
            break
    return result

def main() :
    with open("search_addr.txt", "r") as addrs, open("result.txt", "w") as out :
        for strSearched in addrs :
            tgrSearched = gramming(strSearched)
            with open("full_addr.txt", "r") as base :
                result = search(base, tgrSearched)
                out.writelines(result)

main()
