# Reks Manager

Reks Manager is a powerful Django-based application tailored for effective animal shelter management. This system provides a comprehensive set of features designed to streamline the processes involved in running an animal shelter and facilitating seamless adoptions.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

## Features

1. **Animal Tracking:** Manage and track detailed information about animals, including their type, breed, gender, birth date, and health status.

2. **Health Records:** Keep comprehensive health records for each animal, including allergies, medications, vaccinations, and veterinary visits.

3. **Adopter Management:** Efficiently handle information about adopters, making it easy to track and manage the adoption process.

4. **Public Animal Advertisements:** Showcase animals available for adoption through public advertisements, promoting visibility and encouraging adoption.

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, visit the Sign-Up page, complete the form, and follow the email verification process.

- To create a **superuser account**, use the following command:

  ```bash
  $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.
