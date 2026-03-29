# PawPal+ System Logic Layer

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class Owner:
    owner_id: str
    full_name: str
    address: str
    preferences: str
    available_time: str          # e.g. "07:00-22:00"
    number_of_pets: int

    def get_schedules(self):
        """Retrieve schedules associated with the owner."""
        # Placeholder: Replace with actual database or in-memory store lookup
        return [schedule for schedule in SCHEDULE_STORE if schedule.owner_id == self.owner_id]

    def get_pets(self):
        """Retrieve pets associated with the owner."""
        # Placeholder: Replace with actual database or in-memory store lookup
        return [pet for pet in PET_STORE if pet.owner_id == self.owner_id]


@dataclass
class Pet:
    pet_code: str
    name: str
    pet_type: str
    age: int
    comment: str
    owner_id: str                # FK → Owner.owner_id
    tasks: list = field(default_factory=list)  # Updated to use default_factory for mutable default
    species: str = ""  # Added to store pet species

    def add_pet(self, pet_code: str, name: str, pet_type: str):
        """Add a new pet to the pet store."""
        if not pet_code or not name:
            raise ValueError("Pet code and name cannot be empty.")
        if pet_type not in ["DOG", "CAT", "BIRD", "OTHER"]:
            raise ValueError("Invalid pet type.")
        PET_STORE.append(self)

    def update_pet_info(self, pet_code: str, name=None, pet_type=None, age=None, comment=None):
        """Update information for an existing pet."""
        if self.pet_code != pet_code:
            return
        if name:
            self.name = name
        if pet_type:
            self.pet_type = pet_type
        if age:
            self.age = age
        if comment:
            self.comment = comment

    def validate_pet_info(self):
        """Validate the pet's information for completeness and correctness."""
        if not self.pet_code or not self.name:
            raise ValueError("Pet code and name cannot be empty.")
        if self.age < 0:
            raise ValueError("Age cannot be negative.")
        if self.pet_type not in ["DOG", "CAT", "BIRD", "OTHER"]:
            raise ValueError("Invalid pet type.")

    def add_task(self, task):
        """Add a task to the pet's task list."""
        if not isinstance(task, Task):
            raise ValueError("Only Task objects can be added.")
        self.tasks.append(task)


@dataclass
class Task:
    task_id: str
    name: str
    duration: int                # minutes
    priority: str                # "HIGH" | "MEDIUM" | "LOW"
    task_type: str               # "WALK" | "FEED" | "MEDICATION" | "GROOMING" | etc.
    owner_id: str                # FK → Owner.owner_id
    pet_id: str                  # FK → Pet.pet_code
    completed: bool = False      # added — needed by mark_complete
    description: str = ""        # Added to store task description
    status: str = "incomplete"    # Added to track task status
    start_time: str = ""         # New: Format "HH:MM"
    recurrence: str = "none"      # New: "none", "daily", "weekly"
    due_date: str = ""           # New: ISO date string (YYYY-MM-DD)

    def add_task(self, task_id, name, duration, priority, task_type, owner_id, pet_id):
        """Add a new task with the specified details."""
        self.task_id = task_id
        self.name = name
        self.duration = duration
        self.priority = priority
        self.task_type = task_type
        self.owner_id = owner_id
        self.pet_id = pet_id
        self.validate_task()

    def edit_task(self, task_id, name=None, duration=None, priority=None, task_type=None, pet_id=None):
        """Edit the details of an existing task."""
        if self.task_id != task_id:
            return
        if name:
            self.name = name
        if duration:
            self.duration = duration
        if priority:
            self.priority = priority
        if task_type:
            self.task_type = task_type
        if pet_id:
            self.pet_id = pet_id

    def mark_complete(self, schedule=None):
        """
        Mark the task as complete. If the task is recurring (daily or weekly), automatically create
        a new instance for the next occurrence and add it to the provided schedule.
        The new instance will have its due_date set to the next day or week, as appropriate.
        """
        self.completed = True
        self.status = "complete"
        if schedule and self.recurrence in ("daily", "weekly"):
            from datetime import timedelta, date, datetime as dt
            # Determine the current due date (today if not set)
            if self.due_date:
                try:
                    current_due = dt.strptime(self.due_date, "%Y-%m-%d").date()
                except Exception:
                    current_due = date.today()
            else:
                current_due = date.today()
            # Calculate next due date
            if self.recurrence == "daily":
                next_due = current_due + timedelta(days=1)
            elif self.recurrence == "weekly":
                next_due = current_due + timedelta(weeks=1)
            else:
                next_due = current_due
            # For demo, just copy all fields and update task_id and due_date
            new_task_id = f"{self.task_id}_{self.recurrence}_next"
            new_task = Task(
                task_id=new_task_id,
                name=self.name,
                duration=self.duration,
                priority=self.priority,
                task_type=self.task_type,
                owner_id=self.owner_id,
                pet_id=self.pet_id,
                description=self.description,
                start_time=self.start_time,
                recurrence=self.recurrence,
                due_date=next_due.isoformat()
            )
            if schedule:
                schedule.add_task_to_schedule(new_task)

    def validate_task(self):
        """Validate the task's attributes for correctness."""
        if self.duration <= 0:
            raise ValueError("Duration must be greater than 0.")
        if self.priority not in ["HIGH", "MEDIUM", "LOW"]:
            raise ValueError("Invalid priority.")
        if not self.name:
            raise ValueError("Task name cannot be empty.")
        if self.start_time:
            try:
                datetime.strptime(self.start_time, "%H:%M")
            except ValueError:
                raise ValueError("start_time must be in 'HH:MM' format.")


