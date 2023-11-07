from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Datasets(db.Model):
    name = db.Column(db.String(64), index = True)
    size = db.Column(db.Integer, primary_key = True)
    source = db.Column(db.String(256), index=True)
    db_index = db.Column(db.Double, index=True)
    rdb_index = db.Column(db.Double, index=True)
    gdb_index = db.Column(db.Double, index=True)
    pdb_index = db.Column(db.Double, index=True)


@app.route("/")
def main():
    datasets = Datasets.query
    return render_template('bootstrap_table.html', title='Bootstrap Table', users=datasets)


if __name__ == '__main__':
    app.run()

# do tomorrow morning: https://blog.miguelgrinberg.com/post/beautiful-interactive-tables-for-your-flask-templates
