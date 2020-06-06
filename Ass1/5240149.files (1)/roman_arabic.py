import sys

command = input('How can I help you? ')
command = command.strip()
if len(command)<= 14:
    print('I don\'t get what you want, sorry mate!')
    sys.exit()

if command.split()[0] != 'Please' or command.split()[1] != 'convert' \
        or  len(command.split()) < 3 or len(command.split()) >5  :
    print('I don\'t get what you want, sorry mate!')
    sys.exit()

one = ['I','II','III','IV','V','VI','VII','VIII','IX']
ten = ['X','XX','XXX','XL','L','LX','LXX','LXXX','XC']
hundred = ['C','CC','CCC','CD','D','DC','DCC','DCCC','CM']
thousand = 'M'
# the first question
if len(command.split()) == 3:
    content = command.split()[2]

#digit number to roman
    if content.isdigit():
        if content[0] == '0' or int(content) > 3999:
            print('Hey, ask me something that\'s not impossible to do!')
            sys.exit()
        else:
            num = int(content)
            k = num//1000
            h = (num%1000)//100
            t = (num%100)//10
            o = num % 10
            result = ''
            for i in range(k):
                result += thousand
            if h:
                result += hundred[h-1]
            if t:
                result += ten[t-1]
            if o:
                result += one[o-1]
            print('Sure! It is',result)

# roman to digit number
    elif content.isalpha():
        '''
        for e in content:
            if e!='M' and e not in hundred and e not in ten and e not in one:
                print('Hey, ask me something that\'s not impossible to do!')
                sys.exit()
        
        '''

        result = 0
        sign = 0
        if content[sign] == 'M':
            result += 1000
            sign += 1
            if sign<len(content) and content[sign] == 'M':
                result += 1000
                sign += 1
                if sign<len(content) and content[sign] == 'M':
                    result += 1000
                    sign += 1

        if sign<len(content) and content[sign] == 'C':
            result += 100
            sign += 1
            if sign<len(content) and content[sign] == 'C':
                result += 100
                sign += 1
                if sign < len(content) and content[sign] == 'C':
                    result += 100
                    sign += 1
            elif sign<len(content) and content[sign] == 'M':
                result += 800
                sign += 1
            elif sign<len(content) and content[sign] == 'D':
                result += 300
                sign += 1
        elif sign<len(content) and content[sign] == 'D':
            result += 500
            sign += 1
            num = 0
            while sign < len(content) and content[sign] == 'C' and num < 3:
                result += 100
                sign += 1
                num += 1

        if sign<len(content) and content[sign] == 'X':
            result += 10
            sign += 1
            if sign < len(content) and content[sign] == 'X':
                result += 10
                sign += 1
                if sign < len(content) and content[sign] == 'X':
                    result += 10
                    sign += 1
            elif sign < len(content) and content[sign] == 'C':
                result += 80
                sign += 1
            elif sign < len(content) and content[sign] == 'L':
                result += 30
                sign += 1
        elif sign < len(content) and content[sign] == 'L':
            result += 50
            sign += 1
            num = 0
            while sign<len(content) and content[sign] == 'X' and num <3:
                result += 10
                sign += 1
                num += 1

        if sign<len(content) and content[sign] == 'I':
            result += 1
            sign += 1
            if sign < len(content) and content[sign] == 'I':
                result += 1
                sign += 1
                if sign < len(content) and content[sign] == 'I':
                    result += 1
                    sign += 1
            elif sign < len(content) and content[sign] == 'X':
                result += 8
                sign += 1
            elif sign < len(content) and content[sign] == 'V':
                result += 3
                sign += 1
        elif sign<len(content) and content[sign] == 'V':
            result += 5
            sign += 1
            num = 0
            while sign < len(content) and content[sign] == 'I' and num <3:
                result += 1
                sign += 1
                num += 1

        if sign == len(content):
            print('Sure! It is',result)
        else :
            print('Hey, ask me something that\'s not impossible to do!')

    else :
        print('Hey, ask me something that\'s not impossible to do!')
        sys.exit()



# the second question
def FindTopN(num):
    i=0
    if num<10:
        return num
    else:
        while num // 10 != 0:
            num = num // 10
            i = num
        return i

def check(content):
    if len(content) < 4:
        return
    else:
        for _ in range(len(content) - 3):
            if content[_] == content[_ + 1] == content[_ + 2] == content[_ + 3]:
                print('Hey, ask me something that\'s not impossible to do!')
                sys.exit()

def digitToValue(c,list,v):
    for i in range(len(list)):
        if c == list[i]:
            return v[i]
    print('Hey, ask me something that\'s not impossible to do!')
    sys.exit()

def findMaxIndex(content,list,v,left,right):
    o_sign = left
    max = digitToValue(content[left],list,v)
    max_copy = max
    maxindex = left
    for i in range(left,right):
        if digitToValue(content[i],list,v) > max:
            max = digitToValue(content[i],list,v)
            maxindex = i
    if maxindex - o_sign > 1 or (v.index(max_copy)-v.index(max))>2\
        or (maxindex!=o_sign and FindTopN(max_copy)==5) or \
            (left+1<right and  content[left]==content[left+1] and  (FindTopN(max_copy)==FindTopN(digitToValue(content[left+1],list,v))==5)
             or (left+2<right  and content[left]==content[left+2] != content[left+1] and FindTopN(max_copy)==5 ))\
             or (left+2<right and FindTopN(digitToValue(content[left+1],list,v)) == 5 and content[left] == content[left+2])\
             or left+2<right and maxindex-o_sign == 1 and content[maxindex] == content[maxindex+1]:
        print('Hey, ask me something that\'s not impossible to do!')
        sys.exit()
    else:
        return maxindex

