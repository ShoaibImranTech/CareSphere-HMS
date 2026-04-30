"""
╔══════════════════════════════════════════════════════════════════════════════╗
║           MEDCORE HOSPITAL MANAGEMENT SYSTEM  v2.0                         ║
║           Enterprise-Grade Healthcare Operations Platform                   ║
║           Demonstrating Advanced OOP Principles in Python                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

Architecture:
    - Abstraction       : Person base class with abstract interface
    - Encapsulation     : Private attributes with controlled property access
    - Inheritance       : Patient, Doctor extend Person
    - Polymorphism      : display_info() overridden across all entity classes

Author  : MedCore Systems
Version : 2.0.0
License : MIT
"""

from __future__ import annotations

import os
import json
import uuid
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple


# ─────────────────────────────────────────────────────────────────────────────
# LOGGING CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("MedCore")


# ─────────────────────────────────────────────────────────────────────────────
# ENUMERATIONS
# ─────────────────────────────────────────────────────────────────────────────

class Gender(str, Enum):
    MALE   = "Male"
    FEMALE = "Female"
    OTHER  = "Other"


class AppointmentStatus(str, Enum):
    SCHEDULED  = "Scheduled"
    COMPLETED  = "Completed"
    CANCELLED  = "Cancelled"
    RESCHEDULED = "Rescheduled"


class BloodGroup(str, Enum):
    A_POS  = "A+"
    A_NEG  = "A-"
    B_POS  = "B+"
    B_NEG  = "B-"
    AB_POS = "AB+"
    AB_NEG = "AB-"
    O_POS  = "O+"
    O_NEG  = "O-"


# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM EXCEPTIONS
# ─────────────────────────────────────────────────────────────────────────────

class MedCoreError(Exception):
    """Base exception for all MedCore errors."""

class EntityNotFoundError(MedCoreError):
    """Raised when a requested entity does not exist in the registry."""

class DuplicateEntityError(MedCoreError):
    """Raised when attempting to register a duplicate entity."""

class ValidationError(MedCoreError):
    """Raised when provided data fails validation rules."""

class SchedulingConflictError(MedCoreError):
    """Raised when a scheduling conflict is detected."""


# ─────────────────────────────────────────────────────────────────────────────
# VALUE OBJECTS
# ─────────────────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class ContactInfo:
    """Immutable value object encapsulating contact details."""
    phone:   str
    email:   str = ""
    address: str = ""

    def __post_init__(self) -> None:
        if not self.phone or len(self.phone) < 7:
            raise ValidationError(f"Invalid phone number: '{self.phone}'")

    def __str__(self) -> str:
        parts = [self.phone]
        if self.email:
            parts.append(self.email)
        return " | ".join(parts)


@dataclass(frozen=True)
class MedicalRecord:
    """Immutable record of a single medical encounter."""
    record_id:   str
    date:        str
    diagnosis:   str
    treatment:   str
    notes:       str = ""
    recorded_by: str = "System"

    def __str__(self) -> str:
        return (
            f"[{self.date}] Dx: {self.diagnosis} | "
            f"Tx: {self.treatment} | By: {self.recorded_by}"
        )


# ─────────────────────────────────────────────────────────────────────────────
# ABSTRACT BASE: PERSON  (Abstraction)
# ─────────────────────────────────────────────────────────────────────────────

class Person(ABC):
    """
    Abstract base class representing any individual in the hospital system.

    Demonstrates:
        - Abstraction   : abstract method display_info()
        - Encapsulation : all attributes are private; accessed via properties
    """

    def __init__(
        self,
        person_id: str,
        name:      str,
        age:       int,
        gender:    Gender,
        contact:   ContactInfo,
    ) -> None:
        self._validate_age(age)
        self.__person_id: str        = person_id
        self.__name:      str        = name
        self.__age:       int        = age
        self.__gender:    Gender     = gender
        self.__contact:   ContactInfo = contact

    # ── Validation ───────────────────────────────────────────────────────────

    @staticmethod
    def _validate_age(age: int) -> None:
        if not (0 <= age <= 150):
            raise ValidationError(f"Age must be between 0 and 150 (got {age}).")

    # ── Properties (Encapsulation) ───────────────────────────────────────────

    @property
    def person_id(self) -> str:
        return self.__person_id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        if not value or not value.strip():
            raise ValidationError("Name cannot be empty.")
        self.__name = value.strip()

    @property
    def age(self) -> int:
        return self.__age

    @age.setter
    def age(self, value: int) -> None:
        self._validate_age(value)
        self.__age = value

    @property
    def gender(self) -> Gender:
        return self.__gender

    @property
    def contact(self) -> ContactInfo:
        return self.__contact

    @contact.setter
    def contact(self, value: ContactInfo) -> None:
        self.__contact = value

    # ── Abstract Interface ───────────────────────────────────────────────────

    @abstractmethod
    def display_info(self) -> None:
        """Display a formatted summary of this person's information."""

    # ── Shared Display Helpers ───────────────────────────────────────────────

    def _base_info_lines(self) -> List[str]:
        return [
            f"  ID       : {self.__person_id}",
            f"  Name     : {self.__name}",
            f"  Age      : {self.__age}",
            f"  Gender   : {self.__gender.value}",
            f"  Contact  : {self.__contact}",
        ]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.__person_id!r}, name={self.__name!r})"


