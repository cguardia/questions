=========
Questions
=========


.. image:: https://img.shields.io/pypi/v/questions.svg
        :target: https://pypi.python.org/pypi/questions

.. image:: https://img.shields.io/travis/cguardia/questions.svg
        :target: https://travis-ci.com/cguardia/questions

.. image:: https://readthedocs.org/projects/questions/badge/?version=latest
        :target: https://questions.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Questions is a Python form library that uses the power of SurveyJS_ for the UI.
The philosophy behind Questions is that modern form rendering usually requires
integrating some complex Javascript widgets anyway, so why not skip the markup
generation completely? 

.. image:: https://www.delaguardia.com.mx/questions.gif

In Questions, forms are defined in Python similarly to other form frameworks,
but everything on the front end is handled by SurveyJS. This provides a lot of
benefits:

* Nice, integrated UI, with powerful Javascript widgets.
* SurveyJS is compatible with Angular2, JQuery, KnockoutJS, React and VueJS.
  Questions makes sure that you get the right files for each version.
* More than 20 question types, from simple text inputs and dropdowns to
  elaborate widgets like dynamic panels and checkbox matrices.
* Multiple look and feel options (themes), including Bootstrap_ CSS support.
* Full client side validation (plus server side checking, too).
* Use simple text expressions in question declarations to control which
  questions to show depending on the answers to previous ones.
* Complex forms can be defined easily using class composition.
* Easy multi-page forms, with no state-keeping headaches.
* Create forms directly from JSON definitions using SurveyJS form creator.
* Generate Python code from dynamic JSON import.
* Minimal code for simple apps. If you just need a form or two, you are set.
* Zero Javascript code option. If you can use a CDN, no need to install or
  download any javascript.
* Out of the box integration with popular third party widgets, like select2_
  and ckeditor_.
* Supports the creation of tests and quizzes, by defining "correct" answers to
  the questions, and optionally setting a maximum time to finish.

.. _SurveyJS: https://surveyjs.io
.. _Bootstrap: https://getbootstrap.com
.. _select2: https://select2.org/
.. _ckeditor: https://ckeditor.com/ckeditor-4/


How the Code Looks
------------------

To get a feel for how Questions works, nothing better than looking at a simple
example::

    from questions import Form
    from questions import TextQuestion
    from questions import RadioGroupQuestion


    class SimpleForm(Form):
        name = TextQuestion()
        email = TextQuestion(input_type="email", required="True")
        favorite_number = TextQuestion(title="What is your favorite number?",
            input_type="number")
        language = RadioGroupQuestion(title="Favorite Language",
            choices=["Python", "Other"])
        version = RadioGroupQuestion(title="Preferred Python Version",
            choices=["Python 2", "Python 3"],
            visible_if="{language} = 'Python'")

This is a fairly conventional way to define forms, so no surprises here, but
look at the way the ``input_type`` parameter allows us to use different HTML5
text input methods. Pay special attention to the last line, where we use the
``visible_if`` parameter to only show the Python version question if the
answer to the ``language`` question is "Python". Defining "live" form behavior
in this way is something that is usually out of scope for server side code,
but Questions' SurveyJS integration allows us to do it.


Full Working Multi-page Flask Application
-----------------------------------------

Let's show how easy things can be if your applications needs are simple. The
following is a complete application using the popular Flask_ web framework::

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
        form = Profile()
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
        app.run()

By default, Questions uses a CDN for fetching the Javascript resources, which
is why all that is needed to run the above code is installing Flask and
Questions. Of course, it is possible to install all the dependencies yourself
and configure Questions to use your installation, but sometimes this is all
that's required to get a full working application.

Admittedly, our application doesn't do much, but we get a working form that you
can fill and submit in your browser. See how easy it is to get a multi-page
form with navigation buttons. Also, notice how ``get_json`` is the only Flask
request call we need to get the form data. 

As the code shows, defining a multiple page form is very simple, and allows us
to keep the form pages logically separated, and even using them independently
or in combination with other forms with little additional work.

Finally, take a look at the ``choices_by_url`` parameter in the
DropdownQuestion, which allows us to get the dropdown choices from separate,
restful web services.

.. _Flask: https://flask.palletsprojects.com/


License and Documentation
-------------------------

* Free software: MIT license
* Documentation: https://questions.readthedocs.io.


Credits
-------

This package was created with Cookiecutter_ and the
`audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
