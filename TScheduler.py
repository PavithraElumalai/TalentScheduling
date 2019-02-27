#---------------------------TALENT SCHEDULING WITH DP------------------------

import itertools as it
#input data - global
S = {'s1','s2','s3','s4','s5','s6','s7','s8','s9','s10','s11','s12'}
actors = {'a1':20,'a2':5,'a3':4,'a4':10,'a5':4,'a6':7}
actors_in_scenes = [['s1','s2','s3','s4','s5','s6','s7','s8','s9','s10','s11','s12'],
                    [1,0,1,0,0,1,0,1,1,1,1,1],
                    [1,1,1,1,1,0,1,0,1,0,1,0],
                    [0,1,0,0,0,0,1,1,0,0,0,0],
                    [1,1,0,0,1,1,0,0,0,0,0,0],
                    [0,0,0,1,0,0,0,1,1,0,0,0],
                    [0,0,0,0,0,0,0,0,0,1,0,0]]
a_s = {}
scenes = {'s1':1,'s2':1,'s3':2,'s4':1,'s5':3,'s6':1,'s7':1,'s8':2,'s9':1,'s10':2,'s11':1,'s12':1}
#rez = [[actors_in_scenes[j][i] for j in range(1,len(actors_in_scenes))] for i in range(len(actors_in_scenes[0]))]
rez = []
scost = [0]*(2**len(scenes))    #dp table - list
bit_string = "1"*len(scenes)
a_list = ['s1','s2','s3','s4','s5','s6','s7','s8','s9','s10','s11','s12']
new_scenes = {}
new ={}
temp = {}  #dp dictionary
a_prime = []
order = []
actors_new = {}


#------------------preprocessing functions----------------------------------
#list of pre-processing function(in order):
#   1. all_values_check
#   2. cal_a_prime
#   3. cal_actors_new
#   4. cal_scenes_new


def preprocessing():
    
    global a_prime
    global actors_new

    a_prime = cal_a_prime()
    #print("a_prime : ",a_prime)
    actors_new = cal_actors_new(a_prime)
    #print(" processed actors : ",actors_new)
    cal_scenes_new()
    
#validates the input values
def all_values_check():

    if len(actors) == len(actors_in_scenes):
        return True
    return False

#removes one-scene actors from scene & actors list
def cal_a_prime():

    global actors_in_scenes
    a_prime = {}

    for x in range(1,len(actors)+1):
        if actors_in_scenes[x].count(1) == 1:
            temp = actors_in_scenes[x].index(1)
            actors_in_scenes[x][temp] = 0
            temp = "s"+str(temp+1)
            a_prime["a"+str(x)] = actors.get("a"+str(x))*scenes.get(temp)

    return a_prime

#removes actors in a_prime list         
def cal_actors_new(a_prime):

    actors_new = {}

    for each in actors:
        if each not in a_prime:
            actors_new[each] = actors.get(each)

    return actors_new


#concatenates actor equivalent scenes
def cal_scenes_new():
    global rez
    global new
    global new_scenes
    temp = []
    old =[]
    ne = []
    l={}
    rez = [[actors_in_scenes[j][i] for j in range(1,len(actors_in_scenes))] for i in range(len(actors_in_scenes[0]))]

    for each in rez:
        n = ""
        for bit in each:
            n = n + str(bit)
        old.append(int(n,2))    #decimal equivalent of scenes by each actors
    for each in old:
        l[each] = []
    for x in range (len(old)):
        l[old[x]].append("s"+str(x+1))  #decimal to scenes
    for each in l:
        if len(l.get(each)) > 1:
            ne.append(l.get(each))      #finds duplocate scenes
    #print("ne : ",ne)
    for each in ne:
        for s in each[1:]:
            temp.append(s)
            new[each[0]] = each[1:]     #remembers duplicates to add later
    #print("temp : ",temp)
    for each in S:
        if each not in temp:
            new_scenes[each] = scenes.get(each) #unique scenes dictionary
    
#******************************************************************************       


#-------------------------supporting functions-----------------------------

#list of functions:
#   1. cal_actor_dict
#   2. exclude

#creates the dictionary a_s - key: scene; value : list of actors          
def cal_actor_dict():
    
    for x in range(len(scenes)):
        v=[]
        for y in range(1,len(actors)):
            if(actors_in_scenes[y][x] ==1):
                h = "a"+str(y)
                v.append(h)
        #print(v)
        a_s["s"+str(x+1)] = v
    #print(a_s)

