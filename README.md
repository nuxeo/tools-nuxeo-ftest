# Nuxeo resources for functional tests

This Maven project produces a ZIP file containing resources for ease
running functional tests. Currently, it manages HTML Selenium test
suites, Java WebDriver test suites and FunkLoad test and benchmark.

## Requirements

Functional tests require Firefox 3.6 or Higher. Some tests can also be
run using other browsers than Firefox.

For use on a headless server, a good solution is using x11vnc + Xvfb.

To run benchmark you need to install:

   * [FunkLoad](http://funkload.nuxeo.org/installation.html)

       sudo easy_install -f http://funkload.nuxeo.org/snapshots/ -U funkload

   * curl:

       sudo apt-get install curl

To enable monitoring and reporting:

   sudo apt-get install sysstat atop gnuplot logtail pgfouine
   sudo easy_install logchart


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
set the default URL, allow upload of files holds the base URL,...  It
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

    mvn verify [-f path/to/pom.xml] [-DsomeParam=someValue]

  Maven verify phase automatically calls the previous phases (validate, compile,
  test, package, pre-integration-test, integration-test and post-integration-test).
  See [the Introduction to the Build Lifecycle](http://maven.apache.org/guides/introduction/introduction-to-the-lifecycle.html#Lifecycle_Reference)
  for more details.

### Skip pre- and post- integration phases

  You can avoid executing the whole lifecycle by directly calling a phase on the wanted plugin.
  For instance, if you only want to execute the tests (avoid pre-integration and post-integration phase
  which are starting and stopping Nuxeo), then verify the results.

#### Selenium tests

    mvn org.nuxeo.build:ant-assembly-maven-plugin:integration-test [-Dtarget=run-selenium] [...]
    mvn org.nuxeo.build:ant-assembly-maven-plugin:verify [...]

  The two phases can be called within the same line.

#### WebDriver tests

    mvn org.apache.maven.plugins:maven-failsafe-plugin:integration-test [-Dlog4j.configuration=src/main/resources/log4j.xml] [-Dnuxeo.log.dir=target] [...]
    mvn org.apache.maven.plugins:maven-failsafe-plugin:verify [...]

  The two phases can be called within the same line.

## Available parameters

### System parameters

  The following system parameters are read:

  * `NUXEO_HOME`: if set, takes precedence over nuxeo.home and default values
  * `NUXEO_CONF`: if set, takes precedence over nuxeo.conf and default values
  * `NX_JAVA_HOME`: if set, the server will use this as Java home instead of `JAVA_HOME`

### Java parameters

  The following Java parameters may be given from the command line (with `-DsomeParam=someValue`)
  or from your customized itest.xml file (preferred method; with `<property name="someParam" value="someValue" />`):

  * `nuxeoURL`: default value is `http://localhost:8080/nuxeo/`.
  * `suites`: comma separated Selenium HTML suites' names (without the extension ".html") which must stored in a "tests" directory.
  * `browser`: default value is "chrome".
  * `out.dir`: default value is `${maven.project.build.directory}`.
  * `nuxeo.home`: if `NUXEO_HOME` environment property is not set, default value depends on Maven profile, then values `${out.dir}/tomcat`.
  * `nuxeo.conf`: if `NUXEO_CONF` environment property is not set, default value is `${nuxeo.home}/bin/nuxeo.conf`.
  * `mp.install`: a comma-separated list of instructions for the Marketplace install process. For instance `file:/path/to/some/marketplace-package-1.0-SNAPSHOT.zip`.
  * `zip.file`: the zipped server to use for testing instead of downloading a new one.
  * `env.NUXEO_HOME`: the server to use for testing instead of downloading a new one. Note that its nuxeo.conf file might be changed when running tests.

#### Nuxeo server

The Nuxeo server against which the tests are ran can be:

  * downloaded (default): if `zip.file` and `env.NUXEO_HOME` are not set,
    the artifact `${server.gav}` will be downloaded.
    The default values is `org.nuxeo.ecm.distribution:nuxeo-server-tomcat::zip` (for Tomcat).
  * unzipped from a local archive: using `zip.file` if set.
  * a local directory: using `env.NUXEO_HOME` if set.

### Database parameters

  You can ask the framework to prepare a database to connect to and modify the nuxeo.conf to point to it.
  The choice of the database engine is done by activating the corresponding profile.
  Valid choices are: pgsql (PostgreSQL), mssql (MsSQL), oracle10g (Oracle 10g), oracle11g (Oracle 11g), mysql (MySQL), mariadb (MariaDB)

  The following environment variables are used:

  * `NX_DB_HOST`: database host
  * `NX_DB_PORT`: database port
  * `NX_DB_ADMINNAME`: name of the administrative/default database
  * `NX_DB_ADMINUSER`: database superuser
  * `NX_DB_ADMINPASS`: superuser password
  * `NX_DB_NAME`: name of the database used by nuxeo
  * `NX_DB_USER`: username used by nuxeo to connect to the database
  * `NX_DB_PASS`: password used by nuxeo to connect to the database

  If the administrative parameters are missing, the nuxeo.conf will be modified with the correct values,
  but the build process will not try to create the database nor the user.

  For Oracle, the `NX_DB_ADMINNAME` and `NX_DB_NAME` must be identical (the instance SID).

  If the `NX_DB_NAME`, `NX_DB_USER` or `NX_DB_PASS` are not specified, they will be generated randomly.
  Caveat: if you execute db-create and db-drop in different passes, the generated values will be different.

### NoSQL Database parameters

  Valid choices are: mongodb (MongoDB)

  The following environment variables are used:

  * `NX_MONGODB_SERVER`: MongoDB server URI. Mapped with `nuxeo.mongodb.server` Nuxeo configuration property and defaults to `localhost:27017`
  * `NX_MONGODB_DBNAME`: MongoDB database Name. Mapped with `nuxeo.mongodb.dbname` Nuxeo configuration property and defaults to `nxdbname${rndid}` (`rndid` is a random ID)

## Creating your own Ant targets or overriding existing ones

  As shown in the samples, your customized `itests.xml` will unzip and import `nuxeo-ftest.xml`:

    <unzip dest="${out.dir}/" overwrite="false">
      <artifact:resolveFile key="org.nuxeo:nuxeo-ftest::zip" />
    </unzip>
    <import file="${out.dir}/nuxeo-ftest.xml" />

  Then, you can freely add your own targets, reuse existing targets from `nuxeo-ftest.xml` or override them.

### Targets overview

  * `download`: download and unzip `${groupId}:${artifactId}::zip:${classifier}` from Maven
  * `unzip-local`: alternative to the `download` target. Use a local ZIP archive instead.
  * `prepare-environment`, `prepare-db`, `prepare-tomcat`, `prepare-selenium`: various targets for preparing the testing environment.
  * `run-selenium`: macro target for preparing the environment, starting the server, running the tests, stopping the server.
  Will exit with an error value if a testing suite failed.
  * `set-conf`: convenience target for adding a property to nuxeo.conf
  * `start`, `stop`: start or stop the server.
  * `cleanup-db`: can be used after the tests to remove the user and database that were created for the test.
  * `mp-install`: add comma-separated instructions defined in the `mp.install` property.

## QA results

[![Build Status](https://qa.nuxeo.org/jenkins/buildStatus/icon?job=Misc/tools_nuxeo-ftest-master)](https://qa.nuxeo.org/jenkins/job/Misc/job/tools_nuxeo-ftest-master/)

# About Nuxeo

Nuxeo dramatically improves how content-based applications are built, managed and deployed, making customers more agile, innovative and successful. Nuxeo provides a next generation, enterprise ready platform for building traditional and cutting-edge content oriented applications. Combining a powerful application development environment with SaaS-based tools and a modular architecture, the Nuxeo Platform and Products provide clear business value to some of the most recognizable brands including Verizon, Electronic Arts, Sharp, FICO, the U.S. Navy, and Boeing. Nuxeo is headquartered in New York and Paris. More information is available at www.nuxeo.com.
