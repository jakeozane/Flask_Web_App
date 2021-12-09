# Web Server for CS 340: Databases, Fall, 2021
# Authors:
#   - Jacob Morrow
#   - Lyell Read

# Sources Cited:
#   - Base Flask + MySQL Code from https://stackoverflow.com/questions/9845102/using-mysql-in-flask
#   - Supporting code from CS340 Materials
#   - Additional Flask Config from https://edstem.org/us/courses/14452/discussion/644173
#   - Flask + Jinja 2 templating from https://github.com/gkochera/CS340-demo-flask-app

from flask import Flask, render_template, redirect, request
import os
import connector as db


#
#
#  HELPER FUNCTIONS
#
#


def is_number(string):

    """
    Helper to determine whether a user-provided string is a float / number
    or not. Source:
    https://elearning.wsldp.com/python3/python-check-string-is-a-number/
    """

    try:
        float(string)
        return True
    except ValueError:
        return False


def get_all(table):

    """
    Helper to get all rows in a database table indicated
    by argument table
    """

    query = f"SELECT * FROM {table};"
    return execute_query(query)


def execute_query(query, query_params=()):

    """
    Helper to execute a query with optional arguments in the
    database and return the matching rows. Essentially, this
    is a wrapper around db.execute_query, however it
    facilitates optional arguments.
    """

    db_connection.ping()
    cursor = db.execute_query(
        db_connection=db_connection, query=query, query_params=query_params
    )
    ret = cursor.fetchall()
    cursor.close()
    return ret


def get_informative_productspurchased():

    """
    Add helpful items to the returned dictionary that will be used
    in the table of products purchased so that it's not just a set
    of IDs.

    These helpful items have the PK for the value that the FK
    relates to in order to help the user see what the FK IDs mean
    """

    productspurchased_inforamative = get_all("ProductsPurchased")
    products = get_all("Products")
    purchases = get_all("SaleData")

    for x in productspurchased_inforamative:

        # Find products with same ID, add them to the dictionary
        for y in products:
            if y["productID"] == x["productID"]:
                x["informativeProductID"] = (
                    f"{x['productID']}" + f" ({y['productName']})"
                )

        # Find purchases with same ID, add them to dictionary
        for y in purchases:
            if y["purchaseID"] == x["purchaseID"]:
                x["informativePurchaseID"] = f"{x['purchaseID']}" + f" ({y['total']})"

    return productspurchased_inforamative


# Instantiate the server and database connection to be used
server = Flask(__name__)
db_connection = db.connect_to_database()


#
#
#  INDEX
#
#


@server.route("/")
def index():

    """
    Main route for the index / main page
    """

    return render_template("main.j2")


#
#
#   INVENTORIES
#
#


@server.route("/inventories", methods=["GET", "POST"])
def inventories():

    """
    Route to get and add a new inventory from the database table Inventories

    GET: Will display a table of all inventories
    POST: Will allow the user to add a new inventory
    """

    if request.method == "GET":

        # Simple GET returns simple page
        return render_template("inventories.j2", inventories=get_all("Inventories"))

    elif request.method == "POST":
        try:
            # Post needs to parse args first
            args = request.form.get("location")

            # Check if no required args are blank
            if args != "":

                # Add new item as required
                query = "INSERT INTO Inventories (location) VALUES (%s);"
                results = execute_query(query, args)

                return render_template(
                    "inventories.j2", inventories=get_all("Inventories"), success=True
                )
            # Invalid arguments
            else:
                return render_template(
                    "inventories.j2",
                    inventories=get_all("Inventories"),
                    error="Location parameter cannot be empty",
                )

        except Exception as e:

            # Encountered issue in the function above. Report to the user
            return render_template(
                "inventories.j2",
                inventories=get_all("Inventories"),
                error=str(e)[:100] + "...",
            )

    else:

        # Catch-all for a case that should never happen.
        return redirect("/", code=404)


@server.route("/inventories/inventory/delete/<del_id>", methods=["GET", "POST"])
def delete_inventory(del_id):

    """
    Route to delete an inventory
    """

    try:

        # Try to UPDATE all foreign keys to null
        query = "UPDATE Products SET inventoryID = NULL WHERE inventoryID = (%s);"
        results = execute_query(query, (str(del_id)))

        # Try to DELETE the FKs in inventories
        query = "DELETE FROM Inventories WHERE inventoryID = (%s);"
        results = execute_query(query, (str(del_id)))

        # On success, return successful dialog and render the main Inventories page
        return render_template(
            "inventories.j2", inventories=get_all("Inventories"), success=True
        )

    except Exception as e:

        # Return error dialog on the main Inventories page
        return render_template(
            "inventories.j2",
            inventories=get_all("Inventories"),
            error=str(e)[:100] + "...",
        )


