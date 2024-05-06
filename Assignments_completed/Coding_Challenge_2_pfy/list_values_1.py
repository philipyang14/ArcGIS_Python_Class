# Philip Yang
# NRS 528
# Coding Challenge 2

# Copy list from Assignment: Coding Challenge 2
list = [1, 2, 3, 6, 8, 12, 20, 32, 46, 85]

# Make new list with all elements less than 5
filtered_list = [i for i in list if i<5]
print(filtered_list)

# Trying to do it in one line of code, dunno if this is what you mean here but it works...
print([i for i in [1, 2, 3, 6, 8, 12, 20, 32, 46, 85] if i < 5])

# Sources include stack overflow 
