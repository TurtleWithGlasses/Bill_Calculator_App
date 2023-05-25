from flask.views import MethodView
from wtforms import Form, StringField, SubmitField
from flask import Flask, render_template, request
import flat


app = Flask(__name__)

class HomePage(MethodView):
    
    def get(self):
        return render_template("index.html")

class BillFormPage(MethodView):
    def get(self):

        bill_form = BillForm()
        return render_template("bill_form_page.html",
                               billform=bill_form)

    def post(self):
        billform = BillForm(request.form)


        the_bill = flat.Bill(float(billform.amount.data), billform.period.data)
        flatmate1 = flat.Flatmate(billform.name1.data, float(billform.days_in_house1.data))
        flatmate2 = flat.Flatmate(billform.name2.data, float(billform.days_in_house2.data))
        
        return render_template("bill_form_page.html",
                               result=True,
                               billform=billform,
                               name1=flatmate1.name,
                               amount1=flatmate1.pays(the_bill, flatmate2),
                               name2=flatmate2.name,
                               amount2=flatmate2.pays(the_bill, flatmate1))        

class ResultsPage(MethodView):
    
    # we use post instead of get here because post fucntion is used to create interaction from a page to another
    def post(self): 
        billform = BillForm(request.form)

        name1 = billform.name1.data
        days_in_house = billform.days_in_house1

        the_bill = flat.Bill(float(billform.amount.data), billform.period.data)
        flatmate1 = flat.Flatmate(billform.name1.data, float(billform.days_in_house1.data))
        flatmate2 = flat.Flatmate(billform.name2.data, float(billform.days_in_house2.data))
        
        return render_template("results.html",
                               name1=flatmate1.name,
                               amount1=flatmate1.pays(the_bill, flatmate2),
                               name2=flatmate2.name,
                               amount2=flatmate2.pays(the_bill, flatmate1))

class BillForm(Form):
    # stringfield is used to create space to input string or integer on a webpage
    amount = StringField("Bill Amount: ")
    period = StringField("Bill Period: ")

    name1 = StringField("Name: ")
    days_in_house1 = StringField("Days in the House: ")

    name2 = StringField("Name: ")
    days_in_house2 = StringField("Days in the House: ")

    button = SubmitField("Calculate")

app.add_url_rule("/",
                 view_func=HomePage.as_view("home_page"))
app.add_url_rule("/bill_form_page",
                 view_func=BillFormPage.as_view("bill_form_page"))
# app.add_url_rule("/results",
#                  view_func=ResultsPage.as_view("reults_page"))

app.run(debug=True)