#
#
#   PRODUCTS
#
#


@server.route("/products", methods=["GET", "POST"])
def products():

    """
    Route to serve and display the products from the Products table
    and allow for modification and deletion

    GET will get the list of products from the Products table
    POST will add a new item from the database
    """

    if request.method == "GET":

        # Return the products page rendered with Inventories data for drop-downs
        return render_template(
            "products.j2",
            products=get_all("Products"),
            inventories=get_all("Inventories"),
        )

    elif request.method == "POST":
        try:
            # Make sure that all required arguments are populated
            if (
                request.form.get("productName") == ""
                or request.form.get("inventoryID") == ""
                or request.form.get("price") == ""
            ):
                # Some arguments(s) is/are empty, return an error.
                return render_template(
                    "products.j2",
                    products=get_all("Products"),
                    inventories=get_all("Inventories"),
                    error="Only Description parameter is optional.",
                )

            elif not is_number(request.form.get("price")):

                # The price provided is not an int or float
                return render_template(
                    "products.j2",
                    products=get_all("Products"),
                    inventories=get_all("Inventories"),
                    error="Price must be a numeric value.",
                )

            # Null inventory case must be handled separately as it will require
            # SQL syntax that contains NULL not string 'NULL', therefore a
            # special query is crafted for this case.
            elif request.form.get("inventoryID") == "NULL":
                args = (
                    request.form.get("productName"),
                    request.form.get("description"),
                    request.form.get("price"),
                )
                query = (
                    "INSERT INTO Products (productName,"
                    + " description, price, inventoryID) VALUES (%s, %s, %s, NULL);"
                )

            # Just a standard product delete with all good arguments and no
            # NULL FK
            else:
                args = (
                    request.form.get("productName"),
                    request.form.get("description"),
                    request.form.get("price"),
                    request.form.get("inventoryID"),
                )
                query = (
                    "INSERT INTO Products (productName,"
                    + " description, price, inventoryID) VALUES (%s, %s, %s, %s);"
                )

            # Run whichever query is appropriate with the given args from above
            results = execute_query(query, args)

            # Return the products page rendered with Inventories data for drop-downs
            # Add success dialog
            return render_template(
                "products.j2",
                products=get_all("Products"),
                inventories=get_all("Inventories"),
                success=True,
            )

        except Exception as e:
            # An error was caught. Inform the user using the error dialog.
            return render_template(
                "products.j2",
                products=get_all("Products"),
                inventories=get_all("Inventories"),
                error=str(e)[:100] + "...",
            )

    # Catch all in case request is not POST or GET
    else:
        return redirect("/", code=404)


@server.route("/products/update/<product_id>", methods=["GET", "POST"])
def product_update(product_id):

    """
    Product modification page.

    GET will get the page, prefilled with the product details requested
    POST will edit the product in the database
    """

    if request.method == "GET":

        # Getting the modify page. This requires that the current product's
        # information be gotten from the db to fill in the current values
        query = "SELECT * FROM Products WHERE productID=%s;"
        prod = execute_query(query, (str(product_id)))

        # Render the template for GET
        return render_template(
            "product.j2", product=prod, inventories=get_all("Inventories")
        )

    if request.method == "POST" and request.form.get("productName") != "":
        try:
            # Check required arguments are not empty. If they are, return an error
            if (
                request.form.get("productName") == ""
                or request.form.get("inventoryID") == ""
                or request.form.get("price") == ""
            ):
                # Return the products page rendered with Inventories data for drop-downs
                # with the error dialog indicating error
                return render_template(
                    "products.j2",
                    products=get_all("Products"),
                    inventories=get_all("Inventories"),
                    error="Only Description parameter is optional.",
                )

            elif not is_number(request.form.get("price")):
                # Error if the price is not a float or int. This will return the products
                # page rendered with Inventories data for drop-downs and include the
                return render_template(
                    "products.j2",
                    products=get_all("Products"),
                    inventories=get_all("Inventories"),
                    error="Price must be a numeric value.",
                )

            else:
                # Args are filled, and price is a number. Therefore, we are ready
                # to update entry.
                args = (
                    request.form.get("productName"),
                    request.form.get("description"),
                    request.form.get("price"),
                    request.form.get("inventoryID"),
                    str(product_id),
                )

                query = (
                    "UPDATE Products SET productName = (%s), description = (%s),"
                    + "price = (%s), inventoryID = (%s) WHERE productID = (%s)"
                )
                results = execute_query(query, args)

            # Return the products page rendered with Inventories data for drop-downs
            # and success dialog
            return render_template(
                "products.j2",
                products=get_all("Products"),
                inventories=get_all("Inventories"),
                success=True,
            )

        except Exception as e:
            # Caught an error while executing. Return an error dialog when we
            # return the products page rendered with Inventories data for drop-downs
            return render_template(
                "products.j2",
                products=get_all("Products"),
                inventories=get_all("Inventories"),
                error=str(e)[:100] + "...",
            )

    # Catch all to account for anything unintended
    return redirect("/", code=404)


