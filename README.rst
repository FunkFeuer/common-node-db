README for the CNDB model
===========================

:Authors:

    Christian Tanzer
    <tanzer@swing.co.at>

    Ralf Schlatterbeck
    <rsc@runtux.com>

The common node database is a framework that captures the object model for
community networks, in particular community wireless networks.

It uses the `tapyr framework`_.

.. _`tapyr framework`: https://github.com/Tapyr/tapyr

Object model
------------

This object model (in SVG format) is automagically rendered using
`graph.py`_, the result of the last run is kept under version control
(so you can see our progress) in `nodedb.svg`_.

.. _`nodedb.svg`: https://github.com/FunkFeuer/common-node-db/blob/master/doc/nodedb.png
.. _`graph.py`: https://github.com/FunkFeuer/common-node-db/blob/master/_CNDB/_OMP/graph.py

.. image:: https://raw.githubusercontent.com/CNDB/CNDB/master/doc/nodedb.png
    :alt: Object model graph
    :target: https://github.com/FunkFeuer/common-node-db/blob/master/doc/nodedb.png

Some notes on the object model: We try to keep only the relevant
attributes of a real-world object in the object itself — everything
else is modelled as a relation. The blue arrows denote inheritance
relationships ("IS_A"). The yellow arrows are attributes, e.g., the Node
has an attribute ``manager`` of type ``Person`` which is required (this
is implemented as a foreign key in the database).

The black arrows are 1:N relationships (also implemented as foreign keys
in the database) but the relation objects have their own identity. This
is used to separate the attribute of an object from its links to other
objects. It also implements referential integrity constraints: A link is
deleted if the object to which it points is deleted.

There are different link attributes. A two-way link (implementing an N:M
relationship) has a ``left`` and a ``right`` side which are also the
default attribute names. An example is
``Wireless_Interface_uses_Wireless_Channel``, in the diagram this link
object is displayed as ``_uses_`` between the ``CNDB.Wireless_Channel``
and ``CNDB.Wireless_Interface``. The black arrows connecting these are
labelled ``left`` and ``right`` which indicates how this should be read.
Note that in this case the ``left`` attribute is on the right side in
the diagram. A two-way link like this has an identity and can have
additional attributes besides ``left`` and ``right``.

There are also unary links with only a ``left`` side. An example is the
``Device`` which cannot exist without its ``left`` attribute, the
``Device_Type``. There can be several devices with the same device type.
This relationship is inherited by ``Antenna`` and ``Antenna_Type`` and
``Net_Device`` and ``Net_Device_Type``.


System requirements
--------------------

- Linux or OS X

  * its best to set up a separate account that runs the CNDB instance

- Webserver, one of:

  * nginx plus uwsgi

  * Apache plus mod-fcgid or mod-wsgi

- PostgreSQL

  * an account for the web app that can create databases and tables

- git

- Python (2.7 or 3.5)

  * `rsclib` is not Python 3 compatible, all other code is

- Python packages

  * `Babel`_

  * `BeautifulSoup`_

    optional, only used if the webapp allows user-submitted HTML

  * `docutils`_

  * `flup`_

    optional, necessary when fcgi is used

  * `jinja2`_

  * `py-bcrypt`_

    optional but seriously recommended for improved password hashing

  * `plumbum`_

  * `psycopg2`_

  * `pyquery`_

    optional, only used in some unit tests

  * `pyspkac`_, `pyasn1`_, `m2crypto`_, `pyOpenSSL`_

    optional, only used for client certificates

  * `python-dateutil`_

  * `pytz`_

  * `cssmin`_ or `rcssmin`_, `jsmin` or `rjsmin`_

    optional, only used during deployment for minimization of CSS and
    Javascript files

    `rcssmin` and `rjsmin` are much faster than `cssmin` and `jsmin`

  * `rsclib`_

  * `sqlalchemy`_

  * `werkzeug`_

  Most packages are available via the `Python Package Index`_

