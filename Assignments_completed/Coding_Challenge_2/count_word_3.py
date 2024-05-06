
# Philip Yang
# NRS 528
# Coding Challenge 2


# Paste from prompt

string = 'hi dee hi how are you mr dee'

# Convert to list

word_list = string.split()

# print(word_list)

# Make an empty dictionary to fill

word_count = {}

# For loop to count the words in the list and add the word if it occurs to the dictionary

for word in word_list: 
    if word in word_count:
        word_count[word] += 1
    else:
        word_count[word] = 1
        
print(word_count)

