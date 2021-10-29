import random as r
offspring=[]
a = [1,5,7,3,4,2]
b = [2,3,3,2,4]

def return_smaller_list(x,y):
    if len(x)<=len(y):
        return x
    elif len(y)<len(x):
        return y
def cyclic_list(li,index1,index2):
    if index1<=index2:
        return li[index1:index2+1]
    else:
        return li[index1:]+li[:index2+1]
def duplicate_index(list1,element):
    aux_list=[]
    indexes=[]
    for i in list1:
        aux_list.append(i)
    counter=0
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
def is_subseq_index(x,y):
    indexes = duplicate_index(y,x[0])
    for i in indexes:
        cnt=0
        for k in range(i,i+len(x)):
            if x[cnt]!=y[k%len(y)]:
                break
            if k==i+len(x)-1 and x[cnt]==y[k%len(y)]:
                return [i,k%len(y)]
            cnt=cnt+1
    if i == indexes[-1]:
        return False
def check_biggest_subseq_index(x,y):
    small_list=return_smaller_list(x,y)
    memory=[]
    for i in range(0,len(x)-1):
        eval=is_subseq_index(x[0:len(x)-i],y)
        if eval!=False:
            memory.append(eval)
            #return is_subseq_index(x[0:len(x)-i],y)
        eval=is_subseq_index(x[0+i:len(x)],y)
        if eval!=False:
            memory.append(eval)
    if len(memory)>0:
        diffs=[]
        for i in memory:
            diffs.append(abs(i[0]-i[1]))
        return memory[diffs.index(max(diffs))]
    return False
def return_bigger_list(x,y):
    if len(x)<=len(y):
        return y
    elif len(y)<len(x):
        return x

y = [1,2,3,4,5]
x = [8,5,1,2]
#print(check_biggest_subseq_index(x,y))
a=check_biggest_subseq_index(return_smaller_list(x,y),return_bigger_list(x,y))
print(a)
#print(cyclic_list(return_bigger_list(x,y),a[0],a[1]))
# small_list=return_smaller_list(a,b)
# comparator = min([len(a),len(b)])
# while comparator>1:
#     for i in range(0,len(small_list)):
#     sub_small_list=small_list[i:comparator]

#     comparator = comparator-1
# print(offspring)