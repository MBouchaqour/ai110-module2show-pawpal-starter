# PawPal+ Project Reflection

## 1. System Design

### Refined UML Design to Include Add Methods

#### Owner
- **Attributes**:
  - `Owner_id`: Unique identifier for each owner.
  - `Full name`: The full name of the pet owner.
  - `Address`: The physical address of the owner.
  - `Preferences`: Preferences for pet care (e.g., preferred times for tasks).
  - `Available time`: The time slots available for pet care tasks.
  - `Number of pets`: The total number of pets owned by the owner.
- **Methods**:
  - `add_owner(owner_id, full_name, address)`: Adds a new owner with the specified details.
  - `add_preferences(preferences)`: Adds new preferences for the owner.
  - `add_available_time(time_slots)`: Adds available time slots for the owner.
  - `update_preferences(preferences)`: Updates the owner's preferences.
  - `update_available_time(time_slots)`: Updates the owner's available time slots.
  - `get_preferences()`: Retrieves the owner's preferences.

#### Pet
- **Attributes**:
  - `pet_code`: Unique identifier for the pet.
  - `name`: The name of the pet.
  - `type`: The type of pet (e.g., dog, cat).
  - `age`: The age of the pet.
  - `comment`: Additional information the owner wants to share about the pet.
  - `owner_id`: Links the pet to its owner (foreign key).

- **Methods**:
  - `add_pet(pet_code, name, type)`: Adds a new pet with the specified details.
  - `update_pet_info(pet_code, name=None, type=None, age=None, comment=None)`: Updates the pet's information. Allows partial updates by making parameters optional.
  - `validate_pet_info()`: Ensures that all pet information is complete and valid.

#### Task
- **Attributes**:
  - `task_id`: Unique identifier for the task.
  - `name`: The name of the task (e.g., feeding, walking).
  - `duration`: The time required to complete the task (in minutes).
  - `priority`: The priority level of the task (e.g., high, medium, low).
  - `type`: The type of task (e.g., grooming, enrichment).
  - `owner_id`: Links the task to the owner responsible for it (foreign key).
  - `pet_id`: Links the task to the specific pet it applies to (foreign key).

- **Methods**:
  - `add_task(task_id, name, duration, priority, type, owner_id, pet_id)`: Adds a new task with the specified details.
  - `edit_task(task_id, name=None, duration=None, priority=None, type=None, pet_id=None)`: Edits the task details. Allows partial updates by making parameters optional.
  - `mark_completed(task_id)`: Marks the task as completed.
  - `validate_task()`: Ensures that the task duration is positive and priority is within a valid range.

#### Schedule
- **Attributes**:
  - `schedule_id`: Unique identifier for the schedule.
  - `tasks`: A list of tasks to be completed.
  - `constraints`: Constraints such as time availability, task priorities, and owner preferences.
  - `owner_id`: Links the schedule to the owner responsible for it (foreign key).
  - `pet_id`: Links the schedule to the specific pet it applies to (foreign key).

- **Methods**:
  - `add_task_to_schedule(schedule_id, task, pet_id)`: Adds a new task to the schedule for a specific pet.
  - `generate_schedule(schedule_id, pet_id)`: Creates a daily schedule based on tasks and constraints for a specific pet.
  - `explain_schedule(schedule_id, pet_id)`: Provides reasoning for the generated schedule for a specific pet.
  - `resolve_conflicts(schedule_id, pet_id)`: Handles overlapping tasks and prioritizes based on rules for a specific pet.
  - `handle_dynamic_updates(schedule_id, updated_task, pet_id)`: Updates the schedule dynamically when tasks or constraints change for a specific pet.

### Relationships
- **Owner** has one or more **Pets**.
- **Owner** manages **Tasks** for their **Pets**.
- **Schedule** is generated based on the **Tasks** and the **Owner's** constraints.



**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
