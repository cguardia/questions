.. highlight:: shell

============
Installation
============


Stable release
--------------

To install Questions, run this command in your terminal:

.. code-block:: console

    $ pip install questions

This is the preferred method to install Questions, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for Questions can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/cguardia/questions

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/cguardia/questions/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/cguardia/questions
.. _tarball: https://github.com/cguardia/questions/tarball/master


Installing SurveyJS locally
---------------------------

Questions can be used without installing the SurveyJS Javascript resources,
because by default it gets all resources from a CDN, but sometimes it's
necessary to install all resources locally. Questions does its best to make
that as easy as possible.

The easiest way to install SurveyJS is to use npm_. This is also the recommended
way to go if your project will be using other JS modules. Simply add the SurveyJS
module corresponding to your platform to the dependencies section in your
``package.json`` file:

 - survey-angular
 - survey-jquery
 - survey-knockout
 - survey-react
 - survey-vue

It's also necessary to add the SurveyJS custom widgets (`surveyjs-widgets`),
since they are included in Questions.

If you have ``npm`` available, but are not building a JS application and only
want the SurveyJS resources, create a directory for static resources in your
Python web application project, and do the following:

.. code-block:: console

    $ mkdir static
    $ cd static
    $ npm install survey-knockout
    $ npm install surveyjs-widgets

These commands will download the complete set of resources for the selected
platform. After they complete successfully, the files will be under
`./static/node_modules/`.

If ``npm`` is not available, or you can't use it, Questions includes a command
line script to download the required files. Make sure your virtual environment
is activated (or use the full path to the `bin` directory) and run this command:

.. code-block:: console

    $ download_surveyjs path/to/static/dir {platform} {theme}

The platforms are:

 - angular
 - jquery
 - knockout
 - react
 - vue

The themes are:

 - default
 - bootstrap
 - darkblue
 - darkrose
 - modern
 - orange
 - stone
 - winter
 - winterstone

This command will download all the required resources to the directory specified.
This is by far the simplest way to get running if you don't plan to do any
javascript development as part of your application.

Independently of the method you use to download the resources. You will need to
set up your application to use the resulting resource directory. If all
resources are present in the same directory, all that is needed is to pass in
the URL for this directory when creating the form, like this::

    form = Form(resource_url="/static/your/path")

If the resources are stored using ``npm`` or a different directory layout, it
will be necessary to add the resource definitions to the HTML templates by hand.
How to do this varies from framework to framework. In Flask, the following will
work, assuming you are using the default `static` directory:

.. code-block:: html+jinja

    <script src="{{ url_for('static',
        filename='npm_modules/survey-knockout/survey.ko.min.js') }}">
    </script>

    <link rel="stylesheet" href="{{ url_for('static',
        filename='npm_modules/survey-knockout/survey.css') }}" />

Resources vary by platform, theme and types of questions used. To make sure you
have all the required resources for your application, Questions includes a
script to list them:

.. code-block:: console

    $ list_resources {platform} {theme}

This will list all required resources. Note that custom widgets, like Select2,
require extra JS and CSS resources. To find out if the question types you are
using depend on extra resources, add the `'--include-widgets`` flag to the
command.

.. _npm: https://www.npmjs.com/get-npm
