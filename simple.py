

# 1. Variables and Data Types
name = "Alex"          
age = 25              
height = 1.75         
is_student = True     

# 2. 
skills = ["Python", "Git", "SQL"]
user_profile = {
    "username": "alex_dev",
    "role": "Developer"
}

# 3. 
def check_admission(user_age, student_status):
    """Determines eligibility based on age and student status."""
    if user_age >= 18 and student_status:
        return "Eligible for adult student discount."
    elif user_age >= 18:
        return "Eligible for standard adult admission."
    else:
        return "Eligible for minor admission."

# 4. 
try:
    print(f"--- Welcome, {name}! ---")
    user_input = input("Enter your favorite number to test loops: ")
    iterations = int(user_input)  # Might raise ValueError
    
    # 5. Loops (For and While)
    print("\n[Running Loop Test]")
    for i in range(1, iterations + 1):
        if i % 2 == 0:
            print(f"  Iteration {i}: Even")
        else:
            print(f"  Iteration {i}: Odd")
            
except ValueError:
    print("\n[Error]: That wasn't a valid integer! Defaulting loop to 1.")
    iterations = 1

# 6. 
print("\n--- Summary Review ---")
print(f"Profile: {user_profile['username']} ({user_profile['role']})")
print(f"Skills: {', '.join(skills)}")
print(f"Status: {check_admission(age, is_student)}")
