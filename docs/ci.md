# CI

This project uses a GitLab CI pipeline tailored for RHEL 9 runners.
Jobs run inside the `registry.access.redhat.com/ubi9/python-311` container image.

## Pipeline overview

1. Lint and style checks
2. Unit tests with coverage
3. Optional deployment steps

## Sample job

```yaml
image: registry.access.redhat.com/ubi9/python-311
stages:
  - test

unit_tests:
  stage: test
  script:
    - dnf -y install git ansible-core
    - pip install --disable-pip-version-check --no-cache-dir -r requirements.txt pytest pytest-cov
    - pytest --cov=src --cov-report=xml
  artifacts:
    reports:
      cobertura: coverage.xml
  tags:
    - rhel9
```

The `.gitlab-ci.yml` file in the repository demonstrates additional stages and caching strategies.
