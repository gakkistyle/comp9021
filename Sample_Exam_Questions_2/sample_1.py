# COMP9021 19T3 - Rachid Hamadi
# Sample Exam 2


def remove_consecutive_duplicates(word):
    '''
    >>> remove_consecutive_duplicates('')
    ''
    >>> remove_consecutive_duplicates('a')
    'a'
    >>> remove_consecutive_duplicates('ab')
    'ab'
    >>> remove_consecutive_duplicates('aba')
    'aba'
    >>> remove_consecutive_duplicates('aaabbbbbaaa')
    'aba'
    >>> remove_consecutive_duplicates('abcaaabbbcccabc')
    'abcabcabc'
    >>> remove_consecutive_duplicates('aaabbbbbaaacaacdddd')
    'abacacd'
    '''
    # Insert your code here (the output is returned, not printed out)
    if len(word) == 0:
        return word
    result = word[0]
    for i in range(1,len(word)):
        if word[i] != word[i-1]:
            result += word[i]
    return result

if __name__ == '__main__':
    import doctest
    doctest.testmod()
