"""
Hospital Management System - OOP Project
A comprehensive hospital management system demonstrating OOP principles
"""

from datetime import datetime, date
from typing import List, Optional
import json

# Base Person class (Abstraction and Inheritance)
class Person:
    """Base class for all people in the hospital system"""
    
    def __init__(self, person_id: str, name: str, age: int, gender: str, contact: str):
        self.__person_id = person_id  # Encapsulation (private attribute)
        self.__name = name
        self.__age = age
        self.__gender = gender
        self.__contact = contact
    
    # Getter methods (Encapsulation)
    def get_person_id(self):
        return self.__person_id
    
    def get_name(self):
        return self.__name
    
    def get_age(self):
        return self.__age
    
    def get_gender(self):
        return self.__gender
    
    def get_contact(self):
        return self.__contact
    
    # Setter methods
    def set_name(self, name):
        self.__name = name
    
    def set_age(self, age):
        self.__age = age
    
    def set_contact(self, contact):
        self.__contact = contact
    
    def display_info(self):
        """Display basic person information"""
        print(f"ID: {self.__person_id}")
        print(f"Name: {self.__name}")
        print(f"Age: {self.__age}")
        print(f"Gender: {self.__gender}")
        print(f"Contact: {self.__contact}")


# Patient class (Inheritance from Person)
class Patient(Person):
    """Patient class inheriting from Person"""
    
    def __init__(self, patient_id: str, name: str, age: int, gender: str, 
                 contact: str, disease: str, admission_date: str):
        super().__init__(patient_id, name, age, gender, contact)
        self.__disease = disease
        self.__admission_date = admission_date
        self.__medical_history = []
        self.__assigned_doctor = None
    
    def get_disease(self):
        return self.__disease
    
    def get_admission_date(self):
        return self.__admission_date
    
    def set_disease(self, disease):
        self.__disease = disease
    
    def assign_doctor(self, doctor):
        self.__assigned_doctor = doctor
    
    def get_assigned_doctor(self):
        return self.__assigned_doctor
    
    def add_medical_record(self, record):
        self.__medical_history.append(record)
    
    def get_medical_history(self):
        return self.__medical_history
    
    def display_info(self):
        """Override parent method (Polymorphism)"""
        print("\n=== Patient Information ===")
        super().display_info()
        print(f"Disease: {self.__disease}")
        print(f"Admission Date: {self.__admission_date}")
        if self.__assigned_doctor:
            print(f"Assigned Doctor: Dr. {self.__assigned_doctor.get_name()}")
        print("="*30)


# Doctor class (Inheritance from Person)
class Doctor(Person):
    """Doctor class inheriting from Person"""
    
    def __init__(self, doctor_id: str, name: str, age: int, gender: str, 
                 contact: str, specialization: str, experience: int):
        super().__init__(doctor_id, name, age, gender, contact)
        self.__specialization = specialization
        self.__experience = experience
        self.__patients = []
    
    def get_specialization(self):
        return self.__specialization
    
    def get_experience(self):
        return self.__experience
    
    def add_patient(self, patient):
        self.__patients.append(patient)
        patient.assign_doctor(self)
    
    def get_patients(self):
        return self.__patients
    
    def display_info(self):
        """Override parent method (Polymorphism)"""
        print("\n=== Doctor Information ===")
        super().display_info()
        print(f"Specialization: {self.__specialization}")
        print(f"Experience: {self.__experience} years")
        print(f"Number of Patients: {len(self.__patients)}")
        print("="*30)


# Appointment class
class Appointment:
    """Class to manage appointments"""
    
    def __init__(self, appointment_id: str, patient: Patient, doctor: Doctor, 
                 appointment_date: str, time: str):
        self.__appointment_id = appointment_id
        self.__patient = patient
        self.__doctor = doctor
        self.__appointment_date = appointment_date
        self.__time = time
        self.__status = "Scheduled"
    
    def get_appointment_id(self):
        return self.__appointment_id
    
    def get_patient(self):
        return self.__patient
    
    def get_doctor(self):
        return self.__doctor
    
    def get_appointment_date(self):
        return self.__appointment_date
    
    def get_time(self):
        return self.__time
    
    def get_status(self):
        return self.__status
    
    def set_status(self, status):
        self.__status = status
    
    def display_info(self):
        print("\n=== Appointment Details ===")
        print(f"Appointment ID: {self.__appointment_id}")
        print(f"Patient: {self.__patient.get_name()}")
        print(f"Doctor: Dr. {self.__doctor.get_name()}")
        print(f"Specialization: {self.__doctor.get_specialization()}")
        print(f"Date: {self.__appointment_date}")
        print(f"Time: {self.__time}")
        print(f"Status: {self.__status}")
        print("="*30)


