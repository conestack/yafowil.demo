yafowil.demo
============

Demo Application for YAFOWIL.

Installation
------------

Create ``buildout.cfg`` containing::

    [buildout]
    extends = dev.cfg

    [run]
    recaptcha_private_key = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    recaptcha_public_key = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

Run buildout and start application with generated ``run.sh`` script::

    ./run.sh

Connect your browser to ``http://localhost:8000/``
