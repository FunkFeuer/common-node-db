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

  * **make sure that the locale is set to `utf-8`, not ascii**

- Webserver, one of:

  * nginx plus uwsgi

  * Apache plus mod-fcgid or mod-wsgi

- PostgreSQL

  * an account for the web app that can create databases and tables

- git, unless the Funkfeuer application, common node database, and tapyr are
  all installed via Debian packages or with ``pip install``.

- Python (2.7 or 3.5+)

- Python packages

  * `Babel`_

  * `BeautifulSoup`_

    optional, only used if the webapp allows user-submitted HTML

  * `docutils`_

  * `flup`_

    only necessary when fcgi is used

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

    **should be used to make webserver responses smaller**

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

Debian Stretch
~~~~~~~~~~~~~~~

You can install for either Python-2 or Python-3. In the following, we will
assume an install for nginx and uwsgi.

For Python-2::

  # export pv=''

For Python-3::

  # export pv='3'

  # # make sure that locale is set to `utf-8` !

Almost all packages can be installed via the Debian Stretch
installer::

  # apt-get install \
      git postgresql sudo \
      python${pv}-babel python${pv}-bcrypt python${pv}-bs4 \
      python${pv}-dateutil python${pv}-docutils python${pv}-jinja2 \
      python${pv}-pip python${pv}-plumbum python${pv}-psycopg2 \
      python${pv}-pyquery python${pv}-rcssmin python${pv}-rjsmin \
      python${pv}-setuptools python${pv}-sqlalchemy python${pv}-tz \
      python${pv}-virtualenv python${pv}-werkzeug \
      nginx-full nginx-doc uwsgi uwsgi-plugin-python${pv}

Other packages can be installed using ``pip``::

  # pip${pv} install rsclib

How to install
--------------

Create user and database user permitted to create databases. For instance,
for Funkfeuer Wien::

  # adduser --system --disabled-password --home /srv/ffw${pv} \
      --shell /bin/bash --group ffw${pv}

  # adduser --disabled-password --home /srv/ffw${pv} --no-create-home \
      --shell /bin/false --ingroup ffw${pv} --quiet ffw${pv}-r

  # sudo -u postgres createuser -d ffw${pv} -P

Note: Depending on your setup the createuser command has to be executed by
a different user.

Assuming an account `ffw${pv}` located in /srv/ffw${pv}, you'll need
something like the following::

  # su - ffw${pv}

    $ export pv='3' ### or '' if you use Python-2
    $ alias python="python${pv}"

    ### Define config
    $ vi .ffw.config
      ### Add the lines (using the appropriate values for **your** install)::
      ### No leading spaces are allowed
      cookie_salt   = 'some random value, e.g., the result of uuid.uuid4 ()'
      db_name       = "ffw<pv>" ### best to use the account name here
      db_url        = "postgresql://<account>:<password>@localhost"
      ### email_from:
      ### - `From` address for emails sent, e.g., password reset
      ### - `To`   address for error emails sent
      ###    (contains tracebacks, request data, etc.)
      email_from    = "admin@funkfeuer.at"
      languages     = "de", "en"
      locale_code   = "de"
      smtp_server   = "localhost"
      target_db_url = db_url   ### Must be equal to `db_name` here
      time_zone     = "Europe/Vienna"

Then we continue with the setup of an active and a passive branch of the
web application. With this you can upgrade the passive application while
the active application is running; without risking a non-functional
system should something go wrong during the upgrade::

    ### * the active branch will be the one that serves webserver requests
    ###
    ### * the passive branch can be used for updating the software and
    ###   testing it. It all works will the branches can be switched

    $ mkdir -p v/1/www
    $ ln -s v/1 passive
    $ ln -s v/2 active
    $ git clone git://github.com/Tapyr/tapyr.git              passive/tapyr
    $ git clone git://github.com/FunkFeuer/common-node-db.git passive/cndb
    $ git clone git://github.com/FunkFeuer/Wien.git           passive/www/app
    $ ( cd passive/www ; ln -s app/media ; mkdir -p app/media/v )
    $ cp -a v/1 v/2

    ### Ensure different `db_name` for v/1 and v/2
    ### (using the appropriate values for **your** install)::
    $ echo 'db_name = "ffw<pv>_a"' > active/.ffw.config
    $ echo 'db_name = "ffw<pv>_b"' > passive/.ffw.config

    ### Define PYTHONPATH used by the application
    $ export PYTHONPATH=~/active/cndb:~/active/tapyr

