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
        symbol_total = round(cur_price * shares, 2)
        holding = {
            "symbol": symbol,
            "shares": shares,
            "my_price": my_price,
            "cur_price": cur_price,
            "symbol_total": symbol_total
        }
        holdings.append(holding)
        holdings_total += symbol_total
    holdings = sorted(holdings, key=lambda holding: holding["symbol"])
    sql = "SELECT cash FROM users WHERE id=?"
    cur.execute(sql, (uid,))
    row = cur.fetchone()
    if not row:
        return apology("Cannot get user information", 403)
    cash = round(row["cash"], 2)
    total = round(cash + holdings_total, 2)
    return render_template("index.html", holdings=holdings, cash=cash, total=total)


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
        try:
            shares = int(shares)
        except:
            return apology("Must provide number for shares amount", 403)
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
        symbol = request.args.get("symbol")
        if not symbol:
            symbol = ""
        return render_template("buy.html", symbol=symbol)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    uid = session["user_id"]
    sql = "SELECT * FROM transactions WHERE uid=?"
    cur.execute(sql, (uid,))
    transactions = cur.fetchall()
    transactions = sorted(transactions, key=lambda transaction: (transaction["date"], transaction["time"]))
    for transaction in transactions:
        transaction["total"] = round(transaction["price"] * transaction["shares"], 2)
    return render_template("history.html", transactions=transactions)


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
    if request.method == "POST":
        # Check the validation of symbol
        sell_symbol = request.form.get("symbol")
        if not sell_symbol:
            return apology("Must provide symbol", 403)
        uid = session["user_id"]
        sql = "SELECT symbol FROM holdings WHERE uid=?"
        cur.execute(sql, (uid,))
        rows = cur.fetchall()
        if not rows:
            return apology("Cannot get user holding symbols", 403)
        holding_symbols = set()
        for row in rows:
            holding_symbols.add(row["symbol"])
        if sell_symbol not in holding_symbols:
            return apology("You do not have selected symbol", 403)

        # Check the validation of shares
        shares = request.form.get("shares")
        if not shares:
            return apology("Must provide shares", 403)
        try:
            shares = int(shares)
        except:
            return apology("Must provide number for shares amount", 403)
        sql = "SELECT shares FROM holdings WHERE uid=? AND symbol=?"
        cur.execute(sql, (uid, sell_symbol))
        rows = cur.fetchall()
        if not rows:
            return apology("Cannot get user holding shares", 403)
        holding_shares = 0
        for row in rows:
            holding_shares += row["shares"]
        if shares > holding_shares:
            return apology("The number of shares is over your holding", 403)

        # Update to database - users table
        symbol_info = lookup(sell_symbol)
        if not symbol_info:
            return apology("Cannot get symbol information", 403)
        cur_price = symbol_info["price"]
        gain = cur_price * shares
        sql = "SELECT cash FROM users WHERE id=?"
        cur.execute(sql, (uid,))
        row = cur.fetchone()
        if not row:
            return apology("Cannot get user cash", 403)
        cash = row["cash"] + gain
        sql = "UPDATE users SET cash=? WHERE id=?"
        cur.execute(sql, (cash, uid))
        if cur.rowcount < 1:
            return apology("Update cash to database failed", 403)

        # Update to database - transaction table
        sql = "INSERT INTO transactions (uid, action, date, time, symbol, shares, price) VALUES(?,?,?,?,?,?,?)"
        now = datetime.datetime.now()
        date_str = now.strftime(DATE_FMT)
        time_str = now.strftime(TIME_FMT)
        cur.execute(sql, (uid, ACTION_SELL, date_str, time_str, sell_symbol, shares, cur_price))
        if not cur.lastrowid:
            return apology("Update transaction to database failed", 403)

        # Update to database - holdings table
        sql = "SELECT shares, price FROM holdings WHERE uid=? AND symbol=?"
        cur.execute(sql, (uid, sell_symbol))
        rows = cur.fetchall()
        if not rows:
            return apology("Cannot get symbol holdings", 403)
        symbol_holdings = []
        for row in rows:
            symbol_holding = {
                "shares": row["shares"],
                "price": row["price"]
            }
            symbol_holdings.append(symbol_holding)
        symbol_holdings = sorted(symbol_holdings, key=lambda holding: holding["price"], reverse=True)
        remain_shares = shares
        for symbol_holding in symbol_holdings:
            symbol_shares = symbol_holding["shares"]
            if symbol_shares >= remain_shares:
                symbol_holding["shares"] -= remain_shares
                remain_shares = 0
            else:
                symbol_holding["shares"] = 0
                remain_shares -= symbol_shares
            if symbol_holding["shares"] == 0:
                sql = "DELETE FROM holdings WHERE uid=? AND symbol=? AND shares=? AND price=?"
                cur.execute(sql, (uid, sell_symbol, symbol_shares, symbol_holding["price"]))
                if cur.rowcount < 1:
                    return apology("Update holdings to database failed", 403)
            else:
                sql = "UPDATE holdings SET shares=? WHERE uid=? AND symbol=? AND shares=? AND price=?"
                cur.execute(sql, (symbol_holding["shares"], uid, sell_symbol, symbol_shares, symbol_holding["price"]))
                if cur.rowcount < 1:
                    return apology("Update holdings to database failed", 403)
            if remain_shares == 0:
                break

        # Update to database
        db.commit()

        return redirect("/")
    else:
        # Get the symbols that the current user holding
        uid = session["user_id"]
        sql = "SELECT symbol FROM holdings WHERE uid=?"
        cur.execute(sql, (uid,))
        rows = cur.fetchall()
        symbols = set()
        for row in rows:
            symbols.add(row["symbol"])
        symbols = sorted(symbols)

        # Get arguments from url address
        sell_symbol = request.args.get("symbol")
        shares = request.args.get("shares")
        if shares:
            try:
                shares = int(shares)
                if shares <= 0:
                    shares = 1
            except:
                shares = 1
        else:
            shares = 1
        return render_template("sell.html", symbols=symbols, sell_symbol=sell_symbol, shares=shares)


