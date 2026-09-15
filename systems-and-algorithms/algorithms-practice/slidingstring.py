def strinsubstring(array,k):
    windowsum=0
    windowstart=0
    lists=[]
    maxlenght=0
    hashtable={}
    cureentlenght=0
    for windowend in range(len(array)):
        current_letter=array[windowend]
        if  current_letter not in hashtable:
            hashtable[current_letter] = 0
        
        hashtable[current_letter] = hashtable[current_letter] +1
        while len(hashtable)>k:
            leftest=array[windowstart]
            hashtable[leftest]-=1
            if hashtable[leftest]==0:
                hashtable.pop(leftest)
            windowstart+=1
        maxlenght=max(maxlenght,windowend-windowstart+1)
                
    return maxlenght



def fruitsplit(array,k):
    windowsum=0
    windowstart=0
    lists=[]
    maxlenght=0
    hashtable={}
    cureentlenght=0
    k=2
    for windowend in range(len(array)):
        current_letter=array[windowend]
        if  current_letter not in hashtable:
            hashtable[current_letter] = 0
        
        hashtable[current_letter] = hashtable[current_letter] +1
        while len(hashtable)>k:
            leftest=array[windowstart]
            hashtable[leftest]-=1
            if hashtable[leftest]==0:
                hashtable.pop(leftest)
            windowstart+=1
        maxlenght=max(maxlenght,windowend-windowstart+1)
                
    return maxlenght


array= "araaci" 
S=2
strinsubstring(array,S)
array=['A','B','C','B','B','C']
print(fruitsplit(array,2))


def strinsubstring(array):
    windowsum=0
    windowstart=0
    lists=[]
    maxlenght=0
    hashtable={}
    cureentlenght=0
    for windowend in range(len(array)):
        current_letter=array[windowend]
        if  current_letter not in hashtable:
            hashtable[current_letter] = 0
        
        hashtable[current_letter] = hashtable[current_letter] +1
        while max(hashtable.values())>=2:
            leftest=array[windowstart]
            hashtable[leftest]-=1
            if hashtable[leftest]==0:
                hashtable.pop(leftest)
            windowstart+=1
        maxlenght=max(maxlenght,windowend-windowstart+1)
                
    return maxlenght
array="abccde"
print("max", strinsubstring(array))



def repeatablestring(array,k):
    windowsum=0
    windowstart=0
    lists=[]
    maxlenght=0
    hashtable={}
    cureentlenght=0
    for windowend in range(len(array)):
        current_letter=array[windowend]
        if  current_letter not in hashtable:
            hashtable[current_letter] = 0
        hashtable[current_letter]+=1
        max(hashtable[current_letter],cureentlenght)
        hashtable[current_letter] = hashtable[current_letter] +1
        if (windowend-windowstart+1-cureentlenght)>k:
            leftest=array[windowstart]
            hashtable[leftest]-=1
            windowstart+=1
        maxlenght=max(maxlenght,windowend-windowstart+1)
                
    return maxlenght
array="abccde"
print("repeatareplace", repeatablestring("aabccbb",2))


def binaires(array,k):
    windowsum=0
    windowstart=0
    lists=[]
    maxlenght=0
    hashtable={}
    cureentlenght=0
    maxonecount=0
    for windowend in range(len(array)):
        current_letter=array[windowend]
        if  array[windowend]==1:
            maxonecount+=1
    
        if (windowend-windowstart+1-maxonecount)>k:
            
            if array[windowstart] ==1:
                maxonecount-=1
            windowstart+=1
        maxlenght=max(maxlenght,windowend-windowstart+1)
                
    return maxlenght
array="abccde"
print("binaries", binaires([0,1,1,0,0,0,1,1,0,1,1],2))


