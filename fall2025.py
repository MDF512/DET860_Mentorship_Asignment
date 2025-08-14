"""
Code will take in a list of names of POC (Mentors) form a csv and a list of mentees with preferences from a second csv.
these will be stored in a dataframe

The code will generate a 3rd dataframe to choose the final selection this will be a 2 colum dataframe with mentee in the
first column and mentor in the second column.

A dictionary will also be created listing each mentor and the set number of mentees they can take.

A function will iterate though each mentor and then each mentee counting how many mentees selected them for their first
choice. If the number is less than a set amount the mentees is assigned the mentor in the 3rd dataframe. T If there are more than the allowed amount, the list will be randomized, and the
first X number will be selected. he Mentees are dropped from the preferences dataframe. The dictionary for how many
mentees they can take is updated.

Mentors that are "filled up" are dropped from the list of mentors. This is done by iterating through the dictionary.

The selection function is rerun for second, third and fourth choices.

There is a verification after each run to verify there are still mentors and mentees.

A verification is made to ensure that all mentors have at lease one mentee. If they do not, the preference data frame
is randomized and searched for second preference, third, fourth preference, and so on. The first hit is moved to them.
This verification is run in a while loop till all mentors have a mentee.

when the mentor is assigned a score is also assigned 15 points for first, 10 for second, 7 for third, 5 for fourth.
at the end the score is totaled. and becomes the title of the exported csv. The programs runs X times and the highest
score is selected.
"""
import pandas as pd
import random

# -----------------------------
# CONFIG
# -----------------------------
MENTORS_CSV = "mentors.csv"          # single column: 'Mentor'
MENTEES_CSV = "mentees.csv"          # columns: 'Mentee', 'First', 'Second', 'Third', 'Fourth'
MENTOR_CAPACITY = 3                  # default mentees per mentor
ROUNDS = 10                          # how many times to run for best score
SCORES = {1: 15, 2: 10, 3: 7, 4: 5}  # preference scoring
NUM_MENTORS, NUM_MENTEES, MIN_MENTEES, MENTORS_WITH_EXTRA  = 0, 0, 0, 0
# -----------------------------
# FUNCTIONS
# -----------------------------

def load_data():
    mentors_df = pd.read_csv(MENTORS_CSV)
    mentees_df = pd.read_csv(MENTEES_CSV)
    global NUM_MENTORS, NUM_MENTEES, MIN_MENTEES, MENTORS_WITH_EXTRA
    NUM_MENTORS = len(mentors_df)
    NUM_MENTEES = len(mentees_df)
    MIN_MENTEES = NUM_MENTEES // NUM_MENTORS
    MENTORS_WITH_EXTRA = NUM_MENTEES % NUM_MENTORS
    return mentors_df, mentees_df

def initialize_capacity_dict(mentors_df):
    return {mentor: 1 for mentor in mentors_df["Mentor"]}

def sort_and_tally_max(working_df):
    for index,row in working_df.iterrows():
        count = 0
        columns_to_count = ["First_Choice", "Second_Choice", "Third_Choice", "Fourth_Choice", "Random"]
        for column in columns_to_count:
            count += len(row[column])
        working_df.loc[index, "Count"] = count
    working_df.sort_values(by="Count", ascending=False, inplace=True)
    working_df = working_df.reset_index(drop=True)
    for index,row in working_df.iterrows():
        if index < MENTORS_WITH_EXTRA:
            working_df.loc[index, "Max"] = MIN_MENTEES + 1
        else:
            working_df.loc[index, "Max"] = MIN_MENTEES
    return working_df

