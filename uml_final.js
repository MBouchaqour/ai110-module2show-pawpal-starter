classDiagram
    class Owner {
        +string owner_id
        +string full_name
        +string address
        +string preferences
        +string available_time
        +int number_of_pets
        +get_pets()
        +get_schedules()
    }

    class Pet {
        +string pet_code
        +string name
        +string pet_type
        +string species
        +int age
        +string comment
        +string owner_id
        +list tasks
        +add_pet(pet: Pet)
        +update_pet_info(...)
        +validate_pet_info()
        +add_task(task: Task)
    }

    class Task {
        +string task_id
        +string name
        +int duration
        +string priority
        +string task_type
        +string owner_id
        +string pet_id
        +bool completed
        +string status
        +string start_time
        +string recurrence
        +string due_date
        +string description
        +add_task(...)
        +edit_task(...)
        +mark_complete(schedule=None)
        +validate_task()
    }

    class Schedule {
        +string schedule_id
        +string owner_id
        +string pet_id
        +List~Task~ tasks
        +dict constraints
        +add_task_to_schedule(task: Task)
        +remove_task_from_schedule(task_id: str)
        +generate_schedule()
        +sort_by_time()
        +detect_time_conflicts()
        +filter_tasks_by_completion(completed: bool)
        +filter_tasks_by_pet_name(pet_name: str, pet_store: list)
        +explain_schedule()
        +resolve_conflicts()
        +handle_dynamic_updates(updated_task: Task)
        +add_constraint(key: str, value)
        +validate_constraints()
    }

    Owner "1" --> "*" Pet
    Pet "1" --> "*" Task
    Schedule "1" --> "*" Task
    Schedule "1" --> "1" Owner
    Schedule "1" --> "1" Pet
