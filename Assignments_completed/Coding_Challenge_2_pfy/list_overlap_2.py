
# Philip Yang
# NRS 528 
# Coding Challenge 2

# Copy paste lists a and b
list_a = ['dog', 'cat', 'rabbit', 'hamster', 'gerbil']
list_b = ['dog', 'hamster', 'snake']


# Find what values overlap, got help from Stack Overflow: https://stackoverflow.com/questions/5094083/find-the-overlap-between-2-python-lists

intersection = set(list_a) & set(list_b)
print(f'Overlapping pets:', intersection)

# Find what values do not overlap, got help from Stack Overflow and ChatGPT 3.5 for the symmetric_difference ^ operator

do_not_intersect = set(list_a) ^ set(list_b)
print(f'Non-overlapping pets:', list(do_not_intersect))

