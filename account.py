from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from .models import User
from . import db
from . import read_settings
from werkzeug.security import check_password_hash, generate_password_hash

account = Blueprint(name="account", import_name=__name__)

settings = read_settings()


@account.route("/account", methods=["GET", "POST"])
@login_required
def account_manager():
    if request.method == "POST":
        new_username = request.form.get("username")

        try:
            User.query.filter_by(email=current_user.email).update(dict(
                username=new_username
            ))
            db.session.commit()
            flash("Account Updated", category="success")

            return redirect(url_for("account.account_manager"))

        except:

            flash("Cannot Update Account", category="error")
            return redirect(url_for("account.account_manager"))

    return render_template("account.html", settings=settings, user=current_user)


@account.route("/delete_account")
@login_required
def delete_account():
    try:
        account_to_delete = User.query.filter_by(
            email=current_user.email).first()
        db.session.delete(account_to_delete)
        db.session.commit()

        flash("Account deleted", category="success")
        return redirect(url_for("views.home"))

    except:
        flash("Cant Delete Account", category="error")
        return redirect(url_for("views.home"))


@account.route("/change_password", methods=["GET","POST"])
def change_password():
    if request.method == "POST":
        old_password = request.form.get("old_password")

        new_password = request.form.get("new_password")
        confirm_new_password = request.form.get("confirm_new_password")

        user = User.query.filter_by(email=current_user.email)

        if confirm_new_password != new_password:
            flash("Passwords Does'nt Match", category="error")
            return redirect(url_for("account.account_manager"))
        
        else:
            if check_password_hash(current_user.password, old_password):
                user.update(
                    dict(password=generate_password_hash(confirm_new_password))
                )
                db.session.commit()

            flash("Passsword Changed Successfully", category="success")
            return redirect(url_for("account.account_manager"))

    return render_template("change_password.html",settings=settings, user=current_user)