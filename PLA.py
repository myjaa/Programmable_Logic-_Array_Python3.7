__author__="Mohammad Yusuf Jamal Aziz Azmi"

# LANGUAGE USED :- Python 3
#The main function(I know python dosent have one, but kinda) starts at line 327.
#Please do note : Just like life, nothing is perfect, hence this program might give some shocking outputs in some cases. 
# The table formatting isn't perfect 

# INSTRUCTIONS ON HOW TO USE:-
# 0) COMPILE IT.
# 1) First the user will be prompted to enter the number of bits/inputs he/she want's.
# 2) Then he/she will be propmpted to enter the number of functions/outputs they want followed by number of minterms/products required.
# 3) Now the user will be prompted to enter the cell numbers for each function, WARNING:- STICK TO THE RANGE TOLD TO YOU WHILE ENTERING THE CELL NUMBERS.
# 4) And VOILA!! You have your PLA table/chart, ENJOY!


import itertools

#compare two binary strings, check where there is one difference
def compBinary(s1,s2):
    count = 0
    pos = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            count+=1
            pos = i
    if count == 1:
        return True, pos
    else:
        return False, None


#compare if the number is same as implicant term
#s1 should be the term
def compBinarySame(term,minterm):
    for i in range(len(term)):
        if term[i] != '-':
            if term[i] != minterm[i]:
                return False
    return True

#combine pairs and make new group
def combinePairs(group, unchecked):
    #define length
    l = len(group) -1

    #check list
    check_list = []

    #create next group
    next_group = [[] for x in range(l)]  #groups keep on decreasing by 1 group

    #go through the groups
    for i in range(l):  #so that it dosent check beyond index limit
        #first selected group
        for elem1 in group[i]:
            #next selected group
            for elem2 in group[i+1]:
                boolean, pos = compBinary(elem1, elem2)
                if boolean == True:
                    #append the ones used in check list
                    check_list.append(elem1)
                    check_list.append(elem2)
                    #replace the different bit with '-'
                    new_elem = list(elem1)
                    new_elem[pos] = '-'
                    new_elem = "".join(new_elem)
                    if new_elem not in next_group[i]:
                        next_group[i].append(new_elem)
    for i in group:
        for j in i:
            if j not in check_list:
                unchecked.append(j)

    return next_group, unchecked


#remove useless/redundant lists in 2d list
def remove_redundant(group):
    new_group = []
    for j in group:
        new=[]
        for i in j:
            if i not in new:
                new.append(i)
        new_group.append(new)
    return new_group


#remove redundant in 1d list
def remove_redundant_list(list):
    new_list = []
    for i in list:
        if i not in new_list:
            new_list.append(i)
    return new_list


#return True if empty
def check_empty(group):
    if len(group) == 0:
        return True
    return False


#find essential prime implicants ( col num of ones = 1)
def find_prime(Chart):
    prime = []
    for col in range(len(Chart[0])):
        count = 0
        pos = 0
        for row in range(len(Chart)):
            #find essential
            if Chart[row][col] == 1:
                count += 1
                pos = row

        if count == 1:
            prime.append(pos)

    return prime

def check_all_zero(Chart):
    for i in Chart:
        for j in i:
            if j != 0:
                return False
    return True

#find max value in list
def find_max(l):
    max = -1
    index = 0
    for i in range(len(l)):
        if l[i] > max:
            max = l[i]
            index = i
    return index

#multiply two terms (ex. (p1 + p2)(p1+p4+p5) )..it returns the product
def multiplication(list1, list2):
    list_result = []
    #if empty
    if len(list1) == 0 and len(list2)== 0:
        return list_result
    #if one is empty
    elif len(list1)==0:
        return list2
    #if another is empty
    elif len(list2)==0:
        return list1

    #both not empty
    else:
        for i in list1:
            for j in list2:
                #if two term same
                if i == j:
                    list_result.append(i)
                else:
                    list_result.append(list(set(i+j)))

        #sort and remove useless lists and return this list
        list_result.sort()  #sorted in ascending order
        return list(list_result for list_result,_ in itertools.groupby(list_result))

