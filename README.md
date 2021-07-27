# lucycashflow

You can check on line: [https://lucycashflow.herokuapp.com/](https://lucycashflow.herokuapp.com/). 

p.s. This project it is only for study proposal. Feel free to use it,
but please do not open issues. I do not intend to answer any questions. 

## Last update

- Version 1.1
- *Tue 2021-07-27 19:42:37 -04*, verifique os logs <a href="#logss">aqui</a>.

## Motivation

I would like to learn how to handle with databases, html, and
requests. I tough that a simple and small project could be useful to
improve my skills about computer science. Thus I tried to provide an
open source program for personal finances management. Furthermore I can
archive my spreadsheet and work on my own program. ;)

Why an app to financial management?

Organize financial book is a good way to improve life. Now days there
are several on line sheets, apps for mobile, etc. However, once your data
is on the internet, probably always it will be.
 
Thinking in privacy, `lucyCashflow` was created. It's a quite simple app
to run in your own personal machine. The functions are store,
categorize, and report money inputs and outputs. Intending to simplify
the use, some categories and sub-categories were assigned (the
categories are in Portuguese, Sorry!):

## Installation

Requirements:

- python3 and packages:
    - flask
    - flask_bootstrap
    - import pandas as pd
    - json
- SQLITE3

Usually python3 and SQLITE3 are already available on your operational system. To
install the libraries you can use `pip3`:

`pip3 install <package name>`

Download:

Create a specific folder for this app. Download the all content from
GitHub and unzip in the folder that you created.

## How to use

0. go to terminal and access the folder that you created for the app.
1. remove the file `db_lucycashflow.db`, it is because the database from github is not clean.
2. create a new database, just run: `python3 create_tables.py` . This new database has one account called "MyWallet"

*note: you just need to do the above steps once, but if for some reason you want create a new database, feel free to repeat.*

## How to launch

In terminal, go to the folder that you had created and type:

`python3 app_lucycashflow.py`

It will return a local address like: `http://127.0.0.1:5000/`, just copy
and paste on your browser (Firefox, Chromium, Chrome, etc). Now I hope
you have fun.

## What you can do

- Create accounts
- Insert expenses and incomes and categorize by type
- Transfers between accounts
- Manage transactions
- View reports:
  - cash flow by period
  - account statement
  - balance by account
  - expenses by category

## Development

- DONE Modeling DB (Portuguese);

<img src="/models/dbsql_model.png" alt="" width="300">

- DONE Backend for transactions (SQLITE3);
- DONE FLASK structure
- DONE Logic for transference 
- DONE Reports [100%]
  - [X] Back end balance
  - [X] Front end balance
  - [X] Back end bank statement
  - [X] Front end bank statement
  - [X] Balance group by account
  - [X] Monthly cash flow 
  - [X] Plot monthly cash flow
  - [X] Expenses by categories
  - [X] Expenses by subcategories
  - [X] Floating point for sums
  - [X] Improve cash flow plot
  - [X] Improve balance by account for a specific period
  - [X] Improve reports
  - [X] Deploy in some server
  - [ ] Verify locks for income data as expenses and vice versa
   

## Logs 
<a name="logss"></a> 

### Tue 2021-07-27 19:42:37 -04
- Total of incomes has been included on incomes report

### Sun 2021-07-25 12:27:32 -04
- A incomes report has been included.

### Thu 2021-05-13 11:42:37 -04
- Improvements cashflow chart and update to jsChart 3.0

### Thu 2021-01-28 17:32:37 -04
- Reports has been updated (cashflow, balance, expenses, ...), 

### Sun 2020-09-20 10:20:11 -04
- Updated subcategories, a new one subcategory for vehicle was
added. Two weeks ago the app as deployed on Heroku
[https://lucycashflow.herokuapp.com/](https://lucycashflow.herokuapp.com/). 

### Tue 2020-07-21 19:05:54 -04
- Modeling was altered, the number of categories was decreased. Balance
for account is done. Floating point for sums has been fixed (cents).

### Sat 2020-07-04 18:00:00 -04
- Expenses by categories and subcategories was implemented.

### Sat 2020-07-04 15:33:50 -04
- Readme file improvements.

### Thu 2020-06-30 05:08:06 -04
- A bar plot (first experience with java script) with monthly cash flow
is working in `relatorio.html`. The bars show up after period assignment
and click button. At moment the code is messy. Sub directory were
created for js library.

### Thu 2020-06-25 06:18:14 -04
- A `html` with menu were create for period reports. Balance for
accounts were implemented on front end and back end

### Tue 2020-06-23 23:31:27 -04
- Period report and balance for each account on `extrato.html` and
`app_lucycashflow.py`. The queries for it are in
`./models/genextratos.py`. 

### Mon 2020-18-22 22:10:37 -04
- First README
