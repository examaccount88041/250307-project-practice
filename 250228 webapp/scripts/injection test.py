good_username = "luke.yates1"
bad_username = "' OR 1=1; --"

username = input("Enter your username: ")

naughty_characters = ["<", ">", ",", "'", "="]
for char in username:
    if char in naughty_characters:
        print("Do not use these special characters: > < , ' =")