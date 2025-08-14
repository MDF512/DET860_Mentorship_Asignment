ITERATIONS = 100  # Total number of times to run the test loop
count = 0          # Counter for iterations

# Import the scripts to run
import test_case   # Make sure the file is named 'test_case.py' (no spaces)
import fall2025    # Import the second script to run

# Loop to run the scripts ITERATIONS times
while count < ITERATIONS:
    count = count + 1  # Increment the counter
    test_case.main()   # Call the main() function from test_case.py
    fall2025.main()    # Call the main() function from fall2025.py
