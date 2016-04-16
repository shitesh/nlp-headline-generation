# define all the feature functions here
"""
List of features used:
1. Language model features
2. Headline Length feature
3. Part of Speech Language Model Feature

4. N-Gram Match feature
5. Content selection feature
"""

#structures for headline length feature
unique_length_count =0  # range considered is 3 to 15(13 values )
headline_length_count = {}
headline_length_probablity = {}
#structures for language model feature
unique_bigram_count = 0
language_model_count = {}
language_model_probablity = {}
word_count = {}
#structure for pos headline bigram feature
unique_bigram_pos_count = 0
bigram_model_count = {}

#structure for pos headline trigram feature
unique_trigram_pos_count = 0
trigram_model_count = {}
trigram_model_probablity = {}



def compute_headline_length_counts(headline_word_tag_list):
    """
    Input: A list with each entry having headline from input corpus
    operation: computes the headline length for each article headline  and stores the probablity for each headline length in a length dictionary
    """
    global headline_length_count,Unique_length_count # range considered is 3 to 15(13)


    for headline in headline_word_tag_list:
        count = 0
        tokens = headline.split(" ")
        for entry in tokens:
            word, tag = entry.rsplit('/', 1)
            count = count+1

        if count in headline_length_count:
            headline_length_count[count] +=1
        else:
            headline_length_count[count] =1
            Unique_length_count= Unique_length_count+1



def compute_headline_length_probablity(headline_word_tag_list):
    """
    Input: A list with each entry having headline from input corpus
    operation: computes the headline length for each article headline  and stores the probablity for each headline length in a length dictionary
    """
    global headline_length_count,Unique_length_count,headline_length_probablity # range considered is 3 to 15(13)

    headline_length_probablity = headline_length_count.copy()
    #computing total headline count
    total_no_of_headlines = len(headline_word_tag_list)
    compute_headline_length_counts(headline_word_tag_list)

    for i in headline_length_count:
        #print "key:"+str(i)+" val:"+str(headline_length_count[i])
        temp =  (headline_length_count[i])/float(total_no_of_headlines)
        #print "temp:"+str(temp)
        headline_length_probablity[i]=temp

def compute_word_count(headline_word_tag_list):
    """
    Input: A list with each entry having headline from input corpus
    operation: computes the word count of each word in dataset
    """

    global word_count
    for headline in headline_word_tag_list:
        tokens = headline.split(" ")
        for entry in tokens:
            word, tag = entry.rsplit('/', 1)
            if word in word_count:
                word_count[word] +=1
            else:
                word_count[word] =1



def compute_language_model_counts(headline_word_tag_list):
    """
    Input: A list with each entry having headline from input corpus
    operation: computes the language model counts for each article bigram  and stores the probablity for each bigram in  dictionary
    """
    global language_model_count,unique_bigram_count

    prev = "start"
    cur = "start"

    for headline in headline_word_tag_list:
        tokens = headline.split(" ")
        for entry in tokens:
            word, tag = entry.rsplit('/', 1)
            prev = cur
            cur = word
            if prev in language_model_count:

                if cur in language_model_count[prev]:
                    language_model_count[prev][cur]+=1
                else:
                    language_model_count[prev][cur] =1
            else:
                unique_bigram_count = unique_bigram_count+1
                language_model_count[prev] = {}
                if cur in language_model_count[prev]:
                    language_model_count[prev][cur]+=1
                else:
                    language_model_count[prev][cur] =1

def compute_language_model_probablity(headline_word_tag_list):
    """
    Input: A list with each entry having headline from input corpus
    operation: computes the language model probablity for each article bigram  and stores the probablity for each bigram in  dictionary
    """
    global language_model_count,unique_bigram_count,language_model_probablity,word_count

    compute_word_count(headline_word_tag_list)
    compute_language_model_counts(headline_word_tag_list)

    prev = "start"
    cur = "start"
    language_model_probablity = dict(language_model_count)

    for headline in headline_word_tag_list:
        tokens = headline.split(" ")
        for entry in tokens:
            word, tag = entry.rsplit('/', 1)
            prev = cur
            cur = word
            if prev in language_model_probablity:

                if cur in language_model_probablity[prev]:
                    language_model_probablity[prev][cur] = (language_model_count[prev][cur])/float(word_count[prev])
                else:
                    language_model_probablity[prev][cur] =(language_model_count[prev][cur])/float(word_count[prev])
            else:

                language_model_probablity[prev] = {}
                language_model_probablity[prev][cur] =(1)/float(word_count[prev])




