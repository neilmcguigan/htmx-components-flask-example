from __future__ import annotations

from functools import partial

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from htmx_components_flask import htmx_components_flask
from htmx_components_python import GridConfig
from jinja2 import StrictUndefined
from sqlalchemy import Table, asc, desc, func, select, text

from form import KitchenSink

app = Flask(__name__)
app.register_blueprint(htmx_components_flask)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///northwind.db"
app.config["SECRET_KEY"] = "s3cr3t"

db = SQLAlchemy()
db.init_app(app)

with app.app_context():
    db.reflect()

customers_table = db.metadata.tables["Customers_FTS"]


app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.jinja_env.undefined = StrictUndefined


@app.get("/")
def index():
    return render_template("index.html")


@app.route("/viewgrid", methods=["GET", "POST"])
def viewgrid():
    grid1 = GridConfig(
        columns=[
            "CustomerID",
            "CompanyName",
            "ContactName",
            "ContactTitle",
            "Region",
        ]
    )

    grid1.get_records = partial(get_records, customers_table)
    return render_template("viewgrid.html", grid_config=grid1)


@app.route("/form", methods=["GET", "POST"])
def form():
    form = KitchenSink(request.form)
    form.validate_on_submit()
    return render_template("form.html", form=form)


def get_records(
    table: Table,
    page: int = 1,
    page_size: int = 20,
    sorts: list[tuple[str, str]] | None = None,
    q: str = "",
):
    if not sorts:
        sorts = []

    query = select(table)
    count_query = select(func.count("*")).select_from(table)
    where_clause = text(f"{table.name} match :q")

    if q:
        query = query.filter(where_clause)
        count_query = count_query.filter(where_clause)

    for sort in sorts:
        attr = table.c[sort[0]]
        query = query.order_by(desc(attr) if sort[1] == "desc" else asc(attr))

    query = query.limit(page_size).offset(page_size * (page - 1))

    cursor_result = db.session.execute(query, {"q": f"{q}"})

    result = []
    for row in cursor_result:
        result.append(row._mapping)

    total = db.session.scalar(count_query, {"q": f"{q}"})
    return result, (total // page_size) + 1
