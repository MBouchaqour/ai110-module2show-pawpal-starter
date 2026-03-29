classDiagram
    class Owner {
        +string owner_id
        +string full_name
        +string address
        +string preferences
        +string available_time
        +int number_of_pets
        +add_owner(owner_id, full_name, address)
        +add_preferences(preferences)
        +add_available_time(time_slots)
        +update_preferences(preferences)
        +update_available_time(time_slots)
        +get_preferences()
    }

    class Pet {
        +string pet_code
        +string name
        +string type
        +int age
        +string comment
        +string owner_id
        +add_pet(pet_code, name, type)
        +update_pet_info(pet_code, name, type, age, comment)
        +validate_pet_info()
    }

    class Task {
        +string task_id
        +string name
        +int duration
        +string priority
        +string type
        +string owner_id
        +string pet_id
        +add_task(task_id, name, duration, priority, type, owner_id, pet_id)
        +edit_task(task_id, name, duration, priority, type, pet_id)
        +mark_completed(task_id)
        +validate_task()
    }

    class Schedule {
        +string schedule_id
        +list tasks
        +string constraints
        +string owner_id
        +string pet_id
        +add_task_to_schedule(schedule_id, task, pet_id)
        +generate_schedule(schedule_id, pet_id)
        +explain_schedule(schedule_id, pet_id)
        +resolve_conflicts(schedule_id, pet_id)
        +handle_dynamic_updates(schedule_id, updated_task, pet_id)
    }

    Owner "1" --> "*" Pet
    Owner "1" --> "*" Task
    Task "*" --> "1" Pet
    Schedule "1" --> "*" Task
    Schedule "1" --> "*" Pet