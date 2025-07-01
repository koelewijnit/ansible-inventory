This project is an enterprise-grade Ansible inventory management system. It uses a Python CLI to generate, validate, and manage Ansible inventory files based on a central CSV file.

This `GEMINI.md` file will provide an overview of the project to help you understand its structure and how to work with it.

### About This Project

The core of this project is a Python script, `scripts/ansible_inventory_cli.py`, which serves as a command-line interface for managing Ansible inventory. The inventory is sourced from `inventory_source/hosts.csv` and generated into the `inventory/` directory in a structured YAML format that Ansible can use.

The system is designed for automation and integration into CI/CD pipelines, with features like JSON output, health checks, and lifecycle management for hosts.

### Key Technologies

*   **Ansible:** The automation engine for which the inventory is being managed.
*   **Python:** The language used to build the CLI tool for inventory management.
*   **YAML:** The format used for the generated Ansible inventory files.
*   **CSV:** The format for the master host data.

### Core Scripts & Entrypoints

*   `scripts/ansible_inventory_cli.py`: This is the main entry point for all operations. It's a command-line tool with several subcommands.

### Common Tasks

Here are some common commands you might use when working with this project.

**Generate Inventory:**
To generate the Ansible inventory files from the CSV source:
```bash
python scripts/ansible_inventory_cli.py generate
```

**Check Inventory Health:**
To run a health check on the inventory:
```bash
python scripts/ansible_inventory_cli.py health
```

**Validate Configuration:**
To validate the inventory structure and configuration:
```bash
python scripts/ansible_inventory_cli.py validate
```

**Decommission a Host:**
To mark a host as decommissioned in the source CSV:
```bash
python scripts/ansible_inventory_cli.py lifecycle decommission --hostname <hostname> --date YYYY-MM-DD
```

**Run Ansible with the Generated Inventory:**
Ansible is pre-configured via `ansible.cfg` to use the `inventory/` directory. You can run Ansible commands like this:
```bash
# List hosts in the production environment
ansible all -i inventory/production.yml --list-hosts

# Target a specific group
ansible app_web_server -i inventory/production.yml --list-hosts
```