.. _`Babel`:           http://babel.edgewall.org/
.. _`BeautifulSoup`:   http://www.crummy.com/software/BeautifulSoup/
.. _`Python Package Index`: http://pypi.python.org/pypi
.. _`cssmin`:          https://github.com/zacharyvoase/cssmin
.. _`docutils`:        http://docutils.sourceforge.net/
.. _`flup`:            http://trac.saddi.com/flup
.. _`jinja2`:          http://jinja.pocoo.org/
.. _`jsmin`:           https://bitbucket.org/dcs/jsmin/
.. _`m2crypto`:        http://pypi.python.org/pypi/M2Crypto
.. _`passlib`:         http://code.google.com/p/passlib/
.. _`plumbum`:         http://plumbum.readthedocs.org/en/latest/index.html
.. _`psycopg2`:        http://packages.python.org/psycopg2/
.. _`py-bcrypt`:       http://code.google.com/p/py-bcrypt/
.. _`pyOpenSSL`:       https://launchpad.net/pyopenssl
.. _`pyasn1`:          http://pyasn1.sourceforge.net/
.. _`pyquery`:         http://github.com/gawel/pyquery/
.. _`pyspkac`:         https://pypi.python.org/pypi/pyspkac
.. _`python-dateutil`: http://labix.org/python-dateutil
.. _`pytz`:            http://pytz.sourceforge.net/
.. _`rcssmin`:         http://opensource.perlig.de/rcssmin/
.. _`rjsmin`:          http://opensource.perlig.de/rjsmin/
.. _`rsclib`:          http://rsclib.sourceforge.net/
.. _`sqlalchemy`:      http://www.sqlalchemy.org/
.. _`werkzeug`:        http://werkzeug.pocoo.org/

Package Installation for Debian
-------------------------------

The following is an example installation on Debian. It contains
some information that is applicable to other distributions but is quite
Debian-specific in other parts.

If you are running in a virtual machine, you need at least 384 MB of
RAM, 256 MB isn't enough.


Debian Jessie
~~~~~~~~~~~~~

Almost all packages can be installed via the Debian Jessie
installer::

 $ apt-get --no-install-recommends install \
     git postgresql python-babel python-bcrypt python-bs4 \
     python-dateutil python-docutils python-jinja2 \
     python-pip python-plumbum python-psycopg2 python-pyquery \
     python-rcssmin python-rjsmin python-sqlalchemy python-tz \
     python-werkzeug

Depending on the webserver you want to use, either::

 $ apt-get --no-install-recommends install \
     uwsgi uwsgi-plugin-python
 $ apt-get --no-install-recommends -t jessie-backports install \
     nginx-full nginx-doc

or::

 $ apt-get --no-install-recommends install \
     apache2-mpm-worker libapache2-mod-fcgid python-flup

Other packages can be installed using ``pip``::

 $ pip install rsclib


How to install
--------------

Create user and database user permitted to create databases. For instance,
for Funkfeuer Wien::

 $ adduser --system --disabled-password --home /srv/ffw --shell /bin/bash --group ffw
 $ adduser --disabled-password --home /srv/ffw --shell /bin/false --ingroup ffw ffw-r
 $ sudo -u postgres createuser -d ffw -P

Note: Depending on your setup the createuser command has to be executed by
a different user.

Assuming an account `ffw` located in /srv/ffw, you'll need something
like the following::

  ### Logged in as `ffw`
  $ cd

  ### Define config
  $ vi .ffw.config
    ### Add the lines (using the appropriate values for **your** install)::
    ### No leading spaces are allowed
      cookie_salt   = 'some random value, e.g., the result of uuid.uuid4 ()'
      db_name       = "ffw"
      db_url        = "postgresql://<account>:<password>@localhost"
      languages     = "de", "en"
      locale_code   = "de"
      smtp_server   = "localhost"
      target_db_url = db_url
      time_zone     = "Mars/Olympos Mons"

