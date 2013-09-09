sriracha
========

Image albums and gallery for use with Wok, with local filesystem and imgur support.

Requirements (through pip):

PIL
requests
wok

Setup
=====

Run ```wok```.

Local Filesystem Images
=======================

Albums are folders located in ```media/img/gallery/```.

Store images in the album folder.

The name of the album folder must match the slug in the album's ```.mkd``` content file in ```content/gallery```.

Imgur Images
============

Albums are albums created on ```imgur.com```.

Create a imgur client key and store in ```hooks/config.py``` in ```imgur_client_id```.

In the album's ```.mkd``` content file in ```content/gallery```, set the ```source``` to ```imgur```. Set the ```album-id``` to the album slug from imgur.
