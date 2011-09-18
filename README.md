# Nuxeo resources for functional tests

This Maven project produces a zip file containing resources for ease running functional tests.
Currently, it only manages HTML Selenium and Java WebDriver test suites.

## Selenium tests

### Preparing the infrastructure for running functional tests

  * Copy samples/selenium/pom.xml and samples/selenium/itests.xml at root of a directory.
  * Edit and adapt those files to your case.

### Preparing tests resources

  * Create a tests directory containing your HTML tests suites.
  * Create a data directory containing data resources for your tests.

## Webdriver tests

### Preparing the infrastructure for running functional tests

  * Copy samples/webdriver/pom.xml and samples/webdriver/itests.xml at root of a directory.
  * Edit and adapt those files to your case.

### Preparing tests resources

  * Create a tests directory containing your Java tests suites.

## Running the functional tests

  Run the following Maven command to launch the testing suites:

    `mvn verify [-f path/to/pom.xml] [-DsomeParam=someValue] -P[tomcat|jboss]`

## Available parameters

### System parameters

  The following system parameters are read:

  * NUXEO_HOME: if set, takes precedence over nuxeo.home and default values
  * NUXEO_CONF: if set, takes precedence over nuxeo.conf and default values
  * NX\_JAVA\_HOME: if set, the server will use this as Java home instead of JAVA_HOME

### Maven parameters

  Two Maven profiles are taken in account when setting nuxeo.home: "tomcat" or "jboss".

### Java parameters

  The following Java parameters may be given from the command line (with `-DsomeParam=someValue`)
  or from your customized itest.xml file (preferred method; with `<property name="someParam" value="someValue" />`):

  * nuxeoURL: default value is `http://localhost:8080/nuxeo/`.
  * suites: comma separated Selenium HTML suites' names (without the extension ".html") which must stored in a "tests" directory.
  * browser: default value is "chrome".
  * out.dir: default value is `${maven.project.build.directory}`.
  * nuxeo.home: if NUXEO_HOME environment property is not set, default value depends on Maven profile, then values `${out.dir}/tomcat`.
  * nuxeo.conf: if NUXEO_CONF environment property is not set, default value is `${nuxeo.home}/bin/nuxeo.conf`.
  * zip.file: if set, the server will be unzipped from local file `${zip.file}` instead of being downloaded.
  * groupId, artifactId and classifier: if zip.file is not set, `${groupId}:${artifactId}::zip:${classifier}` will be downloaded.

    Default values respectively are `org.nuxeo.ecm.distribution`, `nuxeo-distribution-tomcat` or `nuxeo-distribution-jboss`, `nuxeo-dm`.

### Database parameters

  You can ask the framework to prepare a database to connect to and modify the nuxeo.conf to point to it.
  The choice of the database engine is done by activating the corresponding profile.
  Valid choices are: pgsql, mssql, oracle10g, oracle11g, mysql

  The following environment variables are used:
  
  * NX\_DB\_HOST : database host
  * NX\_DB\_PORT : database port
  * NX\_DB\_ADMINNAME : name of the administrative/default database
  * NX\_DB\_ADMINUSER : database superuser
  * NX\_DB\_ADMINPASS : superuser password
  * NX\_DB\_NAME : name of the database used by nuxeo
  * NX\_DB\_USER : username used by nuxeo to connect to the database
  * NX\_DB\_PASS : password used by nuxeo to connect to the database

  If the administrative parameters are missing, the nuxeo.conf will be modified with the correct values,
  but the build process will not try to create the database nor the user.

  For Oracle, the NX\_DB\_ADMINNAME and NX\_DB\_NAME must be identical (the instance SID).

  If the NX\_DB\_NAME, NX\_DB\_USER or NX\_DB\_PASS are not specified, they will be generated randomly.
  Caveat: if you execute db-create and db-drop in different passes, the generated values will be different.

## Creating your own Ant targets or overriding existing ones

  As shown in the samples, your customized itests.xml will unzip and import nuxeo-ftest.xml:

    <unzip dest="${out.dir}/" overwrite="false">
      <artifact:resolveFile key="org.nuxeo:nuxeo-ftest::zip" />
    </unzip>
    <import file="${out.dir}/nuxeo-ftest.xml" />

  Then, you can freely add your own targets, reuse existing targets from nuxeo-ftest.xml or override them.

### Targets overview

  * download: download and unzip ${groupId}:${artifactId}::zip:${classifier} from Maven
  * unzip-local: alternative to "download" target. Use a local ZIP archive instead.
  * prepare-environment, prepare-db, prepare-jboss, prepare-tomcat, prepare-selenium: various targets for preparing the testing environment.
  * run-selenium: macro target for preparing the environment, starting the server, running the tests, stopping the server.
  Will exit with an error value if a testing suite failed.
  * set-conf: convenience target for adding a property to nuxeo.conf
  * wizard-on, wizard-off: deprecated targets for setting on/off the wizard; prefer use of "set-conf".
  * start, stop: start or stop the server.
  * cleanup-db: can be used after the tests to remove the user and database that were created for the test.

## About Nuxeo

Nuxeo provides a modular, extensible Java-based [open source software platform for enterprise content management] [1] and packaged
applications for [document management] [2], [digital asset management] [3] and [case management] [4]. Designed by developers for developers,
the Nuxeo platform offers a modern architecture, a powerful plug-in model and extensive packaging capabilities for building content applications.

[1]: http://www.nuxeo.com/en/products/ep
[2]: http://www.nuxeo.com/en/products/document-management
[3]: http://www.nuxeo.com/en/products/dam
[4]: http://www.nuxeo.com/en/products/case-management

More information on: <http://www.nuxeo.com/>