#petrick's method- Getting the SOP
def petrick_method(Chart):
    #initial P
    P = []
    for col in range(len(Chart[0])):
        p =[]
        for row in range(len(Chart)):
            if Chart[row][col] == 1:
                p.append([row])
        P.append(p)
    #multiply
    for l in range(len(P)-1):
        P[l+1] = multiplication(P[l],P[l+1])

    P = sorted(P[len(P)-1],key=len)
    final = []
    #find the terms with min length = this is the one with lowest cost (optimized result)
    min=len(P[0])
    for i in P:
        if len(i) == min:
            final.append(i)
        else:
            break
    #final is the result of petrick's method
    return final

#chart = n*n list
def find_minimum_cost(Chart, unchecked):
    P_final = []
    #essential_prime = list with terms with only one 1 (Essential Prime Implicants)
    essential_prime = find_prime(Chart)
    essential_prime = remove_redundant_list(essential_prime)

    #modifiy the chart to exclude the covered terms
    for i in range(len(essential_prime)):
        for col in range(len(Chart[0])):
            if Chart[essential_prime[i]][col] == 1:
                for row in range(len(Chart)):
                    Chart[row][col] = 0

    #if all zero, no need for petrick method
    if check_all_zero(Chart) == True:
        P_final = [essential_prime]
    else:
        #petrick's method
        P = petrick_method(Chart)

        #find the one with minimum cost
        P_cost = []
        for prime in P:
            count = 0
            for i in range(len(unchecked)):
                for j in prime:
                    if j == i:
                        count = count+ cal_efficient(unchecked[i])
            P_cost.append(count)


        for i in range(len(P_cost)):
            if P_cost[i] == min(P_cost):
                P_final.append(P[i])

        #append prime implicants to the solution of Petrick's method
        for i in P_final:
            for j in essential_prime:
                if j not in i:
                    i.append(j)

    return P_final

#calculate the number of literals
def cal_efficient(s):
    count = 0
    for i in range(len(s)):
        if s[i] != '-':
            count+=1

    return count

#print the binary code to letter
def binary_to_letter(s):
    out = ''
    c = 'a'
    more = False
    n = 0
    for i in range(len(s)):
        #if it is a range a-zA-Z
        if more == False:
            if s[i] == '1':
                out = out + c
            elif s[i] == '0':
                out = out + c+"\'"

        #When we run out of all alphabets we use them with numbers
        if more == True:  
            if s[i] == '1':
                out = out + c + str(n)
            elif s[i] == '0':
                out = out + c + str(n) + "\'"
            n+=1
        #conditions for next operations
        if c=='z' and more == False:
            c = 'A'
        elif c=='Z':
            c = 'a'
            more = True

        elif more == False:
            c = chr(ord(c)+1) #going to the next alphabet by +1 to unicode
    return out

def essential(n_var):
    #get the minterms as input
    a=[int(x) for x in input("Enter the minterms (ex. 0,1,2,3,10) (greater than -1 and less than {0}): ".format((2**n_var))).split(",") if int(x)>-1 and int(x)<(2**n_var)]
    #remove copied minterms
    a_copy=[]
    for i in a:
        if i not in a_copy:
            a_copy.append(i)
    a=a_copy
    #make a group list
    group = [[] for x in range(n_var+1)] #because no of possible groups is bits+1

    for i in range(len(a)):
        #converting to binar+y
        a[i] = bin(a[i])[2:]   #because the output is returned in 0b010100101 format
        if len(a[i]) < n_var:
            #add zeros to fill the n-bits
            for j in range(n_var - len(a[i])):
                a[i] = '0'+ a[i]
        #count the num of 1
        index = a[i].count('1')
        #group by num of 1 separately
        group[index].append(a[i])   #number of 1's is the index of that binary in the list. 

    unchecked = []
    #combine the pairs in series until nothing new can be combined
    while check_empty(group) == False:
        group, unchecked = combinePairs(group,unchecked)

    #make the prime implicant chart
    Chart = [[0 for x in range(len(a))] for x in range(len(unchecked))]

    for i in range(len(a)):
        for j in range (len(unchecked)):
            #checking if term is the same as number
            if compBinarySame(unchecked[j], a[i]):
                Chart[j][i] = 1

    primes = find_minimum_cost(Chart, unchecked)
    primes = remove_redundant(primes)

    essential_prime_implicants=[]
    for prime in primes:
        for i in range(len(unchecked)):
            for j in prime:
                if j == i:
                    essential_prime_implicants.append(unchecked[i])
    return essential_prime_implicants
    
