# Notasting - Database Project


Authors:
- Jacob Morrow
- Lyell Read

## Outline
Notasting, ‘totally not a CIA operation’, sells $1 million of questionable goods a year. To support
this, a database-driven website was implemented in order to record the sales data related to orders
of purchased products from inventory to users whose user information is being sold to third parties.
Essentially, the database will be used to track orders and how that order information has been sold
on to third party information aggregators. This is so that Notasting can understand how their
operations are related to the CIA surveillance they are ‘totally not participating in’.
The database will relate Products to SaleData using ProductsPurchased, an intersection of those
two entities. Further, Products will be related to Inventory in one of the central warehouses that
Notasting runs. The SaleData will be associated with UserData for the user that made the purchase,
and that UserData will be associated with a ThirdParty to whom that UserData was exclusively
sold.

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


