# define all the feature functions here
"""
List of features used:
1. Language model features
2. Headline Length feature
3. Part of Speech Language Model Feature

4. N-Gram Match feature
5. Content selection feature
"""

import math

#model feature tuple
feature_values = []

#structures for headline length feature
Unique_length_count =0  # range considered is 3 to 15(13 values )
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


    for headline in headline_word_tag_list:
        tokens = headline.split(" ")
        prev = "start"
        cur = "start"
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
    language_model_probablity = dict(language_model_count)

    for headline in headline_word_tag_list:

        tokens = headline.split(" ")
        prev = "start"
        cur = "start"
        mycount = 0
        for entry in tokens:
            mycount= mycount+1
            word, tag = entry.rsplit('/', 1)
            prev = cur
            cur = word

            if mycount >= 2:
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

    for headline in headline_word_tag_list:
        tokens = headline.split(" ")
        prev = "start"
        cur = "start"
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
    local_trigram_count = 0
    lc = 0
    #print headline_word_tag_list
    for headline in headline_word_tag_list:
        local_trigram_count+= 1
        #print str(local_trigram_count)+")current line:"+headline

        tokens = headline.split(" ")
        prev = "start"
        cur = "start"
        next = "start"
        #print "line:"+headline
        for entry in tokens:
            word, tag = entry.rsplit('/', 1)
            prev = cur
            cur = next
            next = tag

            #print "LC:"+str(lc)
            if prev in trigram_model_count:
               # print "in if"
                if cur in trigram_model_count[prev]:
                   # print "in if if"
                    if next in trigram_model_count[prev][cur]:
                       # print "in if if if"
                        trigram_model_count[prev][cur][next]= trigram_model_count[prev][cur][next]+1
                        #print "dict:"+str(trigram_model_count)
                    else:
                        #unique_trigram_pos_count = unique_trigram_pos_count+1
                       # print "in if if else"
                        trigram_model_count[prev][cur]={}
                        trigram_model_count[prev][cur][next]=1
                        #print "dict:"+str(trigram_model_count)

                else:
                    #print "in if else"

                    trigram_model_count[prev][cur]={}
                    trigram_model_count[prev][cur][next] =1
                    #print "dict:"+str(trigram_model_count)
            else:
                #print "in else"
                trigram_model_count[prev] = {}
                trigram_model_count[prev][cur]={}
                trigram_model_count[prev][cur][next] =1
                #print "dict:"+str(trigram_model_count)

            lc+=1
        #print "########################################################################"





# P( wi | wi-1 wi-2 ) = count ( wi, wi-1, wi-2 ) / count ( wi-1, wi-2 )



def compute_pos_language_model(headline_word_tag_list):
    """ Input: A list with each entry having headline from input corpus
    operation: computes the language model probablity for each trigrams of POS  and stores the probablity for each trigram POS in  dictionary

    """
    global trigram_model_probablity,trigram_model_count,trigram_model_probablity,bigram_model_count
    compute_trigram_counts(headline_word_tag_list)
    compute_bigram_counts(headline_word_tag_list)

    trigram_model_probablity = dict(trigram_model_count)
    # computes POS language model probablity
    for headline in headline_word_tag_list:
        prev = "start"
        cur = "start"
        next = "start"
        tokens = headline.split(" ")
        mycount = 0
        for entry in tokens:
            word, tag = entry.rsplit('/', 1)
            prev = cur
            cur = next
            next = tag
            #print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
            #print "prev:"+prev+" cur:"+cur+" next:"+next+"my count:"+str(mycount)

            if mycount>1:

                if prev in trigram_model_probablity:

                            if cur in trigram_model_probablity[prev]:

                                if next in trigram_model_probablity[prev][cur]:

                                    temp = (trigram_model_count[prev][cur][next])/float(bigram_model_count[prev][cur])
                                    trigram_model_probablity[prev][cur][next] = temp


                #                 else:
                #                     print "in if if else"
                #                     #unique_trigram_pos_count = unique_trigram_pos_count+1
                #                     trigram_model_probablity[prev][cur][next] = (1)/float(bigram_model_count[prev][cur])
                #             else:
                #                     print "in if else"
                #                     trigram_model_probablity[prev][cur]={}
                #                     trigram_model_probablity[prev][cur][next] = (1)/float(bigram_model_count[prev][cur])
                #
                # else:
                #      print "in else"
                #      trigram_model_probablity[prev]={}
                #      trigram_model_probablity[prev][cur]={}
                #      trigram_model_probablity[prev][cur][next] =(1)/float(bigram_model_count[prev][cur])
            mycount+=1



def compute_POS_language_feature(headline_word_tag_list):
    """ Returns POS language model feature value for the headline
    """
    global trigram_model_probablity
    POSLM_feature = 0
    prev = "start"
    cur = "start"
    next = "start"
    count = 1

    #initialization of dictionary
    tokens = headline_word_tag_list.split(" ")
    for entry in tokens:
        word, tag = entry.rsplit('/', 1)
        prev = cur
        cur = next
        next = tag
        count = count+1
        #print "prev:"+prev+" cur:"+cur+" next:"+next
        if count>2 :
            if prev in trigram_model_probablity:
                if cur in trigram_model_probablity[prev]:
                    if next in trigram_model_probablity[prev][cur]:
                        probablity = trigram_model_probablity[prev][cur][next]
                        POSLM_feature =POSLM_feature+ math.log(probablity, 10)


    return POSLM_feature


