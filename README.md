# Import/Export Database

**_Deprecation: This project has been abandoned in favor of the simpler [PIHEMR Ubuntu Apps](https://github.com/PIH/pihemr-ubuntu-apps)_**

_The main reason for its abandonment is difficulty with portability—Brandon couldn't get it running
on Ubuntu 16.04._

----

Linux GUI applications for dumping and loading MySQL databases.

Will need a small amount of tweaking to get it to work on Windows.

## Setup

To install the application, use the latest `.deb` released on GitHub.

To build and install the application, run `./build.sh` and then `./install.sh`.

To just build the standalone executable and a deb file, run `./build.sh`.

To just set up the Python environment for development, run `./dev_setup.sh`.

## Spec

In order to transfer data from offline clinics to the main office, very non-technical users need to be able to create and load MySQL dumps. Users at the offline clinics should only be able to create dumps. Users at the main office do not need to be able to modify data, so those databases can be overwritten freely.

### Functional Spec
Users at clinics should see an icon on their desktop called “Exportar Base de Datos” (which runs the program “Export database”). Users at the main office should see the same icon plus another,  called “Importar Base de Datos” (which runs the program “Import database”).

#### Export Database

On running the program “Export Database,” a GUI window should open which prompts the user for their password, “Por favor, ingresa la contraseña de usuario “root” de MySQL. También necesitamos la contraseña para cifrar el archivo.” It should have a password  text entry field, which hides the characters entered. It should have a next (“Siguiente”) button (all GUI windows should have the close-window button provided by GNOME).

On clicking the “Next” button, a GUI window should open with a drop-down picker listing the MySQL databases present, prompting the user: “Selecciona la base de datos para exportar.” There should be a Next button.

On clicking that Next button, a file-picker window should open, which should allow the user to select a destination for a database dump. After selecting the location for the database dump, the program should dump the selected database and zip the result, encrypting the zip file with that same database password.

When the process is complete, a dialog box should say “Done!” (“Ya!”).

#### Import Database

On running the program “Import Database,” a GUI window with a a file-picker should open, which should allow the user to select the database dump zip file to load. There should be a “Select” button (“Seleccionar”).

On clicking that button, a GUI window should open which prompts the user for the ZIP file password, “Por favor, ingresa la contraseña para descifrar el archivo.” It should have a password  text entry field, which hides the characters entered. It should have a next (“Siguiente”) button.

On clicking that button, a GUI window should open which prompts the user for the MySQL root password, “Por favor, ingresa la contraseña del usuario “root” de MySQL.” It should have a password  text entry field, which hides the characters entered. It should have a next (“Siguiente”) button.

On clicking the “Next” button, a GUI window should open with a drop-down picker listing the MySQL databases present, prompting the user: “Seleccionar la base de datos para importar.” There should be a “Importar” button. On clicking that button, the program should decrypt the ZIP file with the given password and import the dump file to the selected database. Whatever data already exists in that database will be overwritten.

If importing a typical Mexico clinic database takes more than 30 seconds or so, a progress bar should be shown.

When the process is complete, a dialog box should say “Done!” (“Ya!”).