@dataclass
class Schedule:

    def detect_time_conflicts(self):
        """
        Detect tasks that are scheduled at the same start_time and due_date for the same or different pets.
        Returns:
            List[List[Task]]: A list of lists, where each sublist contains tasks that conflict (i.e., share the same time).
        This lightweight strategy only checks for exact time matches, not overlapping durations.
        """
        conflicts = []
        # Build a mapping: (start_time, due_date) -> list of tasks
        time_map = {}
        for t in self.tasks:
            key = (t.start_time, t.due_date)
            if key not in time_map:
                time_map[key] = []
            time_map[key].append(t)
        # Find all keys with more than one task (conflict)
        for key, task_list in time_map.items():
            if len(task_list) > 1:
                conflicts.append(task_list)
        return conflicts

            def mark_task_complete(self, task_id: str):
                """
                Mark a task as complete by its task_id and handle recurrence if needed.
                If the task is recurring, a new instance for the next occurrence is automatically added.
                Args:
                    task_id (str): The ID of the task to mark as complete.
                """
                for t in self.tasks:
                    if t.task_id == task_id:
                        t.mark_complete(schedule=self)
                        break
        def filter_tasks_by_completion(self, completed: bool = True):
            """
            Return a list of tasks filtered by their completion status.
            Args:
                completed (bool): If True, return completed tasks; if False, return incomplete tasks.
            Returns:
                List[Task]: Filtered list of tasks.
            """
            return [t for t in self.tasks if t.completed == completed]

        def filter_tasks_by_pet_name(self, pet_name: str, pet_store=None):
            """
            Return a list of tasks for a given pet name.
            Args:
                pet_name (str): The name of the pet to filter tasks for.
                pet_store (list, optional): List of Pet objects to resolve pet_name to pet_id.
            Returns:
                List[Task]: Filtered list of tasks for the specified pet name.
            """
            if pet_store is None:
                # If no pet_store provided, cannot resolve pet_name to pet_id
                return []
            pet_ids = [pet.pet_code for pet in pet_store if pet.name == pet_name]
            return [t for t in self.tasks if t.pet_id in pet_ids]
    # ⚠️  FIX APPLIED: non-default fields moved above fields with defaults.
    # Original order caused TypeError: non-default argument after default argument.
    schedule_id: str
    owner_id: str                # FK → Owner.owner_id
    pet_id: str                  # FK → Pet.pet_code
    tasks: List[Task] = field(default_factory=list)
    constraints: dict = field(default_factory=dict)
    def sort_by_time(self):
        """
        Sort tasks in the schedule by their start_time attribute (in HH:MM format).
        Tasks without a start_time are sorted to the beginning.
        """
        self.tasks.sort(key=lambda t: datetime.strptime(t.start_time, "%H:%M") if t.start_time else datetime.min)

    def add_task_to_schedule(self, task: Task):
        """Add a task to the schedule."""
        self.tasks.append(task)

    def remove_task_from_schedule(self, task_id: str):
        """Remove a task from the schedule by its ID."""
        self.tasks = [t for t in self.tasks if t.task_id != task_id]

    def generate_schedule(self):
        """Generate a schedule by sorting tasks based on priority and duration."""
        self.tasks.sort(key=lambda t: (t.priority, t.duration))
        return self.tasks

    def explain_schedule(self):
        """Provide a textual explanation of the schedule."""
        return "\n".join([f"Task {t.name} ({t.priority}) for {t.duration} minutes" for t in self.tasks])

    def resolve_conflicts(self):
        """Resolve conflicts in the schedule by adjusting task durations."""
        for i in range(len(self.tasks) - 1):
            current_task = self.tasks[i]
            next_task = self.tasks[i + 1]
            if current_task.duration > next_task.duration:
                next_task.duration += 10  # Example conflict resolution

    def handle_dynamic_updates(self, updated_task):
        """Handle updates to tasks dynamically and resolve conflicts."""
        for i, task in enumerate(self.tasks):
            if task.task_id == updated_task.task_id:
                self.tasks[i] = updated_task
        self.resolve_conflicts()

    def add_constraint(self, key: str, value):
        """Add a constraint to the schedule."""
        self.constraints[key] = value

    def validate_constraints(self):
        """Validate the constraints for correctness."""
        for key, value in self.constraints.items():
            if key == "max_duration" and value <= 0:
                raise ValueError("Max duration must be greater than 0.")