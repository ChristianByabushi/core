# gestion-loyer

**gestion-loyer** is a web-based application built using Django to manage rental properties, contracts, and tenants. This project provides an interface for landlords to manage contracts, properties (logements), and tenants (locataires), along with filtering and searching capabilities.

## Features

- Manage properties (logements) and tenants (locataires).
- Create, edit, and filter contracts (contrats) by tenant name, property, and contract dates.
- Search and filter contracts easily using form-based filters.
- Generate and view PDF documents related to contracts.
- Handle images and files using Pillow and ReportLab for PDF generation.

## Tech Stack

- **Backend**: Django 5.1.1 (Python web framework)
- **Database**: MySQL (using `mysqlclient`)
- **Frontend**: HTML, CSS, Bootstrap, jQuery
- **Asynchronous Support**: `asgiref`

## Installation

### Prerequisites

- Python 3.x installed on your machine.
- MySQL server installed and running.
- Virtual environment (optional but recommended).

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/gestion-loyer.git
   cd gestion-loyer
