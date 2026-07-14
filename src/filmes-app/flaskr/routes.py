from flask import Blueprint, render_template, request, redirect, url_for
from .db import get_db


bp = Blueprint("filmes", __name__)


@bp.route("/")
def index():
    db = get_db()

    filmes = db.execute(
        "SELECT * FROM filmes"
    ).fetchall()

    return render_template("index.html", filmes=filmes)


@bp.route("/create", methods=("GET", "POST"))
def create():

    if request.method == "POST":

        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        ano = request.form["ano"]

        db = get_db()

        db.execute(
            "INSERT INTO filmes (titulo, descricao, ano) VALUES (?, ?, ?)",
            (titulo, descricao, ano)
        )

        db.commit()

        return redirect(url_for("filmes.index"))

    return render_template("create.html")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
def update(id):

    db = get_db()

    filme = db.execute(
        "SELECT * FROM filmes WHERE id = ?",
        (id,)
    ).fetchone()

    if request.method == "POST":

        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        ano = request.form["ano"]

        db.execute(
            """
            UPDATE filmes
            SET titulo = ?, descricao = ?, ano = ?
            WHERE id = ?
            """,
            (titulo, descricao, ano, id)
        )

        db.commit()

        return redirect(url_for("filmes.index"))

    return render_template("update.html", filme=filme)


@bp.route("/<int:id>/delete", methods=("POST",))
def delete(id):

    db = get_db()

    db.execute(
        "DELETE FROM filmes WHERE id = ?",
        (id,)
    )

    db.commit()

    return redirect(url_for("filmes.index"))