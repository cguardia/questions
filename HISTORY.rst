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

* Update dependencies to lastest versions.

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

* Use correct default value for allow_clear in sugnature pad.

* Set type hints to allow localization arrays in visible text properties.

* Fix bug when generating classes from JSON with dynamic panels.

* Add string representation methods to main classes.

* Feature: add console script for generating code for classes created with
  from_json method.
