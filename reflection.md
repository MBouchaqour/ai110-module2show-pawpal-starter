# PawPal+ Project Reflection

## 1. System Design

### Refined UML Design to Include Add Methods

#### Owner
- **Attributes**:
  - `owner_id`: Unique identifier for each owner.
  - `full_name`: The full name of the pet owner.
  - `address`: The physical address of the owner.
  - `preferences`: Preferences for pet care (e.g., preferred times for tasks).
  - `available_time`: The time slots available for pet care tasks.
  - `number_of_pets`: The total number of pets owned by the owner.
- **Methods**:
  - `add_pet(pet)`: Validates and registers a Pet to the global PET_STORE.
  - `get_pets()`: Retrieves all pets linked to this owner.
  - `get_schedules()`: Retrieves all schedules linked to this owner.

#### Pet
- **Attributes**:
  - `pet_code`: Unique identifier for the pet.
  - `name`: The name of the pet.
  - `pet_type`: The type of pet (e.g., DOG, CAT).
  - `age`: The age of the pet.
  - `comment`: Additional notes about the pet.
  - `owner_id`: Links the pet to its owner (foreign key).
- **Methods**:
  - `add_task(task)`: Appends a Task to the pet's task list.
  - `update_pet_info(...)`: Updates non-None fields on the pet.
  - `validate_pet_info()`: Ensures pet data is complete and valid.

#### Task
- **Attributes**:
  - `task_id`: Unique identifier for the task.
  - `name`: The name of the task.
  - `duration`: Time required in minutes.
  - `priority`: HIGH, MEDIUM, or LOW.
  - `task_type`: Category of task (WALK, FEED, MEDICATION, etc.).
  - `owner_id`: Links the task to the owner (foreign key).
  - `pet_id`: Links the task to the pet (foreign key).
  - `completed`: Boolean flag for completion status.
  - `start_time`: Preferred start time in HH:MM format.
  - `recurrence`: none, daily, or weekly.
- **Methods**:
  - `validate_task()`: Checks duration, priority, and time format.
  - `mark_complete(schedule)`: Marks done and creates next recurrence if needed.
  - `edit_task(...)`: Updates non-None fields on the task.

#### Schedule
- **Attributes**:
  - `schedule_id`: Unique identifier for the schedule.
  - `owner_id`: Links schedule to owner (foreign key).
  - `pet_id`: Links schedule to pet (foreign key).
  - `tasks`: Ordered list of Task objects.
  - `constraints`: Dictionary of scheduling rules.
- **Methods**:
  - `generate_schedule()`: Sorts tasks by priority then duration.
  - `sort_by_time()`: Orders tasks chronologically by start_time.
  - `explain_schedule()`: Returns a human-readable summary.
  - `detect_time_conflicts()`: Flags tasks sharing the same start_time.
  - `resolve_conflicts()`: Adjusts durations of overlapping tasks.

### Relationships
- **Owner** has one or more **Pets**.
- **Owner** manages **Tasks** for their **Pets**.
- **Schedule** is generated based on **Tasks** and the **Owner's** constraints.

### b. Design Changes

Yes, the design changed significantly during implementation.

The most important change was how `Owner` and `Pet` are connected. In the original UML, `Pet` had its own `add_pet()` instance method, which made no sense architecturally — a pet object should not register itself. During implementation this was refactored so that `Owner.add_pet(pet)` is responsible for registering a pet into the global `PET_STORE`, which is the correct pattern. The `Pet` class was also given a `tasks` list and an `add_task()` method so pets could own their tasks directly rather than everything being managed through foreign key strings alone.

A second change was adding `PRIORITY_ORDER = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}` as a global map. The original `generate_schedule()` sorted by the priority string directly, which sorted alphabetically and placed LOW tasks first. Catching this required understanding what the code was actually doing versus what it was intended to do.

---

## 2. Scheduling Logic and Tradeoffs

### a. Constraints and Priorities

The scheduler considers three constraints:

1. **Priority** — HIGH tasks are always scheduled before MEDIUM and LOW tasks using a numeric map to avoid incorrect alphabetical sorting.
2. **Duration** — Within the same priority level, shorter tasks are scheduled first to maximise the number of tasks that fit within the owner's available window.
3. **Start time** — Tasks with an explicit `start_time` are sorted chronologically after priority ordering, so time-sensitive tasks like medication appear at the right point in the day.

Priority was treated as the most important constraint because missing a HIGH priority task (such as medication) has real consequences for the pet's wellbeing, while a LOW priority task like enrichment can be deferred without harm.

### b. Tradeoffs

The scheduler uses exact `start_time` matching to detect conflicts rather than checking for overlapping durations. This means two tasks that overlap in time but do not share the exact same start minute will not trigger a conflict warning.

This tradeoff is reasonable for a household pet care app because most tasks are sequential by nature — a walk follows a feeding, not overlapping with it. The simpler detection logic keeps the code fast and easy to understand, and full overlap detection can be added in a future iteration without redesigning the scheduler.

---

## 3. AI Collaboration

