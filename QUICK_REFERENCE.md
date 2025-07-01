# Quick Reference: Enhanced Ansible Inventory

## 🚀 **Essential Commands**

### Generate Inventories
```bash
# Generate all environment inventories from enhanced CSV
python3 scripts/generate_inventory.py

# Generate with custom CSV file
python3 scripts/generate_inventory.py --csv-file inventory_source/hosts_backup.csv

# Generate specific environments only
python3 scripts/generate_inventory.py --environments production test

# Generate with custom output directory
python3 scripts/generate_inventory.py --output-dir custom_inventory

# Validate inventory structure  
python3 scripts/validate_inventory_structure.py

# Show inventory structure overview
python3 scripts/show_inventory_structure.py
```

### Manage Application Groups
```bash
# Generate application group_vars from CSV data
python3 scripts/create_application_group_vars.py
```

## 🎯 **Targeting Patterns**

### **Cross-Product (Functional) Targeting**
```bash
# ALL directory services (A, B, C)
ansible app_identity_management -i inventory/production.yml --list-hosts

# ALL web servers (Apache + Nginx + other web servers)
ansible app_web_server -i inventory/production.yml --list-hosts

# ALL databases (PostgreSQL + MongoDB + other databases)  
ansible app_database -i inventory/production.yml --list-hosts

# ALL container infrastructure (K8s masters + workers)
ansible app_container_orchestrator,app_container_worker -i inventory/production.yml --list-hosts

# ALL monitoring systems (Prometheus + Grafana + ELK)
ansible app_monitoring_metrics,app_monitoring_visualization,app_monitoring_logging -i inventory/production.yml --list-hosts
```

### **Product-Specific Targeting**
```bash
# ONLY directory service A hosts
ansible product_directory_service_a -i inventory/production.yml --list-hosts

# ONLY Apache HTTP servers (not Nginx)
ansible product_apache_httpd -i inventory/production.yml --list-hosts

# ONLY PostgreSQL databases (not MongoDB)
ansible product_postgresql -i inventory/production.yml --list-hosts

# ONLY Kubernetes masters
ansible product_kubernetes -l "*master*" -i inventory/production.yml --list-hosts

# ONLY Kubernetes workers  
ansible product_kubernetes -l "*worker*" -i inventory/production.yml --list-hosts
```

### **Environment Filtering**
```bash
# Production directory services only
ansible app_identity_management -i inventory/production.yml --list-hosts

# Development web servers only
ansible app_web_server -i inventory/development.yml --list-hosts

# All environments for specific product
ansible product_postgresql -i inventory/production.yml,inventory/development.yml --list-hosts
```

## 📊 **Group Structure Reference**

> **Note:** The following application service groups and product-specific groups are examples. Adapt these to match your own environment, products, and services as needed.

### **Application Service Groups**
```yaml
# Automation-friendly functional groups
app_identity_management      # All identity services (cross-product)
app_web_server              # All web servers (cross-product)  
app_database                # All databases (cross-product)
app_container_orchestrator  # Kubernetes masters
app_container_worker        # Kubernetes workers
app_cache                   # Redis and other caching
app_message_broker          # Kafka and other messaging
app_monitoring_metrics      # Prometheus and metrics systems
app_monitoring_visualization # Grafana and dashboards
app_monitoring_logging      # ELK stack and log systems
app_cicd_repository         # GitLab and SCM systems
app_cicd_automation         # Jenkins and CI systems
app_secrets_management      # Vault and secret stores
app_service_discovery       # Consul and service discovery
app_dns_server              # DNS infrastructure
app_mail_server             # Email systems
app_time_server             # NTP servers
app_storage_server          # Storage infrastructure
app_backup_server           # Backup systems
app_legacy_app              # Legacy applications
# ... 27 total application categories
```

### **Product-Specific Groups**
```yaml
# Software-specific product groups
product_directory_service_a           # Directory Service A
product_directory_service_b           # Directory Service B  
product_directory_service_c           # Directory Service C
product_apache_httpd        # Apache HTTP Server
product_nginx               # Nginx web server
product_postgresql          # PostgreSQL database
product_mongodb             # MongoDB database
product_kubernetes          # Kubernetes (masters + workers)
product_redis               # Redis cache
product_apache_kafka        # Apache Kafka
product_prometheus          # Prometheus monitoring
product_grafana             # Grafana visualization
product_elasticsearch       # Elasticsearch
product_gitlab              # GitLab
product_jenkins             # Jenkins CI/CD
product_hashicorp_vault     # HashiCorp Vault
product_consul              # Consul service discovery
# ... 43 total product types
```

