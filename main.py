from pawpal_system import Owner, Pet, Task, Schedule

# Temporary testing ground
if __name__ == "__main__":
    # Create an owner
    owner = Owner(
        owner_id="O001",
        full_name="Alice Johnson",
        address="456 Pet Street",
        preferences="Evening walks",
        available_time="08:00-20:00",
        number_of_pets=2
    )

    # Create pets
    pet1 = Pet(
        pet_code="P001",
        name="Charlie",
        pet_type="DOG",
        age=4,
        comment="Energetic and loves running",
        owner_id="O001"
    )

    pet2 = Pet(
        pet_code="P002",
        name="Luna",
        pet_type="CAT",
        age=3,
        comment="Calm and loves cuddles",
        owner_id="O001"
    )

    # Create tasks out of order and with start_time
    task1 = Task(
        task_id="T001",
        name="Morning Walk",
        duration=30,
        priority="HIGH",
        task_type="WALK",
        owner_id="O001",
        pet_id="P001",
        start_time="08:30"
    )

    task2 = Task(
        task_id="T002",
        name="Feed Charlie",
        duration=15,
        priority="MEDIUM",
        task_type="FEED",
        owner_id="O001",
        pet_id="P001",
        start_time="07:00"
    )

    task3 = Task(
        task_id="T003",
        name="Groom Luna",
        duration=20,
        priority="LOW",
        task_type="GROOMING",
        owner_id="O001",
        pet_id="P002",
        start_time="09:15"
    )

    # Add two tasks at the same time to test conflict detection
    conflict_task1 = Task(
        task_id="T004",
        name="Vet Visit",
        duration=60,
        priority="HIGH",
        task_type="MEDICAL",
        owner_id="O001",
        pet_id="P001",
        start_time="10:00",
        due_date="2026-03-29"
    )
    conflict_task2 = Task(
        task_id="T005",
        name="Playtime",
        duration=30,
        priority="LOW",
        task_type="PLAY",
        owner_id="O001",
        pet_id="P002",
        start_time="10:00",
        due_date="2026-03-29"
    )

    schedule = Schedule(
        schedule_id="S001",
        owner_id="O001",
        pet_id="P001",
        tasks=[task3, task1, task2, conflict_task1, conflict_task2],  # Out of order, with conflict
        constraints={"max_duration": 120}
    )

    print("Tasks before sorting by time:")
    for t in schedule.tasks:
        print(f"{t.name} at {t.start_time}")

    # Sort by time
    schedule.sort_by_time()
    print("\nTasks after sorting by time:")
    for t in schedule.tasks:
        print(f"{t.name} at {t.start_time}")

    # Lightweight conflict detection: print warning if conflicts found
    conflicts = schedule.detect_time_conflicts()
    if conflicts:
        print("\nWARNING: The following tasks are scheduled at the same time:")
        for conflict_group in conflicts:
            conflict_names = ", ".join(f"{t.name} (Pet: {t.pet_id})" for t in conflict_group)
            print(f"  - {conflict_names} at {conflict_group[0].start_time} on {conflict_group[0].due_date}")
    else:
        print("\nNo scheduling conflicts detected.")

    # Mark one task as complete
    schedule.tasks[0].mark_complete()

    # Filtering by completion
    completed_tasks = schedule.filter_tasks_by_completion(completed=True)
    incomplete_tasks = schedule.filter_tasks_by_completion(completed=False)
    print("\nCompleted tasks:")
    for t in completed_tasks:
        print(f"{t.name} at {t.start_time}")
    print("\nIncomplete tasks:")
    for t in incomplete_tasks:
        print(f"{t.name} at {t.start_time}")

    # Filtering by pet name
    pet_store = [pet1, pet2]
    luna_tasks = schedule.filter_tasks_by_pet_name("Luna", pet_store=pet_store)
    print("\nTasks for Luna:")
    for t in luna_tasks:
        print(f"{t.name} at {t.start_time}")