def compute_headline_length_feature(headline_word_tag_list):
    """
    computes the log probablity of particular headline length and returns the value
    """
    global headline_length_probablity
    Length_feature = 0
    count = 0
    total_no_of_headlines = 0
    for i in headline_length_count:
        total_no_of_headlines = total_no_of_headlines+headline_length_count[i]


    tokens = headline_word_tag_list.split(" ")
    for entry in tokens:
        word, tag = entry.rsplit('/', 1)
        count = count+1

    if count in headline_length_probablity:
        Length_feature = math.log(headline_length_probablity[count], 10)
    else:
        temp = 1/float(total_no_of_headlines)
        Length_feature = math.log(temp,10)
    return Length_feature




def compute_language_model_feature(headline):
    """Returns the language model feature value
    """
    global  language_model_probablity,word_count

    total_word_count = 0
    for i in word_count:
        total_word_count=total_word_count+word_count[i]
   # print "total word count:"+str(total_word_count)

    prev = "start"
    cur = "start"

    headline =  headline.strip()
    WordOfLine = headline.split()
    mycount = 0
    LM_value = 0
    tokens = headline.split(" ")
    for entry in tokens:
        word, tag = entry.rsplit('/', 1)
        prev = cur
        cur = word
        #print "in prev:"+prev+"cur:"+cur+"count:"+str(mycount)
        mycount = mycount+1
        if mycount>1:

            if prev in language_model_probablity:


                        if cur in language_model_probablity[prev]:


                            LM_value = LM_value +math.log(language_model_probablity[prev][cur], 10)
                            #print "log LMvalue:"+str(math.log(language_model_probablity[prev][cur],10))
                        #if word given previous word probablity does not exist we use others value as smoothing measure
                        else:
                             temp = 1/(word_count[prev])
                             LM_value += math.log(temp, 10)
            else:
                        temp = 1/(total_word_count)
                        LM_value += math.log(temp, 10)

    return LM_value



def get_headline_synthesis_features(headline_word_tag_list):
    '''
    calls the feature functions and stores feature values for the model in a tuple in the format
    ({POSLM:"NN VB NN"},outcome,{headline_len,len_val},outcome,
    '''
    global headline_length_probablity,language_model_probablity,trigram_model_probablity,feature_values
    compute_pos_language_model(headline_word_tag_list)
    compute_language_model_probablity(headline_word_tag_list)
    compute_headline_length_probablity(headline_word_tag_list)
    #adding all features of one headline


    for head in headline_word_tag_list:
        #print "####################################################################################"
        #print "line:"+head
        count = 0
        tokens = head.split(" ")
        #adding feature 1
        for entry in tokens:
            word, tag = entry.rsplit('/', 1)
            count = count+1
        temp_dict = {}
        temp_dict['headline_len'] = count

        feature1 = (temp_dict,headline_length_probablity[count])
        #print "current f1 value:"+str(feature1)

        feature_values.append(feature1)

        #adding feature 2
        POSLM_feature = compute_POS_language_feature(head)
        pos_string = ""
        temp_dict = {}
        #print "pos tag string:"+pos_string

        #initialization of dictionary
        #tokens = head.split(" ")
        for entry in tokens:
            word, tag = entry.rsplit('/', 1)
            pos_string = pos_string+tag+" "
        temp_dict['pos_LM']= pos_string
        feature2 = (temp_dict,POSLM_feature)
        feature_values.append(feature2)
        #print temp_dict
        #print "current f2 value:"+str(feature2)
        #adding feature 3
        LM_feature = compute_language_model_feature(head)
        word_bigram_string = ""
        temp_dict = {}
        #print "word  string:"+word_bigram_string
        prev = "start"
        cur = "start"
        lm = 0

        #tokens = head.split(" ")
        for entry in tokens:
            word, tag = entry.rsplit('/', 1)
            prev = cur
            cur = word
            word_bigram_string = word_bigram_string+" "+prev+"-"+cur

        #print "word  string:"+word_bigram_string
        LMvalue = compute_language_model_feature(head)
        temp_dict['LM']= word_bigram_string
        feature3 =(temp_dict,LMvalue)
        feature_values.append(feature3)
        #print "current f3 value:"+str(feature3)
        del feature1
        del feature2
        del feature3
        #print feature_values
    return feature_values


def get_classification_dictionary(headline_word_tag_list):
    '''
    returns the list of the form
    {'headline_len': 3}, ({'pos_LM': 'NN VV MM '},'{'LM': ' start-a a-b b-c'},
    '''
    local_dict = {}
    count = 0
    tokens = headline_word_tag_list.split(" ")
    #adding feature 1
    for entry in tokens:
        count = count+1
    local_dict['headline_len'] = count

    #adding feature 2

    pos_string = ""
    for entry in tokens:
        word, tag = entry.rsplit('/', 1)
        pos_string = pos_string+tag+" "
    local_dict['pos_LM']= pos_string

    word_bigram_string = ""
    prev = "start"
    cur = "start"
    lm = 0

    for entry in tokens:
        word, tag = entry.rsplit('/', 1)
        prev = cur
        cur = word
        word_bigram_string = word_bigram_string+" "+prev+"-"+cur


    local_dict['LM']= word_bigram_string
    return local_dict