With a small config-file, the deploy-app can automatically create a
webserver configuration file and a fcgi/wsgi/uwsgi script. You can find
sample config-files in active/www/app/httpd_config/. For instance,
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

    $ cp active/www/app/httpd_config/nodedb_funkfeuer_at__443__nginx.config \
         deploy.config

    $ vi deploy.config
      ### edit the config to your needs
      ### No leading spaces are allowed

    $ mkdir uwsgi
    $ python active/www/app/deploy.py uwsgi_config -apply_to_version active \
        -HTTP_Config deploy.config

You can use the created webserver configuration as is, or modify it
manually or by modifiying the template.

Finally we create a database and populate it with data::

    ### Byte compile python files
    $ python passive/www/app/deploy.py pycompile -apply_to_version active

    ### Compile translations
    $ python passive/www/app/deploy.py babel compile -apply_to_version active

    ### Create a database
    $ python active/www/app/deploy.py app create -apply_to_version active

    ### Make sure the application cache is setup correctly
    $ python active/www/app/deploy.py app setup_cache \
        -apply_to_version active -verbose

    ### Put some data into the database, e.g., by running a converter from
    ### another database

    ### Logout
    $ exit

For Debian, the nginx configuration should be placed into
``/etc/nginx/sites-available/`` and linked to from
``/etc/nginx/sites-enabled/``::

  # cp /srv/ffw${pv}/uwsgi/<your-config-name>.conf /etc/nginx/sites-available/
  # ( cd /etc/nginx/sites-enabled \
    ; echo ln -s ../sites-available/<your-config-name>.conf
    )

For Debian, the uwsgi configuration should be placed into
``/etc/uwsgi/apps-available`` and linked to from
``/etc/uwsgi/apps-enabled``::

  # cp /srv/ffw${pv}/uwsgi/<your-config-name>.ini \
       /etc/uwsgi/apps-available/
  # ( cd /etc/uwsgi/apps-enabled/ \
    ; ln -s ../apps-available/<your-config-name>.ini
    )

To test if the uwsgi configuration is correct, run the following command
and check for errors and the use of the right python interpreter::

  # uwsgi --ini /etc/uwsgi/apps-enabled/<your-config-name>.ini

If that looks good, restart uwsgi and nginx::

  # /etc/init.d/uwsgi restart ; /etc/init.d/nginx restart

How to upgrade the installation
--------------------------------

Whenever we need to upgrade the installation, we can update the passive
configuration, set up everything, migrate the data from the active to
the passive configuration, and if everything went OK, enable it by
exchanging the symbolic links to the active and passive configuration::

  $ export pv='3' ### or '' if you use Python-2
  $ alias python="python${pv}"
  $ export PYTHONPATH=~/passive/cndb:~/passive/tapyr

  ### Update source code
  $ python passive/www/app/deploy.py update

  ### Byte compile python files
  $ python passive/www/app/deploy.py pycompile

  ### Compile translations
  $ python passive/www/app/deploy.py babel compile

  ### Migrate database from active to passive
  $ python passive/www/app/deploy.py migrate -Active -Passive -verbose

  ### Optionally, test if database is still looking good
  $ python passive/www/app/Command.py shell
    ### Use queries in interactive Python shell, like::
    >>> scope.MOM.Id_Entity.count
    >>> scope.CNDB.Node.instance ("some-important-name's-name")
    >>> scope.Auth.Account.query (Q.superuser).all ()

  ### Setup app cache
  $ python passive/www/app/deploy.py setup_cache

  ### Switch active and passive branches
  $ python passive/www/app/deploy.py switch

  $ sudo /etc/init.d/uwsgi restart
  $ sudo /etc/init.d/nginx restart

Contact
-------

Christian Tanzer <tanzer@swing.co.at> and
Ralf Schlatterbeck <rsc@runtux.com>