# ─────────────────────────────────────────────────────────────────────────────
# PATIENT  (Inheritance from Person)
# ─────────────────────────────────────────────────────────────────────────────

class Patient(Person):
    """
    Represents a hospital patient.

    Demonstrates:
        - Inheritance   : extends Person
        - Polymorphism  : overrides display_info()
        - Encapsulation : private medical data with controlled access
    """

    def __init__(
        self,
        patient_id:     str,
        name:           str,
        age:            int,
        gender:         Gender,
        contact:        ContactInfo,
        primary_diagnosis: str,
        admission_date: str,
        blood_group:    Optional[BloodGroup] = None,
    ) -> None:
        super().__init__(patient_id, name, age, gender, contact)
        self.__primary_diagnosis: str                  = primary_diagnosis
        self.__admission_date:    str                  = admission_date
        self.__blood_group:       Optional[BloodGroup] = blood_group
        self.__medical_history:   List[MedicalRecord]  = []
        self.__assigned_doctor:   Optional[Doctor]     = None
        self.__is_discharged:     bool                 = False

    # ── Properties ───────────────────────────────────────────────────────────

    @property
    def primary_diagnosis(self) -> str:
        return self.__primary_diagnosis

    @primary_diagnosis.setter
    def primary_diagnosis(self, value: str) -> None:
        if not value or not value.strip():
            raise ValidationError("Diagnosis cannot be empty.")
        self.__primary_diagnosis = value.strip()

    @property
    def admission_date(self) -> str:
        return self.__admission_date

    @property
    def blood_group(self) -> Optional[BloodGroup]:
        return self.__blood_group

    @property
    def assigned_doctor(self) -> Optional[Doctor]:
        return self.__assigned_doctor

    @property
    def medical_history(self) -> List[MedicalRecord]:
        return list(self.__medical_history)   # return a copy; protect internals

    @property
    def is_discharged(self) -> bool:
        return self.__is_discharged

    # ── Medical Operations ───────────────────────────────────────────────────

    def assign_doctor(self, doctor: Doctor) -> None:
        self.__assigned_doctor = doctor

    def add_medical_record(self, record: MedicalRecord) -> None:
        self.__medical_history.append(record)
        logger.info("Medical record added for patient %s.", self.person_id)

    def discharge(self) -> None:
        self.__is_discharged = True
        logger.info("Patient %s has been discharged.", self.person_id)

    # ── Polymorphic Display ──────────────────────────────────────────────────

    def display_info(self) -> None:
        """Override: display comprehensive patient information."""
        status_tag = "[ DISCHARGED ]" if self.__is_discharged else "[ ADMITTED ]"
        _box_print("PATIENT RECORD", self._base_info_lines() + [
            f"  Status   : {status_tag}",
            f"  Diagnosis: {self.__primary_diagnosis}",
            f"  Admitted : {self.__admission_date}",
            f"  Blood Grp: {self.__blood_group.value if self.__blood_group else 'Unknown'}",
            f"  Doctor   : {'Dr. ' + self.__assigned_doctor.name if self.__assigned_doctor else 'Unassigned'}",
            f"  Records  : {len(self.__medical_history)} entries",
        ])

    def to_dict(self) -> dict:
        return {
            "patient_id":         self.person_id,
            "name":               self.name,
            "age":                self.age,
            "gender":             self.gender.value,
            "contact":            str(self.contact),
            "primary_diagnosis":  self.__primary_diagnosis,
            "admission_date":     self.__admission_date,
            "blood_group":        self.__blood_group.value if self.__blood_group else None,
            "is_discharged":      self.__is_discharged,
            "medical_records":    [str(r) for r in self.__medical_history],
        }


# ─────────────────────────────────────────────────────────────────────────────
# DOCTOR  (Inheritance from Person)
# ─────────────────────────────────────────────────────────────────────────────

