
# Philip Yang
# NRS 528
# Coding Challenge 2

# Paste from assignment

letter_scores = {
    "aeioulnrst": 1,
    "dg": 2,
    "bcmp": 3,
    "fhvwy": 4,
    "k": 5,
    "jx": 8,
    "qz": 10
}


# Write a function to calculate scrabble score
#### Note: used this prompt in ChatGPT 3.5 "write me a function that uses this dictionary to compute 
#### what any combination of letters or words entered in would result in a scrabble score"
# Added my own comments to describe what the parts of the function

def scrabble_score():
    letter_scores = {
        "aeioulnrst": 1,
        "dg": 2,
        "bcmp": 3,
        "fhvwy": 4,
        "k": 5,
        "jx": 8,
        "qz": 10
    }
    
    # Prompt for a word input
    word = str(input("Enter a word: "))
    
    # Start score at 0 initially
    score = 0
    
    # Write a nested for loop to iterate over letters in the entered word (converted to lowercase)
    for letter in word.lower():
        for key in letter_scores:
            if letter in key:
                score += letter_scores[key]
                break  # Exit the inner loop once the letter is found

    return score

# Example usage:
result = scrabble_score()
print(f"The Scrabble score for the entered word is: {result}")

# Tested Supernova and got 14!

