import streamlit as st
from pawpal_system import Owner, Pet, Task, Schedule

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# ---------------------------------------------------------------------------
# Session state initialisation — runs ONCE, survives every rerun
# ---------------------------------------------------------------------------
# Think of this block as the "vault setup".
# Each `if "key" not in st.session_state` check means:
#   "only create this object if it doesn't already exist in the vault."

if "owner" not in st.session_state:
    st.session_state.owner = None          # set properly when the form is submitted

if "pet" not in st.session_state:
    st.session_state.pet = None

if "tasks" not in st.session_state:
    st.session_state.tasks = []            # list of Task objects (was plain dicts)

if "schedule" not in st.session_state:
    st.session_state.schedule = None

# Convenient local references — always point at the vault, not a fresh copy
owner    = st.session_state.owner
pet      = st.session_state.pet
tasks    = st.session_state.tasks
schedule = st.session_state.schedule

# ---------------------------------------------------------------------------
# Owner + Pet setup
# ---------------------------------------------------------------------------
st.subheader("Owner & Pet Info")


col1, col2 = st.columns(2)
with col1:
    owner_name     = st.text_input("Owner name", value="Jordan")
    available_time = st.text_input("Available window", value="07:00-22:00")
with col2:
    pet_name = st.text_input("Pet name", value="Mochi")
    species  = st.selectbox("Species", ["Dog", "Cat", "Bird", "Other"])
    pet_age  = st.number_input("Pet age (years)", min_value=0, max_value=30, value=3)


if st.button("Save owner & pet"):
    # Step 1 — create Owner and store in vault (only if not already there)
    if st.session_state.owner is None:
        st.session_state.owner = Owner(
            owner_id="001",
            full_name=owner_name,
            address="",
            preferences="",
            available_time=available_time,
            number_of_pets=1,
        )


    # Step 2 — create Pet object
    pet_type = species.upper()
    new_pet = Pet(
        pet_code=f"P{len(st.session_state.owner.get_pets() or []) + 1:03}",
        name=pet_name,
        pet_type=pet_type,
        age=pet_age,
        comment="",
        owner_id=st.session_state.owner.owner_id,
    )

    # Step 3 — hand Pet to the Owner via its method (this is the backend call)
    # Owner.add_pet() validates + registers the pet; UI reflects it on rerun
    try:
        new_pet.validate_pet_info()                  # Pet validates itself first
        st.session_state.owner.add_pet(new_pet)      # Owner takes ownership
        st.session_state.pet = new_pet               # keep a quick-access ref
        st.success(f"✅ {pet_name} added to {owner_name}'s profile!")
    except ValueError as e:
        st.error(f"Could not add pet: {e}")

    owner = st.session_state.owner
    pet   = st.session_state.pet

# Show a status badge so the user can see what's in the vault
if st.session_state.owner and st.session_state.pet:
    st.caption(f"🔒 Vault: Owner **{st.session_state.owner.full_name}** "
               f"+ Pet **{st.session_state.pet.name}** in session")
elif st.session_state.owner:
    st.caption(f"🔒 Vault: Owner **{st.session_state.owner.full_name}** in session (no pet yet)")
else:
    st.caption("🔒 Vault: no owner saved yet — fill in the form above")

st.divider()

# ---------------------------------------------------------------------------
# Task entry
# ---------------------------------------------------------------------------
st.subheader("Tasks")
st.caption("Tasks are stored as real Task objects in session state.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["LOW", "MEDIUM", "HIGH"], index=2)

if st.button("Add task"):
    if not st.session_state.pet:
        st.warning("Save an owner & pet first before adding tasks.")
    else:
        new_task = Task(
            task_id=f"T{len(st.session_state.tasks) + 1:03}",
            name=task_title,
            duration=int(duration),
            priority=priority,
            task_type="GENERAL",
            owner_id=st.session_state.owner.owner_id,
            pet_id=st.session_state.pet.pet_code,
        )
        # Step 1 — Task validates itself
        try:
            new_task.validate_task()
        except ValueError as e:
            st.error(f"Invalid task: {e}")
            st.stop()

        # Step 2 — Schedule receives the task via its method
        # If no schedule exists yet, create one now
        if st.session_state.schedule is None:
            st.session_state.schedule = Schedule(
                schedule_id="S001",
                owner_id=st.session_state.owner.owner_id,
                pet_id=st.session_state.pet.pet_code,
            )
        st.session_state.schedule.add_task_to_schedule(new_task)

        # Step 3 — also keep tasks list in sync for the table display
        st.session_state.tasks.append(new_task)

if st.session_state.tasks:
    st.write("Current tasks:")
    # Display Task objects as a readable table
    st.table([
        {
            "ID":       t.task_id,
            "Task":     t.name,
            "Duration": f"{t.duration} min",
            "Priority": t.priority,
            "Done":     "✓" if t.completed else "○",
        }
        for t in st.session_state.tasks
    ])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# ---------------------------------------------------------------------------
# Schedule generation
# ---------------------------------------------------------------------------
st.subheader("Build Schedule")


# --- Updated: Use Schedule methods for sorting and conflict detection ---
if st.button("Generate schedule"):
    if not st.session_state.owner or not st.session_state.pet:
        st.warning("Please save an owner & pet first.")
    elif not st.session_state.tasks:
        st.warning("Please add at least one task first.")
    else:
        sched = Schedule(
            schedule_id="S001",
            owner_id="001",
            pet_id="P001",
        )
        for t in st.session_state.tasks:
            sched.add_task_to_schedule(t)

        sched.generate_schedule()        # your scheduling logic runs here
        sched.sort_by_time()             # ensure tasks are sorted chronologically
        st.session_state.schedule = sched


if st.session_state.schedule:
    # Conflict detection
    conflicts = st.session_state.schedule.detect_time_conflicts()
    if conflicts:
        st.warning(f"⚠️ {len(conflicts)} time slot(s) have overlapping tasks. Please review:")
        for conflict_group in conflicts:
            st.table([
                {
                    "Task ID": t.task_id,
                    "Task": t.name,
                    "Pet ID": t.pet_id,
                    "Start Time": t.start_time,
                    "Due Date": t.due_date,
                    "Priority": t.priority
                }
                for t in conflict_group
            ])

    st.success("Schedule generated!")
    # Show sorted schedule as a professional table
    st.subheader("Sorted Schedule")
    st.table([
        {
            "Task ID": t.task_id,
            "Task": t.name,
            "Pet ID": t.pet_id,
            "Start Time": t.start_time,
            "Due Date": t.due_date,
            "Duration": f"{t.duration} min",
            "Priority": t.priority,
            "Done": "✓" if t.completed else "○",
        }
        for t in st.session_state.schedule.tasks
    ])
    explanation = st.session_state.schedule.explain_schedule()
    if explanation:
        st.markdown(explanation)
    else:
        st.caption("explain_schedule() not yet implemented — add it in pawpal_system.py")