# Installation

Follow these steps to prepare a RHEL 9 system or GitLab Runner for the inventory tools.

## Prerequisites

- RHEL 9 with `sudo` access
- Network access to install packages

## Install system packages

```bash
sudo dnf install -y python3.11 python3.11-pip ansible-core git gitlab-runner
```

If you plan to run pipelines, register the runner:

```bash
sudo gitlab-runner register --executor shell
```

## Clone the repository

```bash
git clone https://example.com/ansible-inventory-cli.git
cd ansible-inventory-cli
```

## Create a Python environment

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Continue with the [usage guide](usage.md) to run commands.
