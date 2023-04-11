=======
History
=======

0.5.0a0 (2020-10-01)
--------------------

* First release on PyPI.

0.5.0a1 (2020-12-09)
--------------------

* Fix bug that caused Questions to crash when two or more panels were used in
  one form.

* Add feature for creating Form subclasses from JSON data.

* Add screencast to README page.

* Update docs.

* Update dependencies to latest versions.

0.5.0a2 (2020-12-09)
--------------------

* Fix bug with form parameters in from_json conversion.

0.5.0a3 (2020-12-10)
--------------------

* Make sure jinja templates are included in manifest.

0.7.0a4 (2020-12-13)
--------------------

* Update installation docs to mention typing-extensions requirement for
  Python < 3.8.

* Use correct default value for allow_clear in signature pad.

* Set type hints to allow localization arrays in visible text properties.

* Fix bug when generating classes from JSON with dynamic panels.

* Add string representation methods to main classes.

* Feature: add console script for generating code for classes created with
  from_json method.

0.7.1 (2022-09-18)
------------------

* Bug fix: do not add a default page when other pages are defined.
* Update js CDN and tests.

0.8.0 (2023-04-10)
------------------

* Bug fix: fix choices with translatable text (thanks @joan-qida).
* Bug fix: fix read the docs build.
* Update SurveyJS version.
* Use current SurveyJS supported themes.
* Include newer Python versions in tests.
* Add documentation for i18n.
* Various dependency updates.
