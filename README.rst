yafowil.demo
============

Demo Application for YAFOWIL.


Installation
------------

::

    pip install gunicorn yafowil.demo


Running
-------

::

    gunicorn yafowil.demo:app -t 3600 -b 127.0.0.1:8080

Browse localhost:8080

Try bootstrap 3 theme (bootstrap 5 is default)::

    export YAFOWIL_THEME=bootstrap3
    gunicorn yafowil.demo:app -t 3600 -b 127.0.0.1:8080


Development
-----------

Build docker container::

    make install
    docker compose build
