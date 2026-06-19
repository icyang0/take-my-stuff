import os
import cloudinary
import cloudinary.uploader
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///local.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Cloudinary config
cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
)

CATEGORIES = ["Clothes", "Books", "Home Goods", "Electronics", "Kitchen", "Outdoor", "Other"]

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "changeme")


# ---------- Models ----------

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    note = db.Column(db.String(300), nullable=True)
    category = db.Column(db.String(60), nullable=False)
    photo_url = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(20), default="available")  # available | claimed | gone
    claimed_by = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "note": self.note,
            "category": self.category,
            "photo_url": self.photo_url,
            "status": self.status,
            "claimed_by": self.claimed_by,
        }


with app.app_context():
    db.create_all()


# ---------- Auth ----------

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated


# ---------- Public routes ----------

@app.route("/")
def index():
    category = request.args.get("category", "")
    query = Item.query.filter(Item.status != "gone")
    if category and category in CATEGORIES:
        query = query.filter_by(category=category)
    items = query.order_by(Item.created_at.desc()).all()
    return render_template("index.html", items=items, categories=CATEGORIES, active_category=category)


@app.route("/claim/<int:item_id>", methods=["POST"])
def claim(item_id):
    item = Item.query.get_or_404(item_id)
    if item.status != "available":
        return jsonify({"error": "This item is no longer available."}), 409
    name = request.form.get("name", "").strip()
    if not name:
        return jsonify({"error": "Please enter your name."}), 400
    item.status = "claimed"
    item.claimed_by = name
    db.session.commit()
    return jsonify({"success": True, "message": f"Claimed! {name}, the owner will check in on this soon."})


# ---------- Admin routes ----------

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
        flash("Wrong password.")
    return render_template("admin_login.html")


@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/admin")
@login_required
def admin_dashboard():
    available = Item.query.filter_by(status="available").order_by(Item.created_at.desc()).all()
    claimed = Item.query.filter_by(status="claimed").order_by(Item.created_at.desc()).all()
    gone = Item.query.filter_by(status="gone").order_by(Item.created_at.desc()).all()
    return render_template("admin_dashboard.html", available=available, claimed=claimed, gone=gone, categories=CATEGORIES)


@app.route("/admin/upload", methods=["POST"])
@login_required
def admin_upload():
    title = request.form.get("title", "").strip()
    note = request.form.get("note", "").strip()
    category = request.form.get("category", "")
    photo = request.files.get("photo")

    if not title or not category or not photo:
        flash("Title, category, and photo are all required.")
        return redirect(url_for("admin_dashboard"))

    if category not in CATEGORIES:
        flash("Invalid category.")
        return redirect(url_for("admin_dashboard"))

    try:
        result = cloudinary.uploader.upload(photo, folder="free-stuff-board")
        photo_url = result["secure_url"]
    except Exception as e:
        flash(f"Photo upload failed: {e}")
        return redirect(url_for("admin_dashboard"))

    item = Item(title=title, note=note, category=category, photo_url=photo_url)
    db.session.add(item)
    db.session.commit()
    flash(f'"{title}" posted successfully.')
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/mark-gone/<int:item_id>", methods=["POST"])
@login_required
def mark_gone(item_id):
    item = Item.query.get_or_404(item_id)
    item.status = "gone"
    db.session.commit()
    flash(f'"{item.title}" marked as gone.')
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/delete/<int:item_id>", methods=["POST"])
@login_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash(f'"{item.title}" deleted.')
    return redirect(url_for("admin_dashboard"))


if __name__ == "__main__":
    app.run(debug=True)
