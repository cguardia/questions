===========
Quick Start
===========

Questions forms are basically class definitions, where each question is a form
attribute::

    from questions import Form
    from questions import DropdownQuestion
    from questions import TextQuestion

    
    class PreferencesForm(Form):
        email = TextQuestion(input_type="email")
        email_format = DropdownQuestion(choices=["PDF", "HTML", "Plain Text"])

There are many kinds of :doc:`questions </questions>`, for different kinds of
input types. Most questions have several possible parameters, but most of them
are optional, so the question can be defined with just the parameters that are
needed for each case, as in the example above.

To use a form, an instance has to be created. The Form constructor also
accepts various parameters, but like the Question parameters, they are only
used when they are needed::

    prefs = PreferencesForm()

Generating a form from a JSON file
==================================

SurveyJS offers a free to use (but not open source) form creator. Questions
supports generating form classes from the JSON data that the form creator
exports. To do that, instead of defining the class, use the ``from_json``
method of the ``Form`` class::

    from questions import Form

    json = """
    {
        questions: [
            {
                type: "text",
                name: "email",
                inputType: "email"
            },
            {
                type: "dropdown",
                name: "email_format",
                choices: ["PDF", "HTML", "Plain Text"]
            }
        ]
    }
    """

    PreferencesForm = Form.from_json(json, "PreferencesForm")

The forms generated using the ``from_json`` class method are dynamic types
that have no code equivalent. Questions includes a console script that can
generate actual Python code for these forms::

.. code-block:: console

    $ generate_code {class_name} path/to/file.json

All the script needs is a class name for the generated form class, and the
path to the JSON file with the SurveyJS form definition.
                  
Displaying the forms
====================

Questions generates a SurveyJS form, which requires a few Javascript and CSS
resources to work. The simplest way to display a form is to use the SurveyJS
CDN to serve all these resources, which requires no work and is the default
form display mode. A full HTML page with all required resources and Javascript
code can be generated like this::

    prefs = PreferencesForm()
    html = prefs.render_html()

This should be just enough for many small applications, but most applications
will need to combine the form code with their own layout and resources. Again,
this can be accomplished using the CDN or not. Here's a simple example of how
to integrate a Questions form into an existing web application using the CDN:

Python view code
----------------

To render a form in a template, the Python view code must pass the form
instance to the template. In a generic Python web framework, this would look
like the following::

    def preferences_form():
        prefs = PreferencesForm()
        return {"form": prefs}

HTML template
-------------

In the template, using Jinja_ the form would be used like this:

.. code-block:: html+jinja

    <html>
      <head>
        <!-- the JS for the web application goes here -->
        <!-- the form has a property with the required JS for SurveyJS -->
        {% for script in form.js %}
          <script src={{ script }} type="text/javascript"></script>
        {% endfor %}

        <!-- the script with the form definition and initialization  -->
        <script type="text/javascript">
          {{ form.render_js() }}
        </script>

        <!-- the CSS for the web application goes here -->
        <!-- the form has a property with the required CSS for SurveyJS -->
        {% for stylesheet in form.css %}
          <link href={{ stylesheet }} rel="stylesheet" />
        {% endfor %}
      </head>

      <body>
        <!-- the web application layout goes here -->
        <div id="questions_form"></div>
      </body>
    </html>

What is needed to make the form work is to insert all the required JS and CSS
resources, followed by the form definition and initialization script. The only
thing needed on the HTML side, is the ``div`` where the form will be inserted.
It *must* use the `questions_form` id, unless a different id is passed in
when creating the form, by using the ``html_id`` parameter.

.. _Jinja: https://jinja.palletsprojects.com/

Displaying forms without using the CDN
--------------------------------------

When not using the SurveyJS CDN, there are two ways to display the forms. The
first one requires downloading or installing all the resources under the same
directory, and passing the URL for this directory to the form constructor::

    prefs = PreferencesForm(resource_url="/static_resources")

This is the easiest way to do it, and requires no changes to the HTML above.
If your application includes many forms, you can set the resource URL for all
forms using the ``set_resource_url`` class method of the :class:`Form`
class::

    from questions import Form


    class PreferencesForm(Form):
        email = TextQuestion(input_type="email")
        email_format = DropdownQuestion(choices=["PDF", "HTML", "Plain Text"])


    Form.set_resource_url("/static_resources")
    prefs = PreferencesForm()
    other = OtherForm()

In this example, both the `prefs` and `other` form instances will use the
`/static_resources` URL for getting the form resources.

The other way to do this also requires downloading or installing all the
required resources, but instead of using the `resource_url` parameter, remove
the JS and CSS loops from the HTML template, and in their place put in the
list of locally installed resources. See :doc:`installation` to learn how
this is done.

Panels
======

A panel is a container of form controls that are presented as a group. It's
like a question with multiple parts. To create a panel, a separate form has to
be defined, and it is then passed in to the panel constructor::

    from questions import Form
    from questions import FormPanel
    from questions import BooleanQuestion
    from questions import DropdownQuestion
    from questions import TextQuestion


    class PreferencesForm(Form):
        email = TextQuestion(input_type="email")
        email_format = DropdownQuestion(choices=["PDF", "HTML", "Plain Text"])


    class ProfileForm(Form):
        receive_newsletter = BooleanQuestion(
            title="Do you wish to receive our newsletter?",
            required=True,
        )
        newsletter_panel = FormPanel(
            PreferencesForm,
            title="Newsletter Preferences",
            visible_if="{receive_newsletter} == True",
        )

In the example above, ``PreferencesForm`` will act as a panel inside
``ProfileForm``. Note that that the ``FormPanel`` constructor takes the form
definition (the class) as the parameter, *not* an instance of the form. The
use of the ``visible_if`` condition makes sure the newsletter preferences
panel will only be shown if the user elects to receive the newsletter.

