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

### Visual C++ 2013 Resdestributable
#### Background:

In order for the 'cx_Oracle' package to connect to the Oracle client files, it needs the Visual C++ Redistributable software to be installed on your computer. Hence, the correct VC++ from the Microsoft website has been downloaded and saved as part of this project.

1. Double click on the exe file located at /drivers/visual_c++/vcredist_x64.exe and install the software.
1. Your computer may or may not need to be restarted. Follow the instrcutions if any after the VC++ installation is successful.

### Python
1. Install the latest version of Python 3.6 from the Python website

## Setup

### Python Virtual Environment
#### Background:

The actual python package.
