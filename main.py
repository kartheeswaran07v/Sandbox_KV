from io import BytesIO
import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, send_file
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, DateTime, Float, or_, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import DetachedInstanceError
import math
import csv
import pandas
import os

# app configuration
app = Flask(__name__)

app.config['SECRET_KEY'] = "kkkkk"

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABase_URL1", "sqlite:///item_cases_csv.db")
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///item_cases_csv.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# 7
class itemMaster(db.Model):
    __tablename__ = "itemMaster"
    id = Column(Integer, primary_key=True)
    alt = Column(String(300))
    tag_no = Column(String(300))
    unit_price = Column(String(300))
    qty = Column(String(300))
    # relationship as parent
    cases = relationship("itemCases", back_populates="item")


class itemCases(db.Model):
    __tablename__ = "itemCases"
    id = Column(Integer, primary_key=True)
    flowrate = Column(Integer)
    iPressure = Column(Integer)
    oPressure = Column(Integer)
    iTemp = Column(Integer)
    sGravity = Column(Integer)
    vPressure = Column(Integer)
    viscosity = Column(Integer)
    vaporMW = Column(Integer)
    vaporInlet = Column(Integer)
    vaporOutlet = Column(Integer)
    CV = Column(Integer)
    openPercent = Column(Integer)
    valveSPL = Column(Integer)
    iVelocity = Column(Integer)
    oVelocity = Column(Integer)
    pVelocity = Column(Integer)
    chokedDrop = Column(Integer)
    Xt = Column(Integer)
    warning = Column(Integer)
    trimExVelocity = Column(Integer)
    sigmaMR = Column(Integer)
    reqStage = Column(Integer)
    fluidName = Column(Integer)
    fluidState = Column(Integer)
    criticalPressure = Column(Integer)
    iPipeSize = Column(Integer)
    iPipeSizeSch = Column(Integer)
    oPipeSize = Column(Integer)
    oPipeSizeSch = Column(Integer)

    # relationship as child
    itemID = Column(Integer, ForeignKey("itemMaster.id"))
    item = relationship("itemMaster", back_populates="cases")


class Upload(db.Model):
    __tablename__ = "Upload"
    id = Column(Integer, primary_key=True)
    filename = Column(String(300))
    data = Column(LargeBinary)


with app.app_context():
    db.create_all()


@app.route('/', methods=["GET", "POST"])
def projectNotes():
    if request.method == "POST":
        with app.app_context():
            cases = itemCases.query.all()

            # field names
            fields = ['Flow Rate', 'Inlet Pressure', 'Outlet Pressure', 'Inlet Temperature', 'Specific Gravity',
                      'Calculated Cv', 'Open %', 'Valve SPL', 'Inlet Velocity', 'Outlet Velocity', 'Valve Velocity',
                      'Inlet Pipe Size', 'Outlet Pipe Size']

            # data rows of csv file
            rows = []
            for i in cases:
                case_list = [i.flowrate, i.iPressure, i.oPressure, i.iTemp, i.sGravity, i.CV, i.openPercent, i.valveSPL,
                             i.iVelocity, i.oVelocity, i.pVelocity, i.iPipeSize, i.oPipeSize]
                rows.append(case_list)

            # with open('GFG123.csv', 'w') as f:
            # using csv.writer method from CSV package
            # write = csv.writer(f)
            # write.writerow(fields)
            # write.writerows(rows)

            pd = pandas.DataFrame(rows, columns=fields)
            pd.to_csv("C:/Users/FCC/Desktop/mylist.csv")

        return f"<h1>{len(cases)}</h1>"
    return render_template("test_csv.html")


def sort_list_latest(list_1, selected):
    for i in list_1:
        if i['id'] == selected:
            removing_element = i
            list_1.remove(removing_element)
            print(list_1)
            list_1 = [removing_element] + list_1
    return list_1


length_unit_list = [{'id': 'inch', 'name': 'inch'}, {'id': 'm', 'name': 'm'}, {'id': 'mm', 'name': 'mm'},
                    {'id': 'cm', 'name': 'cm'}]