# Hospital class (Main Management System)
class Hospital:
    """Main hospital management class"""
    
    def __init__(self, name: str):
        self.__name = name
        self.__patients = {}
        self.__doctors = {}
        self.__appointments = {}
        self.__patient_counter = 1
        self.__doctor_counter = 1
        self.__appointment_counter = 1
    
    # Patient Management Methods
    def add_patient(self, name: str, age: int, gender: str, contact: str, 
                   disease: str, admission_date: str):
        patient_id = f"P{self.__patient_counter:04d}"
        patient = Patient(patient_id, name, age, gender, contact, disease, admission_date)
        self.__patients[patient_id] = patient
        self.__patient_counter += 1
        print(f"\n✓ Patient added successfully! Patient ID: {patient_id}")
        return patient
    
    def view_patient(self, patient_id: str):
        if patient_id in self.__patients:
            self.__patients[patient_id].display_info()
        else:
            print(f"\n✗ Patient with ID {patient_id} not found!")
    
    def view_all_patients(self):
        if not self.__patients:
            print("\n✗ No patients registered!")
            return
        print("\n=== All Patients ===")
        for patient in self.__patients.values():
            patient.display_info()
    
    def update_patient(self, patient_id: str, name=None, age=None, contact=None, disease=None):
        if patient_id in self.__patients:
            patient = self.__patients[patient_id]
            if name:
                patient.set_name(name)
            if age:
                patient.set_age(age)
            if contact:
                patient.set_contact(contact)
            if disease:
                patient.set_disease(disease)
            print(f"\n✓ Patient {patient_id} updated successfully!")
        else:
            print(f"\n✗ Patient with ID {patient_id} not found!")
    
    def delete_patient(self, patient_id: str):
        if patient_id in self.__patients:
            del self.__patients[patient_id]
            print(f"\n✓ Patient {patient_id} deleted successfully!")
        else:
            print(f"\n✗ Patient with ID {patient_id} not found!")
    
    # Doctor Management Methods
    def add_doctor(self, name: str, age: int, gender: str, contact: str, 
                  specialization: str, experience: int):
        doctor_id = f"D{self.__doctor_counter:04d}"
        doctor = Doctor(doctor_id, name, age, gender, contact, specialization, experience)
        self.__doctors[doctor_id] = doctor
        self.__doctor_counter += 1
        print(f"\n✓ Doctor added successfully! Doctor ID: {doctor_id}")
        return doctor
    
    def view_doctor(self, doctor_id: str):
        if doctor_id in self.__doctors:
            self.__doctors[doctor_id].display_info()
        else:
            print(f"\n✗ Doctor with ID {doctor_id} not found!")
    
    def view_all_doctors(self):
        if not self.__doctors:
            print("\n✗ No doctors registered!")
            return
        print("\n=== All Doctors ===")
        for doctor in self.__doctors.values():
            doctor.display_info()
    
    def search_doctors_by_specialization(self, specialization: str):
        found_doctors = []
        for doctor in self.__doctors.values():
            if specialization.lower() in doctor.get_specialization().lower():
                found_doctors.append(doctor)
        
        if found_doctors:
            print(f"\n=== Doctors specializing in {specialization} ===")
            for doctor in found_doctors:
                doctor.display_info()
        else:
            print(f"\n✗ No doctors found with specialization: {specialization}")
        return found_doctors
    
    # Appointment Management Methods
    def book_appointment(self, patient_id: str, doctor_id: str, 
                        appointment_date: str, time: str):
        if patient_id not in self.__patients:
            print(f"\n✗ Patient with ID {patient_id} not found!")
            return None
        
        if doctor_id not in self.__doctors:
            print(f"\n✗ Doctor with ID {doctor_id} not found!")
            return None
        
        appointment_id = f"A{self.__appointment_counter:04d}"
        patient = self.__patients[patient_id]
        doctor = self.__doctors[doctor_id]
        
        appointment = Appointment(appointment_id, patient, doctor, appointment_date, time)
        self.__appointments[appointment_id] = appointment
        self.__appointment_counter += 1
        
        # Assign doctor to patient if not already assigned
        if patient.get_assigned_doctor() is None:
            doctor.add_patient(patient)
        
        print(f"\n✓ Appointment booked successfully! Appointment ID: {appointment_id}")
        return appointment
    
    def view_appointment(self, appointment_id: str):
        if appointment_id in self.__appointments:
            self.__appointments[appointment_id].display_info()
        else:
            print(f"\n✗ Appointment with ID {appointment_id} not found!")
    
    def view_all_appointments(self):
        if not self.__appointments:
            print("\n✗ No appointments scheduled!")
            return
        print("\n=== All Appointments ===")
        for appointment in self.__appointments.values():
            appointment.display_info()
    
    def cancel_appointment(self, appointment_id: str):
        if appointment_id in self.__appointments:
            self.__appointments[appointment_id].set_status("Cancelled")
            print(f"\n✓ Appointment {appointment_id} cancelled successfully!")
        else:
            print(f"\n✗ Appointment with ID {appointment_id} not found!")
    
    # Hospital Statistics
    def display_statistics(self):
        print(f"\n{'='*40}")
        print(f"   {self.__name} - Statistics")
        print(f"{'='*40}")
        print(f"Total Patients: {len(self.__patients)}")
        print(f"Total Doctors: {len(self.__doctors)}")
        print(f"Total Appointments: {len(self.__appointments)}")
        
        active_appointments = sum(1 for apt in self.__appointments.values() 
                                 if apt.get_status() == "Scheduled")
        print(f"Active Appointments: {active_appointments}")
        print(f"{'='*40}\n")


