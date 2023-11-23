from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dbindex import test as t
from dbindex import dbIndex

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

dbCalculated = False

class Datasets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True)
    size = db.Column(db.String(4), index=True)
    source = db.Column(db.String(256), index=True)
    db_index = db.Column(db.Double, index=True)
    rdb_index = db.Column(db.Double, index=True)
    gdb_index = db.Column(db.Double, index=True)
    pdb_index = db.Column(db.Double, index=True)


class LLMS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True)
    size = db.Column(db.String(4), index=True)
    source = db.Column(db.String(256), index=True)
    glue = db.Column(db.Double, index=True)
    stereoset = db.Column(db.Double, index=True)
    mb_index = db.Column(db.Double, index=True)


with app.app_context():
    db.create_all()

    # Sample record creation
    dataset1 = Datasets(id=0, name="RedPajama-Data-V2", size=37, source="togethercomputer", db_index=0, rdb_index=2,
                        gdb_index=2, pdb_index=3)
    dataset2 = Datasets(id=1, name="ultrachat_200k", size=200000, source="HuggingFaceH4", db_index=0, rdb_index=100,
                        gdb_index=2, pdb_index=30)
    llm1 = LLMS(id=0, name="Yi-34B", size="34B", source="01-ai", glue=0, stereoset=2, mb_index=2)
    llm2 = LLMS(id=1, name="OpenChat 3.5", size="7B", source="OpenChat", glue=0, stereoset=4, mb_index=1)
    db.session.add_all([dataset1, dataset2, llm1, llm2])
    db.session.commit()


@app.route("/datasets")
def datasets():
    datasets = Datasets.query
    return render_template('datasets.html', title='Dataset Bias Leaderboard', datasets=datasets)


@app.route("/dbindex")
def dbindex():
    return render_template('dbindex.html')


@app.route("/calculate_db_index", methods=["POST"])
def calculate_db_index():
    if request.method == "POST":
        link = request.form.get('dsetlabel')
        return render_template("calculated.html", dbi=dbIndex((link)))


@app.route("/llms")
def llms():
    llms = LLMS.query
    return render_template('llms.html', title="LLM Bias Leaderboard", llms=llms)


@app.route("/")
def main():
    return render_template("home.html")


if __name__ == '__main__':
    app.run()

# do tomorrow morning: https://blog.miguelgrinberg.com/post/beautiful-interactive-tables-for-your-flask-templates
