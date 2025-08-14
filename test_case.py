import pandas as pd
import random

# Parameters
NUM_MENTORS = 30  # Total number of mentors to generate
NUM_MENTEES = 70  # Total number of mentees to generate


def main():
    # Create a list of mentor names: Mentor_1, Mentor_2, ..., Mentor_30
    mentors = [f"Mentor_{i}" for i in range(1, NUM_MENTORS + 1)]

    # Save the mentors list to a CSV file called 'example_mentors.csv'
    pd.DataFrame({"Mentor": mentors}).to_csv("example_mentors.csv", index=False)

    # Prepare an empty list to hold mentee information
    mentees_data = []

    # Loop to generate each mentee's data
    for i in range(1, NUM_MENTEES + 1):
        mentee_name = f"Mentee_{i}"  # Generate the mentee's name

        # Randomly assign a "year" value based on a probability - this feature is AIPed
        selector = random.random()  # random number between 0 and 1
        if selector < 0.35:
            year = 200  # 35% chance
        else:
            year = 100  # 65% chance

        # Randomly select 4 unique mentors for the mentee's preferences
        preferences = random.sample(mentors, 4)  # ensures no duplicates

        # Append the mentee info as a list: [name, year, 4 preferences]
        mentees_data.append([mentee_name] + [year] + preferences)

    # Convert the list of mentees to a DataFrame
    mentees_df = pd.DataFrame(
        mentees_data,
        columns=["Mentee", "AS Year", "First", "Second", "Third", "Fourth"]
    )

    # Save the mentees DataFrame to 'example_mentees.csv'
    mentees_df.to_csv("example_mentees.csv", index=False)

    # Print confirmation that the CSVs were created
    print("Test CSVs created: example_mentors.csv and example_mentees.csv")


# Ensures main() only runs when this file is executed directly
if __name__ == "__main__":
    main()
