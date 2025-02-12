
# Continuous-Integration-Group10

# Continuous Integration Project - DD2480 Assignment 2

## Overview

The project is a python CI service.

## Project Structure


```
CONTINUOUS-INTEGRATION-GROUP10//
├── src/
│   ├── CommitStatus.py
│   ├── ContinuousIntegrationServer.py
│   ├── Database.py
│   ├── __init__.py
│   ├──templates/
│   │   ├── build.html
│   │   ├── build_history.html
├── tests/
│   ├── mock_test/
│   │   ├── tests/
│   │   │   ├──test.py
│   │   │   ├──setup.py
│   ├── __init__.py
│   ├── testCloneRepoTest.py
│   ├── testCommitStatus.py
│   ├── testDatabase.py
│   ├── testRunTests.py
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── setup.py

```
## Prerequisites
   - Python (atleast version 3.10)


## Installation & Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/jannikhoesch/Continuous-Integration-Group10.git
   cd CONTINUOUS-INTEGRATION-GROUP10
   ```
2. Install dependencies
   ```sh
   pip install -r requirements.txt
   ```
3. Create a .env file identical to .env.example and add your github token.

## Running the server
   ```sh
   cd src
   python ContinuousIntegrationServer.py
   ```

## Contributing

1. Fork the repository
2. Create an issue
3. Create a feature branch (`git checkout -b {branchname}`)
4. Commit your changes (`git commit`)
5. Push to the branch (`git push origin {branchname}`)
6. Open a Pull Request

## Commit Naming Convention

Title: `{type}: {title}`  
Description: `{description of change} #{issueNr}`

## Branch Naming Convention

Title: `issue/{issueNr}`  
Description: `{description of change} #{issueNr}`

---
## Way of Working  

We continued with a similar workflow from how we completed assignment 1. This time we were a bit more used to using git. Using the **Essence Standard Checklist**, we currently consider ourselves to be in the **“In Place”** state since using the tools is working properly, but we are still not entirely used to working with Git in this way yet, which causes some problems to arise from time to time. We believe, however, that more practice will optimize our way of working and that we are on a good path to reaching an efficient workflow.  

## Task Distribution

### **Harald**

- **Tasks:**
   - P3 (including github token management)
   - README.md
   - requirements.txt
   - .gitignore

---

### **Jannik**

- **Tasks:**

---

### **Amanda**

- **Tasks:**

---

### **Zyad**

- **Tasks:**