def permutation(array,pattern):
    windowsum=0
    windowstart=0
    lists=[]
    maxlenght=0
    hashtable={}
    cureentlenght=0
    maxonecount=0
    length=len(pattern)
    matched=0
    for letter in pattern:
        if letter not in hashtable:
            hashtable[letter]=0
        hashtable[letter]+=1
        
        
    for windowend in range(len(array)):
        right_letter=array[windowend]
        
        if right_letter  in hashtable:
            hashtable[right_letter]-=1
            if hashtable[right_letter]==0:
                matched+=1
        if matched== len(hashtable):
            return True
            
        if windowend>=length-1:
            
            if array[windowstart] in hashtable:
                if hashtable[array[windowstart]]==0:
                    matched-=1
                hashtable[array[windowstart]]+=1
            windowstart+=1
            
   
    return False
        

                
    return maxlenght
array="abccde"
print("binaries", permutation("oidbcaf", "abc"))



        



def matchingletters(array,pattern):
    windowsum=0
    windowstart=0
    lists=[]
    maxlenght=0
    hashtable={}
    cureentlenght=0
    maxcount=0
    length=len(pattern)
    matched=0
    min_lenght=len(array) +1 
    substrg_start=0
    for letter in pattern:
        if letter not in hashtable:
            hashtable[letter]=0
        hashtable[letter]+=1
        
        
    for windowend in range(len(array)):
        right_letter=array[windowend]
        
        if right_letter  in hashtable:
            hashtable[right_letter]-=1
            if hashtable[right_letter]>=0:
                matched+=1

            
        while matched==length:
            if min_lenght> windowend - windowstart+1:
                min_lenght= windowend - windowstart+1
                substrg_start=windowstart
            left_char=array[windowstart]
            windowstart+=1
            if left_char in hashtable:
                if hashtable[array[windowstart]]==0:
                    matched-=1
                hashtable[array[windowstart]]+=1
    if min_lenght>len(array):
        return ""
    return array[substrg_start:substrg_start + min_lenght]
            
   
print("maatchingletters",matchingletters("aabdec", "abc"))
        




def concatanating(array,pattern):
    windowsum=0
    windowstart=0
    lists=[]
    maxlenght=0
    hashtable={}
    cureentlenght=0
    maxcount=0
    length=len(pattern)
    matched=0
    min_lenght=len(array) +1 
    substrg_start=0
    for letter in pattern:
        if letter not in hashtable:
            hashtable[letter]=0
        hashtable[letter]+=1
        
        
    for windowend in range(len(array)):
        right_letter=array[windowend]
        
        if right_letter  in hashtable:
            hashtable[right_letter]-=1
            if hashtable[right_letter]>=0:
                matched+=1

            
        while matched==length:
            if min_lenght> windowend - windowstart+1:
                min_lenght= windowend - windowstart+1
                substrg_start=windowstart
            left_char=array[windowstart]
            windowstart+=1
            if left_char in hashtable:
                if hashtable[array[windowstart]]==0:
                    matched-=1
                hashtable[array[windowstart]]+=1
    if min_lenght>len(array):
        return ""
    return array[substrg_start:substrg_start + min_lenght]
            
   
print("maatchingletters",matchingletters("aabdec", "abc"))
        

def anagram(array,words):
    windowsum=0
    windowstart=0
    lists=[]
    maxlenght=0
    hashtable={}
    cureentlenght=0
    maxonecount=0
    length=len(words)
    matched=0
    result=[]
    for word in word:
        if word not in hashtable:
            hashtable[word]=0
        hashtable[word]+=1
    word_count=len(words) 
    word_lenght= len(words[0])
        
    for i in range(len(array)- word_count*word_lenght)+1:
        word_seen={}
        for j in range(word_count):
            next_word_index= i+j*word_lenght
            word=array[next_word_index:next_word_index+word_lenght]
            if word not in hashtable:
                break
            if word in word_seen:
                word_seen = 0
            word_seen[word]+=1
            if word_seen[word]> hashtable.get(word,0):
                break
            if j+1== word_count:
                result.append(i)
    return result  