def compute_bigram_counts(headline_word_tag_list):
    """
    Input: A list with each entry having headline from input corpus
    operation: computes the language model counts for each article bigram  and stores the probablity for each bigram POSin  dictionary
    """
    global bigram_model_count,unique_bigram_pos_count

    prev = "start"
    cur = "start"

    for headline in headline_word_tag_list:
        tokens = headline.split(" ")
        for entry in tokens:
            word, tag = entry.rsplit('/', 1)
            prev = cur
            cur = tag
            if prev in bigram_model_count:

                if cur in bigram_model_count[prev]:
                    bigram_model_count[prev][cur]+=1
                else:
                    bigram_model_count[prev][cur] =1
            else:
                unique_bigram_pos_count = unique_bigram_pos_count+1
                bigram_model_count[prev] = {}
                if cur in bigram_model_count[prev]:
                    bigram_model_count[prev][cur]+=1
                else:
                    bigram_model_count[prev][cur] =1


def compute_trigram_counts(headline_word_tag_list):
    """
    Input: A list with each entry having headline from input corpus
    operation: computes the language model counts for each article trigram  and stores the probablity for each trigram POS in  dictionary
    """
    global trigram_model_count,unique_trigram_pos_count

    prev = "start"
    cur = "start"
    next = "start"

    for headline in headline_word_tag_list:
        tokens = headline.split(" ")
        for entry in tokens:
            word, tag = entry.rsplit('/', 1)
        prev = cur
        cur = next
        next = tag

        if prev in trigram_model_count:

                if cur in trigram_model_count[prev]:

                    if next in trigram_model_count[prev][cur]:

                        trigram_model_count[prev][cur][next]+=1
                    else:
                        unique_trigram_pos_count = unique_trigram_pos_count+1
                        trigram_model_count[prev][cur][next] =1

                else:

                    trigram_model_count[prev][cur]={}
                    if next in trigram_model_count[prev][cur]:

                        trigram_model_count[prev][cur][next]+=1
                    else:
                        unique_trigram_pos_count = unique_trigram_pos_count+1
                        trigram_model_count[prev][cur][next] =1

        else:

             trigram_model_count[prev]={}
             if cur in trigram_model_count[prev]:

                    if next in trigram_model_count[prev][cur]:

                        trigram_model_count[prev][cur][next]+=1
                    else:
                        unique_trigram_pos_count = unique_trigram_pos_count+1
                        trigram_model_count[prev][cur][next] =1

             else:

                    trigram_model_count[prev][cur]={}
                    if next in trigram_model_count[prev][cur]:

                        trigram_model_count[prev][cur][next]+=1
                    else:
                        unique_trigram_pos_count = unique_trigram_pos_count+1
                        trigram_model_count[prev][cur][next] =1


# P( wi | wi-1 wi-2 ) = count ( wi, wi-1, wi-2 ) / count ( wi-1, wi-2 )



def compute_pos_language_model(headline_word_tag_list):
    """ Input: A list with each entry having headline from input corpus
    operation: computes the language model probablity for each trigrams of POS  and stores the probablity for each trigram POS in  dictionary

    """
    global trigram_model_probablity,trigram_model_count,trigram_model_probablity
    compute_trigram_counts(headline_word_tag_list)
    compute_bigram_counts(headline_word_tag_list)

    trigram_model_probablity = dict(trigram_model_count)

    prev = "start"
    cur = "start"
    next = "start"
    #count =0

    total_trigram_count = 0

    #computes total trigram in the dataset
    # for tag1 in trigram_model_count:
    #     if tag1 == 'start':
    #         continue
    #     for tag2 in trigram_model_count[tag1]:
    #         if tag2 == 'start':
    #             continue
    #
    #         for tag3 in trigram_model_count[tag1][tag2]:
    #             if tag3 == 'start':
    #                   continue
    #             total_trigram_count = total_trigram_count+trigram_model_count[tag1][tag2][tag3]



    # computes POS language model probablity
    for headline in headline_word_tag_list:
        tokens = headline.split(" ")
        for entry in tokens:
            word, tag = entry.rsplit('/', 1)
            prev = cur
            cur = next
            next = tag

            if prev in trigram_model_probablity:

                        if cur in trigram_model_probablity[prev]:

                            if next in trigram_model_probablity[prev][cur]:
                                trigram_model_probablity[prev][cur][next] = (trigram_model_count[prev][cur][next])/float(bigram_model_count[prev][cur])
                            else:
                                #unique_trigram_pos_count = unique_trigram_pos_count+1
                                trigram_model_probablity[prev][cur][next] = (1)/float(bigram_model_count[prev][cur])
                        else:
                                trigram_model_probablity[prev][cur]={}
                                trigram_model_probablity[prev][cur][next] = (1)/float(bigram_model_count[prev][cur])

            else:

                 trigram_model_probablity[prev]={}
                 trigram_model_probablity[prev][cur]={}
                 trigram_model_probablity[prev][cur][next] =(1)/float(bigram_model_count[prev][cur])




