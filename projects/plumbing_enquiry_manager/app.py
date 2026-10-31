from flask import Flask, render_template, request, redirect, url_for, flash

from database import (
    init_db,
    add_enquiry,
    get_enquiries,
    update_enquiry_status
)

app = Flask(__name__)
app.secret_key = "change-this-demo-secret"

init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit_enquiry():
    name = request.form.get("customer_name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    service = request.form.get("service", "").strip()
    message = request.form.get("message", "").strip()

    if not all([name, email, phone, service]):
        flash("Please complete all required fields.", "error")
        return redirect(url_for("home"))

    if "@" not in email:
        flash("Please enter a valid email address.", "error")
        return redirect(url_for("home"))

    add_enquiry(name, email, phone, service, message)

    flash("Your enquiry has been submitted successfully.", "success")
    return redirect(url_for("home"))


@app.route("/dashboard")
def dashboard():
    enquiries = get_enquiries()
    return render_template("dashboard.html", enquiries=enquiries)


@app.route("/update-status/<int:enquiry_id>", methods=["POST"])
def update_status(enquiry_id):
    status = request.form.get("status", "")

    try:
        updated = update_enquiry_status(enquiry_id, status)
    except ValueError:
        flash("Invalid status.", "error")
        return redirect(url_for("dashboard"))

    if not updated:
        flash("Enquiry not found.", "error")

    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)