# Main Menu System
def print_menu():
    print("\n" + "="*50)
    print("   HOSPITAL MANAGEMENT SYSTEM")
    print("="*50)
    print("1.  Add Patient")
    print("2.  View Patient")
    print("3.  View All Patients")
    print("4.  Update Patient")
    print("5.  Delete Patient")
    print("6.  Add Doctor")
    print("7.  View Doctor")
    print("8.  View All Doctors")
    print("9.  Search Doctors by Specialization")
    print("10. Book Appointment")
    print("11. View Appointment")
    print("12. View All Appointments")
    print("13. Cancel Appointment")
    print("14. Hospital Statistics")
    print("0.  Exit")
    print("="*50)


def main():
    hospital = Hospital("City General Hospital")
    
    # Adding some sample data
    print("\n*** Initializing Hospital System with Sample Data ***")
    hospital.add_doctor("Sarah Johnson", 45, "Female", "555-0101", "Cardiology", 15)
    hospital.add_doctor("Michael Chen", 38, "Male", "555-0102", "Neurology", 10)
    hospital.add_doctor("Emily Davis", 42, "Female", "555-0103", "Pediatrics", 12)
    
    hospital.add_patient("John Smith", 35, "Male", "555-0201", "Heart Disease", "2024-01-15")
    hospital.add_patient("Mary Wilson", 28, "Female", "555-0202", "Migraine", "2024-01-16")
    
    hospital.book_appointment("P0001", "D0001", "2024-02-20", "10:00 AM")
    
    while True:
        print_menu()
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "1":
            print("\n--- Add New Patient ---")
            name = input("Enter name: ")
            age = int(input("Enter age: "))
            gender = input("Enter gender: ")
            contact = input("Enter contact: ")
            disease = input("Enter disease: ")
            admission_date = input("Enter admission date (YYYY-MM-DD): ")
            hospital.add_patient(name, age, gender, contact, disease, admission_date)
        
        elif choice == "2":
            patient_id = input("\nEnter Patient ID: ")
            hospital.view_patient(patient_id)
        
        elif choice == "3":
            hospital.view_all_patients()
        
        elif choice == "4":
            print("\n--- Update Patient ---")
            patient_id = input("Enter Patient ID: ")
            print("Leave blank to skip updating a field")
            name = input("New name: ") or None
            age_input = input("New age: ")
            age = int(age_input) if age_input else None
            contact = input("New contact: ") or None
            disease = input("New disease: ") or None
            hospital.update_patient(patient_id, name, age, contact, disease)
        
        elif choice == "5":
            patient_id = input("\nEnter Patient ID to delete: ")
            confirm = input(f"Are you sure you want to delete {patient_id}? (yes/no): ")
            if confirm.lower() == "yes":
                hospital.delete_patient(patient_id)
        
        elif choice == "6":
            print("\n--- Add New Doctor ---")
            name = input("Enter name: ")
            age = int(input("Enter age: "))
            gender = input("Enter gender: ")
            contact = input("Enter contact: ")
            specialization = input("Enter specialization: ")
            experience = int(input("Enter years of experience: "))
            hospital.add_doctor(name, age, gender, contact, specialization, experience)
        
        elif choice == "7":
            doctor_id = input("\nEnter Doctor ID: ")
            hospital.view_doctor(doctor_id)
        
        elif choice == "8":
            hospital.view_all_doctors()
        
        elif choice == "9":
            specialization = input("\nEnter specialization to search: ")
            hospital.search_doctors_by_specialization(specialization)
        
        elif choice == "10":
            print("\n--- Book Appointment ---")
            patient_id = input("Enter Patient ID: ")
            doctor_id = input("Enter Doctor ID: ")
            appointment_date = input("Enter appointment date (YYYY-MM-DD): ")
            time = input("Enter time (e.g., 10:00 AM): ")
            hospital.book_appointment(patient_id, doctor_id, appointment_date, time)
        
        elif choice == "11":
            appointment_id = input("\nEnter Appointment ID: ")
            hospital.view_appointment(appointment_id)
        
        elif choice == "12":
            hospital.view_all_appointments()
        
        elif choice == "13":
            appointment_id = input("\nEnter Appointment ID to cancel: ")
            hospital.cancel_appointment(appointment_id)
        
        elif choice == "14":
            hospital.display_statistics()
        
        elif choice == "0":
            print("\n*** Thank you for using Hospital Management System! ***")
            break
        
        else:
            print("\n✗ Invalid choice! Please try again.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