@server.route("/products/delete/<product_id>", methods=["GET", "POST"])
def product_delete(product_id):

    """
    Product modification page.

    GET will get the page, prefilled with the product details requested
    POST will edit the product in the database
    """

    if request.method == "GET":

        # User should never get this page, if so just redirect
        return redirect("/", code=404)

    if request.method == "POST":

        try:
            # Try to delete the entry that the user specified.
            query = (
                "UPDATE ProductsPurchased SET productID = NULL WHERE productID = (%s);"
            )
            results = execute_query(query, (str(product_id)))

            query = "DELETE FROM Products WHERE productID = (%s);"
            results = execute_query(query, (str(product_id)))

            # Return the products page rendered with Inventories data for drop-downs
            # and success dialog.
            return render_template(
                "products.j2",
                products=get_all("Products"),
                inventories=get_all("Inventories"),
                success=True,
            )

        except Exception as e:
            # Return the products page rendered with Inventories data for drop-downs
            # with error dialog containing the caught error.
            return render_template(
                "products.j2",
                products=get_all("Products"),
                inventories=get_all("Inventories"),
                error=str(e)[:100] + "...",
            )

    # Catch all to account for anything unintended
    return redirect("/", code=404)


#
#
#   PRODUCTS PURCHASED
#
#


@server.route("/productspurchased", methods=["GET", "POST"])
def productspurchased():

    """
    Route to serve products purchased from the ProductsPurchased
    table in the database

    GET will get all the products purchased
    POST will allow the user to add a productspurchased relationship
    """

    if request.method == "GET":

        # Sends the results back to the web browser.
        return render_template(
            "productspurchased.j2",
            productspurchased=get_informative_productspurchased(),
            products=get_all("Products"),
            salesdata=get_all("SaleData"),
        )

    if request.method == "POST":

        try:
            # Check arguments that are required are not blank
            if (
                request.form.get("productID") == ""
                or request.form.get("purchaseID") == ""
            ):
                # Blank args, return error dialog
                return render_template(
                    "productspurchased.j2",
                    productspurchased=get_informative_productspurchased(),
                    products=get_all("Products"),
                    salesdata=get_all("SaleData"),
                    error="Both Product ID and Purchase ID are required.",
                )
            else:
                # No blank arguments, good to go
                args = (request.form.get("productID"), request.form.get("purchaseID"))

                query = "INSERT INTO ProductsPurchased (productID, purchaseID) VALUES (%s, %s);"
                results = execute_query(query, args)

                # Return the page with the success dialog
                return render_template(
                    "productspurchased.j2",
                    productspurchased=get_informative_productspurchased(),
                    products=get_all("Products"),
                    salesdata=get_all("SaleData"),
                    success=True,
                )

        except Exception as e:
            # Return the page with the error dialog included, as we caught
            # an error during function execution.
            return render_template(
                "productspurchased.j2",
                productspurchased=get_informative_productspurchased(),
                products=get_all("Products"),
                salesdata=get_all("SaleData"),
                error=str(e)[:100] + "...",
            )


