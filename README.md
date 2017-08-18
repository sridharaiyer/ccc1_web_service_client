# Documentation for ccc1_web_service_client
## Installation [WINDOWS]
```
Follow the same order in installing the different software\tools.
```
### Oracle Client
#### Background:

The actual python package for connecting to Oracle Databases is the `cx_Oracle`. However, in order for this to work, it needs an Oracle client files (downloaded from the Oracle website), which should match the bit type (32 or 64) of the `cx_Oracle` package. As of Aug-2017, the latest cx_oracle package version is 6.0, supporting python version 3.6+ and it is 32 bit. Hence, the correct Oracle client from the Oracle website has been downloaded and saved as part of this project.

1. Copy the client folder **instantclient_12_2_32bit** which is under /drivers/oracle.
1. Paste it in a location such as C:\Program Files\Oracle Client.
1. Add the location to the Environment PATH, (Right click My Computer -> Properties -> Environment Properties -> System => Append to the end of the PATH variable value. For example, add **;C:\Program Files\Oracle Client\instantclient_12_2_32bit ** to the end of the PATH variable value)

### Visual C++ 2013 Re-distributable
#### Background:

In order for the `cx_Oracle` package to connect to the Oracle client files, it needs the Visual C++ Re-distributable software to be installed on your computer. Hence, the correct VC++ from the Microsoft website has been downloaded and saved as part of this project.

1. Double click on the exe file located at /drivers/visual_c++/vcredist_x64.exe and install the software.
1. Your computer may or may not need to be restarted. Follow the instructions if any after the VC++ installation is successful.

### Python
1. Download the latest version of Python 3.6 from the Python website
1. **Remember to select the checkbox which says *Add Python to PATH* in the first screen during installation**
1. Continue installation with the default options

### Git
1. Download and install the latest version of Git for Windows from the GitHub website with all the default options.


## Setup

### Python Virtual Environment
#### Background:

Python's package management and usage is a big departure from the maven methodology follwed for a JAVA project. In maven, the version controlling of the different dependencies (which is the equivalent of packages in Python) happens in the POM file of the project, and all the different depenedencies including their different versions are stored in the .m2 directory in the HOME directory of your computer.

Whereas the philosophy followed in Python package management is - **'Have all the packages needed for the project in the project directory'**

Hence the concept of *Virtual Environment*

For further reading visit https://docs.python.org/3/library/venv.html

1. To create a virtual environment, for Python 3, simply go to the project home directory and type:
   
   `python -m venv venv`
   
   The second **venv** is the name of the directory which will be created under ccc1_web_service_client, which will eventaually contain al the packages needed for the project downloaded and installed.
1. To use this environment, the term used in Python is **activate**. So in Windows, to activate the virtual environment, run this at the command prompt:

   `venv\Scripts\activate.bat`
1. You should see your DOS command prompt change, where you will see the name of the virtual environment pre-fixed next to the directory prompt.

   `(venv)C:\Users\ABC\Documents\projects\ccc1_web_service_client`
   
   **Remember: the (venv) prefix in your command prompt has to be present all the time when using the project to assure that you are using the packages installed in the virtual environment. For any reason, such as you exit and re-enter your command prompt and forgot to activate your virtual environment, then while running any program you will see a `package does not exist error`**
1. All the packages needed for the project are listed out in the file `requirements.txt` in the project home directory.
1. Before installing packages from the *requirements.txt* file, make sure the Python library `pip`, which is the native Python Package Installer comes out-of-the box with Python is up-to-date using the command:
   
   `python -m install pip -U`
1 Install all the packages from the *requirements.txt* file using:
   
   `pip install -r requirements.txt`
1. The installation of packages is a one-time activity when you are setting up your project. The only other time you need to install new or upgrade old package is when some developer uses or upgrades a new one and commits the project. When anyone updates/adds any package, they need to run this command, so that the requirements.txt file gets updated with the new package information:
   
   `pip freeze > requirements.txt`
   
   Then you can repeat the previous step of installing the new or updated packages

### Fiddler capture
1. The tool currently supports only a RF capture.
1. Any number of supplements are supported.
1. Only 1 unique digital file per estimate or supplement is supported.
1. No events are suported currently.
1. Wait until the **StatusChange** traffic appears on the fiddler session, before proceeding with locking the next supplement. Otherwise, you will get StatusChange files with E01 and S01 etc mixed up in the same file.


## Usage

1. While you are in the virtual environment, run:
   
   `python ccc1_client.py -i Fiddler_Captures/S0208182017.saz -a=rf`
   
   This will run the sample S02 file present in the Fiddler_Captures directory of this project.

1. If you just need to inspect the file, run:

   `python ccc1_client.py -i Fiddler_Captures/S0208182017.saz -a=rf --show`

1. For detailed debug level messages, use:

   `python ccc1_client.py -i Fiddler_Captures/S0208182017.saz -a=rf --show --log=DEBUG`
