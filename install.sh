#! /bin/sh

./build.sh

sudo dpkg -i dist/export_database.deb
cp /usr/share/applications/exportDatabase.desktop ~/Desktop/

