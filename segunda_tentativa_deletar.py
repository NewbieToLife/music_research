def return_smaller_list(list1,list2):
    if len(list1)<=len(list2):
        return list1
    else:
        return list2

def return_bigger_list(list1,list2):
    if len(list1)>len(list2):
        return list1
    else:
        return list2

def repeated_index(li,element):
    aux_list=[]
    indexes=[]
    for i in li:
        aux_list.append(i)
    counter = 0
    while True:
        try:
            indexes.append(aux_list.index(element)+counter)
            aux_list.pop(aux_list.index(element))
            counter=counter+1
        except:
            if counter == 0:
                return False
            else:
                return indexes
    return False

def cyclic_list(li,index1,index2):
    if index2<=len(li):
        return li[index1:index2]
    else:
        return li[index1:]+li[:index2%len(li)]

def is_subsequence(small_list,big_list):
    indexes = repeated_index(big_list,small_list[0])
    if indexes == False:
        return [False]
    for i in indexes:
        if small_list==cyclic_list(big_list,i,i+len(small_list)):
            return [small_list,i,i+len(small_list)]
    return [False]

def get_bigger_subsequence(x,y):
    small = return_smaller_list(x,y)
    big = return_bigger_list(x,y)
    memory=[]
    for i in range(0,len(small)-2):
        eval = is_subsequence(small[i:len(small)],big)
        if eval[0]!=False:
            memory.append(eval+[i,len(small)])
        eval = is_subsequence(small[0:len(small)-i],big)
        if eval[0]!=False:
            memory.append(eval+[0,len(small)-i])
    diffs=[]
    if len(memory)>0:
        for i in memory:
            diffs.append(len(i[0]))
        return memory[diffs.index(max(diffs))]
    
    return None


x=[0,2,3,4,8,9,9]
y=[1,3,4,8,9,9,1,3,2,2]
small=return_smaller_list(x,y)
big = return_bigger_list(x,y)
print(get_bigger_subsequence(small,big))
w=get_bigger_subsequence(small,big)
print(small[:w[-1]]+big[w[-3]:])
print(big[:w[-4]]+small[w[-2]:])
