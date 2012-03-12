# Nuxeo resources for functional tests

This Maven project produces a zip file containing resources for ease running functional tests.
Currently, it only manages HTML Selenium and Java WebDriver test suites.

## Requirements

Functional tests require Firefox 3.6 or Higher. Some tests can also be
run using other browsers than Firefox.

For use on a headless server, a good solution is using x11vnc + Xvfb.

## Selenium tests

### Preparing the infrastructure for running functional tests

  * Copy samples/selenium/* at root of a directory.
  * Edit and adapt those files to your case.

### Preparing tests resources

  * Create a tests directory containing your HTML tests suites.
  * Create a data directory containing data resources for your tests.

### Test settings

Selenium tests are run using a custom firefox profile, as well as
custom extensions.

The file at ffprofile/prefs.js.sample adds settings on the browser to
set the default url, allow upload of files holds the base url,...  It
also holds the current language (en). When using Selenium IDE, make
sure English is your default language.

user-extensions.js.sample holds helper commands used in suites. It
also sets the current folder absolute path to make it possible to
upload files when running tests.

## WebDriver tests

### Preparing the infrastructure for running functional tests

  * Copy samples/webdriver/* at root of a directory.
  * Edit and adapt those files to your case.

### Preparing tests resources

  * Create a tests directory containing your Java tests suites.

## Running the functional tests

  Run the following Maven command to launch the testing suites:

    mvn verify [-f path/to/pom.xml] [-DsomeParam=someValue] -P[tomcat|jboss]

  Maven verify phase automatically calls the previous phases (validate, compile,
  test, package, pre-integration-test, integration-test and post-integration-test).
  See [the Introduction to the Build Lifecycle](http://maven.apache.org/guides/introduction/introduction-to-the-lifecycle.html#Lifecycle_Reference)
  for more details.

  You can avoid executing the whole lifecycle by directly calling a phase on the wanted plugin.
  For instance, if you only want to execute the tests (avoid pre-integration and post-integration phase
  which are starting and stopping Nuxeo), run:

    mvn org.nuxeo.build:nuxeo-distribution-tools:integration-test -Dtarget=run-selenium

  and for verifying the results:

    mvn nuxeo-distribution-tools:verify [...]

  The two phases can be called within the same line.

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
  * wizard.preset: the wizard preset to activate on the distribution. The value could be `nuxeo-cap` (does nothing), `nuxeo-dm`, `nuxeo-dam`, `nuxeo-cmf` or `nuxeo-sc`, default value is `nuxeo-dm`.
  * mp.install: a comma-separated list of instructions for the Marketplace install process. For instance `file:/path/to/some/marketplace-package-1.0-SNAPSHOT.zip`.
  * zip.file: the zipped server to use for testing instead of downloading a new one.
  * env.NUXEO_HOME: the server to use for testing instead of downloading a new one. Note that its nuxeo.conf file might be changed when running tests.

#### Nuxeo server

The Nuxeo server against which the tests are ran can be:

  * downloaded (default): if `zip.file` and `env.NUXEO_HOME` are not set,
    the artifact `${groupId}:${artifactId}::zip:${classifier}` will be downloaded.
    The default values are `org.nuxeo.ecm.distribution:nuxeo-distribution-tomcat:nuxeo-cap` (for Tomcat)
    and `org.nuxeo.ecm.distribution:nuxeo-distribution-jboss:nuxeo-dm` (for JBoss).
  * unzipped from a local archive: using `zip.file` if set.
  * a local repository: using `env.NUXEO_HOME` if set.

The Nuxeo server type (Tomcat or JBoss) depends on Maven profiles:

  * JBoss if `jboss` Maven profile is activated,
  * Tomcat (default) else, or if `tomcat` Maven profile is activated.

### Database parameters

  You can ask the framework to prepare a database to connect to and modify the nuxeo.conf to point to it.
  The choice of the database engine is done by activating the corresponding profile.
  Valid choices are: pgsql (PostgreSQL), mssql (MsSQL), oracle10g (Oracle 10g), oracle11g (Oracle 11g), mysql (MySQL)

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
  * activate-wizard-preset: activate the wizard preset defined in the `wizard.preset` property.
  * mp-install: add comma-separated instructions defined in the `mp.install` property.

## About Nuxeo

Nuxeo provides a modular, extensible Java-based [open source software platform for enterprise content management] [1] and packaged
applications for [document management] [2], [digital asset management] [3] and [case management] [4]. Designed by developers for developers,
the Nuxeo platform offers a modern architecture, a powerful plug-in model and extensive packaging capabilities for building content applications.

[1]: http://www.nuxeo.com/en/products/ep
[2]: http://www.nuxeo.com/en/products/document-management
[3]: http://www.nuxeo.com/en/products/dam
[4]: http://www.nuxeo.com/en/products/case-management

More information on: <http://www.nuxeo.com/>
