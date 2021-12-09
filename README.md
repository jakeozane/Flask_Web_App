# Notasting CS 340 Project

Authors:
- Jacob Morrow
- Lyell Read

## Notes

- Data Definition Queries (`./notasting_db_ddq.sql`) can be imported using `mysql` commandline utility.
- This website is known to be extremely vulnerable to SQL Injection.

## Project Submission Folder Structure

```
├── images --------------------------- Images used in rendering portfolio
│    └── ...
├── notasting_db_ddq.sql ------------- Data Definition Queries
├── notasting_db_dmq.sql ------------- Data Manipulation Queries
├── notasting-project ---------------- Project Source Code (see below)
│    └── ...
├── portfolio.md --------------------- Portfolio in MarkDown / Latex Mixed Format
├── portfolio.pdf -------------------- Rendered Portfolio in PDF Format
└── README.md ------------------------ This File.
```

## Source Code Structure

```
notasting-project
├── config.py.example ---------------- Example DB Configuration
├── connector.py --------------------- Database Connector Module
├── README.md ------------------------ README
├── requirements.txt ----------------- pip requirements. See README.md
├── server.py ------------------------ Web server code
├── static --------------------------- Statically Served Files
│    └── css ------------------------- Statically Served CSS Files
│         └── style.css -------------- Main CSS File
└── templates ------------------------ Jinja2 Templates
    ├── inventories.j2 --------------- Template for Inventories view
    ├── main.j2 ---------------------- Template for Home view
    ├── product.j2 ------------------- Template for Product Update view
    ├── products.j2 ------------------ Template for Products view
    ├── productspurchased.j2 --------- Template for ProductsPurchased view
    ├── productspurchased_update.j2 -- Template for ProductsPurchased Update view
    ├── salesdata.j2 ----------------- Template for SaleData view
    ├── thirdparties.j2 -------------- Template for ThirdParties view
    └── userdata.j2 ------------------ Template for UserData view
```