class Doctor(Person):
    """
    Represents a hospital doctor / physician.

    Demonstrates:
        - Inheritance   : extends Person
        - Polymorphism  : overrides display_info()
    """

    def __init__(
        self,
        doctor_id:      str,
        name:           str,
        age:            int,
        gender:         Gender,
        contact:        ContactInfo,
        specialization: str,
        experience:     int,
        qualification:  str = "",
    ) -> None:
        super().__init__(doctor_id, name, age, gender, contact)
        self.__specialization: str          = specialization
        self.__experience:     int          = experience
        self.__qualification:  str          = qualification
        self.__patients:       List[Patient] = []
        self.__is_available:   bool         = True

    # ── Properties ───────────────────────────────────────────────────────────

    @property
    def specialization(self) -> str:
        return self.__specialization

    @property
    def experience(self) -> int:
        return self.__experience

    @property
    def qualification(self) -> str:
        return self.__qualification

    @property
    def is_available(self) -> bool:
        return self.__is_available

    @is_available.setter
    def is_available(self, value: bool) -> None:
        self.__is_available = value

    @property
    def patient_count(self) -> int:
        return len(self.__patients)

    # ── Patient Operations ───────────────────────────────────────────────────

    def assign_patient(self, patient: Patient) -> None:
        if patient not in self.__patients:
            self.__patients.append(patient)
            patient.assign_doctor(self)
            logger.info("Patient %s assigned to Dr. %s.", patient.person_id, self.name)

    def get_patients(self) -> List[Patient]:
        return list(self.__patients)

    # ── Polymorphic Display ──────────────────────────────────────────────────

    def display_info(self) -> None:
        """Override: display comprehensive doctor information."""
        avail = "Available" if self.__is_available else "Unavailable"
        _box_print("PHYSICIAN PROFILE", self._base_info_lines() + [
            f"  Specialty: {self.__specialization}",
            f"  Exp.     : {self.__experience} years",
            f"  Qualif.  : {self.__qualification or 'N/A'}",
            f"  Patients : {len(self.__patients)} assigned",
            f"  Status   : {avail}",
        ])

    def to_dict(self) -> dict:
        return {
            "doctor_id":      self.person_id,
            "name":           self.name,
            "age":            self.age,
            "gender":         self.gender.value,
            "contact":        str(self.contact),
            "specialization": self.__specialization,
            "experience":     self.__experience,
            "qualification":  self.__qualification,
            "patient_count":  len(self.__patients),
            "is_available":   self.__is_available,
        }


# ─────────────────────────────────────────────────────────────────────────────
# APPOINTMENT
# ─────────────────────────────────────────────────────────────────────────────

class Appointment:
    """Encapsulates a scheduled meeting between a Patient and a Doctor."""

    def __init__(
        self,
        appointment_id: str,
        patient:        Patient,
        doctor:         Doctor,
        date:           str,
        time:           str,
        notes:          str = "",
    ) -> None:
        self.__appointment_id: str               = appointment_id
        self.__patient:        Patient           = patient
        self.__doctor:         Doctor            = doctor
        self.__date:           str               = date
        self.__time:           str               = time
        self.__status:         AppointmentStatus = AppointmentStatus.SCHEDULED
        self.__notes:          str               = notes
        self.__created_at:     str               = datetime.now().strftime("%Y-%m-%d %H:%M")

    # ── Properties ───────────────────────────────────────────────────────────

    @property
    def appointment_id(self) -> str:
        return self.__appointment_id

    @property
    def patient(self) -> Patient:
        return self.__patient

    @property
    def doctor(self) -> Doctor:
        return self.__doctor

    @property
    def date(self) -> str:
        return self.__date

    @property
    def time(self) -> str:
        return self.__time

    @property
    def status(self) -> AppointmentStatus:
        return self.__status

    @status.setter
    def status(self, value: AppointmentStatus) -> None:
        self.__status = value

    @property
    def notes(self) -> str:
        return self.__notes

    # ── Display ──────────────────────────────────────────────────────────────

    def display_info(self) -> None:
        _box_print("APPOINTMENT DETAILS", [
            f"  Appt. ID : {self.__appointment_id}",
            f"  Patient  : {self.__patient.name}  [{self.__patient.person_id}]",
            f"  Doctor   : Dr. {self.__doctor.name}  [{self.__doctor.person_id}]",
            f"  Specialty: {self.__doctor.specialization}",
            f"  Date     : {self.__date}",
            f"  Time     : {self.__time}",
            f"  Status   : {self.__status.value}",
            f"  Notes    : {self.__notes or 'None'}",
            f"  Booked   : {self.__created_at}",
        ])

    def to_dict(self) -> dict:
        return {
            "appointment_id": self.__appointment_id,
            "patient_id":     self.__patient.person_id,
            "patient_name":   self.__patient.name,
            "doctor_id":      self.__doctor.person_id,
            "doctor_name":    self.__doctor.name,
            "date":           self.__date,
            "time":           self.__time,
            "status":         self.__status.value,
            "notes":          self.__notes,
            "created_at":     self.__created_at,
        }

    def __repr__(self) -> str:
        return (
            f"Appointment(id={self.__appointment_id!r}, "
            f"patient={self.__patient.name!r}, "
            f"doctor={self.__doctor.name!r}, "
            f"status={self.__status.value!r})"
        )