def print_table(higher):
    print("|"," "*(len(max(common_list_of_EPI_letters))-2)," "*int((higher/2) -1), "|", " "*(higher-1),"Products"," "*int((higher/2)-4),"|"," "*int((higher)), s, " "*(higher),"|", end=" "*higher)
    for i in range(n_fun):
        print(" F",i+1,end=" "*(int(higher/2)-1))
    print(" "*(higher-n_fun),"|")
    #printing the contents
    for i in range(len(common_list_of_EPI)):
        print("|", common_list_of_EPI_letters[i], "|", " "*n_var,"P", i, " "*n_var, "|", " "*n_var, common_list_of_EPI[i]," "*n_var,"|",end=" "*(n_var+1))
        for j in range(n_fun):
            print(display_list[i][j],end=" "*(n_var))
        print("   |")

#-------------------------------------------------------------    MAIN    -------------------------------------------------------------------------------------------------------------------#

#get the num of variables (bits) as input
n_var = int(input("Enter the number of variables(bits): "))  #number of inputs
n_fun=int(input("Enter the number of functions: "))    #number of outputs
n_products=int(input("Enter number of products: "))       #number of products/minterms
list_of_EPI=[]     # for collecting essential prime implicants of every function
print("\n---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
# collecting essential prime impl.
for i in range(n_fun):
    print("function",i+1," :")
    essent=essential(n_var)
    list_of_EPI.append(essent)
    print("Essential Prime Implicants:",end=" ")
    # displaying EPI
    for j in essent:                                  
        if essent.index(j)!=(len(essent)-1):
            print(binary_to_letter(j),end="+")
        else:
            print(binary_to_letter(j))
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

# finding common prime implicants to reduce the number of products
common_list_of_EPI=[]
for i in list_of_EPI:
    for j in i:
        if j not in common_list_of_EPI:
            common_list_of_EPI.append(j)
    if len(common_list_of_EPI)>n_products:   # making sure it implies with number of allowed products
        common_list_of_EPI=common_list_of_EPI[:-(len(common_list_of_EPI)-n_products)]

# A nested list for the chart 
display_list=[[[] for i in range(n_fun)] for x in range(len(common_list_of_EPI))]

# marking the products used 
for i in range( n_fun ): #no of functions with '1'
    for k in range( len( list_of_EPI[i] ) ):
        for m in range( len( common_list_of_EPI ) ):
            if list_of_EPI[i][k]==common_list_of_EPI[m]:
                display_list[m][i]='1'

# marking the unused products with '-'
for i in range(len(display_list)):
    for j in range(len(display_list[i])):
        if display_list[i][j]!='1':
            display_list[i][j]='-'

common_list_of_EPI_letters=[binary_to_letter(i) for i in common_list_of_EPI]   #list of minterms/products in variable form

max_len=len(max(common_list_of_EPI_letters)) #finding the max len of the available elements in the list
# formatting the elements for displaying them properly
for i in range(len(common_list_of_EPI_letters)): 
    if (len(common_list_of_EPI_letters[i]))< max_len+2:
        common_list_of_EPI_letters[i] = common_list_of_EPI_letters[i]+ ' '*(max_len - len(common_list_of_EPI_letters[i]) + 2) 

# Printing the table
print("") #for new line

#printing the header
#Getting the letters required to display common EPI
s=''
c='A'
for i in range(n_var):
    boolean=True
    n=0
    s+=c
    if c=='Z' and boolean==True:
        c='A'+str(n)
        n+=1
        boolean=False
    elif boolean==False:
        C=list(c)
        if C[0]=='Z':
            c='Z'
            boolean=True
        else:
            c=chr(ord(C[0]+1))+C[1]
    elif boolean==True:
        c=chr(ord(c)+1)

# if there are more functions than bits
if n_fun>n_var:
    print_table(n_fun)
# if there are more bits than the function
elif n_fun<n_var:
    print_table(n_var)
   
