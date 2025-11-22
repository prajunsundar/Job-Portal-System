# The Job Portal System is a backend REST API built using Django and Django REST Framework (DRF).
It manages the complete workflow between Admins, Employers, and Job Seekers, enabling job postings, applications, approvals, and user management.

This repository contains only the backend API.
Frontend (web/mobile) can consume these APIs easily using JSON.



🔹 Admin Module

Admin authentication

Manage profile & reset password

Approve / block / delete:Employers,Job Seekers

Approve / disapprove job postings

View all job listings & applicant statistics

Email alerts for:

New employer/user registrations

New job postings awaiting approval


🔹 Employer Module

Company registration with:Logo,Website,Address

Post new job listings

Edit or delete posted jobs

View all posted jobs

Reset password

Email notifications for job approval


🔹 Job Seeker Module

Register with:
Name,Email (unique),Mobile Number,Password (strong policy),Date of Birth


Receive confirmation email with auto-generated 6-digit temporary password

Manage profile: picture, education, address

Search jobs using filters:Location,Job Title,Job Type


Apply to jobs

Track application status:Accepted,Rejected,Viewed,Visited

Receive email notifications for application updates

🔐 Authentication & Security

Role-based login (Admin, Employer, Job Seeker)

JWT / Token-based authentication (according to your implementation)

Password strength validation:Minimum length,Special character,Number

Throttling & permissions (DRF built-in)