@app.route("/account")
@login_required
def account():
    uid = session["user_id"]
    sql = "SELECT cash FROM users WHERE id=?"
    cur.execute(sql, (uid,))
    row = cur.fetchone()
    if not row:
        return apology("Cannot get user info", 403)
    cash = round(row["cash"], 2)
    return render_template("account.html", cash=cash)


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        # Check old password validation
        old_passwd = request.form.get("old_passwd")
        if not old_passwd:
            return apology("Must provide old password", 403)

        uid = session["user_id"]
        sql = "SELECT hash FROM users WHERE id=?"
        cur.execute(sql, (uid,))
        row = cur.fetchone()
        if not row:
            return apology("Cannot get user info", 403)
        user_passwd_hash = row["hash"]
        if not check_password_hash(user_passwd_hash, old_passwd):
            return apology("Provided password is not correct", 403)

        # Check new password validation
        new_passwd = request.form.get("new_passwd")
        if not new_passwd:
            return apology("Must provide new password", 403)

        # Check new password confirmation validation
        new_passwd_confirm = request.form.get("new_passwd_confirm")
        if not new_passwd_confirm:
            return apology("Must provide new password confirmation", 403)

        # Check password match
        if not new_passwd == new_passwd_confirm:
            return apology("New password and confirmation do not match", 403)

        # Write new password to database
        new_passwd_hash = generate_password_hash(new_passwd)
        sql = "UPDATE users SET hash=? WHERE id=?"
        cur.execute(sql, (new_passwd_hash, uid))
        if cur.rowcount < 1:
            return apology("Update new password to database failed", 403)

        # Update new data to database
        db.commit()

        return redirect("/")
    else:
        return render_template("change_password.html")


@app.route("/deposit", methods=["POST", "GET"])
@login_required
def deposit():
    if request.method == "POST":
        # Check validation of deposit
        deposit = request.form.get("deposit")
        if not deposit:
            return apology("Must provide deposit amount", 403)
        try:
            deposit = int(deposit)
        except:
            return apology("Must provide number for deposit amount", 403)
        if not deposit > 0:
            return apology("Must provide positive number for deposit amount", 403)

        # Update to database
        uid = session["user_id"]
        sql = "SELECT cash FROM users WHERE id=?"
        cur.execute(sql, (uid,))
        row = cur.fetchone()
        if not row:
            return apology("Cannot get user info", 403)
        cash = row["cash"]

        sql = "UPDATE users SET cash=? WHERE id=?"
        cur.execute(sql, (cash + deposit, uid))
        if cur.rowcount < 1:
            return apology("Deposit to account failed", 403)

        db.commit()

        return redirect("/")
    else:
        return render_template("deposit.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