def assign_mentors(mentors_df, mentees_df):
    # Set up the structure to store the assignments
    working_df = pd.DataFrame(
        columns=["Mentor", "First_Choice", "Second_Choice", "Third_Choice", "Fourth_Choice", "Random", "Count", "Max"]
    )
    working_df["Mentor"] = mentors_df["Mentor"] # Populate the Mentor column
    working_df["Count"] = 0  # populate the count column
    working_df["Max"] = 0 # populate the Max Colum
    for col in ["First_Choice", "Second_Choice", "Third_Choice", "Fourth_Choice", "Random"]:  #populate these with empty lists
        working_df[col] = [[] for _ in range(len(mentors_df))]

    # First just assign everyone their first choice
    for _, row in mentees_df.iterrows():
        mentee = row["Mentee"]
        mentor = row["First"]
        # Find the mentor in working_df
        mask = working_df["Mentor"] == mentor
        # Append mentee name to First_Choice list
        working_df.loc[mask, "First_Choice"] = working_df.loc[mask, "First_Choice"].apply(lambda lst: lst + [mentee])
        # Increment count
        working_df.loc[mask, "Count"] += 1

    working_df = sort_and_tally_max(working_df)

    def move_mentees():
        #Search the mentees assigned to mentors with too many mentees for candiates to switch to mentors with zero mentees
        # create a list of potential mentees
        venerable_to_move_mentees = []
        mentors_0 = []
        mentors_1 = []
        for index, row in working_df.iterrows():
            if working_df.loc[index, "Count"] > working_df.loc[index, "Max"]:
                venerable_to_move_mentees += working_df.loc[index, 'First_Choice']
            if working_df.loc[index, "Count"] == 0:
                mentors_0.append(working_df.loc[index, 'Mentor'])
            if working_df.loc[index, "Count"] == 1:
                mentors_1.append(working_df.loc[index, 'Mentor'])

        if len(venerable_to_move_mentees) == 0:
            return False
        elif len(mentors_1) == 0 and len(mentors_0) == 0:
            # This is where someone has too many but everyone has at least 2. then randomly pick on and assign to second
            mentee = random.choice(venerable_to_move_mentees)
            mask = mentees_df["Mentee"] == mentee
            second = mentees_df.loc[mask, "Second"].values[0]
            for index,row in working_df.iterrows():
                if mentee in row["First_Choice"]:
                    old_mentor = row["Mentor"]
                    working_df.loc[index, "First_Choice"].remove(mentee)
                    working_df.loc[index, "Count"] = working_df.loc[index, "Count"] - 1
            mask = working_df["Mentor"] == second
            working_df.loc[mask, "Second_Choice"] = working_df.loc[mask, "Second_Choice"].apply(
                lambda lst: lst + [mentee])
            working_df.loc[mask, "Count"] += 1
            return True


        for mentee in venerable_to_move_mentees:
            mask = mentees_df["Mentee"] == mentee
            second = mentees_df.loc[mask, "Second"].values[0]
            if second in mentors_0 or second in mentors_1:
                for index,row in working_df.iterrows():
                    if mentee in row["First_Choice"]:
                        old_mentor = row["Mentor"]
                        working_df.loc[index, "First_Choice"].remove(mentee)
                        working_df.loc[index, "Count"] = working_df.loc[index, "Count"] - 1
                mask = working_df["Mentor"] == second
                working_df.loc[mask, "Second_Choice"] = working_df.loc[mask, "Second_Choice"].apply(
                    lambda lst: lst + [mentee])
                working_df.loc[mask, "Count"] += 1
                return True

        for mentee in venerable_to_move_mentees:
            mask = mentees_df["Mentee"] == mentee
            third = mentees_df.loc[mask, "Third"].values[0]
            if third in mentors_0 or third in mentors_1:
                for index, row in working_df.iterrows():
                    if mentee in row["First_Choice"]:
                        old_mentor = row["Mentor"]
                        working_df.loc[index, "First_Choice"].remove(mentee)
                        working_df.loc[index, "Count"] = working_df.loc[index, "Count"] - 1
                mask = working_df["Mentor"] == third
                working_df.loc[mask, "Third_Choice"] = working_df.loc[mask, "Third_Choice"].apply(
                    lambda lst: lst + [mentee])
                working_df.loc[mask, "Count"] += 1
                return True
        for mentee in venerable_to_move_mentees:
            mask = mentees_df["Mentee"] == mentee
            fourth = mentees_df.loc[mask, "Fourth"].values[0]
            if fourth in mentors_0 or fourth in mentors_1:
                for index, row in working_df.iterrows():
                    if mentee in row["First_Choice"]:
                        old_mentor = row["Mentor"]
                        working_df.loc[index, "First_Choice"].remove(mentee)
                        working_df.loc[index, "Count"] = working_df.loc[index, "Count"] - 1
                mask = working_df["Mentor"] == fourth
                working_df.loc[mask, "Fourth_Choice"] = working_df.loc[mask, "Fourth_Choice"].apply(
                    lambda lst: lst + [mentee])
                working_df.loc[mask, "Count"] += 1
                return True

        mentee = random.choice(venerable_to_move_mentees)
        for index, row in working_df.iterrows():
            if mentee in row["First_Choice"]:
                old_mentor = row["Mentor"]
                working_df.loc[index, "First_Choice"].remove(mentee)
                working_df.loc[index, "Count"] = working_df.loc[index, "Count"] - 1
        if len(mentors_0) > 0:
            random.shuffle(mentors_0)
            new_mentor = mentors_0[0]
        else:
            random.shuffle(mentors_1)
            new_mentor = mentors_1[0]
        mask = working_df["Mentor"] == new_mentor
        working_df.loc[mask, "Random"] = working_df.loc[mask, "Random"].apply(
            lambda lst: lst + [mentee])
        working_df.loc[mask, "Count"] += 1
        return True


    need_to_move_mentees = True #assume there are some to move
    while need_to_move_mentees:
        need_to_move_mentees = move_mentees()
        working_df = sort_and_tally_max(working_df)

    for index,_ in working_df.iterrows():
        assert working_df.loc[index, "Count"] == working_df.loc[index, "Max"], "ERROR: Unable to properly assign mentees"

    return working_df