## 💼 **Common Use Cases**

### **Security Updates**
```bash
# Update SSL certificates on ALL web servers
ansible app_web_server -m copy -a "src=ssl-cert.pem dest=/etc/ssl/certs/"

# Update security policies on ALL identity systems
ansible app_identity_management -m copy -a "src=security.conf dest=/etc/security/"

# Patch ALL databases with security update
ansible app_database -m yum -a "name=security-update state=latest"
```

### **Service Management**
```bash
# Restart ALL web services
ansible app_web_server -m service -a "name={{web_service_name}} state=restarted"

# Stop ALL monitoring for maintenance
ansible app_monitoring_metrics,app_monitoring_visualization -m service -a "name={{service_name}} state=stopped"

# Scale Kubernetes workers
ansible product_kubernetes -l "*worker*" -m shell -a "kubectl scale deployment app --replicas=5"
```

### **Configuration Management**
```bash
# Deploy new Apache config to Apache servers only (not Nginx)
ansible product_apache_httpd -m copy -a "src=httpd.conf dest=/etc/httpd/conf/"

# Update directory service drivers specifically
ansible product_directory_service_a -m copy -a "src=directory-drivers.xml dest=/opt/directory_service_a/"

# Deploy database schema to PostgreSQL only (not MongoDB)
ansible product_postgresql -m postgresql_db -a "name=myapp state=present"
```

### **Maintenance Operations**
```bash
# Backup ALL databases (cross-product)
ansible app_database -m shell -a "{{backup_command}}"

# Check disk space on ALL servers by environment
ansible all -i inventory/production.yml -m shell -a "df -h"

# Update ALL system packages in development
ansible all -i inventory/development.yml -m yum -a "name=* state=latest"
```

## 📁 **File Locations**

### **Source Files**
```
inventory_source/hosts_demo.csv    # Demo CSV showing complete functionality

```

### **Generated Inventories**
```
inventory/production.yml        # 142 hosts, 61 groups
inventory/development.yml       # 43 hosts, 51 groups  
inventory/test.yml              # 30 hosts, 47 groups
inventory/acceptance.yml        # 30 hosts, 47 groups
```

### **Configuration Files**
```
inventory/group_vars/applications/     # Auto-generated app configs
inventory/group_vars/products/         # Auto-generated product configs
inventory/group_vars/all/              # Manual global settings
inventory/host_vars/                   # Auto-generated host data
```

## 🔧 **Validation & Debugging**

### **Check Host Variables**
```bash
# Show all variables for specific host
ansible-inventory -i inventory/production.yml --host prd-dirsvc1-use1-01 --yaml

# List all hosts in a group
ansible app_identity_management -i inventory/production.yml --list-hosts

# Show group membership for host
ansible-inventory -i inventory/production.yml --graph
```

### **Validation Commands**
```bash
# Validate inventory structure
python3 scripts/validate_inventory_structure.py

# Check CSV format
python3 scripts/validate_inventory_structure.py --csv-only

# Show inventory statistics
python3 scripts/show_inventory_structure.py
```

### **Troubleshooting**
```bash
# Check Ansible can connect to hosts
ansible app_web_server -i inventory/production.yml -m ping

# Test specific host connectivity
ansible prd-dirsvc1-use1-01 -i inventory/production.yml -m setup

# Verify group targeting
ansible app_identity_management -i inventory/production.yml --list-hosts
```

## ⚡ **Pro Tips**

### **Combining Groups**
```bash
# Multiple functional groups
ansible app_web_server,app_database -i inventory/production.yml --list-hosts

# Product-specific with environment filtering  
ansible product_kubernetes -i inventory/production.yml -l "*master*" --list-hosts

# Exclude specific hosts
ansible app_monitoring_metrics -i inventory/production.yml --limit '!prd-prometheus-use1-02' --list-hosts
```

### **Advanced Patterns**
```bash
# All identity services in US regions only
ansible app_identity_management -i inventory/production.yml -l "*use1*" --list-hosts

# All databases except MongoDB
ansible app_database -i inventory/production.yml --limit '!product_mongodb' --list-hosts

# Staging environments (test + acceptance)
ansible all -i inventory/test.yml,inventory/acceptance.yml --list-hosts
```

---

**Enhanced Ansible Inventory** - Dual targeting for maximum flexibility and precision. 