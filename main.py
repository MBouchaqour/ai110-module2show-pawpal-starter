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

    # Create tasks
    task1 = Task(
        task_id="T001",
        name="Morning Walk",
        duration=30,
        priority="HIGH",
        task_type="WALK",
        owner_id="O001",
        pet_id="P001"
    )

    task2 = Task(
        task_id="T002",
        name="Feed Charlie",
        duration=15,
        priority="MEDIUM",
        task_type="FEED",
        owner_id="O001",
        pet_id="P001"
    )

    task3 = Task(
        task_id="T003",
        name="Groom Luna",
        duration=20,
        priority="LOW",
        task_type="GROOMING",
        owner_id="O001",
        pet_id="P002"
    )

    # Create a schedule
    schedule = Schedule(
        schedule_id="S001",
        owner_id="O001",
        pet_id="P001",
        tasks=[task1, task2, task3],
        constraints={"max_duration": 120}
    )

    # Generate and print today's schedule
    schedule.generate_schedule()
    print("Today's Schedule:")
    print(schedule.explain_schedule())