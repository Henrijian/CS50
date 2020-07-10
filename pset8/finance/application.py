import os

import sqlite3
import datetime
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd, dict_factory

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configuration for using SQLite database
db = sqlite3.connect("finance.db", check_same_thread=False)
db.row_factory = dict_factory
cur = db.cursor()

# Database data format
DATE_FMT = "%Y-%m-%d"
TIME_FMT = "%H:%M:%S"
ACTION_BUY = "BUY"
ACTION_SELL = "SELL"

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    uid = session["user_id"]
    sql = "SELECT * FROM holdings WHERE uid=?"
    cur.execute(sql, (uid,))
    rows = cur.fetchall()
    holdings = []
    holdings_total = 0
    for row in rows:
        symbol = row["symbol"]
        shares = row["shares"]
        my_price = row["price"]
        symbol_info = lookup(symbol)
        cur_price = symbol_info["price"]
        symbol_total = cur_price * shares
        holding = {
            "symbol": symbol,
            "shares": shares,
            "my_price": my_price,
            "cur_price": cur_price,
            "symbol_total": symbol_total
        }
        holdings.append(holding)
        holdings_total += symbol_total
    sql = "SELECT cash FROM users WHERE id=?"
    cur.execute(sql, (uid,))
    row = cur.fetchone()
    if not row:
        return apology("Cannot get user information", 403)
    cash = row["cash"]
    balance = cash + holdings_total
    return render_template("index.html", holdings=holdings, balance=balance)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # Check validation of symbol
        symbol = request.form.get("symbol")
        # Check existence of symbol
        if not symbol:
            return apology("Must provide symbol name", 403)
        symbol_info = lookup(symbol)
        if not symbol_info:
            return apology("Cannot find queried symbol", 403)
        symbol = symbol.upper()

        # Check validation of shares
        shares = request.form.get("shares")
        if not shares:
            return apology("Must provide shares number", 403)
        shares = int(shares)
        if not shares > 0:
            return apology("Shares number must be positive", 403)

        # Check if the user can afford the number of shares
        uid = session["user_id"]
        sql = "SELECT cash FROM users WHERE id=?"
        cur.execute(sql, (uid,))
        row = cur.fetchone()
        if not row:
            return apology("Cannot get user cash", 403)
        cash = row["cash"]
        share_price = symbol_info["price"]
        shares_price = shares * share_price
        if shares_price > cash:
            return apology("You cannot afford the amount of shares", 403)

        # Write to database
        # Write to users table
        sql = "UPDATE users SET cash=? WHERE id=?"
        balance = cash - shares_price
        cur.execute(sql, (balance, uid))
        if cur.rowcount < 1:
            return apology("Buy shares of symbol failed", 403)
        # Write to transactions table
        now = datetime.datetime.now()
        date_str = now.strftime(DATE_FMT)
        time_str = now.strftime(TIME_FMT)
        sql = "INSERT INTO transactions (uid, action, date, time, symbol, shares, price) VALUES(?,?,?,?,?,?,?)"
        cur.execute(sql, (uid, ACTION_BUY, date_str, time_str, symbol, shares, share_price))
        if not cur.lastrowid:
            return apology("Buy shares of symbol failed", 403)
        # Write to holdings table
        sql = "SELECT rowid, * FROM holdings WHERE uid=? AND symbol=? AND price=?"
        cur.execute(sql, (uid, symbol, share_price))
        row = cur.fetchone()
        if row:
            rowid = row["rowid"]
            holding_shares = row["shares"] + shares
            sql = "UPDATE holdings SET shares=? WHERE rowid=?"
            cur.execute(sql, (holding_shares, rowid))
        else:
            holding_shares = shares
            sql = "INSERT INTO holdings (uid, symbol, shares, price) VALUES(?,?,?,?)"
            cur.execute(sql, (uid, symbol, holding_shares, share_price))
        if not cur.lastrowid:
            return apology("Buy shares of symbol failed", 403)
        # If everything is ok, update to database
        db.commit()

        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        sql = "SELECT * FROM users WHERE username = ?"
        username = request.form.get("username")
        cur.execute(sql, (username,))
        rows = cur.fetchall()

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
        symbol = request.form.get("symbol")
        # Ensure symbol was submitted
        if not symbol:
            return apology("Must provide symbol name", 403)

        symbol_info = lookup(symbol)
        # Ensure having symbol information
        if not symbol_info:
            return apology("Cannot find queried symbol", 403)

        return render_template("quoted.html", name=symbol_info["name"],
                               price=symbol_info["price"],
                               symbol=symbol_info["symbol"])
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation", 403)

        # Check whether username already exists
        sql = "SELECT * FROM users WHERE username = ?"
        username = request.form.get("username")
        cur.execute(sql, (username,))
        row = cur.fetchone()
        if row:
            return apology("username already exists", 403)

        # Check whether password and confirmation match
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if password != confirmation:
            return apology("password and confirmation do not match", 403)

        # Add new user to database
        hash_password = generate_password_hash(password)
        sql = "INSERT INTO users (username, hash) VALUES(?,?)"
        cur.execute(sql, (username, hash_password))
        if cur.lastrowid:
            db.commit()
        else:
            return apology("register user failed, please try again", 403)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