Then we continue with the setup of an active and a passive branch of the
web application. With this you can upgrade the passive application while
the active application is running without risking a non-functional
system should something go wrong during the upgrade::

  ### create a directory with an `active` and `passive` branch of the
  ### web application
  ###
  ### * the active branch will be the one that serves apache requests
  ###
  ### * the passive branch can be used for updating the software and
  ###   testing it. It all works will the branches can be switched
  ###

  $ mkdir fcgi
  $ mkdir -p v/1/www/media
  $ ln -s v/1 active
  $ ln -s v/2 passive
  $ git clone git://github.com/Tapyr/tapyr.git              v/1/tapyr
  $ git clone git://github.com/FunkFeuer/common-node-db.git v/1/cndb
  $ git clone git://github.com/FunkFeuer/Wien.git           v/1/www/app
  $ (cd v/1/www/media ; ln -s ../app/media/images images)
  $ cp -a v/1 v/2

  $ vi active/.ffw.config
    ### Add the lines (using the appropriate values for **your** install)::
      db_name       = "ffw1"
  $ vi passive/.ffw.config
      db_name       = "ffw2"

  ### Define PYTHONPATH
  $ export PYTHONPATH=~/active/cndb:~/active/tapyr

With a small config-file, the deploy-app can automatically create an
Apache configuration file and a fcgi script. You can find sample
config-files in active/www/app/httpd_config/. For instance,
active/www/app/httpd_config/nodedb_funkfeuer_at__443.config contains::

      config_path         = "~/fcgi/nodedb_funkfeuer_at__443.config"
      host_macro          = "gtw_host_ssl"
      port                = "443"
      script_path         = "~/fcgi/nodedb_funkfeuer_at__443.fcgi"
      server_admin        = "admin@funkfeuer.at"
      server_name         = "nodedb.funkfeuer.at"
      ssl_certificate     = "nodedb.funkfeuer.at.crt"
      ssl_certificate_key = "nodedb.funkfeuer.at.key"

Please note, the lines in the file must not contain leading whitespace.

Create a config::

  ### Create a fcgi script and config for Apache
  $ cp active/www/app/httpd_config/ffw_gg32_com__443.config deploy.config
  $ vi deploy.config
    ### edit the config to your needs
  $ python active/www/app/deploy.py fcgi_config \
      -HTTP_Config <your-config> -apache2_4 -input_encoding=utf-8

Finally we create a database and populate it with data::

  ### Create a database
  $ python active/www/app/deploy.py app create -apply_to_version active

  ### Put some data into the database

Log out user `ffw`

You can use the created Apache configuration as is, or modify it
manually or by modifiying the template.

For Debian, the apache configuration should be placed into
``/etc/apache2/sites-available/``, e.g., into the file
``nodedb2.example.com``, and enabled. You probably will have to disable
the default site installed. We used the following commands — we
also enable some needed modules::

  $ a2ensite nodedb2.example.com
  $ a2dissite default
  $ a2enmod expires
  $ a2enmod fcgid
  $ /etc/init.d/apache2 restart

For https sites, you'll also need the modules::

  $ a2enmod rewrite
  $ a2enmod ssl

Whenever we need to upgrade the installation, we can update the passive
configuration, set up everything, migrate the data from the active to
the passive configuration, and if everything went OK, enable it by
exchanging the symbolic links to the active and passive configuration::

  ### Test deployment script and generate some needed files
    ### Update source code
    $ python passive/www/app/deploy.py update

    ### Byte compile python files
    $ python passive/www/app/deploy.py pycompile

    ### Compile translations
    $ python passive/www/app/deploy.py babel compile

    ### Migrate database from active to passive
    $ python passive/www/app/deploy.py migrate -Active -Passive -verbose

    ### Setup app cache
    $ python passive/www/app/deploy.py setup_cache

  ### Switch active and passive branches
  $ python passive/www/app/deploy.py switch
  $ sudo /etc/init.d/apache2 restart

Contact
-------

Christian Tanzer <tanzer@swing.co.at> and
Ralf Schlatterbeck <rsc@runtux.com>
