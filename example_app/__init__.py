from flask import Flask
from flask import redirect
from flask import request

from questions import Form
from questions import FormPage
from questions import TextQuestion
from questions import DropdownQuestion


class PageOne(Form):
    name = TextQuestion()
    email = TextQuestion(input_type="email", required="True")


class PageTwo(Form):
    country = DropdownQuestion(choices_by_url={"value_name": "name",
        "url": "https://restcountries.eu/rest/v2/all"})
    birthdate = TextQuestion(input_type="date")


class Profile(Form):
    page_one = FormPage(PageOne, title="Identification Information")
    page_two = FormPage(PageTwo, title="Additional Information")


app = Flask(__name__)

@app.route("/", methods=("GET",))
def form():
    form = Profile(platform='react')#,resource_url='/Users/hugoevers/VScode-projects/CA_data_platform/src/app/static/node_modules')
    form._construct_survey()
    form.to_json()
    return form.render_html()

@app.route("/", methods=("POST",))
def post():
    form_data = request.get_json()
    # Here, we would save to a database or something
    print(form_data)
    return redirect("/thanks")

@app.route("/thanks")
def thanks():
    return "Thanks for your information"

if __name__ == "__main__":
    app.run(port=8000)