@server.route(
    "/productspurchased/delete/<product_id>/<purchase_id>", methods=["GET", "POST"]
)
def delete_productspurchased(product_id, purchase_id):

    """
    Route to delete a productspurchased relationship

    This route exists as HTML forms cannot issue DELETE requests, and
    thus this is handled in a route
    """

    try:
        # Handle the case where productID us null separately, as we must ensure
        # the SQL syntax contains `is NULL` rather than `= 'NULL'`
        if product_id == "None":

            query = "DELETE FROM ProductsPurchased WHERE (productID is NULL AND purchaseID = (%s)) LIMIT 1;"
            results = execute_query(query, (str(purchase_id)))

        else:

            query = "DELETE FROM ProductsPurchased WHERE (productID = (%s) AND purchaseID = (%s)) LIMIT 1;"
            results = execute_query(query, (str(product_id), str(purchase_id)))

        # Return the view with the success dialog rendered
        return render_template(
            "productspurchased.j2",
            productspurchased=get_informative_productspurchased(),
            products=get_all("Products"),
            salesdata=get_all("SaleData"),
            success=True,
        )

    except Exception as e:
        # An error was caught, return the error dialog with the error message
        return render_template(
            "productspurchased.j2",
            productspurchased=get_informative_productspurchased(),
            products=get_all("Products"),
            salesdata=get_all("SaleData"),
            error=str(e)[:100] + "...",
        )


@server.route(
    "/productspurchased/update/<product_id>/<purchase_id>", methods=["GET", "POST"]
)
def update_productspurchased(product_id, purchase_id):

    """
    Route to update a productspurchased relation
    """

    if request.method == "GET":
        # Handle the case where productID us null separately, as we must ensure
        # the SQL syntax contains `is NULL` rather than `= 'NULL'`
        if product_id == "None":

            query = "SELECT * FROM ProductsPurchased WHERE (productID IS NULL AND purchaseID=%s);"
            results = execute_query(query, (str(purchase_id)))

        else:

            query = "SELECT * FROM ProductsPurchased WHERE (productID=%s AND purchaseID=%s);"
            results = execute_query(query, (str(product_id), str(purchase_id)))

        # Return the view filled with the required information.
        return render_template(
            "productspurchased_update.j2",
            product=results,
            products=get_all("Products"),
            saledata=get_all("SaleData"),
        )

    if request.method == "POST":

        try:
            # Check required arguments are not empty
            if (
                request.form.get("productID") == ""
                or request.form.get("purchaseID") == ""
            ):
                # Some args are empty, return an error dialog
                return render_template(
                    "productspurchased.j2",
                    productspurchased=get_informative_productspurchased(),
                    products=get_all("Products"),
                    salesdata=get_all("SaleData"),
                    error="Both Product ID and Purchase ID are required.",
                )
            else:
                # Good to process arguments and run query.
                args = (
                    request.form.get("productID"),
                    request.form.get("purchaseID"),
                    str(product_id),
                    str(purchase_id),
                )

                query = (
                    "UPDATE ProductsPurchased SET productID = (%s), purchaseID = (%s)"
                    + " WHERE (productID = (%s) AND purchaseID = (%s))"
                )
                results = execute_query(query, args)

            # Return the page with the success dialog
            return render_template(
                "productspurchased.j2",
                productspurchased=get_informative_productspurchased(),
                products=get_all("Products"),
                salesdata=get_all("SaleData"),
                success=True,
            )

        except Exception as e:
            # An error was caught. Issue an error dialog to the user.
            return render_template(
                "productspurchased.j2",
                productspurchased=get_informative_productspurchased(),
                products=get_all("Products"),
                salesdata=get_all("SaleData"),
                error=str(e)[:100] + "...",
            )

    # If code execution ever gets here, something is wrong.
    return redirect("/", code=404)


#
#
#   SALEDATA
#
#


@server.route("/salesdata", methods=["GET", "POST"])
def salesdata():

    """
    Route to allow the user to get information from the SaleData table

    GET will allow the user to see all existing SaleData entries
    POST will allow the user to add a new SaleData entry
    """

    if request.method == "GET":

        return render_template(
            "salesdata.j2", salesdata=get_all("SaleData"), userdata=get_all("UserData")
        )

    elif request.method == "POST":
        try:
            # Check that required arguments are not empty.
            if request.form.get("userID") == "" or request.form.get("total") == "":
                # Some args are empty, return an error dialog
                return render_template(
                    "salesdata.j2",
                    salesdata=get_all("SaleData"),
                    userdata=get_all("UserData"),
                    error="Both User ID and Total are required parameters",
                )

            elif not is_number(request.form.get("total")):

                # total is not an int or float, issue an error dialog to the user
                return render_template(
                    "salesdata.j2",
                    salesdata=get_all("SaleData"),
                    userdata=get_all("UserData"),
                    error="Total must be a numeric value",
                )

            else:
                # Good to process arguments and run query.
                args = (
                    request.form.get("userID"),
                    request.form.get("total"),
                )

                query = "INSERT INTO SaleData (userID, total) VALUES (%s, %s);"
                results = execute_query(query, args)

                # Return view with success dialog.
                return render_template(
                    "salesdata.j2",
                    salesdata=get_all("SaleData"),
                    userdata=get_all("UserData"),
                    success=True,
                )

        except Exception as e:
            # An error was caught. Issue an error dialog to the user.
            return render_template(
                "salesdata.j2",
                salesdata=get_all("SaleData"),
                userdata=get_all("UserData"),
                error=str(e)[:100] + "...",
            )

    else:
        return redirect("/", code=404)


