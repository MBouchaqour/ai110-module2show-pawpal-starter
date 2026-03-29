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