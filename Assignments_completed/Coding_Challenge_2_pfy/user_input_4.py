
# Philip Yang
# NRS 528
# Coding Challenge 2

# Paste hint from assignment

# age = input("What is your age? ")
# print "Your age is " + str(age)

# Write function that asks for age input and returns age until retirement at 65 yrs 

def years_until_bliss():
    try:
        # Ask for age
        age = int(input("Enter your age: "))

        # Check for positive age
        if age < 0:
            print("Please enter a valid age.")
            return
        
        # Check for age >65
        if age > 65:
            print("Blasted! You could be retired already, friend, what happened...? ")
            return

        # Calculate the number of years until retirement at 65 yrs
        years_until_bliss = max(0, 65 - age)

        # Display the result
        print(f"Sorry mate, you have {years_until_bliss} years until blissful retirement at age 65.")
    
    except ValueError:
        print("Please enter a valid age as a number.")

# Call the function
years_until_bliss()


# Got help from ChatGPT 3.5