### a. How AI Was Used

AI tools were used across every phase of this project:

- **Design phase**: Used to generate the initial UML class diagram and discuss the relationships between Owner, Pet, Task, and Schedule before writing any code.
- **Scaffolding phase**: Agent Mode in VS Code was used to flesh out all method stubs in `pawpal_system.py` from detailed `# TODO` comments, saving significant time on boilerplate.
- **Debugging phase**: AI identified three structural bugs Copilot had introduced — the `add_pet` method placed outside the `Owner` class, `Schedule` fields declared after methods inside the dataclass, and reversed priority sorting.
- **UI wiring phase**: AI explained how `st.session_state` works as a persistent vault and rewrote the Streamlit button handlers to call real class methods instead of manipulating plain dictionaries.

The most helpful prompts were specific and file-scoped, for example: *"implement all TODO methods in #file:pawpal_system.py following the contract in each comment"* rather than broad questions like *"how do I build a scheduler?"*

### b. Judgment and Verification

The most important moment of human judgment came when Copilot generated the `generate_schedule()` method sorting tasks by `t.priority` as a plain string. The code looked correct at first glance, but testing revealed that `"HIGH"` sorts after `"LOW"` alphabetically, meaning the lowest priority tasks were being scheduled first — the opposite of the intended behaviour.

The suggestion was rejected and replaced with a numeric priority map:
```python
PRIORITY_ORDER = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
self.tasks.sort(key=lambda t: (-PRIORITY_ORDER.get(t.priority, 0), t.duration))
```

This was verified by manually tracing through a small list of tasks with mixed priorities and confirming HIGH tasks appeared first in the output. AI generated plausible-looking code, but only human review caught the logical error.

### c. Separate Chat Sessions Per Phase

Using separate chat sessions for design, implementation, and debugging kept each conversation focused on one concern. The design session stayed at the UML level without getting pulled into Streamlit syntax. The debugging session could reference the actual error messages without needing to re-explain the whole system. This mirrors how a real development team separates planning meetings from code reviews — mixing them produces noise and loses context.

---

## 4. Testing and Verification

### a. What Was Tested

- **Validation methods**: Confirmed that `validate_pet_info()` raises `ValueError` for negative age, empty name, and unrecognised pet type. Confirmed that `validate_task()` rejects zero duration and invalid priority strings.
- **Priority sorting**: Verified that `generate_schedule()` places HIGH priority tasks before MEDIUM and LOW after fixing the alphabetical sort bug.
- **Session state persistence**: Verified that the Owner and Pet objects survive Streamlit reruns by checking the vault status badge after each interaction.
- **Conflict detection**: Verified that `detect_time_conflicts()` correctly groups tasks sharing the same `start_time` and `due_date`.

These tests mattered because the scheduler's core promise is that important tasks run first. If priority sorting is wrong, the whole system produces misleading output regardless of how polished the UI looks.

### b. Confidence and Edge Cases

Confidence is moderate for the happy path — creating an owner, adding a pet, adding tasks, and generating a schedule all work correctly. Edge cases that would be tested next with more time:

- An owner with zero available hours — does the scheduler handle an empty time window gracefully?
- Two pets with tasks at the same time — does conflict detection work across pet boundaries?
- A recurring task being marked complete multiple times — does it create duplicate future instances?
- Very long tasks that exceed the owner's total available window — are they placed in `unscheduled` with a clear explanation?

---

## 5. Reflection

### a. What Went Well

The session state architecture worked cleanly. Storing `Owner`, `Pet`, `Schedule`, and tasks in the vault with the `if "key" not in st.session_state` pattern meant that data persisted correctly across all Streamlit reruns without any state management bugs. The separation between the backend classes in `pawpal_system.py` and the UI in `app.py` also made debugging straightforward — errors in the logic layer were isolated from the display layer.

### b. What Would Be Improved

The global `PET_STORE` and `SCHEDULE_STORE` lists are a shortcut that would not scale. In a real application these would be replaced with a proper database or at minimum a class-level registry on `Owner`. The current design means all pets from all owners share one flat list, which works for a single-user demo but breaks immediately with multiple owners.

The `Schedule` class also conflates too many responsibilities — it handles sorting, conflict detection, explanation, and constraint validation all in one place. A future iteration would extract a dedicated `Scheduler` service class that takes an `Owner` and returns a `Schedule`, keeping the `Schedule` class as a pure data container.

### c. Key Takeaway

The most important lesson from this project is that **AI is a powerful first-draft tool but a poor final-draft tool**. Copilot generated working-looking code quickly, but it introduced structural bugs (fields after methods in a dataclass), logical bugs (alphabetical priority sorting), and architectural oddities (a Pet registering itself) that required human review to catch.

Being the lead architect means defining the structure clearly before asking AI to fill it in, reviewing every suggestion against the intended design rather than just running it, and understanding that AI optimises for code that looks correct rather than code that is correct. The developer's job shifts from writing every line to asking the right questions, setting the right constraints, and verifying the output — which is a different skill but no less demanding than writing code from scratch.