#given a value and a set returns the set removing the value
def exclude(Q,s):
    
    temp = []

    for each in Q:
        if(each != s):
            temp.append(each)
    temp = set(temp)

    return temp

#returns the decimal value of the bitstrig for the input set of scenes
def cal_bit(Q):
    
    b_s = [0]*len(scenes)
    b = ""

    for each in Q:
        ind = a_list.index(each)
        b_s[ind] = 1
    for each in b_s:
        b = b+str(each)
    #print(int(b,2))

    return int(b,2)

#***************************************************************************


#------------------------scheduling functions--------------------------------
#list of scheduling functions:
#   1. actors_in_scene
#   2. L_function
#   3. lower
#   4. cost
#   5. ind_min

#a(s) function: gives set of actors in a given scene
def actors_in_scene(scene):

    val = actors_in_scenes[0].index(scene)
    actr = []

    for x in range(1, len(actors)+1):
        if(actors_in_scenes[x][val] == 1):
            actr.append("a"+str(x))

    return actr
#returns the set of actors in the curr scene who appeared and will appear
def L_function(s,Q):
    A = set(new_scenes)
    #print("A : ",A)
    B = []
    res = set()

    for each in A:
        #print(each)
        if each not in Q:
            B.append(each)   #scenes that are to be scheduled before Q
    B = set(B)
    #print("Q : ",Q, "s : ",s, " Q-{s} : ",B)
    before = set()
    after = set()
    for each in B:
        before = before.union(set(a_s.get(each)))   #a's needed after s
    for each in Q:
        after = after.union(set(a_s.get(each))) #a's needed before s
    #print("before : ",before)
    #print("after : ",after)
    res = before.intersection(after)
    #print(res)

    return res
    
#returns the cost of scheduling s before any scene in B
def cost(s,B):
    #print("cost : ",B)
    c = 0
    b = L_function(s,B)

    for each in b:
        c = c + actors.get(each)
    d = scenes.get(s)
    #print("cost : ",s,b,c*d)

    return c*d

#returns the lower bound of the cost of scheduling the scenes in B
def lower(B):
    #print("lower ",B)
    low = 0

    for scene in B:
        a = actors_in_scene(scene)
        sal = 0
        for actr in a:
            sal = sal + actors.get(actr)
        d = scenes.get(scene)
        low = low + (d*sal)

    return low

#returns the s in Q that causes the expression to take the minimum value
def ind_min(T):

    #print("ind_min",T)
    M = 10000
    h = T

    for each in T:
        ex = exclude(h,each)
        #print("ex : ",ex)
        val = cost(each,ex) + lower(ex)
        if val<M:
            M = val
            scene = each
    #print("ind_min result : ",scene)

    return scene

#***************************************************************************

#--------------------------actual scheduler---------------------------------


def schedule(Q):
    Min = 1000000
    global order
    #print("Q : ",Q)

    bs = cal_bit(Q)
    #print("scost[bs] : ",scost[bs])
    if(len(Q) == 0):
        return 0
    if(scost[bs]):
        return scost[bs]

    T = Q
    while(len(T) != 0):
        s = ind_min(T)
        #print("T : ",T)
        #print("s : ",s)
        #if s not in order:
        order.append(s)
        T = exclude(T,s)
        #print("T : ",T)
        if(cost(s,exclude(T,s)) + lower(exclude(T,s)) >= Min):
            break
        sp = cost(s,exclude(T,s)) + schedule(exclude(T,s))
        #print("sp : ",sp)
        if(sp < Min):
            Min = sp
    #print("sp : ",sp)
    #print("Min : ",Min)
    temp[str(bs)] = Min
    scost[bs] = Min
    return Min
    
#***************************************************************************

#---------------------------final schedule-----------------------------------
#list of function:
#   1. f_s

def f_s(order):
    final = []
    for each in order:
        final.append(each)
        if each in new:
            final = final + new.get(each)
    print(final)
    for each in final:
        print(each,a_s.get(each))
        
#***************************************************************************

#main function

def main():
    if  preprocessing():
        return 0
    cal_actor_dict()
    #L_function('s2',{'s1','s4','s5'})
    c = schedule(set(new_scenes))
    """for each in a_prime:
        c = c + a_prime.get(each)"""
    f_s(order[:len(order)//2])

          
main()
