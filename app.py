import os
from flask import Flask, render_template, request, redirect, url_for, flash
from db import get_db_connection

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-only-change-me")

@app.route("/")
def home():
    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()
    favorites_only = request.args.get("favorites") == "1"

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM bookmarks WHERE 1=1"
    values = []

    if search:
        query += " AND (title LIKE %s OR url LIKE %s)"
        values.extend([f"%{search}%", f"%{search}%"])

    if category:
        query += " AND category = %s"
        values.append(category)

    if favorites_only:
        query += " AND is_favorite = TRUE"

    query += " ORDER BY created_at DESC"

    cursor.execute(query, values)
    bookmarks = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "index.html",
        bookmarks=bookmarks,
        search=search,
        category=category,
        favorites_only=favorites_only
    )


@app.route("/add", methods=["POST"])
def add_bookmark():
    title = request.form.get("title", "").strip()
    url = request.form.get("url", "").strip()
    category = request.form.get("category", "").strip()
    notes = request.form.get("notes", "").strip()

    if not title or not url or not category:
        flash("Please fill in all required fields.", "error")
        return redirect(url_for("home"))

    if not url.startswith(("http://", "https://")):
        flash("Please enter a valid URL starting with http:// or https://.", "error")
        return redirect(url_for("home"))

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO bookmarks (title, url, category, notes)
            VALUES (%s, %s, %s, %s)
            """,
            (title, url, category, notes)
        )
        connection.commit()
        flash("Bookmark saved successfully!", "success")
    except Exception:
        connection.rollback()
        flash("Could not save bookmark.", "error")
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for("home"))


@app.route("/favorite/<int:bookmark_id>", methods=["POST"])
def toggle_favorite(bookmark_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE bookmarks
            SET is_favorite = NOT is_favorite
            WHERE id = %s
            """,
            (bookmark_id,)
        )
        connection.commit()
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for("home"))


@app.route("/delete/<int:bookmark_id>", methods=["POST"])
def delete_bookmark(bookmark_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "DELETE FROM bookmarks WHERE id = %s",
            (bookmark_id,)
        )
        connection.commit()
        flash("Bookmark deleted.", "success")
    except Exception:
        connection.rollback()
        flash("Could not delete bookmark.", "error")
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
