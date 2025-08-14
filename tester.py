ITTERATIONS = 100
count = 0

import test_case   # rename file to test_case.py (no spaces)
import fall2025



while count < ITTERATIONS:
    count = count + 1
    test_case.main()  # assuming test_case.py has a main() function
    fall2025.main()