flowrate_unit_list = [{'id': 'm3/hr', 'name': 'm3/hr'}, {'id': 'scfh', 'name': 'scfh'}, {'id': 'gpm', 'name': 'gpm'},
                      {'id': 'lb/hr', 'name': 'lb/hr'}, {'id': 'kg/hr', 'name': 'kg/hr'}]

pressure_unit_list = [{'id': 'bar', 'name': 'bar (a)'}, {'id': 'bar', 'name': 'bar (g)'},
                      {'id': 'kpa', 'name': 'kPa (a)'}, {'id': 'kpa', 'name': 'kPa (g)'},
                      {'id': 'mpa', 'name': 'MPa (a)'}, {'id': 'mpa', 'name': 'MPa (g)'},
                      {'id': 'pa', 'name': 'Pa (a)'}, {'id': 'pa', 'name': 'Pa (g)'},
                      {'id': 'inh20', 'name': 'in H2O (a)'}, {'id': 'inh20', 'name': 'in H2O (g)'},
                      {'id': 'inhg', 'name': 'in Hg (a)'}, {'id': 'inhg', 'name': 'in Hg (g)'},
                      {'id': 'kg/cm2', 'name': 'kg/cm2 (a)'}, {'id': 'kg/cm2', 'name': 'kg/cm2 (g)'},
                      {'id': 'mmh20', 'name': 'm H2O (a)'}, {'id': 'mmh20', 'name': 'm H2O (g)'},
                      {'id': 'mbar', 'name': 'mbar (a)'}, {'id': 'mbar', 'name': 'mbar (g)'},
                      {'id': 'mmhg', 'name': 'mm Hg (a)'}, {'id': 'mmhg', 'name': 'mm Hg (g)'},
                      {'id': 'psia', 'name': 'psi (a)'}, {'id': 'psia', 'name': 'psi (g)'}]

temp_unit_list = [{'id': 'C', 'name': '°C'}, {'id': 'F', 'name': '°F'}, {'id': 'K', 'name': 'K'},
                  {'id': 'R', 'name': 'R'}]

units_pref = [length_unit_list, flowrate_unit_list, pressure_unit_list, temp_unit_list]


@app.route('/', methods=["GET", "POST"])
def home():
    return "<h1>Welcome to Sandbox KV</h1>"


@app.route('/try-post', methods=["GET", "POST"])
def try2post():
    global units_pref
    list__ = units_pref
    if request.method == 'POST':
        if request.form.get('ServerDetails'):
            selected_item0 = request.form.get('check_order0')
            return_list0 = sort_list_latest(list__[0], selected_item0)
            selected_item1 = (request.form.get('check_order1'))
            return_list1 = sort_list_latest(list__[1], selected_item1)
            selected_item2 = (request.form.get('check_order2'))
            return_list2 = sort_list_latest(list__[2], selected_item2)
            selected_item3 = (request.form.get('check_order3'))
            return_list3 = sort_list_latest(list__[3], selected_item3)
            list__ = [return_list0, return_list1, return_list2, return_list3]
            units_pref = list__

            return redirect(url_for('try2post'))
        if request.form.get('GenerateFile'):
            return "Generate file"
        else:
            return "NOne"

    return render_template('try_two_post.html', list__=units_pref)


@app.route('/enter-tab', methods=["GET", "POST"])
def enterTab():
    if request.method == 'POST':
        return 'success'
    return render_template('enterTab.html')


@app.route('/change-picklist', methods=["GET", "POST"])
def changePicklist():
    with app.app_context():
        item_cases = itemCases.query.all()

    if request.method == 'POST':
        return 'success'
    return render_template('change_picklist.html', data=item_cases, len_c=range(len(item_cases)))


@app.route('/upload', methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files['file']
        with app.app_context():
            upload__ = Upload(filename=file.filename, data=file.read())
            db.session.add(upload__)
            db.session.commit()
        return f"Upload: {file.filename}"
    return render_template('upload_doc.html')


@app.route('/download/<upload_id>', methods=["GET", "POST"])
def download(upload_id):
    upload__ = Upload.query.filter_by(id=upload_id).first()
    return send_file(BytesIO(upload__.data), as_attachment=True, download_name=upload__.filename)


if __name__ == "__main__":
    app.run(debug=True)