# ─────────────────────────────────────────────────────────────────────────────
# HOSPITAL  (Facade / Management Orchestrator)
# ─────────────────────────────────────────────────────────────────────────────

class Hospital:
    """
    Central management facade for MedCore Hospital Operations.

    Responsibilities:
        - CRUD operations for Patients, Doctors, and Appointments
        - Assignment of Doctors to Patients
        - Statistical reporting
        - JSON-based persistence (export / import)
    """

    def __init__(self, name: str, address: str = "") -> None:
        self.__name:                str                          = name
        self.__address:             str                          = address
        self.__patients:            Dict[str, Patient]           = {}
        self.__doctors:             Dict[str, Doctor]            = {}
        self.__appointments:        Dict[str, Appointment]       = {}
        self.__patient_seq:         int                          = 1
        self.__doctor_seq:          int                          = 1
        self.__appointment_seq:     int                          = 1
        logger.info("Hospital '%s' initialized.", name)

    # ── ID Generators ─────────────────────────────────────────────────────────

    def _next_patient_id(self) -> str:
        pid = f"P{self.__patient_seq:05d}"
        self.__patient_seq += 1
        return pid

    def _next_doctor_id(self) -> str:
        did = f"D{self.__doctor_seq:05d}"
        self.__doctor_seq += 1
        return did

    def _next_appointment_id(self) -> str:
        aid = f"A{self.__appointment_seq:05d}"
        self.__appointment_seq += 1
        return aid

    # ── PATIENT CRUD ─────────────────────────────────────────────────────────

    def register_patient(
        self,
        name:              str,
        age:               int,
        gender:            Gender,
        phone:             str,
        primary_diagnosis: str,
        admission_date:    Optional[str] = None,
        email:             str           = "",
        blood_group:       Optional[BloodGroup] = None,
    ) -> Patient:
        """Register a new patient and return the created instance."""
        contact = ContactInfo(phone=phone, email=email)
        admission_date = admission_date or date.today().strftime("%Y-%m-%d")
        pid     = self._next_patient_id()
        patient = Patient(pid, name, age, gender, contact, primary_diagnosis, admission_date, blood_group)
        self.__patients[pid] = patient
        logger.info("Patient registered: %s (%s).", name, pid)
        _success(f"Patient registered successfully.  ID: {pid}")
        return patient

    def get_patient(self, patient_id: str) -> Patient:
        if patient_id not in self.__patients:
            raise EntityNotFoundError(f"Patient '{patient_id}' not found.")
        return self.__patients[patient_id]

    def view_patient(self, patient_id: str) -> None:
        try:
            self.get_patient(patient_id).display_info()
        except EntityNotFoundError as e:
            _error(str(e))

    def view_all_patients(self) -> None:
        if not self.__patients:
            _warn("No patients are currently registered.")
            return
        _section_header(f"ALL PATIENTS  ({len(self.__patients)} total)")
        for patient in self.__patients.values():
            patient.display_info()

    def update_patient(
        self,
        patient_id: str,
        name:       Optional[str] = None,
        age:        Optional[int] = None,
        phone:      Optional[str] = None,
        diagnosis:  Optional[str] = None,
    ) -> None:
        try:
            patient = self.get_patient(patient_id)
            if name:
                patient.name = name
            if age is not None:
                patient.age = age
            if phone:
                patient.contact = ContactInfo(phone=phone, email=patient.contact.email)
            if diagnosis:
                patient.primary_diagnosis = diagnosis
            _success(f"Patient {patient_id} updated successfully.")
            logger.info("Patient %s updated.", patient_id)
        except (EntityNotFoundError, ValidationError) as e:
            _error(str(e))

    def discharge_patient(self, patient_id: str) -> None:
        try:
            patient = self.get_patient(patient_id)
            patient.discharge()
            _success(f"Patient {patient_id} ({patient.name}) has been discharged.")
        except EntityNotFoundError as e:
            _error(str(e))

    def delete_patient(self, patient_id: str) -> None:
        if patient_id in self.__patients:
            name = self.__patients[patient_id].name
            del self.__patients[patient_id]
            _success(f"Patient {patient_id} ({name}) removed from the registry.")
            logger.info("Patient %s deleted.", patient_id)
        else:
            _error(f"Patient '{patient_id}' not found.")

    def add_medical_record(
        self,
        patient_id: str,
        diagnosis:  str,
        treatment:  str,
        notes:      str           = "",
        doctor_id:  Optional[str] = None,
    ) -> None:
        try:
            patient = self.get_patient(patient_id)
            doctor_name = "System"
            if doctor_id:
                doc = self.get_doctor(doctor_id)
                doctor_name = f"Dr. {doc.name}"
            record = MedicalRecord(
                record_id   = str(uuid.uuid4())[:8].upper(),
                date        = date.today().strftime("%Y-%m-%d"),
                diagnosis   = diagnosis,
                treatment   = treatment,
                notes       = notes,
                recorded_by = doctor_name,
            )
            patient.add_medical_record(record)
            _success(f"Medical record added for patient {patient_id}.")
        except EntityNotFoundError as e:
            _error(str(e))

    # ── DOCTOR CRUD ─────────────────────────────────────────────────────────

    def register_doctor(
        self,
        name:           str,
        age:            int,
        gender:         Gender,
        phone:          str,
        specialization: str,
        experience:     int,
        email:          str = "",
        qualification:  str = "",
    ) -> Doctor:
        """Register a new doctor and return the created instance."""
        contact = ContactInfo(phone=phone, email=email)
        did     = self._next_doctor_id()
        doctor  = Doctor(did, name, age, gender, contact, specialization, experience, qualification)
        self.__doctors[did] = doctor
        logger.info("Doctor registered: Dr. %s (%s).", name, did)
        _success(f"Doctor registered successfully.  ID: {did}")
        return doctor

    def get_doctor(self, doctor_id: str) -> Doctor:
        if doctor_id not in self.__doctors:
            raise EntityNotFoundError(f"Doctor '{doctor_id}' not found.")
        return self.__doctors[doctor_id]

    def view_doctor(self, doctor_id: str) -> None:
        try:
            self.get_doctor(doctor_id).display_info()
        except EntityNotFoundError as e:
            _error(str(e))

    def view_all_doctors(self) -> None:
        if not self.__doctors:
            _warn("No doctors are currently registered.")
            return
        _section_header(f"ALL PHYSICIANS  ({len(self.__doctors)} total)")
        for doctor in self.__doctors.values():
            doctor.display_info()

    def search_doctors_by_specialization(self, specialization: str) -> List[Doctor]:
        matches = [
            d for d in self.__doctors.values()
            if specialization.strip().lower() in d.specialization.lower()
        ]
        if matches:
            _section_header(f"DOCTORS  —  Specialization: {specialization.title()}")
            for doc in matches:
                doc.display_info()
        else:
            _warn(f"No doctors found with specialization matching '{specialization}'.")
        return matches

    def assign_doctor_to_patient(self, doctor_id: str, patient_id: str) -> None:
        try:
            doctor  = self.get_doctor(doctor_id)
            patient = self.get_patient(patient_id)
            doctor.assign_patient(patient)
            _success(f"Dr. {doctor.name} assigned to patient {patient.name}.")
        except EntityNotFoundError as e:
            _error(str(e))

    # ── APPOINTMENT CRUD ─────────────────────────────────────────────────────

    def book_appointment(
        self,
        patient_id: str,
        doctor_id:  str,
        appt_date:  str,
        time:       str,
        notes:      str = "",
    ) -> Optional[Appointment]:
        """Book a new appointment between a patient and a doctor."""
        try:
            patient = self.get_patient(patient_id)
            doctor  = self.get_doctor(doctor_id)
        except EntityNotFoundError as e:
            _error(str(e))
            return None

        if not doctor.is_available:
            _warn(f"Dr. {doctor.name} is currently marked as unavailable.")

        aid         = self._next_appointment_id()
        appointment = Appointment(aid, patient, doctor, appt_date, time, notes)
        self.__appointments[aid] = appointment

        # Auto-assign doctor if patient has none
        if patient.assigned_doctor is None:
            doctor.assign_patient(patient)

        logger.info("Appointment %s booked: %s → Dr. %s.", aid, patient.name, doctor.name)
        _success(f"Appointment booked successfully.  ID: {aid}")
        return appointment

    def get_appointment(self, appointment_id: str) -> Appointment:
        if appointment_id not in self.__appointments:
            raise EntityNotFoundError(f"Appointment '{appointment_id}' not found.")
        return self.__appointments[appointment_id]

    def view_appointment(self, appointment_id: str) -> None:
        try:
            self.get_appointment(appointment_id).display_info()
        except EntityNotFoundError as e:
            _error(str(e))

    def view_all_appointments(self) -> None:
        if not self.__appointments:
            _warn("No appointments are currently scheduled.")
            return
        _section_header(f"ALL APPOINTMENTS  ({len(self.__appointments)} total)")
        for appointment in self.__appointments.values():
            appointment.display_info()

    def update_appointment_status(
        self,
        appointment_id: str,
        status:         AppointmentStatus,
    ) -> None:
        try:
            appt = self.get_appointment(appointment_id)
            appt.status = status
            _success(f"Appointment {appointment_id} marked as '{status.value}'.")
            logger.info("Appointment %s → %s.", appointment_id, status.value)
        except EntityNotFoundError as e:
            _error(str(e))

    def cancel_appointment(self, appointment_id: str) -> None:
        self.update_appointment_status(appointment_id, AppointmentStatus.CANCELLED)

    # ── STATISTICS ───────────────────────────────────────────────────────────

    def display_statistics(self) -> None:
        active_appts    = sum(1 for a in self.__appointments.values()
                              if a.status == AppointmentStatus.SCHEDULED)
        discharged      = sum(1 for p in self.__patients.values() if p.is_discharged)
        available_docs  = sum(1 for d in self.__doctors.values() if d.is_available)

        _section_header(f"{self.__name.upper()} — OPERATIONAL STATISTICS")
        rows = [
            ("Total Patients",           len(self.__patients)),
            ("  ↳ Active (admitted)",    len(self.__patients) - discharged),
            ("  ↳ Discharged",           discharged),
            ("Total Physicians",         len(self.__doctors)),
            ("  ↳ Available",            available_docs),
            ("  ↳ Unavailable",          len(self.__doctors) - available_docs),
            ("Total Appointments",       len(self.__appointments)),
            ("  ↳ Scheduled (active)",   active_appts),
            ("  ↳ Completed / Other",    len(self.__appointments) - active_appts),
        ]
        w = max(len(label) for label, _ in rows) + 2
        for label, value in rows:
            print(f"  {label:<{w}} {value}")
        print()

    # ── PERSISTENCE ──────────────────────────────────────────────────────────

    def export_to_json(self, filepath: str) -> None:
        """Serialize full hospital data to a JSON file."""
        data = {
            "hospital":     self.__name,
            "exported_at":  datetime.now().isoformat(),
            "patients":     [p.to_dict() for p in self.__patients.values()],
            "doctors":      [d.to_dict() for d in self.__doctors.values()],
            "appointments": [a.to_dict() for a in self.__appointments.values()],
        }
        with open(filepath, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)
        _success(f"Data exported to '{filepath}'.")
        logger.info("Hospital data exported to %s.", filepath)


