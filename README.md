# Nuxeo resources for functional tests

This Maven project produces a zip file containing resources for ease running functional tests.
Currently, it only manages HTML Selenium test suites.


## Preparing the infrastructure for running functional tests

  * Copy pom.xml.sample and assembly.xml.sample at root of a directory.
  * Rename (removing ".sample"), edit and adapt those files to your case.


## Preparing tests resources

  * Create a tests directory containing your HTML tests suites.
  * Create a data directory containing data resources for your tests.


## Running the functional tests

  Run the following Maven command to launch the testing suites:

    mvn integration-test [-f path/to/pom.xml] [-DnuxeoURL=http://otherURL/] [-Dsuites=...] -P[tomcat|jboss]

  Note should avoid specifying the suites in the command line by setting them via the "suites" parameter in your customized assembly.xml file.


## About Nuxeo

Nuxeo provides a modular, extensible Java-based [open source software platform for enterprise content management] [1] and packaged applications for [document management] [2], [digital asset management] [3] and [case management] [4]. Designed by developers for developers, the Nuxeo platform offers a modern architecture, a powerful plug-in model and extensive packaging capabilities for building content applications.

[1]: http://www.nuxeo.com/en/products/ep
[2]: http://www.nuxeo.com/en/products/document-management
[3]: http://www.nuxeo.com/en/products/dam
[4]: http://www.nuxeo.com/en/products/case-management

More information on: <http://www.nuxeo.com/>