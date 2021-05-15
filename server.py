"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken, Katie Byers.
"""

from flask import Flask, render_template, redirect, flash, session
import jinja2

import melons

app = Flask(__name__)

# A secret key is needed to use Flask sessioning features
app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.
app.jinja_env.undefined = jinja2.StrictUndefined

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    # `print("*"*20)
    # print(f"melon list = melons.get_all() : {melon_list}")`
    return render_template("all_melons.html",
                           melon_list=melon_list)


@app.route("/melon/<melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)
    # print(melon)
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def show_shopping_cart():
    """Display content of shopping cart."""
    
    current_cart = session["cart"]
    # print("~~~~~~~~~~~~~~~~")
    # print(f"current cart = {current_cart}")
    melon_objects = []
    current_order_total = 0
    total_cost_for_melon_type = {}
    for melon in current_cart:
        # import pdb; pdb.set_trace()
        melon_object = melons.get_by_id(melon) # retrieve Melon object using get_by_id function
        # print("~~~~~~~~~~~~~~~~")
        # print(f"melon = {melon}")
        # print(f"melon object = {melon_object}")
        
        # Add quantity and total price attributes to the Melon object.
        melon_object_price = melon_object.price
        # print("~~~~~~~~~~~~~~~~")
        # print(f"melon object price = {melon_object.price}")
        # print(f"type: melon object price = {type(melon_object.price)}")
        melon_object.quantity = (current_cart[melon])
        # print("~~~~~~~~~~~~~~~~")
        # print(f"melon object quantity = {melon_object.quantity}")
        # print(f"type: melon object quantity = {type(melon_object_quantity)}")
        melon_object.total_price = (melon_object.price)*(float(melon_object.quantity))
        # print("~~~~~~~~~~~~~~~~")
        # print(f"melon object total price = {melon_object.total_price}")
        # print(f"type: melon object quantity = {type(melon_object_total_price)}")

        # Add the melon object to a cart list
        melon_objects.append(melon_object)
        # print("~~~~~~~~~~~~~~~~")
        # print(f"melon objects list = {melon_objects}")

        # Add the total price for that melon type to a running tally of total cost for the order
        current_order_total += melon_object.total_price
        # print("~~~~~~~~~~~~~~~~")
        # print(f"current order total = {current_order_total}")
        

    return render_template("cart.html",
                            current_total=current_order_total,
                            melon_objects_in_cart=melon_objects)
    

    # TODO: Display the contents of the shopping cart.

    # The logic here will be something like:
    #
    # - get the cart dictionary from the session
    # - create a list to hold melon objects and a variable to hold the total
    #   cost of the order
    # - loop over the cart dictionary, and for each melon id:
    #    - get the corresponding Melon object
    #    - compute the total cost for that type of melon
    #    - add this to the order total
    #    - add quantity and total cost as attributes on the Melon object
    #    - add the Melon object to the list created above
    # - pass the total order cost and the list of Melon objects to the template
    #
    # Make sure your function can also handle the case wherein no cart has
    # been added to the session

    # return render_template("cart.html")
    


@app.route("/add_to_cart/<melon_id>")
def add_to_cart(melon_id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Melon successfully added to
    cart'."""
    #session['session_id'] = 12345
    if "cart" in session:
        
        if melon_id in session["cart"]:
            session["cart"][melon_id] += 1
            flash("Melon added")
        else:
            session["cart"][melon_id] = 1
            flash("Melon added")

    else:
            
        session["cart"] = {}

        if melon_id in session["cart"]:
            session["cart"][melon_id] += 1
            flash("Melon added")
        else:
            session["cart"][melon_id] = 1
            flash("Melon added")

        #print(session["cart"])
        #add melons to dictionary 
        # melon_id = key
        # count = value in session dictionary
        # if melon_id in cart
        #   increment the count
        # else
        #   set it equal to 1  

        

    # TODO: Finish shopping cart functionality

    # The logic here should be something like:
    #
    # - check if a "cart" exists in the session, and create one (an empty
    #   dictionary keyed to the string "cart") if not
    # - check if the desired melon id is the cart, and if not, put it in
    # - increment the count for that melon id by 1
    # - flash a success message
    # - redirect the user to the cart page

    return redirect("/cart")

@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    # TODO: Need to implement this!

    # The logic here should be something like:
    #
    # - get user-provided name and password from request.form
    # - use customers.get_by_email() to retrieve corresponding Customer
    #   object (if any)
    # - if a Customer with that email was found, check the provided password
    #   against the stored one
    # - if they match, store the user's email in the session, flash a success
    #   message and redirect the user to the "/melons" route
    # - if they don't, flash a failure message and redirect back to "/login"
    # - do the same if a Customer with that email doesn't exist

    return "Oops! This needs to be implemented"


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
