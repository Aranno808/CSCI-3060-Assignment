<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
![Contributors][contributors-shield]
![Issues][issues-shield]


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="">
    <img width="200" height="200" alt="bank" src="https://github.com/user-attachments/assets/bee9c564-3d1e-482e-9bda-632506d09c7c" />
  </a>
</div>

<!-- PROJECT HEADER SECTION (Links need to be added later down the line) -->

<h3 align="center">
  <a>Banking System</a>
</h3>


  <p align="center">
    System managing account balances and transactions.
    <br />
    <a href=""><strong>Explore the docs (Coming Soon)»</strong></a>
    <br />
    <br />
    <a href="">View Demo</a>
    &middot;
    <a href="">Report Bug</a>
    &middot;
    <a href="">Request Feature</a>
  </p>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href=#architecture>Architecture</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#tests">Running Automated Tests</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

<img width="200" height="200" alt="bank" src="https://github.com/user-attachments/assets/bee9c564-3d1e-482e-9bda-632506d09c7c" />

The Banking System is a modular command-line application that simulates core banking operations including withdrawals, deposits, transfers, bill payments, and administrative account management.
The system enforces strict banking rules, session controls, and privilege levels while serializing transactions for backend processing.

Key Features:
* Modular architecture
* Session-based login system (Standard & Admin roles)
* Banking rule enforcement (limits, balance checks, validation)
* Admin operations (create, delete, disable, change plan)
* Transaction serialization
* Automated regression testing with shell script framework

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

![Python][Python]
<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Architecture

<img width="1706" height="900" alt="mermaid-diagram-2026-02-13-015709" src="https://github.com/user-attachments/assets/19192f01-1a31-4f41-8f77-5b5c1f31bd81" />

Editable Mermaid source: `docs/uml-class-diagram.md`

## Getting Started

To get a local copy up and running follow these steps.

### Prerequisites

* Python 3.9+

### Installation

1. Clone the repo
```sh
git clone https://github.com/Aranno808/CSCI-3060-Assignment
cd CSCI-3060-Assignment
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage
This repository has two command-line entry points:

* `frontend/main.py` handles interactive banking sessions and writes a daily transaction file
* `backend/main.py` applies a merged transaction file to a master accounts file

### Frontend

Run the frontend from the repository root:
```sh
python frontend/main.py frontend/accounts.txt frontend/outputs/manual.atf
```

Arguments:

* `accounts_file`: the current accounts file to load at login
* `transaction_output_file`: where the session's serialized transactions will be written on logout

Example interactive session:
```text
Banking System
> login
Enter session kind (admin/standard): standard
Enter account holder name: Ifeanyi
> paybill
Enter account number: 10002
Enter company name: EC
Enter amount to pay: 100
Pay bill successful.
> logout
```

This produces a transaction file like:
```text
03 Ifeanyi              10002 00100.00 EC
00                      00000 00000.00
```

You can also replay one of the included test scenarios without typing anything manually:
```sh
python frontend/main.py frontend/accounts.txt frontend/outputs/paybill_success.atf < frontend/inputs/paybill_success.txt
```

Useful frontend files already included in the repo:

* `frontend/accounts.txt`: starter account data used by the frontend
* `frontend/inputs/*.txt`: scripted command sequences for stdin-driven runs
* `frontend/expected/*.etf`: expected transaction-file outputs
* `frontend/expected/*.out`: expected terminal output logs

Example current accounts file:
```text
10001 Aedin                A 00050.00
10002 Ifeanyi              A 01050.00
10003 Aranno               A 00500.00
10004 Jhaden               D 01500.00
00000 END_OF_FILE          A 00000.00
```

Field layout:

* account number: 5 digits
* account holder name: 20 characters
* status: `A` for active or `D` for disabled
* balance: fixed-width amount in dollars

### Backend

Run the backend from the repository root:
```sh
python backend/main.py <old_master_accounts_file> <merged_transactions_file> <new_current_accounts_file> <new_master_accounts_file>
```

Example:
```sh
python backend/main.py backend/old_master_accounts.txt backend/merged_transactions.txt backend/new_current_accounts.txt backend/new_master_accounts.txt
```

Create the two input files first, then run the command above.

The backend expects:

`old_master_accounts.txt`
```text
10001 Alice                A 01000.00 0000 SP
10002 Bob                  A 00500.00 0000 NP
00000 END_OF_FILE          A 00000.00 0000 NP
```

`merged_transactions.txt`
```text
04 Alice                10001 00050.00
02 Alice                10001 00025.00 10002
00                      00000 00000.00
```

With those inputs, the backend writes output files similar to:

`new_current_accounts.txt`
```text
10001 Alice                A 01024.90 SP
10002 Bob                  A 00525.00 NP
00000 END_OF_FILE          A 00000.00 NP
```

`new_master_accounts.txt`
```text
10001 Alice                A 01024.90 0002 SP
10002 Bob                  A 00525.00 0000 NP
00000 END_OF_FILE          A 00000.00 0000 NP
```

### Common Workflows

Create a transaction file from one frontend session:
```sh
python frontend/main.py frontend/accounts.txt frontend/outputs/session.atf
```

Replay an included admin scenario:
```sh
python frontend/main.py frontend/accounts.txt frontend/outputs/admin_create_success.atf < frontend/inputs/admin_create_success.txt
```

Inspect the expected output for comparison:
```sh
cat frontend/expected/admin_create_success.etf
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Running Automated Tests
The automated test scripts live in `frontend/` and are written for a POSIX shell such as Git Bash, WSL, or Linux/macOS.

From the repository root:
```sh
cd frontend
chmod +x run_tests.sh
./run_tests.sh
```
This will: 
- Execute all the test cases in the `inputs` directory
- Create outputs in the `outputs` directory

```sh
chmod +x check_tests.sh
./check_tests.sh
```
This will: 
- Diff outputs against the files in `expected/` and print the test result (PASS / FAIL)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Shield Links -->
[Python]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[contributors-shield]: https://img.shields.io/github/contributors/Aranno808/CSCI-3060-Assignment.svg?style=for-the-badge
[issues-shield]: https://img.shields.io/github/issues/Aranno808/CSCI-3060-Assignment.svg?style=for-the-badge