# ─────────────────────────────────────────────────────────────────────────────
# DISPLAY UTILITIES
# ─────────────────────────────────────────────────────────────────────────────

_WIDTH = 70


def _box_print(title: str, lines: List[str]) -> None:
    """Print a titled box around content lines."""
    top    = f"┌{'─' * (_WIDTH - 2)}┐"
    mid    = f"│  {title:<{_WIDTH - 4}}│"
    sep    = f"├{'─' * (_WIDTH - 2)}┤"
    bottom = f"└{'─' * (_WIDTH - 2)}┘"
    print(top)
    print(mid)
    print(sep)
    for line in lines:
        padded = f"│{line:<{_WIDTH - 1}}│"
        print(padded)
    print(bottom)
    print()


def _section_header(title: str) -> None:
    bar = "═" * _WIDTH
    print(f"\n{bar}")
    print(f"  {title}")
    print(f"{bar}")


def _success(msg: str) -> None:
    print(f"\n  ✔  {msg}")


def _error(msg: str) -> None:
    print(f"\n  ✘  {msg}")


def _warn(msg: str) -> None:
    print(f"\n  ⚠  {msg}")


def _prompt(label: str) -> str:
    return input(f"    {label}: ").strip()


def _prompt_optional(label: str) -> Optional[str]:
    val = input(f"    {label} (optional — press Enter to skip): ").strip()
    return val if val else None


