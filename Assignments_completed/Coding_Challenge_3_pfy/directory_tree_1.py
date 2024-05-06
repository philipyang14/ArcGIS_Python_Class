# Philip Yang
# NRS 528
# Coding Challenge 3

# modules needed
import os
import shutil  # Use shutil to delete an entire directory tree rather than os.rmdir that can only rm emtpy directories

# Define the path using a way to get the current directory so the code can be run on any machine
current_dir = os.getcwd()

# Make a list of the directory structure for the problem in one new directory "new_dir" (made a central one to make it easier to delete)
dirs_list = [
    "new_dir/draft_code/pending",
    "new_dir/draft_code/complete",
    "new_dir/includes",
    "new_dir/layouts/default",
    "new_dir/layouts/post/posted",
    "new_dir/site"
]

# # Create directories with a for loop in the list, using os.path.join to append the list values into main dir path
for dirs in dirs_list:
    os.makedirs(os.path.join(current_dir, dirs), exist_ok=True)

print("Directories created successfully.")


##### UNCOMMENT WHEN WANT TO DELETE THE NEW DIR TREE "new_dir" #####
# shutil.rmtree(os.path.join(current_dir, "new_dir"))

# Learned about shutil from ChatGPT 3.5