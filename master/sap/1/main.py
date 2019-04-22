#!/usr/bin/env python3


def substring(s, i, k):
    if k == 1:
        return s[i]
    else:
        return substring(s, i, 1) + substring(s, i + 1, k - 1)


def count_word(s, word):
    if s == word:
        return 1
    else:
        i = s.find(' ')
        if i == -1:
            return 0
        else:
            return count_word(s[:i], word) + count_word(s[i + 1:], word)


def word_duplicates(s):
    i = s.find(' ')
    if i == -1:
        return 0
    else:
        return count_word(s[i + 1:], s[:i]) == 1 or word_duplicates(s[i + 1:])


def replace_word(s, word_1, word_2):
    if s == word_1:
        return word_2
    else:
        i = s.find(' ')
        if i == -1:
            return s
        else:
            return replace_word(s[:i], word_1, word_2) + ' ' + replace_word(s[i + 1:], word_1, word_2)


def reverse_words(s):
    i = s.find(' ')
    if i == -1:
        return s
    else:
        return reverse_words(s[i + 1:]) + ' ' + reverse_words(s[:i])


def check_word_in_both(s1, s2):
    i = s1.find(' ')
    if i == -1:
        return False
    else:
        return count_word(s2, s1[:i]) == 1 or check_word_in_both(s1[i + 1:], s2)


def length(s):
    if not s:
        return 0
    else:
        return length(s[1:]) + 1


def swap_first_and_last(s):
    i = s.find(' ')
    j = s.rfind(' ')
    if i == -1 and j == -1:
        return s
    else:
        return s[j + 1:] + ' ' + s[i + 1:j] + ' ' + s[:i]


if __name__ == '__main__':
    print(substring('abcdefgh', 4, 4))
    print(count_word("123 323 32321 123 123 323 323", "123"))
    print(word_duplicates("123 323 32321 123 123 323 323"))
    print(replace_word('123 321 123', '321', 'abc'))
    print(reverse_words('abc cde efg thj'))
    print(check_word_in_both('abc cde efg', 'abc123 cde'))
    print(length('abc'))
    print(swap_first_and_last('abc cde efg thj'))