# ─────────────────────────────────────────────────────────────────────────────
# CLI MENU
# ─────────────────────────────────────────────────────────────────────────────

def _print_main_menu() -> None:
    bar = "═" * _WIDTH
    print(f"\n{bar}")
    print(f"{'MEDCORE HOSPITAL MANAGEMENT SYSTEM':^{_WIDTH}}")
    print(f"{'Enterprise Healthcare Operations Platform':^{_WIDTH}}")
    print(f"{bar}")
    options = [
        ("PATIENT MANAGEMENT",  None),
        ("1",  "Register New Patient"),
        ("2",  "View Patient Record"),
        ("3",  "List All Patients"),
        ("4",  "Update Patient Details"),
        ("5",  "Add Medical Record"),
        ("6",  "Discharge Patient"),
        ("7",  "Remove Patient"),
        ("PHYSICIAN MANAGEMENT", None),
        ("8",  "Register New Doctor"),
        ("9",  "View Doctor Profile"),
        ("10", "List All Doctors"),
        ("11", "Search by Specialization"),
        ("12", "Assign Doctor to Patient"),
        ("APPOINTMENT MANAGEMENT", None),
        ("13", "Book Appointment"),
        ("14", "View Appointment"),
        ("15", "List All Appointments"),
        ("16", "Cancel Appointment"),
        ("17", "Mark Appointment Completed"),
        ("SYSTEM",              None),
        ("18", "Hospital Statistics"),
        ("19", "Export Data to JSON"),
        ("0",  "Exit System"),
    ]
    for code, label in options:
        if label is None:
            print(f"\n  ── {code} {'─' * (_WIDTH - len(code) - 6)}")
        else:
            print(f"  [{code:>2}]  {label}")
    print(f"\n{'─' * _WIDTH}")


