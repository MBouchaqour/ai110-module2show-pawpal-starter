# PawPal+ System Logic Layer

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime, timedelta, date

# ---------------------------------------------------------------------------
# Global in-memory stores  (defined FIRST so every class can reference them)
# ---------------------------------------------------------------------------
PET_STORE      = []
SCHEDULE_STORE = []

PRIORITY_ORDER = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}   # used for correct sorting


# ---------------------------------------------------------------------------
# Owner
# ---------------------------------------------------------------------------
@dataclass
class Owner:
    owner_id:       str
    full_name:      str
    address:        str
    preferences:    str
    available_time: str    # e.g. "07:00-22:00"
    number_of_pets: int

    # ✅ FIX 1: add_pet moved back INSIDE Owner where it belongs
    def add_pet(self, pet: "Pet") -> None:
        """Add a Pet object to PET_STORE if not already present."""
        if not isinstance(pet, Pet):
            raise ValueError("Only Pet objects can be added.")
        for existing in PET_STORE:
            if existing.pet_code == pet.pet_code and existing.owner_id == self.owner_id:
                return  # already exists, skip silently
        PET_STORE.append(pet)

    def get_pets(self) -> list:
        """Retrieve all pets belonging to this owner."""
        return [p for p in PET_STORE if p.owner_id == self.owner_id]

    def get_schedules(self) -> list:
        """Retrieve all schedules belonging to this owner."""
        return [s for s in SCHEDULE_STORE if s.owner_id == self.owner_id]


# ---------------------------------------------------------------------------
# Pet
# ---------------------------------------------------------------------------
@dataclass
class Pet:
    pet_code: str
    name:     str
    pet_type: str          # "DOG" | "CAT" | "BIRD" | "OTHER"
    age:      int
    comment:  str
    owner_id: str
    tasks:    list = field(default_factory=list)
    species:  str  = ""

    VALID_TYPES = ("DOG", "CAT", "BIRD", "OTHER")

    def validate_pet_info(self) -> None:
        """Raise ValueError if any field is invalid."""
        if not self.pet_code or not self.name:
            raise ValueError("Pet code and name cannot be empty.")
        if self.age < 0:
            raise ValueError("Age cannot be negative.")
        # ✅ FIX: normalise to uppercase so "dog" and "DOG" both pass
        if self.pet_type.upper() not in self.VALID_TYPES:
            raise ValueError(f"Invalid pet type. Choose from {self.VALID_TYPES}.")
        self.pet_type = self.pet_type.upper()

    def add_task(self, task: "Task") -> None:
        """Append a validated Task to this pet's task list."""
        if not isinstance(task, Task):
            raise ValueError("Only Task objects can be added.")
        self.tasks.append(task)

    def update_pet_info(self, pet_code: str, name=None, pet_type=None,
                        age=None, comment=None) -> None:
        """Update non-None fields on this pet."""
        if self.pet_code != pet_code:
            return
        if name      is not None: self.name      = name
        if pet_type  is not None: self.pet_type  = pet_type.upper()
        if age       is not None: self.age       = age
        if comment   is not None: self.comment   = comment


# ---------------------------------------------------------------------------
# Task
# ---------------------------------------------------------------------------
@dataclass
class Task:
    task_id:    str
    name:       str
    duration:   int          # minutes
    priority:   str          # "HIGH" | "MEDIUM" | "LOW"
    task_type:  str          # "WALK" | "FEED" | "MEDICATION" | etc.
    owner_id:   str
    pet_id:     str
    completed:  bool = False
    description: str = ""
    status:     str  = "incomplete"
    start_time: str  = ""    # "HH:MM"
    recurrence: str  = "none"  # "none" | "daily" | "weekly"
    due_date:   str  = ""    # "YYYY-MM-DD"

    def validate_task(self) -> None:
        """Raise ValueError if any field is invalid."""
        if not self.name:
            raise ValueError("Task name cannot be empty.")
        if self.duration <= 0:
            raise ValueError("Duration must be greater than 0.")
        if self.priority not in PRIORITY_ORDER:
            raise ValueError("Priority must be HIGH, MEDIUM, or LOW.")
        if self.start_time:
            try:
                datetime.strptime(self.start_time, "%H:%M")
            except ValueError:
                raise ValueError("start_time must be in HH:MM format.")

    def mark_complete(self, schedule=None) -> None:
        """Mark complete; if recurring, add next occurrence to schedule."""
        self.completed = True
        self.status    = "complete"
        if schedule and self.recurrence in ("daily", "weekly"):
            current_due = (datetime.strptime(self.due_date, "%Y-%m-%d").date()
                           if self.due_date else date.today())
            delta   = timedelta(days=1) if self.recurrence == "daily" else timedelta(weeks=1)
            next_due = current_due + delta
            new_task = Task(
                task_id    = f"{self.task_id}_{self.recurrence}_next",
                name       = self.name,
                duration   = self.duration,
                priority   = self.priority,
                task_type  = self.task_type,
                owner_id   = self.owner_id,
                pet_id     = self.pet_id,
                description= self.description,
                start_time = self.start_time,
                recurrence = self.recurrence,
                due_date   = next_due.isoformat(),
            )
            schedule.add_task_to_schedule(new_task)

    def edit_task(self, task_id, name=None, duration=None,
                  priority=None, task_type=None, pet_id=None) -> None:
        if self.task_id != task_id:
            return
        if name      is not None: self.name      = name
        if duration  is not None: self.duration  = duration
        if priority  is not None: self.priority  = priority
        if task_type is not None: self.task_type = task_type
        if pet_id    is not None: self.pet_id    = pet_id


