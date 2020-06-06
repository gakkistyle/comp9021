def average_of_digits(digit=None):
    if digit == None:
        return -1
    if len(digit) == 1:
        digit_set = set(str(digit[0]))
        sum = 0
        for e in digit_set:
            sum += int(e)
        return sum/len(digit_set)
    common = []
    word_set1 = set(str(digit[0]))
    word_set2 = set(str(digit[1]))
    for e in word_set1:
        if e in word_set2:
            common.append(e)
    for i in range(2,len(digit)):
        word_setn = set(str(digit[i]))
        for e in common:
            if e not in word_setn:
                common.remove(e)

    if common == []:
        return -1
    sum = 0
    for e in common:
        sum += int(e)
    return sum/len(common)

print(average_of_digits([3136823,665537857,8363265,35652385]))
    
    