#
#
#   THIRDPARTIES
#
#


@server.route("/thirdparties", methods=["GET", "POST"])
def thirdparties():

    """
    Route to allow the user to get information from the ThirdParties table

    GET will allow the user to see all existing ThirdParties entries
    POST will allow the user to add a new ThirdParties entry
    """

    if request.method == "GET":

        return render_template("thirdparties.j2", thirdparties=get_all("ThirdParties"))

    elif request.method == "POST":
        try:
            # Check that required arguments are not empty.
            if request.form.get("thirdPartyName") == "":
                # Some args are empty, return an error dialog
                return render_template(
                    "thirdparties.j2",
                    thirdparties=get_all("ThirdParties"),
                    error="Third Party Name is a required parameter.",
                )
            else:
                # Good to process arguments and run query.
                args = (
                    request.form.get("thirdPartyName"),
                    request.form.get("description"),
                )

                query = (
                    "INSERT INTO ThirdParties (thirdPartyName, "
                    + "description) VALUES (%s, %s);"
                )
                results = execute_query(query, args)

                # Return view with success dialog.
                return render_template(
                    "thirdparties.j2",
                    thirdparties=get_all("ThirdParties"),
                    success=True,
                )

        except Exception as e:
            # An error was caught. Issue an error dialog to the user.
            return render_template(
                "thirdparties.j2",
                thirdparties=get_all("ThirdParties"),
                error=str(e)[:100] + "...",
            )

    else:
        return redirect("/", code=404)


#
#
#   USEREDATA
#
#


@server.route("/userdata", methods=["GET", "POST"])
def userdata():

    """
    Route to allow the user to get information from the UserData table

    GET will allow the user to see all existing UserData entries
    POST will allow the user to add a new UserData entry
    """

    if request.method == "GET":
        # Sends the results back to the web browser.
        return render_template(
            "userdata.j2",
            userdata=get_all("UserData"),
            thirdparties=get_all("ThirdParties"),
        )

    elif request.method == "POST":
        try:
            # Check that required arguments are not empty.
            if (
                request.form.get("firstName") == ""
                or request.form.get("lastName") == ""
                or request.form.get("streetAddress") == ""
                or request.form.get("zipCode") == ""
                or request.form.get("countryCode") == ""
                or request.form.get("thirdPartyID") == ""
            ):
                return render_template(
                    "userdata.j2",
                    userdata=get_all("UserData"),
                    thirdparties=get_all("ThirdParties"),
                    error="No parameters are allowed to be empty",
                )
            else:
                # Good to process arguments and run query.
                args = (
                    request.form.get("firstName"),
                    request.form.get("lastName"),
                    request.form.get("streetAddress"),
                    request.form.get("zipCode"),
                    request.form.get("countryCode"),
                    request.form.get("thirdPartyID"),
                )

                query = (
                    "INSERT INTO UserData (firstName, "
                    + "lastName, streetAddress, zipCode, countryCode, thirdPartyID)"
                    + " VALUES (%s, %s, %s, %s, %s, %s);"
                )
                results = execute_query(query, args)

                # Return view with success dialog.
                return render_template(
                    "userdata.j2",
                    userdata=get_all("UserData"),
                    thirdparties=get_all("ThirdParties"),
                    success=True,
                )
        except Exception as e:
            # An error was caught. Issue an error dialog to the user.
            return render_template(
                "userdata.j2",
                userdata=get_all("UserData"),
                thirdparties=get_all("ThirdParties"),
                error=str(e)[:100] + "...",
            )

    else:
        return redirect("/", code=404)


#
#
#   MAIN
#
#

if __name__ == "__main__":

    """
    Main function
    """

    port = int(os.environ.get("PORT", 4096))
    server.run(host="0.0.0.0", port=port, debug=True)
