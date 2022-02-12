import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///movies.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

genres = [Action, Adult, Adventure, Animation, Biography, Comedy, Crime, Documentary, Drama, Family, Fantasy, Film Noir, Game Show, History, Horror, Musical, Music, Mystery, News, Reality-TV, Romance, Sci-Fi, Short, Sport, Talk-Show, Thriller, War, Western]

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    stocks = db.execute("SELECT symbol, stock_name, SUM(shares) AS totShares, price FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    grandTotal = cash

    for stock in stocks:
        grandTotal += stock["price"] * stock["totShares"]
    return render_template("index.html", stocks=stocks, cash=cash, total=grandTotal, usd=usd)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # Get inputted symbol
        symbol = request.form.get("symbol")
        # Check if blank
        if not symbol:
            return apology("please enter a symbol")

        quote = lookup(symbol)
        # Check if it exists
        if quote == None:
            return apology("lookup unsuccessful")

        # Get shares int
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("shares must be an integer")

        if not shares > 0:
            return apology("shares must be a positive integer")

        # See how much cash user has
        user_id = session["user_id"]
        cashAmt = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        # Get total share cost
        price = quote["price"]
        totalCost = price*shares

        # Check if user can afford purchase
        if cashAmt < totalCost:
            return apology("not enough money :(")
        else:
            # Take cash out of users bank
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cashAmt - totalCost, user_id)
            # Now update transactions to reflect purchase
            name = quote["name"]
            db.execute("INSERT INTO transactions (user_id, stock_name, symbol, shares, price, owned) VALUES (?, ?, ?, ?, ?, ?)",
                        user_id, name, symbol, shares, price, 'buy')
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    stocks = db.execute("SELECT symbol, owned, price, shares, time FROM transactions WHERE user_id = ? ORDER BY time DESC", user_id)
    return render_template("history.html", stocks=stocks, usd=usd)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        # Get inputted symbol
        symbol = request.form.get("symbol")
        # Check that symbol was entered
        if not symbol:
            return apology("please enter a symbol")

        quote = lookup(symbol)
        # Check if it worked
        if quote == None:
            return apology("lookup unsuccessful")
        return render_template("quoted.html", quotes=quote)

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # if user input is blank
        if not request.form.get("username"):
            return apology("must provide username")

        # if password is blank
        if not request.form.get("password"):
            return apology("must provide password")

        # if confirmation is blank
        if not request.form.get("confirmation"):
            return apology("must provide confirmation of password")

        # Username already exists
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) > 0:
            return apology("username already exists")

        # Check if password and confirmation match
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match")

        # Generate password hash before inserting into database
        hash = generate_password_hash(request.form.get("password"))

        # Insert into database
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), hash)

        row = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        # Remember which user has logged in
        session["user_id"] = row[0]["id"]
        return redirect("/")

    else:
        return render_template("registration.html")

@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    """Show history of transactions"""
    user_id = session["user_id"]
    if request.method == "POST":
        newPassword = request.form.get("password")
        # if password is blank
        if not newPassword:
            return apology("must provide password")

        # if confirmation is blank
        if not request.form.get("confirmation"):
            return apology("must provide confirmation of password")

        # Check if new password and confirmation match
        if newPassword != request.form.get("confirmation"):
            return apology("passwords do not match")

        newHash = generate_password_hash(newPassword)
        oldHash = db.execute("SELECT hash FROM users WHERE id = ?", user_id )[0]["hash"]
        # Check that new password does not match old password
        if newHash == oldHash:
            return apology("new password matches old password")

        db.execute("UPDATE users SET hash = ? WHERE id = ?", newHash, user_id )
        return redirect("/")
    else:
        return render_template("password.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]
    symbols = db.execute("SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)

    if request.method == "POST":
        selectedSymbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        # Shares less than zero
        if shares <= 0:
            return apology("must be a positive integer")

        stockPrice = lookup(selectedSymbol)["price"]
        stockName = lookup(selectedSymbol)["name"]

        sharesOwned = db.execute("SELECT shares FROM transactions WHERE symbol = ? AND user_id = ?", selectedSymbol, user_id)[0]["shares"]
        if sharesOwned < shares:
            return apology("not enough shares to sell")

        currentCash =  db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        db.execute("UPDATE users SET cash = ?  WHERE id = ?", currentCash + (shares*stockPrice), user_id)

        db.execute("INSERT INTO transactions (user_id, stock_name, symbol, shares, price, owned) VALUES (?, ?, ?, ?, ?, ?)",
                        user_id, stockName, selectedSymbol, -shares, stockPrice, 'sell')
        return redirect("/")
    else:
        return render_template("sell.html", symbols=symbols)