#! /bin/sh

./dev_setup.sh

VERSION=0.1
PACKAGE_NAME=export_database_${VERSION}-1

rm -r build/
./env/bin/pyinstaller --clean -F \
    src/export_database.py

DEB_ROOT=build/${PACKAGE_NAME}
BIN_DIR=${DEB_ROOT}/usr/local/bin
DESKTOP_DIR=${DEB_ROOT}/usr/share/applications
ICON_DIR=${DEB_ROOT}/usr/share/icons/hicolor/scalable/apps

mkdir -p ${BIN_DIR}
mkdir -p ${DESKTOP_DIR}
mkdir -p ${ICON_DIR}

cp dist/export_database ${BIN_DIR}
cp packaging/desktop/exportDatabase.desktop ${DESKTOP_DIR}
cp packaging/icon/exportDatabase.png ${ICON_DIR}
cp -r packaging/DEBIAN ${DEB_ROOT}

dpkg-deb --build ${DEB_ROOT} dist/export_database.deb
