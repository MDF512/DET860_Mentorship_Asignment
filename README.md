# Mentee-Mentor Assignment Tool

This project provides a Python-based solution for automatically assigning mentees to mentors based on preferences. It includes three main Python scripts and produces results formatted for easy review.

## Files

1. **`fall2025.py`**

   * Runs the main algorithm to assign mentees to mentors.
   * Ensures each mentor has the appropriate number of mentees, taking into account mentees’ ranked preferences.
   * Produces statistics showing the percentage of mentees assigned to their 1st, 2nd, 3rd, 4th, or random choice.

2. **`test_case.py`**

   * Generates test CSV data for mentors and mentees.
   * Creates `mentors.csv` (unique mentor names) and `mentees.csv` (unique mentees with ranked preferences).
   * Useful for quickly generating mock data to test the algorithm.

3. **`tester.py`**

   * Runs multiple iterations of the assignment algorithm using `fall2025.py` and test data from `test_case.py`.
   * Useful for stress testing or evaluating the distribution of assignment outcomes over many runs.

---

## Input File Format

### 1. `mentors.csv`

* Single column titled `Mentor`.
* Each row contains a unique mentor name.
* Example:

| Mentor    |
| --------- |
| Mentor\_1 |
| Mentor\_2 |
| Mentor\_3 |

### 2. `mentees.csv`

* Columns: `Mentee, AS Year, First, Second, Third, Fourth`
* `Mentee`: Unique mentee names
* `AS Year`: Included for future use but not currently used by the algorithm
* `First`–`Fourth`: Mentor preferences. Must exactly match a name in `mentors.csv`.

Example:

| Mentee    | AS Year | First     | Second    | Third     | Fourth    |
| --------- | ------- | --------- | --------- | --------- | --------- |
| Mentee\_1 | 100     | Mentor\_1 | Mentor\_2 | Mentor\_3 | Mentor\_4 |
| Mentee\_2 | 200     | Mentor\_2 | Mentor\_3 | Mentor\_1 | Mentor\_4 |

---

## Output

The assignment results are exported as an **Excel file with two sheets**:

1. **Mentors Sheet**

   * Each row corresponds to a mentor
   * Column `Mentees` contains all assigned mentees, separated by semicolons
   * Shows how mentees were assigned (1st–4th choice or random)

2. **Mentees Sheet**

   * Each row corresponds to a mentee
   * Column `Mentor` contains the assigned mentor

Example:

**Mentors Sheet**

| Mentor    | Mentees                         |
| --------- | ------------------------------- |
| Mentor\_1 | Mentee\_1; Mentee\_5; Mentee\_7 |
| Mentor\_2 | Mentee\_2; Mentee\_3; Mentee\_6 |

**Mentees Sheet**

| Mentee    | Mentor    |
| --------- | --------- |
| Mentee\_1 | Mentor\_1 |
| Mentee\_2 | Mentor\_2 |
| Mentee\_3 | Mentor\_2 |

---

## Usage

1. Prepare input CSV files (`mentors.csv` and `mentees.csv`) following the required format. Place them in the same
folder as the python scripts. 

2. Optionally, generate test data:

```bash
python test_case.py
```

3. Run the main assignment script:

```bash
python fall2025.py
```

4. Optionally, run multiple iterations to test the algorithm:

```bash
python tester.py
```

5. Results will be saved in **`mentor_results.csv`** and **`mentee_results.csv`**, or you can combine them into a single Excel file as needed.
