# MedCore Hospital Management System
### Enterprise-Grade Healthcare Operations Platform · Python OOP Edition · v2.0.0

---

## Overview

**MedCore HMS** is a fully object-oriented Python application that models the core operational workflows of a hospital — patient registration, physician management, appointment scheduling, and medical record keeping. It was purpose-built to demonstrate professional-grade application of the four pillars of Object-Oriented Programming in a realistic, maintainable codebase.

---

## OOP Architecture

| Pillar | Where Applied |
|---|---|
| **Abstraction** | `Person` is an abstract base class (`ABC`) with an abstract `display_info()` method. No `Person` instance can be created directly. |
| **Encapsulation** | All class attributes are private (name-mangled with `__`). All access is mediated through typed properties with validation logic. |
| **Inheritance** | `Patient` and `Doctor` both extend `Person`, inheriting shared identity fields while adding domain-specific attributes and behaviour. |
| **Polymorphism** | `display_info()` is overridden in `Patient`, `Doctor`, and `Appointment` — each produces a context-appropriate formatted output through the same interface. |

---

## Project Structure

```
medcore-hms/
├── hospital_management_system.py   # Single-file application (all classes + CLI)
└── README.md
```

### Class Hierarchy

```
Person  (ABC — abstract base)
├── Patient
└── Doctor

Appointment          (standalone entity linking Patient ↔ Doctor)
Hospital             (management facade / orchestrator)

ContactInfo          (frozen dataclass — value object)
MedicalRecord        (frozen dataclass — value object)

Gender               (Enum)
AppointmentStatus    (Enum)
BloodGroup           (Enum)

MedCoreError         (base exception)
├── EntityNotFoundError
├── DuplicateEntityError
├── ValidationError
└── SchedulingConflictError
```

---

## Features

### Patient Management
- Register patients with demographic and clinical information
- View individual patient records or list all patients
- Update name, age, phone number, or primary diagnosis
- Append immutable medical records to a patient's history
- Discharge patients with an audit trail
- Remove patients from the registry (with confirmation)

### Physician Management
- Register doctors with specialization, experience, and qualifications
- View individual profiles or list all physicians
- Full-text search by specialization keyword
- Manually assign a doctor to a patient

### Appointment Management
- Book appointments linking a patient and a doctor by their IDs
- Auto-assign doctor to patient if none is assigned
- View individual appointments or list all appointments
- Cancel or mark appointments as completed

### System
- Real-time operational statistics dashboard
- JSON export of all hospital data with timestamp
- Structured logging to stdout (timestamp, severity, message)
- Demo data seeded on startup for immediate exploration

---

## Requirements

- Python 3.9 or higher
- Standard library only — **no third-party packages required**

---

## Getting Started

### 1 — Clone or copy the file

```bash
# If cloning:
git clone https://github.com/your-org/medcore-hms.git
cd medcore-hms

# Or simply download:
# hospital_management_system.py
```

### 2 — Run the application

```bash
python hospital_management_system.py
```

You will be prompted for a hospital name. Press Enter to use the default (`City General Hospital`). Demo data is seeded automatically.

---

## Usage Walkthrough

### Registering a Patient

```
Select option: 1

  ── Register New Patient
    Full name: John Hartley
    Age: 52
    Gender (M / F / O): M
    Phone number: 555-9900
    Primary diagnosis: Type 2 Diabetes
    Email (optional): j.hartley@email.com
    Blood Group (optional): B+

  ✔  Patient registered successfully.  ID: P00003
```

### Booking an Appointment

```
Select option: 13

  ── Book Appointment
    Patient ID: P00003
    Doctor ID: D00001
    Appointment date (YYYY-MM-DD): 2024-03-10
    Time (e.g. 10:00 AM): 09:30 AM
    Notes (optional): Initial cardiology consultation

  ✔  Appointment booked successfully.  ID: A00003
```

### Viewing Statistics

```
Select option: 18

══════════════════════════════════════════════════════════════════════
  CITY GENERAL HOSPITAL — OPERATIONAL STATISTICS
══════════════════════════════════════════════════════════════════════
  Total Patients              3
    ↳ Active (admitted)       2
    ↳ Discharged              1
  Total Physicians            3
    ↳ Available               3
    ↳ Unavailable             0
  Total Appointments          3
    ↳ Scheduled (active)      3
    ↳ Completed / Other       0
```

### Exporting Data

```
Select option: 19
    Output filepath (optional): backup_2024_03.json

  ✔  Data exported to 'backup_2024_03.json'.
```

---

## Design Decisions

**Why a single file?**
This is an academic/portfolio project. Keeping everything in one file makes it trivially portable and easy to submit or share. In a production codebase, each class would live in its own module.

**Why frozen dataclasses for `ContactInfo` and `MedicalRecord`?**
These are value objects — they have no identity beyond their data. Making them immutable (`frozen=True`) prevents accidental mutation and communicates intent clearly.

**Why custom exceptions?**
Specific exception types (`EntityNotFoundError`, `ValidationError`, etc.) make error handling explicit and allow callers to react differently to different failure modes — a professional pattern absent in basic scripts.

**Why `ABC` instead of a plain base class?**
The `@abstractmethod` decorator on `display_info()` enforces that every concrete subclass provides its own implementation. Attempting to instantiate `Person` directly raises a `TypeError` — this is true abstraction, not just convention.

---

## OOP Concepts — Quick Reference

```python
# Abstraction: Person cannot be instantiated
from abc import ABC, abstractmethod
class Person(ABC):
    @abstractmethod
    def display_info(self) -> None: ...

# Encapsulation: private attributes, property access
class Patient(Person):
    def __init__(self, ...):
        self.__diagnosis = diagnosis   # private

    @property
    def primary_diagnosis(self) -> str:
        return self.__diagnosis        # controlled read access

    @primary_diagnosis.setter
    def primary_diagnosis(self, value: str) -> None:
        if not value:
            raise ValidationError("Diagnosis cannot be empty.")
        self.__diagnosis = value       # validated write access

# Inheritance: Patient extends Person
class Patient(Person):
    def __init__(self, patient_id, name, age, gender, contact, ...):
        super().__init__(patient_id, name, age, gender, contact)  # parent init

# Polymorphism: same method name, different behaviour
patient.display_info()   # → formatted patient card
doctor.display_info()    # → formatted physician profile
```

---

## License

MIT License. Free to use, modify, and distribute for educational and commercial purposes with attribution.

---

*Built with Python · Standard Library · No dependencies*
