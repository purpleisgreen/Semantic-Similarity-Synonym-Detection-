'''
- Part C done
- Part B done
- Part A done
- Part D done but not tested
- Part E
'''


def build_semantic_descriptors(sentences):
    res = {}
    for sentence in sentences:
        unique_in_sentence = list(set(sentence))  # Unique words in THIS sentence only
        for w in unique_in_sentence:
            if w not in res:
                res[w] = {}

        # Only compare words WITHIN this sentence (not all uniqueWords)
        for i, w in enumerate(unique_in_sentence):
            for j, u in enumerate(unique_in_sentence):
                if i == j:
                    continue
                res[w][u] = res[w].get(u, 0) + 1
    return res

def build_semantic_descriptors_from_file0(filenames):
    allText = ""
    lengthOfFiles = len(filenames)
    for i in range (lengthOfFiles):
        with open(filenames[i], "r", encoding = "latin1") as f:
            allText = allText + f.read()
    #splits the text into sentences
    listOfSentences = spliter(allText)
    #print(listOfSentences)
    #gets the semantic descriptors
    semanticDescriptors = build_semantic_descriptors(listOfSentences)
    return semanticDescriptors

def cosine_similarity(vec1, vec2):
    #vec1 and vec2 are dictionaries, just the values, does not include the keys

    if vec1 == {}:
        return -1
    if vec2 == {}:
        return -1

    wordOneSquared = 0
    wordTwoSquared = 0

    for coordinate in vec1.values():
        wordOneSquared = wordOneSquared + coordinate * coordinate
    for coor in vec2.values():
        wordTwoSquared = wordTwoSquared + coor * coor

    bottom = wordOneSquared * wordTwoSquared
    bottom = bottom ** 0.5

    top = 0
    for value in vec1.keys():
        if value in vec2.keys():
            valueOne = vec1[value]
            valueTwo = vec2[value]
            top = top + valueOne * valueTwo

    if bottom == 0:
        return -1
    return top/bottom

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    indexMax = 0
    maxValue = -2
    i = 0
    counter = 0
    if word not in semantic_descriptors:
        return choices[0]
    for w in choices:
        if w not in semantic_descriptors:
            tempRes = -1
        else:
            counter = 0
            vec1 = semantic_descriptors[w]
            vec2 = semantic_descriptors[word]
            tempRes = similarity_fn(vec1, vec2)
        if tempRes > maxValue:
            maxValue = tempRes
            indexMax = i
        i = i + 1
    return choices[indexMax]

def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    counter = 0
    numCorrect = 0
    with open(filename, 'r') as file:
        for line in file:
            counter = counter + 1
            words = line.split()
            w = words[0]
            rightAnswer = words[1]
            choices = words[2:]
            answer = most_similar_word(w, choices, semantic_descriptors, similarity_fn)
            print(w, rightAnswer, answer)
            if answer == rightAnswer:
                numCorrect = numCorrect + 1
    percent = numCorrect/counter
    percent = percent*100
    return round(percent, 1)
def spliter(text):
    # Seperates sentences: . ! ? -> have to check which one is first, make the list, and then splice it
    # Does not seperate sentences: , - -- : ; ' " -> have to remove these
    resList = []
    stopChar1 = "."
    stopChar2 = "!"
    stopChar3 = "?"

    #Removes all unnessary characters
    text = text.replace(",", "")
    text = text.replace("-", " ")
    text = text.replace("--", " ")
    text = text.replace(":", " ")
    text = text.replace(";", " ")
    text = text.replace("'", "")
    text = text.replace('"', "")

    #Splitting into sentences using . ! and ?
    done = False
    resList = []
    while done is False:
        indexStopChar1 = text.find(stopChar1)
        indexStopChar2 = text.find(stopChar2)
        indexStopChar3 = text.find(stopChar3)

        validIndices = []
        if indexStopChar1 != -1:
            validIndices.append(indexStopChar1)
        if indexStopChar2 != -1:
            validIndices.append(indexStopChar2)
        if indexStopChar3 != -1:
            validIndices.append(indexStopChar3)
        if validIndices == []:
            done = True
            break
        index = min(validIndices)
        tempString = text[:index]
        words = tempString.split()
        resList.append(words)
        text = text[index+1:]
    return resList


if __name__ == "__main__":
    files = (["WarAndPeace.txt", "SwannsWay.txt"])
    semanticDescriptors = build_semantic_descriptors_from_file0(files)
    print(run_similarity_test("test.txt", semanticDescriptors, cosine_similarity))