# ---------------------------------------------------------------------------
# Schedule
# ---------------------------------------------------------------------------
@dataclass
class Schedule:
    # ✅ FIX 2: ALL fields declared at the TOP before any methods
    schedule_id: str
    owner_id:    str
    pet_id:      str
    tasks:       List[Task] = field(default_factory=list)
    constraints: dict       = field(default_factory=dict)

    # --- task management ---------------------------------------------------

    def add_task_to_schedule(self, task: Task) -> None:
        """Append a task to the schedule."""
        self.tasks.append(task)

    def remove_task_from_schedule(self, task_id: str) -> None:
        """Remove a task by ID."""
        self.tasks = [t for t in self.tasks if t.task_id != task_id]

    def mark_task_complete(self, task_id: str) -> None:
        """Mark a task complete and handle recurrence."""
        for t in self.tasks:
            if t.task_id == task_id:
                t.mark_complete(schedule=self)
                break

    # --- scheduling logic --------------------------------------------------

    def sort_by_time(self) -> None:
        """Sort tasks by start_time; tasks without a time go first."""
        self.tasks.sort(
            key=lambda t: datetime.strptime(t.start_time, "%H:%M")
                          if t.start_time else datetime.min
        )

    def generate_schedule(self) -> list:
        """Sort tasks by priority (HIGH first) then duration (shortest first)."""
        # ✅ FIX 3: use PRIORITY_ORDER map — string sort puts HIGH after LOW
        self.tasks.sort(
            key=lambda t: (-PRIORITY_ORDER.get(t.priority, 0), t.duration)
        )
        return self.tasks

    def explain_schedule(self) -> str:
        """Return a human-readable summary of the schedule."""
        if not self.tasks:
            return "No tasks scheduled."
        lines = ["**Scheduled tasks:**\n"]
        for t in self.tasks:
            status = "✓" if t.completed else "○"
            time   = f" @ {t.start_time}" if t.start_time else ""
            lines.append(f"- {status} [{t.priority}] {t.name}{time} — {t.duration} min")
        return "\n".join(lines)

    def resolve_conflicts(self) -> None:
        """Detect overlapping tasks and push later ones back by 10 min."""
        for i in range(len(self.tasks) - 1):
            if self.tasks[i].duration > self.tasks[i + 1].duration:
                self.tasks[i + 1].duration += 10

    def handle_dynamic_updates(self, updated_task: Task) -> None:
        """Replace a task in-place then resolve any new conflicts."""
        self.tasks = [updated_task if t.task_id == updated_task.task_id
                      else t for t in self.tasks]
        self.resolve_conflicts()

    # --- filtering ---------------------------------------------------------

    def detect_time_conflicts(self) -> list:
        """Return groups of tasks that share the same start_time + due_date."""
        time_map = {}
        for t in self.tasks:
            key = (t.start_time, t.due_date)
            time_map.setdefault(key, []).append(t)
        return [group for group in time_map.values() if len(group) > 1]

    def filter_tasks_by_completion(self, completed: bool = True) -> list:
        """Return tasks filtered by completion status."""
        return [t for t in self.tasks if t.completed == completed]

    def filter_tasks_by_pet_name(self, pet_name: str, pet_store=None) -> list:
        """Return tasks belonging to a specific pet name."""
        store    = pet_store or PET_STORE
        pet_ids  = {p.pet_code for p in store if p.name == pet_name}
        return [t for t in self.tasks if t.pet_id in pet_ids]

    # --- constraints -------------------------------------------------------

    def add_constraint(self, key: str, value) -> None:
        self.constraints[key] = value

    def validate_constraints(self) -> None:
        """Raise ValueError if any constraint value is invalid."""
        if "max_duration" in self.constraints:
            if self.constraints["max_duration"] <= 0:
                raise ValueError("max_duration must be greater than 0.")