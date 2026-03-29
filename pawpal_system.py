# PawPal+ System Logic Layer

from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Owner:
    def __init__(self, owner_id, full_name, address, preferences, available_time, number_of_pets):
        self.owner_id = owner_id
        self.full_name = full_name
        self.address = address
        self.preferences = preferences
        self.available_time = available_time
        self.number_of_pets = number_of_pets

    def add_owner(self, owner_id, full_name, address):
        pass  # Logic to add owner

    def add_preferences(self, preferences):
        pass  # Logic to add preferences

    def add_available_time(self, time_slots):
        pass  # Logic to add available time

    def update_preferences(self, preferences):
        pass  # Logic to update preferences

    def update_available_time(self, time_slots):
        pass  # Logic to update available time

    def get_preferences(self):
        pass  # Logic to get preferences


@dataclass
class Pet:
    pet_code: str
    name: str
    pet_type: str
    age: int
    comment: str
    owner_id: str

    def add_pet(self, pet_code, name, pet_type):
        pass  # Logic to add pet

    def update_pet_info(self, pet_code, name=None, pet_type=None, age=None, comment=None):
        pass  # Logic to update pet info

    def validate_pet_info(self):
        pass  # Logic to validate pet info


@dataclass
class Task:
    task_id: str
    name: str
    duration: int
    priority: str
    task_type: str
    owner_id: str
    pet_id: str

    def add_task(self, task_id, name, duration, priority, task_type, owner_id, pet_id):
        pass  # Logic to add task

    def edit_task(self, task_id, name=None, duration=None, priority=None, task_type=None, pet_id=None):
        pass  # Logic to edit task

    def mark_completed(self, task_id):
        pass  # Logic to mark task as completed

    def validate_task(self):
        pass  # Logic to validate task


class Schedule:
    def __init__(self, schedule_id, tasks, constraints, owner_id, pet_id):
        self.schedule_id = schedule_id
        self.tasks = tasks
        self.constraints = constraints
        self.owner_id = owner_id
        self.pet_id = pet_id

    def add_task_to_schedule(self, schedule_id, task, pet_id):
        pass  # Logic to add task to schedule

    def generate_schedule(self, schedule_id, pet_id):
        pass  # Logic to generate schedule

    def explain_schedule(self, schedule_id, pet_id):
        pass  # Logic to explain schedule

    def resolve_conflicts(self, schedule_id, pet_id):
        pass  # Logic to resolve conflicts

    def handle_dynamic_updates(self, schedule_id, updated_task, pet_id):
        pass  # Logic to handle dynamic updates