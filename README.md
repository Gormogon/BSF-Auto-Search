# BSF Auto Search
BSF Auto Search is a Python script that allows mass data entry into the Barracuda Spam Firewall message log search using Selenium WebDriver browser automation.

### Dependencies
* Python > 3.4.0
* Selenium Python Module >= 2.48.0
* [Selenium Browser Driver](http://www.seleniumhq.org/download/) (currently BSF Auto Search supports Firefox, Chrome, and IE)
  * For best results, the Firefox browser driver is recommended. 

### Setup
1. Verify that both the Selenium Browser Driver and Python are installed.
2. Install the Selenium Python Module using PIP:
  ```
pip install -r REQUIREMENTS
```
3. Add your settings to the included ‘settings.ini’.
4. Add your search data to the included ‘search.txt’ (one entry per line).
5. Run the script:
  ```
python bsfas.py
```

### Contributing
To find out how you can contribute, please look [here](https://github.com/Gormogon/BSF-Auto-Search/blob/master/CONTRIBUTING.md).

### Versioning

This project implements the Semantic Versioning guidelines.

Releases will be numbered with the following format:

`<major>.<minor>.<patch>`

And constructed with the following guidelines:
* Breaking backward compatibility bumps the major (and resets the minor and patch)
* New additions without breaking backward compatibility bumps the minor (and resets the patch)
* Bug fixes and misc changes bumps the patch
 
For more information on SemVer, please visit [http://semver.org](http://semver.org).

For the changlog, please look [here](https://github.com/Gormogon/BSF-Auto-Search/blob/master/CHANGELOG.md).

### License
GNU General Public License, Version 3 (GNU GPLv3)

This project is __not__ affiliated with Barracuda Networks, Inc.

### Thanks
Thanks goes to the [Selenium Browser Automation](http://www.seleniumhq.org/) project. BSF Auto Search would not have been possible without it.