def convert_Digit_to_Number(content,list,v):
    check(content)
    result = 0
    for i in range(len(content)):
        j = findMaxIndex(content,list,v,i,len(content))
        if i == j:
            plus = v[list.index(content[i])]
            result = result + plus
        else:
            minus = v[list.index(content[i])]
            result = result - minus
    return result

def convert_Number_to_Digit(content,list,v):
    num = int(content)
    if (FindTopN(v[0]) != 5 and num >= v[0] * 4) or \
       (FindTopN(v[0]) == 5 and num >= v[0] * 1.8)   or  num ==0 \
        or content[0] == '0':
        print('Hey, ask me something that\'s not impossible to do!')
        sys.exit()
    else:
        result = ''
        for  i in range(len(content)):
            digit_num = len(content) - i
            getN = int(content[i])
            if getN ==0:
                continue
            elif getN >=1 and getN <= 3:
                result = result +  getN*list[(-2)*digit_num+1]
            elif getN == 4:
                result = result + list[(-2)*digit_num+1] + list[(-2)*digit_num]
            elif getN == 5:
                result = result + list[(-2)*digit_num]
            elif getN >=6 and getN <=8:
                result = result + list[(-2)*digit_num] + (getN-5) * list[(-2)*digit_num+1]
            elif getN == 9:
                result = result + list[(-2)*digit_num+1] + list[(-2)*digit_num-1]
            else :
                print('Hey, ask me something that\'s not impossible to do!')
                sys.exit()
    return result

def Findesamechar(string):
    for i in range(len(string)):
        for j in range(i+1,len(string)):
            if string[i] == string[j]:
                return True
    return False

if len(command.split()) == 5:
    if command.split()[3] != 'using':
        print('I don\'t get what you want, sorry mate!')
        sys.exit()
    elif command.split()[4].isalpha() == False or Findesamechar(command.split()[4]):
        print('Hey, ask me something that\'s not impossible to do!')
        sys.exit()
    else:
        digit = command.split()[4]
        content = command.split()[2]
        n = 1
        v = []
        v.append(n)
        for _ in range(1, len(digit)):
            if _ % 2 == 1:
                n = n * 5
            else:
                n = n * 2
            v.append(n)
        v.reverse()
        # self-make to number
        if content.isalpha():
            result = convert_Digit_to_Number(content, digit, v)
            print('Sure! It is', result)
        # number to self make
        elif content.isdigit():
            result = convert_Number_to_Digit(content, digit, v)
            print('Sure! It is', result)
        else :
            print('Hey, ask me something that\'s not impossible to do!')


# the third question
def FindOnce(word,list):
    count = 0
    for e in list:
        if word == e:
            count += 1
    if count == 1:
        return True
    else:
        return False

if len(command.split()) == 4:
    if command.split()[3] != 'minimally':
        print('I don\'t get what you want, sorry mate!')
        sys.exit()

    if command.split()[2].isalpha() == False:
        print('Hey, ask me something that\'s not impossible to do!')
        sys.exit()

    content = command.split()[2]
    alphabet = []
    for i in range(-1,-len(content)-1,-1):
        if content[i] not in alphabet:
            alphabet.append(content[i])
        else:
            if content[i] != content[i+1]:
                if content[i] == content[i+2] :
                    index = alphabet.index(content[i])
                    if index%2 == 0:
                        alphabet[index] = alphabet[index+1]
                        alphabet[index+1] = '_'
                        alphabet.append(content[i])
                    elif index == len(alphabet) -1:
                        alphabet[index] = '_'
                        alphabet.append(content[i])
                    else:
                        alphabet[index] = '_'
                        alphabet.append('_')
                        alphabet.append(content[i])
                elif i+3 <0 and content[i] == content[i+3] != content[i+2]:
                    index = alphabet.index(content[i])
                    if index%2 == 1:
                        alphabet[index] = '_'
                        alphabet.append(content[i])
                        alphabet.append(alphabet[index+2])
                        alphabet[index + 2] = '_'
                    else:
                        alphabet.append(alphabet[index+2])
                        alphabet[index+2] = content[i]
                        alphabet[index] = alphabet[index+1]
                        alphabet[index+1] = '_'
            elif content[i] == content[i+1]:
                index = alphabet.index(content[i])
                if index%2 == 1:
                    alphabet.append(content[i])
                    alphabet[index] = '_'
    for i in range(len(alphabet)):
        if len(alphabet) >1 and i%2 == 1:
            if FindOnce(alphabet[i],content) and FindOnce(alphabet[i-1],content):
                alphabet[i],alphabet[i-1] = alphabet[i-1],alphabet[i]

    alphabet.reverse()
    list = ''.join(alphabet)
    n = 1
    v = []
    v.append(n)
    for _ in range(1, len(alphabet)):
        if _ % 2 == 1:
            n = n * 5
        else:
            n = n * 2
        v.append(n)
    v.reverse()
    result = convert_Digit_to_Number(content,list,v)
    print(f'Sure! It is {result} using {list}')






