def _pick_gender() -> Gender:
    while True:
        val = _prompt("Gender (M / F / O)").upper()
        mapping = {"M": Gender.MALE, "F": Gender.FEMALE, "O": Gender.OTHER}
        if val in mapping:
            return mapping[val]
        _error("Enter M, F, or O.")


def _pick_blood_group() -> Optional[BloodGroup]:
    raw = _prompt_optional("Blood Group (A+/A-/B+/B-/AB+/AB-/O+/O-)")
    if not raw:
        return None
    for bg in BloodGroup:
        if bg.value == raw.upper():
            return bg
    _warn(f"Blood group '{raw}' not recognised — leaving blank.")
    return None


# ─────────────────────────────────────────────────────────────────────────────
# MAIN ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

def _seed_demo_data(hospital: Hospital) -> None:
    """Populate the hospital with illustrative demo records."""
    print("\n  Seeding demonstration data …")

    d1 = hospital.register_doctor(
        "Sarah Mitchell", 47, Gender.FEMALE, "555-0101",
        "Cardiology", 18, "s.mitchell@medcore.hospital", "MD, FACC",
    )
    d2 = hospital.register_doctor(
        "James Chen", 39, Gender.MALE, "555-0102",
        "Neurology", 11, "j.chen@medcore.hospital", "MD, FAAN",
    )
    hospital.register_doctor(
        "Priya Sharma", 44, Gender.FEMALE, "555-0103",
        "Pediatrics", 14, "p.sharma@medcore.hospital", "MBBS, MRCPCH",
    )

    p1 = hospital.register_patient(
        "Robert Caldwell", 58, Gender.MALE, "555-0201",
        "Coronary Artery Disease", "2024-01-15",
        blood_group=BloodGroup.O_POS,
    )
    p2 = hospital.register_patient(
        "Amelia Foster", 34, Gender.FEMALE, "555-0202",
        "Chronic Migraine", "2024-01-16",
        blood_group=BloodGroup.A_NEG,
    )

    d1.assign_patient(p1)
    d2.assign_patient(p2)

    hospital.book_appointment("P00001", "D00001", "2024-02-20", "10:00 AM",
                              "Follow-up post-stent procedure")
    hospital.book_appointment("P00002", "D00002", "2024-02-21", "02:30 PM",
                              "Neurological assessment")

    hospital.add_medical_record(
        "P00001", "Stable CAD", "Continue Aspirin 75 mg + Atorvastatin 40 mg",
        "BP well-controlled", "D00001",
    )

    print("  Demo data loaded successfully.\n")