It is possible to have a panel inside a panel, and even more nested panels if
desired. However, be aware that multiple levels of nesting can be confusing
for the user and require more complex code to get at the form data later.

Dynamic panels
==============

A dynamic panel is also a container for questions with multiple parts, but it
has the added feature that copies of it can be dynamically added and removed
from a form. In this way a user can add two or more related panels, like for
example relatives, social media accounts, or previous illnesses. It is
defined in the same way as a regular panel, except the ``dynamic`` parameter
is set to true::

    from questions import Form
    from questions import FormPanel
    from questions import BooleanQuestion
    from questions import DropdownQuestion
    from questions import TextQuestion


    class SocialMediaForm(Form):
        service = DropdownQuestion(choices=["Twitter", "Instagram", "Snapchat"])
        account = TextQuestion()


    class ProfileForm(Form):
        social_media = FormPanel(
            SocialMediaForm,
            title="Social Media Accounts",
            dynamic=True,
            panel_count=2,
        )

The above form will allow the user to add any number of social accounts. Pay
attention to the ``panel_count`` parameter, which signals that two panels will
be active when the form is first rendered.

Pages
=====

Questions also allows the user to easily create multiple page forms. A page
form is like a panel that will be presented on its own page. When a form has
more than one page, Questions will add page navigation controls to move back
and forth between the pages. The final page will show a `complete` button::

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


    class ProfileForm(Form):
        page_one = FormPage(PageOne, title="Identification Information")
        page_two = FormPage(PageTwo, title="Additional Information")

Although Questions will not complain if a page is added to another page, the
nested page will be treated like a panel, not a page.

Accessing form data
===================

Once a questions form is submitted, the data will be posted to the page URL. To
get the form data, simply use you web framework's way of accessing JSON data.
For example, in Flask::

    @app.route("/", methods=("POST",))
    def post():
        form_data = request.get_json()

The form data is returned in a dictionary format, a key for each form field,
regardless of the page and panel structure of the form. A dynamic panel will
be represented as a list of dictionaries. For example::

    {
     'name': 'John Smith',
     'email': 'smith@smith.me',
     'birthdate': '1980-05-08',
     'country': 'US'
    }

Since the data is returned as a single dictionary, it's not allowed to use
the same name for more than one field, even if the form has multiple pages.

Edit Forms
==========

An edit form is a form that shows predetermined values at render time. The
user can then change only the desired values. This would be used to edit
objects stored in a database, for example. To set up an edit form in
Questions, simply pass in a dictionary with the data to the form rendering
method, using the ``form_data`` parameter::

    form = ProfileForm()

    profile_data = {
     'name': 'John Smith',
     'email': 'smith@smith.me',
     'birthdate': '1980-05-08',
     'country': 'US'
    }

    questions_js = form.render_js(form_data=profile_data)

Here we are using a simple dictionary to set up the data, but of course the
usual thing to do for an edit form would be to get the data from a database.

Updating objects with form data
-------------------------------

Since we are on the subject of edit forms, it's a good time to mention that
Questions provides an utility method for updating objects with data coming
from a form::

    @app.route("/", methods=("POST",))
    def post():
        form = ProfileForm()
        profile = User.get_profile("jsmith")  # sample generic code
        form_data = request.get_json()
        form.update_object(profile, form_data)

The ``update_object`` method does two things. First, it validates the data,
to avoid getting invalid data into the object. It then goes through all the
form fields and sets the corresponding attributes of the object with the
values from the form.

Validation
==========

Form questions can have one or more validators assigned. The form data will be
validated on the front end, and the form cannot be sent unless they all pass.
Still, a user or bot could submit a Questions form directly to the Python
view, bypassing the validation. This is why questions includes mirror
validators that perform the same checks as the SurveyJS front end on the
server side.

SurveyJS has five standard validators:

 - `Numeric`. Fails if the question answer is not a number, or if an entered
   number is outside the ``min_value`` and ``max_value`` range.
 - `Text`. Fails the entered text length is outside the ``min_length`` and
   ``max_length`` range.
 - `Expression`. Fails when ``expression`` returns false.
 - `Regex`. Fails if the entered value does not fit a regular expression
   (``regex``).
 - `Email`. Fails if the entered value is not a valid e-mail.

Questions allows the use of any of these validators, using its corresponding
validator classes::

    from questions import Form
    from questions import DropdownQuestion
    from questions import TextQuestion
    from questions import ExpressionValidator
    from questions import NumericValidator

    class ValidatedForm(Form):
        age = TextQuestion(
            input_type="number",
            validators=[
                NumericValidator(
                    max_value=130,
                    message="We sincerely doubt that is your age",
                )
            ]
        )
        tickets = DropdownQuestion(
            choices=[1, 2, 3, 4, 5],
            validators = [
                ExpressionValidator(
                    expression="{age} > 18 or {tickets} < 2",
                    message="Minors can only buy one ticket",
                )
            ]
        )

Notice that the expression validator allows referring to any other question
on the form, using the question name in brackets. This permits complex
validations.

As mentioned above, validation will be performed in the front end, but it is
recommended to call the mirroring server side validation anyway, for safety.
To do that simply call the ``validate`` method on the form data::

    @app.route("/", methods=("POST",))
    def post():
        form = form.ValidatedForm()
        form_data = request.get_json()
        if form.validate(form_data):
            # validation successful. Save data or something.
            return redirect("success_page")
        else:
            return form.render_html(form_data=form_data)

This example demonstrates a common pattern for responding to form POST
requests. If the validation is successful, the data is saved, and then we
return a redirection to the success or thanks page. If validation fails,
we redisplay the form with the data that was sent, and the errors will be
highlighted.
