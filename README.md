# BSF Auto Search
BFS Auto Search is a Python script that allows mass data entry into the Barracuda Spam Firewall message log search using Selenium WebDriver browser automation.

### Dependencies
* Python > 3.4.0
* Selenium Python Module >= 2.45.0
* Selenium Browser Addon (currently the script supports Firefox, Chrome, and IE)

### Setup
1. Install Python: https://www.python.org/downloads/
2. Install the Selenium Python Module using PIP:
  ```
pip install -r REQUIREMENTS
```
3. Run the script:
  ```
python bfsas.py
```

### Versioning

This project implements the Semantic Versioning guidelines.

Releases will be numbered with the following format:

`<major>.<minor>.<patch>`

And constructed with the following guidelines:
* Breaking backward compatibility bumps the major (and resets the minor and patch)
* New additions without breaking backward compatibility bumps the minor (and resets the patch)
* Bug fixes and misc changes bumps the patch
 
For more information on SemVer, please visit [http://semver.org](http://semver.org).

### License
GNU General Public License, Version 3 (GNU GPLv3)
