PyMirage -- Find similar songs
===============================

PyMirage implements the functionality of Mirage (http://hop.at/mirage/) in Python.

It is useful for finding similar music, and for generating playlists

Functionality
--------------
* Compute similarity between songs
* [TODO] walk through full music collection
* [TODO] copy files onto MP3 player from a few existing songs
* [TODO] generate a playlist from a few recent songs
* [TODO] generate a gephi visualization from distances
* [TODO] integrate into various players (AmaroK, clementine, ...)
	* for this, need notification when a track was completed (or is almost complete)
	* and need a channel to suggest next few songs
	* and need to keep track to avoid repeating stuff


Differences to Mirage
----------------------
* less, and more expressive code thanks to numpy/scipy (Python, not Mono)
* not using full covariance in KL distance, because it is numerically unstable


Related projects
------------------
* Mirage -- http://hop.at/mirage/
	* original project
* Autoqueue plugin for quodlibet (see README) -- https://launchpad.net/autoqueue/trunk
	* Source: https://bazaar.launchpad.net/~thisfred/autoqueue/trunk/files
	* Does very much similar things
	* includes some form of clustering of songs
	* includes DBUS similarity service
	* also as "PyMirage" on: https://github.com/georgewhewell/pymirage/
* Aubio -- https://github.com/piem/aubio
	* supports some basic feature extraction



