import spacy
import sys
import gensim
from gensim.test.utils import datapath
from gensim.models import KeyedVectors
#keeping the sentence global
sentence=""

#list of stop triggers
#list of stop triggers
negationtriggers=["no", "not","denies","nothing","asymptomatic","atypical","deny","denied","denying","free","lack","negative","never","without","nor"]

hypothetical=["believes","believe","agree","agree","agreement","favor","favoured","outline","outlined","likely","risk","possible","typical","typically","candidate",
              "regarding","discuss","discussion","publication","advised","advise","advising","agreeable","agreed","allows","discussed","amenable","anticipate",
              "approximately","recommend","recommended","recommending","ask","authorization","await","initiation","chance","concern","concerened","concerning","consent"
              "could","can","criteria","desire","desired","desires","educate","meant","prefer","prefers","emphasize","emphasized","evaluate","express","expressed","extrapolate",
              "fear","felt","feel","example","information","conversation","decide","decided","declined","elected","wondering","thought","stated","opinion","likelihood",
              "probability","suspicious","hoping","beneficial","usually","reasonable","willing","leaning","likehood","consider","considered","feasible"
              "indicated","recommended","recommends","interested","trying","contemplating","suggests","suspect","suspects","potentially","potential","hesitate"]

family=["sister","daughter","father","brother","cousin","aunt","uncle","family"]
triggers=negationtriggers+hypothetical+family

stoplist=["but","otherwise","confirming","however","positive","confirms","confirmed"]

# EXPAND DECISION POINTS
EXPANDLIST=[
    "ADJ-JJ-acomp-hypothetical",
    "ADJ-JJ-acomp-negation",
    "ADJ-JJ-advmod-negation"
    "ADJ-JJ-advmod-hypothetical",
    "ADJ-JJ-amod-negation",
    "ADJ-JJ-attr-hypothetical",
    "ADJ-JJ-conj-hypothetical",
    "ADJ-JJ-dobj-negation",
    "ADJ-JJ-intj-negation",
    "ADV-RB-acomp-hypothetical",
    "ADV-RB-advcl-negation",
    "ADV-RB-advmod-hypothetical"
    "ADV-RB-neg-negation",
    "ADV-RB-preconj-negation",
    "CCONJ-CC-cc-negation",
    "DET-DT-det-negation",
    "DET-DT-quantmod-negation",
    "INTJ-UH-appos-negation",
    "INTJ-UH-intj-negation",
    "NOUN-NN-appos-family",
    "NOUN-NN-compound-negation",
    "NOUN-NN-compound-hypothetical",
    "NOUN-NN-nsubj-family",
    "NOUN-NN-nsubjpass-family",
    "VERB-VBG-amod-hypothetical",
    "VERB-VBN-amod-hypothetical"


]
# list of found spans

# get root of sentence
def getroot(sentence,doc):
    return [token for token in doc if token.head == token][0]

# get parse with given node as root
def getsubtree(doc,root,triggertype,bool):
    stop=0
    #print("here")
    span=[]
    length=0
    stopid=0
    if bool==True:
        for i in range(len(doc)):
            if str(doc[root].head.text)==str(doc[i]):
                root=i

    print(doc[root].text)
    for i in doc[root].subtree:
        if i.text in stoplist:
            stopid=i.idx
            #print(stopid)
        span.append(i.idx)
        length=len(i)


    if stopid!=0:
        #print("blah")
        if min(span)<stopid:
            #print("blah")
            return ([min(span),stopid, triggertype])

    #print(str(sentence[min(span):max(span)+length]))
    #print(doc[root].text)
    if str(sentence[min(span):max(span)+length])==doc[root].text:
        return fallback(doc,root,triggertype)

    return ([min(span),max(span)+length,triggertype])


def hello():
    return "hello world"
def parse(sentence):
    foundspans=[]
    #wv_from_bin = KeyedVectors.load_word2vec_format(datapath("model.bin"), binary=True)

    #sentence=sys.argv[1]
    print(sentence)
    #load english model
    nlp= spacy.load('en_core_web_sm')
    #convert string to unicode
    sentence=unicode(sentence,"utf-8")
    #pass sentence to get doc struct of spacy for sentence
    doc=nlp(sentence)

    #using span
    span=doc
    #get root
    if len(sentence)==0:
        return foundspans,"Please enter a sentence"
    sentroot=getroot(sentence,doc)

    #print(sentroot)


    for trigger in triggers :
        for i in range(len(doc)):
            if trigger==str(doc[i]):
                pattern=""
                triggertype=0
                if trigger in negationtriggers:
                    pattern = str(doc[i].pos_) + "-" + str(doc[i].tag_) + "-" + str(doc[i].dep_) + "-" +"negation"
                    #print(pattern)
                    triggertype=1
                elif trigger in hypothetical:
                    pattern = str(doc[i].pos_) + "-" + str(doc[i].tag_) + "-" + str(doc[i].dep_) + "-" + "hypothetical"
                    #print(pattern)
                    triggertype=2
                elif trigger in family:
                    pattern = str(doc[i].pos_) + "-" + str(doc[i].tag_) + "-" + str(doc[i].dep_) + "-" + "family"
                    #print(pattern)
                    triggertype=3
                print(str(doc[i]),i)
                if pattern in EXPANDLIST:

                    foundspans.append(getsubtree(doc, i, triggertype,True))
                else:
                    foundspans.append(getsubtree(doc,i,triggertype,False))





    print(foundspans)
    return foundspans,str(sentence)
    #print(sentence[15:37])


def fallback(doc,trigger,triggertype):
    print("running fallback")
    stopindex=-1
    for token in doc:
        if str(token.text) in stoplist:
            stopindex=token.idx

    starindex=doc[trigger].idx
    #print(starindex)
    #print(stopindex)

    if stopindex==-1:
        return [starindex,starindex+len(sentence),triggertype]
    else:
        return [starindex,stopindex,triggertype]