def main() -> None:
    os.system("cls" if os.name == "nt" else "clear")
    bar = "═" * _WIDTH
    print(f"\n{bar}")
    print(f"{'╔══ MEDCORE HOSPITAL MANAGEMENT SYSTEM ══╗':^{_WIDTH}}")
    print(f"{'Enterprise Healthcare Operations Platform':^{_WIDTH}}")
    print(f"{'v2.0.0  |  Python OOP Edition':^{_WIDTH}}")
    print(f"{bar}\n")

    hospital_name = input("  Enter hospital name [City General Hospital]: ").strip()
    if not hospital_name:
        hospital_name = "City General Hospital"

    hospital = Hospital(hospital_name)
    _seed_demo_data(hospital)

    while True:
        _print_main_menu()
        choice = input("  Select option: ").strip()

        try:
            # ── PATIENT OPERATIONS ───────────────────────────────────────────
            if choice == "1":
                print("\n  ── Register New Patient")
                hospital.register_patient(
                    name              = _prompt("Full name"),
                    age               = int(_prompt("Age")),
                    gender            = _pick_gender(),
                    phone             = _prompt("Phone number"),
                    primary_diagnosis = _prompt("Primary diagnosis"),
                    email             = _prompt_optional("Email") or "",
                    blood_group       = _pick_blood_group(),
                )

            elif choice == "2":
                hospital.view_patient(_prompt("Patient ID"))

            elif choice == "3":
                hospital.view_all_patients()

            elif choice == "4":
                print("\n  ── Update Patient Details")
                pid = _prompt("Patient ID")
                hospital.update_patient(
                    pid,
                    name      = _prompt_optional("New name"),
                    age       = (lambda v: int(v) if v else None)(_prompt_optional("New age")),
                    phone     = _prompt_optional("New phone"),
                    diagnosis = _prompt_optional("New diagnosis"),
                )

            elif choice == "5":
                print("\n  ── Add Medical Record")
                hospital.add_medical_record(
                    patient_id = _prompt("Patient ID"),
                    diagnosis  = _prompt("Diagnosis"),
                    treatment  = _prompt("Treatment"),
                    notes      = _prompt_optional("Notes") or "",
                    doctor_id  = _prompt_optional("Doctor ID (leave blank for system entry)"),
                )

            elif choice == "6":
                hospital.discharge_patient(_prompt("Patient ID"))

            elif choice == "7":
                pid = _prompt("Patient ID to remove")
                confirm = _prompt(f"Type 'CONFIRM' to permanently remove {pid}").upper()
                if confirm == "CONFIRM":
                    hospital.delete_patient(pid)
                else:
                    _warn("Deletion cancelled.")

            # ── DOCTOR OPERATIONS ────────────────────────────────────────────
            elif choice == "8":
                print("\n  ── Register New Doctor")
                hospital.register_doctor(
                    name           = _prompt("Full name"),
                    age            = int(_prompt("Age")),
                    gender         = _pick_gender(),
                    phone          = _prompt("Phone number"),
                    specialization = _prompt("Specialization"),
                    experience     = int(_prompt("Years of experience")),
                    email          = _prompt_optional("Email") or "",
                    qualification  = _prompt_optional("Qualifications") or "",
                )

            elif choice == "9":
                hospital.view_doctor(_prompt("Doctor ID"))

            elif choice == "10":
                hospital.view_all_doctors()

            elif choice == "11":
                hospital.search_doctors_by_specialization(_prompt("Specialization keyword"))

            elif choice == "12":
                hospital.assign_doctor_to_patient(
                    _prompt("Doctor ID"),
                    _prompt("Patient ID"),
                )

            # ── APPOINTMENT OPERATIONS ───────────────────────────────────────
            elif choice == "13":
                print("\n  ── Book Appointment")
                hospital.book_appointment(
                    patient_id = _prompt("Patient ID"),
                    doctor_id  = _prompt("Doctor ID"),
                    appt_date  = _prompt("Appointment date (YYYY-MM-DD)"),
                    time       = _prompt("Time (e.g. 10:00 AM)"),
                    notes      = _prompt_optional("Notes") or "",
                )

            elif choice == "14":
                hospital.view_appointment(_prompt("Appointment ID"))

            elif choice == "15":
                hospital.view_all_appointments()

            elif choice == "16":
                hospital.cancel_appointment(_prompt("Appointment ID"))

            elif choice == "17":
                hospital.update_appointment_status(
                    _prompt("Appointment ID"),
                    AppointmentStatus.COMPLETED,
                )

            # ── SYSTEM OPERATIONS ────────────────────────────────────────────
            elif choice == "18":
                hospital.display_statistics()

            elif choice == "19":
                path = _prompt_optional("Output filepath") or "hospital_export.json"
                hospital.export_to_json(path)

            elif choice == "0":
                print(f"\n{'═' * _WIDTH}")
                print(f"{'Thank you for using MedCore HMS.':^{_WIDTH}}")
                print(f"{'Goodbye.':^{_WIDTH}}")
                print(f"{'═' * _WIDTH}\n")
                break

            else:
                _warn("Invalid selection. Please choose a valid option.")

        except (ValueError, ValidationError) as exc:
            _error(f"Input error: {exc}")
        except KeyboardInterrupt:
            print("\n\n  Session interrupted. Goodbye.")
            break

        input("\n  Press Enter to continue…")


if __name__ == "__main__":
    main()
