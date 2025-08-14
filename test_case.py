import pandas as pd
import random

# Parameters
NUM_MENTORS = 30
NUM_MENTEES = 70

def main():
    # Create mentors list
    mentors = [f"Mentor_{i}" for i in range(1, NUM_MENTORS + 1)]
    pd.DataFrame({"Mentor": mentors}).to_csv("mentors.csv", index=False)

    # Create mentees with random preferences
    mentees_data = []
    for i in range(1, NUM_MENTEES + 1):
        mentee_name = f"Mentee_{i}"
        selector = random.random()
        if selector < 0.35:
            year = 200
        else:
            year = 100
        preferences = random.sample(mentors, 4) # unique 4 random mentors
        mentees_data.append([mentee_name] + [year] + preferences)

    mentees_df = pd.DataFrame(mentees_data, columns=["Mentee", "AS Year", "First", "Second", "Third", "Fourth"])
    mentees_df.to_csv("mentees.csv", index=False)

    print("Test CSVs created: mentors.csv and mentees.csv")

if __name__ == "__main__":
    main()