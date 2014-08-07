sriracha
========

Image albums and gallery with local filesystem, imgur, and flickr support.
Powered by wok, a static website generator.

Authors:

- [Kevin Ngo](http://ngokevin.com)
- [Jacques Uber](http://uberj.com)

Requirements (through pip):

- PIL
- requests
- wok

Live Sites
==========

Sriracha is hot!

- [ngokevin](http://ngokevin.com/photography)
- [molly.cat](http://molly.cat)
- [sriracha demo](http://sriracha.ngokevin.com)

Setup
=====

Run ```wok``` or ```wok --server``` to generate the site.

Local Filesystem Images
=======================

Albums are folders located in ```media/img/gallery/```.

Store images in the album folder.

The name of the album folder must match the slug in the album's ```.mkd```
content file in ```content/gallery```.

Imgur Images
============

Albums are albums created on ```imgur.com```.

Create a imgur client key and store in ```hooks/config.py``` in ```IMGUR_CLIENT_ID```.

In the album's ```.mkd``` content file in ```content/gallery```, set the
```source``` to ```imgur```. Set the ```album-id``` to the album slug from
imgur.


Flickr Images
=============

Albums are photosets created on ```flickr.com```.

Create a flickr client key and store in ```hooks/config.py``` in ```FLICKR_CLIENT_ID```.

In the album's ```.mkd``` content file in ```content/gallery```, set the
```source``` to ```flickr```. Set the ```album-id``` to the photoset ID from
flickr.


Screenshots
===========

![gallery](http://imgur.com/9EYEUol.jpg)

![album](http://imgur.com/pT2t0aj.jpg)
