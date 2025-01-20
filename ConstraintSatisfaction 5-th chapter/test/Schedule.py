import numpy as np

nurses = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
shift_preference = [[1, 0, 0], [1, 1, 0], [0, 0, 1], [0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 1, 1], [1, 1, 1]]
shift_min = [2, 2, 1]
shift_max = [3, 4, 2]
max_shifts_per_week = 5
weeks = 1
shift_per_day = len(shift_min)
shifts_per_week = 7 * shift_per_day
hard_constraint_penalty = 10

def get_nurse_shifts(schedule):
    shifts_per_nurse = len(nurses) * shifts_per_week * weeks // len(nurses)
    print("shifts_per_nurse =", shifts_per_nurse)
    nurse_shifts_dict = {nurse: schedule[i * shifts_per_nurse:(i + 1) * shifts_per_nurse] for i, nurse in enumerate(nurses)}
    print("nurse_shifts_dict =", nurse_shifts_dict)
    return nurse_shifts_dict

def count_consecutive_shift_violations(nurse_shifts_dict):
    return sum(1 for shifts in nurse_shifts_dict.values() for s1, s2 in zip(shifts, shifts[1:]) if s1 == 1 and s2 == 1)

def count_shifts_per_week_violations(nurse_shifts_dict):
    violations = 0
    for shifts in nurse_shifts_dict.values():
        weekly_shifts = [sum(shifts[i:i + shifts_per_week]) for i in range(0, weeks * shifts_per_week, shifts_per_week)]
        violations += sum(max(0, shifts - max_shifts_per_week) for shifts in weekly_shifts)
    return violations

def count_nurses_per_shift_violations(nurse_shifts_dict):
    total_per_shift = [sum(shift) for shift in zip(*nurse_shifts_dict.values())]
    violations = sum(max(0, total - shift_max[i % shift_per_day]) + max(0, shift_min[i % shift_per_day] - total) 
                     for i, total in enumerate(total_per_shift))
    return violations

def count_shift_preference_violations(nurse_shifts_dict):
    violations = 0
    for i, pref in enumerate(shift_preference):
        expanded_pref = pref * (shifts_per_week // shift_per_day)
        violations += sum(1 for p, s in zip(expanded_pref, nurse_shifts_dict[nurses[i]]) if p == 0 and s == 1)
    return violations

def get_cost(schedule):
    nurse_shifts_dict = get_nurse_shifts(schedule)
    hard_violations = (count_consecutive_shift_violations(nurse_shifts_dict) + 
                       count_shifts_per_week_violations(nurse_shifts_dict) + 
                       count_nurses_per_shift_violations(nurse_shifts_dict))
    soft_violations = count_shift_preference_violations(nurse_shifts_dict)
    return hard_constraint_penalty * hard_violations + soft_violations

np.random.seed(42)
random_solution = np.random.randint(2, size=len(nurses) * shifts_per_week * weeks)

print("Random Solution =", random_solution)
print("Total Cost =", get_cost(random_solution))
