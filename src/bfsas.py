#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# BSF Auto Search: Barracuda Spam Firewall message log review with Selenium browser automation.
#    Copyright (C) 2015  Michael Sincavage
#
#       This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
#
import argparse
import configparser
import ipaddress
import re
import ssl
import sys
import urllib.error
import urllib.request

from selenium import webdriver
from selenium.common import exceptions as selenium_exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


BFS_AS_VERSION = '0.0.1'

req_version = (3, 4, 0)
cur_version = sys.version_info

if cur_version > req_version:
    # REFERENCE: https://www.python.org/dev/peps/pep-0476/#opting-out
    ssl._create_default_https_context = ssl._create_unverified_context

    config = configparser.ConfigParser()
    config.read('settings.ini')

    print("  ╔══════════════════════════════════════════════════════════════════════════╗")
    print("  ║                             BFS Auto Search                              ║")
    print("  ╚══════════════════════════════════════════════════════════════════════════╝")

    def test_connection():
        """ Simple test to verify connection to Barracuda appliance.

            TODO: Improve this test to verify that the URL is actually a Barracuda appliance.
        """
        try:
            if config['DEFAULT']['BARRACUDA_URL'] != "":
                urllib.request.urlopen(config['DEFAULT']['BARRACUDA_URL'] + "/cgi-mod/index.cgi")
            else:
                print("    > ERROR!: Required field is empty in settings file.")
                sys.exit(1)
        except (KeyError, TypeError, ValueError):
            print("    > ERROR!: Looks like there is a misconfiguration in your settings file.")
            sys.exit(1)
        except urllib.error.URLError:
            print("    > ERROR!: Unable to contact configured Barracuda appliance.")
            sys.exit(1)

    parser = argparse.ArgumentParser(prog="BFS Auto Search", usage="python bfsas.py [OPTION]", add_help=False)

    group = parser.add_argument_group("options")
    group.add_argument("-h", "--help", help="Show this Help Message", action="help")
    group.add_argument("-f", "--firefox", help="Launch with Firefox", action="store_true")
    group.add_argument("-c", "--chrome", help="Launch with Chrome", action="store_true")
    group.add_argument("-i", "--ie", help="Launch with Internet Explorer", action="store_true")
    group.add_argument("-v", "--version", help="Display BFS Auto Search Version", action="store_true")

    args = parser.parse_args()

    # Handle submitted arguments, test connection, assign a webdriver class, and handle unconficured webdrivers.
    if args.firefox:
        try:
            test_connection()
            print("    > Trying to start Mozilla Firefox...")
            driver = webdriver.Firefox()
        except selenium_exceptions.WebDriverException:
            print("    > ERROR!: 'firefoxdriver' not found in PATH. Make sure it is installed.")
            sys.exit(1)
    elif args.chrome:
        try:
            test_connection()
            print("    > Trying to start Google Chrome...")
            driver = webdriver.Chrome()
        except selenium_exceptions.WebDriverException:
            print("    > ERROR!: 'chromedriver' not found in PATH. Make sure it is installed.")
            sys.exit(1)
    elif args.ie:
        try:
            test_connection()
            print("    > Trying to start Microsoft Internet Explorer...")
            driver = webdriver.Ie()
        except selenium_exceptions.WebDriverException:
            print("    > ERROR!: 'IEDriver' not found in PATH. Make sure it is installed.")
            sys.exit(1)
    elif args.version:
        print("    > BFS Auto Search:", BFS_AS_VERSION)
        sys.exit(0)
    else:
        parser.print_help()
        sys.exit(0)

    try:  # Try to open the search data file.
        if config['DEFAULT']['SEARCH_DATA_FILE'] != "":
            with open(config['DEFAULT']['SEARCH_DATA_FILE']) as search_data:
                try:  # Try to visit the configured Barracuda appliance and wait until page is loaded.
                    print("    > Trying to go to your Barracuda appliance...")
                    if config['DEFAULT']['BARRACUDA_URL'] != "" and config['DEFAULT']['TIMEOUT'] != "":
                        driver.get(config['DEFAULT']['BARRACUDA_URL'] + "/cgi-mod/index.cgi")
                        page_load = WebDriverWait(driver, int(config['DEFAULT']['TIMEOUT'])).until(expected_conditions.presence_of_element_located((By.ID, 'user')))
                    else:
                        print("    > ERROR!: Required field is empty in settings file.")
                        sys.exit(1)
                except selenium_exceptions.TimeoutException:
                    print("    > ERROR!: Your request has timed out.")
                    sys.exit(1)
                except (KeyError, TypeError, ValueError, selenium_exceptions.WebDriverException):
                    print("    > ERROR!: Looks like there is a misconfiguration in your settings file.")
                    sys.exit(1)

                print("    > Trying to log in...")

                try:  # Try to find the username field and enter the configured username.
                    enter_username = driver.find_element_by_id('user')
                    if config['DEFAULT']['BARRACUDA_USERNAME'] != "":
                        enter_username.send_keys(config['DEFAULT']['BARRACUDA_USERNAME'])
                    else:
                        print("    > ERROR!: Required field is empty in settings file.")
                        sys.exit(1)
                except (KeyError, TypeError, ValueError):
                    print("    > ERROR!: Looks like there is a misconfiguration in your settings file.")
                    sys.exit(1)

                try:  # Try to find the password field and enter the conficured password.
                    enter_password = driver.find_element_by_id('password_entry')
                    if config['DEFAULT']['BARRACUDA_PASSWORD'] != "":
                        enter_password.send_keys(config['DEFAULT']['BARRACUDA_PASSWORD'])
                    else:
                        print("    > ERROR!: Required field is empty in settings file.")
                        sys.exit(1)
                except (KeyError, TypeError, ValueError):
                    print("    > ERROR!: Looks like there is a misconfiguration in your settings file.")
                    sys.exit(1)

                try:  # Try to subbmit the credentials and wait for the page to load.
                    driver.find_element_by_id('Submit').click()
                    login_load = WebDriverWait(driver, int(config['DEFAULT']['TIMEOUT'])).until(expected_conditions.presence_of_element_located((By.LINK_TEXT, 'Message Log')))
                except selenium_exceptions.TimeoutException:
                    print("    > ERROR!: Your request has timed out.")
                    sys.exit(1)
                except (KeyError, TypeError, ValueError):
                    print("    > ERROR!: Looks like there is a misconfiguration in your settings file.")
                    sys.exit(1)

                try:  # Try to navigate the the 'Message Log' page and wait for it to load.
                    driver.find_element_by_link_text('Message Log').click()
                    log_load = WebDriverWait(driver, int(config['DEFAULT']['TIMEOUT'])).until(expected_conditions.presence_of_element_located((By.ID, 'filters1')))
                except selenium_exceptions.TimeoutException:
                    print("    > ERROR!: Your request has timed out.")
                    sys.exit(1)
                except (KeyError, TypeError, ValueError):
                    print("    > ERROR!: Looks like there is a misconfiguration in your settings file.")
                    sys.exit(1)

                print("    > Starting data entry process...")

                ip_counter = 0
                filters_tag = 0
                valnode_tag = 0
                line_num = 0
                data = ""
                for line in search_data:  # Read each line in the search data
                    line_num += 1
                    line = line.strip().replace("\n", "")
                    try:  # Try to validate line as an ip address. This is expected to throw a 'ValueError' exception on some lines.
                        if ipaddress.ip_address(line) == ipaddress.IPv4Address(line) or ipaddress.IPv6Address(line):
                            data = "IP Address"
                            if ip_counter is 0:
                                filters_tag += 1
                                valnode_tag += 1
                                driver.find_element_by_css_selector('option[value="search_sourceip"]').click()
                                enter_ip = driver.find_element_by_id('valNode_{0}'.format(valnode_tag))
                                enter_ip.send_keys(str(line))
                                driver.find_element_by_id('filter_row_add_btn_1').click()
                                driver.find_element_by_xpath('//*[@value=\'AND\']').click()
                                ip_counter += 1
                                continue
                            elif ip_counter is not 0:
                                filters_tag += 1
                                valnode_tag += 1
                                driver.find_element_by_css_selector('#filters{0} > option[value="search_sourceip"]'.format(filters_tag)).click()
                                enter_ip = driver.find_element_by_id('valNode_{0}'.format(valnode_tag))
                                enter_ip.send_keys(str(line))
                                driver.find_element_by_id('filter_row_add_btn_1').click()
                                driver.find_element_by_xpath('//*[@value=\'AND\']').click()
                                ip_counter += 1
                                continue
                    except ValueError:
                        pass

                    # Try to validate line as a domain name.
                    if re.fullmatch(r'\b((?=[a-z0-9-]{1,63}\.)(xn--)?[a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,63}\b', line) is not None:
                        data = "Domain Name"
                        if ip_counter is 0:
                            filters_tag += 1
                            valnode_tag += 1
                            driver.find_element_by_css_selector('option[value="search_from3"]').click()
                            enter_domain = driver.find_element_by_id('valNode_{0}'.format(valnode_tag))
                            enter_domain.send_keys(str(line))
                            driver.find_element_by_id('filter_row_add_btn_1').click()
                            driver.find_element_by_xpath('//*[@value=\'AND\']').click()
                            ip_counter += 1
                            continue
                        else:
                            filters_tag += 1
                            valnode_tag += 1
                            driver.find_element_by_css_selector('#filters{0} > option[value="search_from3"]'.format(filters_tag)).click()
                            enter_domain = driver.find_element_by_id('valNode_{0}'.format(valnode_tag))
                            enter_domain.send_keys(str(line))
                            driver.find_element_by_id('filter_row_add_btn_1').click()
                            driver.find_element_by_xpath('//*[@value=\'AND\']').click()
                            ip_counter += 1
                            continue

                    # If the line is not an ip address or a domain name, print a log message showing that the line was unable to be processed.
                    if data != "IP Address" or "Domain Name":
                        print("        > LOG: Unable to process '{0}' on line '{1}' as it does not appear to be formatted as a domain or ip address.".format(line, line_num))
                        continue
        else:
            print("    > Required field is empty in settings file.")
            sys.exit(1)

        print("    > BSF Auto Search successfully completed!")
    except IOError:
        print("    > ERROR!: Could not open configured 'SEARCH_DATA_FILE'.")
    except KeyError:
        print("    > ERROR!: Looks like there is a misconfiguration in your settings file.")
else:
    print("Sorry, your version of Python is not supported. Please use a version higher than 3.4.0.")
