import pytest
from pawpal_system import Owner, Pet, Task, Schedule

def test_owner_creation():
    owner = Owner(
        owner_id="O001",
        full_name="Alice Johnson",
        address="456 Pet Street",
        preferences="Evening walks",
        available_time="08:00-20:00",
        number_of_pets=2
    )
    assert owner.owner_id == "O001"
    assert owner.full_name == "Alice Johnson"

def test_pet_creation():
    pet = Pet(
        pet_code="P001",
        name="Charlie",
        pet_type="DOG",
        age=4,
        comment="Energetic and loves running",
        owner_id="O001"
    )
    assert pet.pet_code == "P001"
    assert pet.name == "Charlie"

def test_task_creation():
    task = Task(
        task_id="T001",
        name="Morning Walk",
        duration=30,
        priority="HIGH",
        task_type="WALK",
        owner_id="O001",
        pet_id="P001"
    )
    assert task.task_id == "T001"
    assert task.priority == "HIGH"

def test_schedule():
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
    schedule = Schedule(
        schedule_id="S001",
        owner_id="O001",
        pet_id="P001",
        tasks=[task1, task2],
        constraints={"max_duration": 120}
    )
    schedule.generate_schedule()
    assert len(schedule.tasks) == 2
    assert schedule.tasks[0].priority == "HIGH"

# Updated test to include required arguments for Task
def test_task_completion():
    task = Task(task_id="1", name="Feed the dog", description="Feed the dog in the morning", status="incomplete", duration=30, priority="HIGH", task_type="FEED", owner_id="owner1", pet_id="pet1")
    task.mark_complete()
    assert task.status == "complete", "Task status should be 'complete' after calling mark_complete()"