def stats(assignments):
    first_choice, second_choice, third_choice, fourth_choice, random_choice = 0, 0, 0, 0, 0
    for row in assignments["First_Choice"]:
        first_choice += len(row)
    for row in assignments["Second_Choice"]:
        second_choice += len(row)
    for row in assignments["Third_Choice"]:
        third_choice += len(row)
    for row in assignments["Fourth_Choice"]:
        fourth_choice += len(row)
    for row in assignments["Random"]:
        random_choice += len(row)
    first_choice = (first_choice / NUM_MENTEES) * 100
    second_choice = (second_choice / NUM_MENTEES) * 100
    third_choice = (third_choice / NUM_MENTEES) * 100
    fourth_choice = (fourth_choice / NUM_MENTEES) * 100
    random_choice = (random_choice / NUM_MENTEES) * 100
    print("------STATISTICS------")
    print(f'1st choice:    {first_choice:6.2f}%')
    print(f'2nd choice:    {second_choice:6.2f}%')
    print(f'3rd choice:    {third_choice:6.2f}%')
    print(f'4th choice:    {fourth_choice:6.2f}%')
    print(f'Random choice: {random_choice:6.2f}%')
    print("----------------------")

def format_and_export(assignments):
    mentee_rows = []
    for _, row in assignments.iterrows():
        mentor = row["Mentor"]
        for col in ["First_Choice", "Second_Choice", "Third_Choice", "Fourth_Choice", "Random"]:
            for mentee in row[col]:
                mentee_rows.append({"Mentee": mentee, "Mentor": mentor})

    mentee_results = pd.DataFrame(mentee_rows)
    mentee_results.to_csv("mentee_results.csv", index=False)

    mentor_df = assignments.copy()
    mentor_df["Mentees"] = mentor_df[
        ["First_Choice", "Second_Choice", "Third_Choice", "Fourth_Choice", "Random"]].apply(
        lambda row: "; ".join([m for lst in row for m in lst]), axis=1
    )

    # Keep only Mentor and Mentees columns
    mentor_results = mentor_df[["Mentor", "Mentees"]]
    mentor_results.to_csv("mentor_results.csv", index=False)

# -----------------------------
# MAIN RUN LOOP
# -----------------------------
def main():
    mentors_df, mentees_df_original = load_data()
    mentees_df = mentees_df_original.copy()
    final_assignments = assign_mentors(mentors_df, mentees_df)
    stats(final_assignments)
    format_and_export(final_assignments)

if __name__ == "__main__":
    main()
