def analyze_runs(nums):
    if not nums:
        return {
            "longest_increasing_run": 0,
            "longest_decreasing_run": 0,
            "num_increasing_runs": 0,
            "num_decreasing_runs": 0,
            "longest_run_values": []
        }

    # Initialize state
    current_run = [nums[0]]
    direction = None  # "inc", "dec"
    
    longest_increasing = 0
    longest_decreasing = 0
    num_increasing = 0
    num_decreasing = 0
    longest_run_values = []

    def finalize_run(run, direction):
        nonlocal longest_increasing, longest_decreasing
        nonlocal num_increasing, num_decreasing, longest_run_values

        length = len(run)

        if direction == "inc":
            num_increasing += 1
            if length > longest_increasing:
                longest_increasing = length
                longest_run_values = run[:]

        elif direction == "dec":
            num_decreasing += 1
            if length > longest_decreasing:
                longest_decreasing = length
                longest_run_values = run[:]

    # Traverse list
    for i in range(1, len(nums)):
        prev = nums[i - 1]
        curr = nums[i]

        if curr > prev:
            if direction == "dec":
                finalize_run(current_run, "dec")
                current_run = [prev]
            direction = "inc"
            current_run.append(curr)

        elif curr < prev:
            if direction == "inc":
                finalize_run(current_run, "inc")
                current_run = [prev]
            direction = "dec"
            current_run.append(curr)

        else:
            # equal → break run
            if direction == "inc":
                finalize_run(current_run, "inc")
            elif direction == "dec":
                finalize_run(current_run, "dec")

            current_run = [curr]
            direction = None

    # finalize last run
    if direction == "inc":
        finalize_run(current_run, "inc")
    elif direction == "dec":
        finalize_run(current_run, "dec")

    return {
        "longest_increasing_run": longest_increasing,
        "longest_decreasing_run": longest_decreasing,
        "num_increasing_runs": num_increasing,
        "num_decreasing_runs": num_decreasing,
        "longest_run_values": longest_run_values
    }


# ---------------- MENU SYSTEM ---------------- #

while True:
    print("\n=== RUN ANALYZER MENU ===")
    print("Enter a list of integers separated by commas")
    
    raw_input_list = input("List (e.g. 3,5,7,2,1,4): ")

    try:
        nums = [int(x.strip()) for x in raw_input_list.split(",") if x.strip() != ""]
    except ValueError:
        print("Invalid input. Please enter integers only.")
        continue

    result = analyze_runs(nums)

    print("\nRESULT:")
    for key, value in result.items():
        print(f"{key}: {value}")

    choice = input("\nPress 'c' to continue or 'q' to quit: ").lower()

    if choice == "q":
        print("Exiting program...")
        break