# Updated test to include required arguments for Pet
def test_task_addition():
    pet = Pet(pet_code="pet1", name="Buddy", species="Dog", pet_type="DOG", age=3, comment="Friendly dog", owner_id="owner1")
    initial_task_count = len(pet.tasks)
    new_task = Task(task_id="2", name="Walk the dog", description="Take Buddy for a walk", duration=20, priority="MEDIUM", task_type="WALK", owner_id="owner1", pet_id="pet1")
    pet.add_task(new_task)
    assert len(pet.tasks) == initial_task_count + 1, "Adding a task should increase the pet's task count by 1"

    # --- Happy Path: Sorting tasks by time ---
    def test_schedule_sort_by_time():
        t1 = Task(task_id="t1", name="Feed", duration=10, priority="LOW", task_type="FEED", owner_id="o1", pet_id="p1", start_time="09:00")
        t2 = Task(task_id="t2", name="Walk", duration=20, priority="HIGH", task_type="WALK", owner_id="o1", pet_id="p1", start_time="08:00")
        sched = Schedule(schedule_id="s1", owner_id="o1", pet_id="p1", tasks=[t1, t2])
        sched.sort_by_time()
        assert sched.tasks[0].start_time == "08:00"
        assert sched.tasks[1].start_time == "09:00"

    # --- Happy Path: Recurring task creates new instance ---
    def test_recurring_task_completion_creates_new_instance():
        sched = Schedule(schedule_id="s1", owner_id="o1", pet_id="p1", tasks=[])
        t = Task(task_id="t1", name="Feed", duration=10, priority="LOW", task_type="FEED", owner_id="o1", pet_id="p1", recurrence="daily", due_date="2026-03-29")
        sched.add_task_to_schedule(t)
        t.mark_complete(schedule=sched)
        # Should have 2 tasks: original (complete) and new (incomplete, next day)
        assert len(sched.tasks) == 2
        new_task = [task for task in sched.tasks if task.task_id != "t1"][0]
        assert new_task.due_date == "2026-03-30"
        assert new_task.recurrence == "daily"
        assert new_task.status == "incomplete"

    # --- Happy Path: Filtering by completion and pet name ---
    def test_filter_tasks_by_completion_and_pet_name():
        t1 = Task(task_id="t1", name="Feed", duration=10, priority="LOW", task_type="FEED", owner_id="o1", pet_id="p1", completed=True)
        t2 = Task(task_id="t2", name="Walk", duration=20, priority="HIGH", task_type="WALK", owner_id="o1", pet_id="p1", completed=False)
        sched = Schedule(schedule_id="s1", owner_id="o1", pet_id="p1", tasks=[t1, t2])
        completed = sched.filter_tasks_by_completion(completed=True)
        incomplete = sched.filter_tasks_by_completion(completed=False)
        assert t1 in completed
        assert t2 in incomplete
        # Pet name filter
        pet = Pet(pet_code="p1", name="Buddy", pet_type="DOG", age=2, comment="", owner_id="o1")
        pet_store = [pet]
        filtered = sched.filter_tasks_by_pet_name("Buddy", pet_store=pet_store)
        assert t1 in filtered and t2 in filtered

    # --- Edge Case: Pet with no tasks ---
    def test_pet_with_no_tasks():
        pet = Pet(pet_code="p2", name="NoTasks", pet_type="CAT", age=1, comment="", owner_id="o1")
        assert pet.tasks == []

    # --- Edge Case: Two tasks at the exact same time ---
    def test_detect_time_conflicts():
        t1 = Task(task_id="t1", name="Feed", duration=10, priority="LOW", task_type="FEED", owner_id="o1", pet_id="p1", start_time="08:00", due_date="2026-03-29")
        t2 = Task(task_id="t2", name="Walk", duration=20, priority="HIGH", task_type="WALK", owner_id="o1", pet_id="p2", start_time="08:00", due_date="2026-03-29")
        sched = Schedule(schedule_id="s1", owner_id="o1", pet_id="p1", tasks=[t1, t2])
        conflicts = sched.detect_time_conflicts()
        assert len(conflicts) == 1
        assert t1 in conflicts[0] and t2 in conflicts[0]

    # --- Edge Case: Task with invalid time ---
    import pytest
    def test_task_with_invalid_time():
        with pytest.raises(ValueError):
            Task(task_id="t1", name="Feed", duration=10, priority="LOW", task_type="FEED", owner_id="o1", pet_id="p1", start_time="25:00")

    # --- Edge Case: Marking recurring task complete multiple times ---
    def test_recurring_task_mark_complete_multiple_times():
        sched = Schedule(schedule_id="s1", owner_id="o1", pet_id="p1", tasks=[])
        t = Task(task_id="t1", name="Feed", duration=10, priority="LOW", task_type="FEED", owner_id="o1", pet_id="p1", recurrence="daily", due_date="2026-03-29")
        sched.add_task_to_schedule(t)
        t.mark_complete(schedule=sched)
        t.mark_complete(schedule=sched)
        # Only one new instance per completion, so should not duplicate
        assert len([task for task in sched.tasks if task.task_id.startswith("t1_daily_next")]) <= 1

    # --- Edge Case: Filtering for non-existent pet or status ---
    def test_filter_nonexistent_pet_or_status():
        t1 = Task(task_id="t1", name="Feed", duration=10, priority="LOW", task_type="FEED", owner_id="o1", pet_id="p1", completed=True)
        sched = Schedule(schedule_id="s1", owner_id="o1", pet_id="p1", tasks=[t1])
        # No pet with this name
        pet_store = [Pet(pet_code="p1", name="Buddy", pet_type="DOG", age=2, comment="", owner_id="o1")]
        filtered = sched.filter_tasks_by_pet_name("Ghost", pet_store=pet_store)
        assert filtered == []
        # No incomplete tasks
        incomplete = sched.filter_tasks_by_completion(completed=False)
        assert incomplete == []

    # --- Edge Case: Task with due date in the past ---
    def test_task_with_past_due_date():
        import datetime
        yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
        t = Task(task_id="t1", name="Feed", duration=10, priority="LOW", task_type="FEED", owner_id="o1", pet_id="p1", due_date=yesterday)
        assert t.due_date == yesterday

    # --- Edge Case: Tasks with same time but different priorities ---
    def test_sort_same_time_different_priority():
        t1 = Task(task_id="t1", name="Feed", duration=10, priority="LOW", task_type="FEED", owner_id="o1", pet_id="p1", start_time="08:00")
        t2 = Task(task_id="t2", name="Walk", duration=20, priority="HIGH", task_type="WALK", owner_id="o1", pet_id="p1", start_time="08:00")
        sched = Schedule(schedule_id="s1", owner_id="o1", pet_id="p1", tasks=[t1, t2])
        sched.tasks.sort(key=lambda t: (t.start_time, t.priority))
        assert sched.tasks[0].priority == "HIGH"