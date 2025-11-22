# Tutorial: Converting GitLab CI/CD to GitHub Actions

This tutorial walks through the process of converting a `.gitlab-ci.yml` file to a GitHub Actions `ci.yml` workflow file, using the Not Another List App project as a real-world example.

## Table of Contents
1. [Understanding the Differences](#understanding-the-differences)
2. [Step-by-Step Conversion Process](#step-by-step-conversion-process)
3. [Key Concept Mappings](#key-concept-mappings)
4. [Testing Your Workflow](#testing-your-workflow)

---

## Understanding the Differences

Before converting, it's important to understand the fundamental differences between GitLab CI/CD and GitHub Actions:

| Concept | GitLab CI/CD | GitHub Actions |
|---------|--------------|----------------|
| **Configuration File** | `.gitlab-ci.yml` (root) | `.github/workflows/*.yml` |
| **Job Runner** | GitLab Runner | GitHub-hosted or self-hosted runners |
| **Default Environment** | Configurable base image | Ubuntu by default |
| **Docker Support** | Docker-in-Docker (DinD) | Native Docker support |
| **Stages** | Explicit stages with dependencies | Jobs with `needs` dependencies |
| **Syntax** | YAML with GitLab-specific keys | YAML with GitHub-specific keys |

---

## Step-by-Step Conversion Process

### Step 1: Create the GitHub Actions Directory Structure

First, create the required directory structure for GitHub Actions:

```bash
mkdir -p .github/workflows
```

GitHub Actions workflows must be placed in `.github/workflows/` directory.

### Step 2: Set Up the Workflow File Header

**GitLab CI/CD:**
```yaml
image: docker:stable

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: ""
  DOCKER_HOST: tcp://docker:2375

services:
  - name: docker:dind
    entrypoint: ["env", "-u", "DOCKER_HOST"]
    command: ["dockerd-entrypoint.sh"]
```

**GitHub Actions:**
```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
```

**Key Changes:**
- Add a descriptive `name` for the workflow
- Replace GitLab's implicit triggers with explicit `on:` triggers
- Remove Docker-in-Docker configuration (GitHub runners have Docker pre-installed)
- Remove global `image` and `services` definitions

### Step 3: Convert the Build Job

**GitLab CI/CD:**
```yaml
stages:         
  - build

build-job:
  stage: build
  image: aymdev/dind-compose
  before_script:
    - docker version
    - apk add --no-cache py-pip
    - pip install docker-compose
    - docker-compose version 
  script:
    - docker-compose build
```

**GitHub Actions:**
```yaml
jobs:
  build:
    name: Build (docker-compose)
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Show Docker and Docker Compose info
        run: |
          docker --version
          docker compose version

      - name: Free disk space
        run: |
          sudo rm -rf /usr/share/dotnet
          sudo rm -rf /usr/local/lib/android
          docker image prune -a -f

      - name: Build containers with docker compose
        run: docker compose build
```

**Key Changes:**
1. **Job structure**: `build-job` → `build` (under `jobs:`)
2. **Runner**: `image: aymdev/dind-compose` → `runs-on: ubuntu-latest`
3. **Checkout**: Add explicit `actions/checkout@v4` step (GitLab does this automatically)
4. **Steps**: Convert `before_script` and `script` into individual `steps`
5. **Docker Compose**: Use `docker compose` (v2 syntax) instead of `docker-compose`
6. **No setup needed**: Docker and Docker Compose are pre-installed on GitHub runners

### Step 4: Convert the Static Analysis Job

**GitLab CI/CD:**
```yaml
flake8:
  stage: static_analysis
  image: "python:3.9"
  before_script:
    - python --version
    - pip --version
    - pip install -U flake8
  script:
    - flake8 --max-line-length=120 backend/src
```

**GitHub Actions:**
```yaml
  flake8:
    name: Static analysis - flake8
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python 3.9
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install flake8
        run: |
          python -m pip install --upgrade pip
          pip install -U flake8

      - name: Run flake8
        run: flake8 --max-line-length=120 backend/src
```

**Key Changes:**
1. **Python setup**: Instead of `image: "python:3.9"`, use the `actions/setup-python@v4` action
2. **Parallel execution**: This job runs in parallel with `build` (no stage dependency)
3. **Explicit steps**: Each logical action gets its own named step for clarity

### Step 5: Convert the Test Job with Dependencies

**GitLab CI/CD:**
```yaml
unit-test-job:
  stage: test
  image: aymdev/dind-compose
  before_script:
    - docker-compose build --parallel
    - docker-compose up -d natl_backend_api db
  script:
    - docker-compose run --rm test || exit $?
```

**GitHub Actions:**
```yaml
  unit-tests:
    name: Unit tests (docker-compose)
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Show Docker and Docker Compose info
        run: |
          docker --version
          docker compose version

      - name: Build required containers
        run: docker compose build --parallel

      - name: Start backend and db services
        run: docker compose up -d natl_backend_api db

      - name: Run tests (inside test container)
        run: docker compose run --rm test
```

**Key Changes:**
1. **Dependencies**: `stage: test` (runs after `static_analysis`) → `needs: build` (explicit dependency)
2. **Error handling**: Remove `|| exit $?` - GitHub Actions automatically fails on non-zero exit codes
3. **Stage vs needs**: GitLab uses stages for ordering; GitHub Actions uses `needs` for explicit dependencies

---

## Key Concept Mappings

### 1. Stages → Jobs with Dependencies

**GitLab Stages (Sequential):**
```yaml
stages:
  - build
  - static_analysis
  - test

job1:
  stage: build

job2:
  stage: static_analysis  # Waits for all 'build' jobs

job3:
  stage: test  # Waits for all 'static_analysis' jobs
```

**GitHub Actions (Explicit Dependencies):**
```yaml
jobs:
  job1:
    runs-on: ubuntu-latest
    # Runs immediately
  
  job2:
    runs-on: ubuntu-latest
    # Runs in parallel with job1 (no dependency)
  
  job3:
    runs-on: ubuntu-latest
    needs: job1  # Explicit dependency - waits only for job1
```

**Benefits of GitHub Actions approach:**
- Jobs without dependencies run in parallel automatically
- More granular control over dependencies
- Faster pipeline execution

### 2. Images → Runners and Actions

**GitLab (Custom Images):**
```yaml
job:
  image: python:3.9
  script:
    - python --version
```

**GitHub Actions (Setup Actions):**
```yaml
job:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    - run: python --version
```

**Common Setup Actions:**
- `actions/setup-python@v4` - Set up Python
- `actions/setup-node@v4` - Set up Node.js
- `actions/setup-java@v4` - Set up Java
- `actions/checkout@v4` - Checkout repository code

### 3. Before Script → Multiple Steps

**GitLab (before_script):**
```yaml
job:
  before_script:
    - echo "Setup step 1"
    - echo "Setup step 2"
  script:
    - echo "Main step"
```

**GitHub Actions (Named Steps):**
```yaml
job:
  runs-on: ubuntu-latest
  steps:
    - name: Setup step 1
      run: echo "Setup step 1"
    
    - name: Setup step 2
      run: echo "Setup step 2"
    
    - name: Main step
      run: echo "Main step"
```

**Benefits:**
- Better visibility in logs
- Each step can be independently monitored
- Easier to debug failures

### 4. Docker Compose Commands

**GitLab CI/CD:**
```yaml
script:
  - docker-compose build
  - docker-compose up -d service
  - docker-compose run --rm test
```

**GitHub Actions:**
```yaml
steps:
  - run: docker compose build
  - run: docker compose up -d service
  - run: docker compose run --rm test
```

**Note:** GitHub runners use Docker Compose V2 (`docker compose`) by default, not V1 (`docker-compose`).

---

## Testing Your Workflow

### Local Testing (Optional)

You can test GitHub Actions workflows locally using [act](https://github.com/nektos/act):

```bash
# Install act
brew install act  # macOS
# or
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash  # Linux

# Run workflows locally
act                    # Run default event (push)
act pull_request       # Run pull request event
act -j build           # Run specific job
```

### Push and Monitor

1. **Commit and push your workflow:**
   ```bash
   git add .github/workflows/ci.yml
   git commit -m "Add GitHub Actions CI workflow"
   git push origin your-branch
   ```

2. **Monitor on GitHub:**
   - Go to your repository on GitHub
   - Click the **Actions** tab
   - You'll see your workflow running
   - Click on a run to see detailed logs for each job and step

### Common Issues and Solutions

#### Issue 1: Workflow not triggering
**Solution:** Check that:
- File is in `.github/workflows/` directory
- YAML syntax is valid
- Branch matches the `on:` trigger configuration

#### Issue 2: Docker Compose not found
**Solution:** Use `docker compose` (V2) instead of `docker-compose` (V1)

#### Issue 3: Tests fail in GitHub Actions but work locally
**Solution:** Check:
- Environment variables
- Service startup timing (add health checks or wait scripts)
- Disk space (GitHub runners have limited space)

#### Issue 4: Jobs running in wrong order
**Solution:** Add explicit `needs:` dependencies:
```yaml
job2:
  needs: job1  # Wait for job1 to complete
```

---

## Quick Reference: Side-by-Side Comparison

| Feature | GitLab CI/CD | GitHub Actions |
|---------|--------------|----------------|
| **Workflow file** | `.gitlab-ci.yml` | `.github/workflows/ci.yml` |
| **Job definition** | `job-name:` | `jobs: job-name:` |
| **Runner** | `image: ubuntu` | `runs-on: ubuntu-latest` |
| **Checkout code** | Automatic | `uses: actions/checkout@v4` |
| **Commands** | `script:` | `steps: - run:` |
| **Setup tasks** | `before_script:` | Separate `steps:` |
| **Dependencies** | `stage:` (implicit order) | `needs:` (explicit) |
| **Trigger on push** | Default | `on: push:` |
| **Environment vars** | `variables:` | `env:` |
| **Docker** | Requires DinD setup | Pre-installed |

---

## Advanced Topics

### Parallel Jobs

**GitLab (same stage):**
```yaml
stages:
  - test

test-job-1:
  stage: test
  script: echo "Test 1"

test-job-2:
  stage: test
  script: echo "Test 2"
```

**GitHub Actions (no dependencies):**
```yaml
jobs:
  test-1:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Test 1"
  
  test-2:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Test 2"
```

### Matrix Builds

Test against multiple versions:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', 3.11]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - run: python --version
```

### Caching Dependencies

Speed up builds with caching:

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: actions/setup-python@v4
    with:
      python-version: '3.9'
      cache: 'pip'
  - run: pip install -r requirements.txt
```

---

## Conclusion

Converting from GitLab CI/CD to GitHub Actions involves:

1. ✅ Creating `.github/workflows/` directory structure
2. ✅ Adding explicit code checkout steps
3. ✅ Replacing `image:` with `runs-on:` and setup actions
4. ✅ Converting stages to jobs with `needs:` dependencies
5. ✅ Breaking `before_script` and `script` into named steps
6. ✅ Using Docker Compose V2 syntax (`docker compose`)
7. ✅ Leveraging pre-installed tools on GitHub runners

The GitHub Actions approach provides:
- Better parallelization (jobs run concurrently by default)
- Clearer dependency management
- Rich ecosystem of reusable actions
- Native Docker support without DinD complexity

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Migrating from GitLab CI/CD to GitHub Actions](https://docs.github.com/en/actions/migrating-to-github-actions/migrating-from-gitlab-cicd-to-github-actions)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
