from modules import ftp
from modules.web import http
from modules import smb

import config
import utils
import platform
import cpe_utils


def detect_os(cpe_list):
    for cpe in cpe_list:
        cpe_retrieved = cpe.firstChild.nodeValue
        cpe_os_type = "cpe:/o"
        if cpe_retrieved.startswith(cpe_os_type):
            print(utils.normal_message(), "Target OS appears to be", cpe_utils.CPE(cpe_retrieved).human())
            if cpe_utils.CPE(cpe_retrieved).matches(cpe_utils.CPE("cpe:/o:microsoft:windows")) \
                    and platform.system() == "linux":
                print(utils.warning_message(), "Target machine is running Microsoft Windows."
                                               "Will commence enumeration using enum4linux")
                print(utils.warning_message(), "enum4linux not yet implemented")


def detect_apps(cpe_list):
    for cpe in cpe_list:
        cpe_retrieved = cpe.firstChild.nodeValue
        cpe_app_type = "cpe:/a"
        if cpe_retrieved.startswith(cpe_app_type):
            print(utils.normal_message(), "Installed application is reported as", cpe_utils.CPE(cpe_retrieved).human())


def detect_service(openport):
    for service in openport.getElementsByTagName('service'):
        port = int(openport.attributes['portid'].value)
        service_type = service.attributes['name'].value
        try:
            service_name = service.attributes['product'].value
        except KeyError:
            service_name = service_type

        print(utils.normal_message(), service_name, "is open on port", port)
        # Ignore the port if its in the list of ports to skip
        if port not in config.args.skipPorts:
            # Some kind of ftp service
            if service_type == "ftp":
                print(utils.warning_message(), service_name, "is recognised by nmap as a ftp program")
                ftp.ftp(openport)
            # Some kind of SSH server
            if service_type == "ssh":
                print(utils.warning_message(), service_name, "is recognised by nmap as an ssh server")
            # Some kind of http service
            if service_type == "http":
                if config.args.quiet:
                    print(utils.warning_message(), service_name, "is recognised by nmap as a http program")
                else:
                    print(utils.warning_message(), service_name, "is recognised by nmap as a http program. Will"
                                                                 "commence enumeration using gobuster and Nikto...")
                    print("")
                    url = "http://" + config.args.target + ":" + str(port)
                    # Scan using gobuster
                    http.gobuster(url)
                    # Scan using nikto
                    http.nikto(url)
            # Smb share
            # TODO: Maybe don't use hardcoded ports
            if port == 445:
                if config.args.quiet:
                    print(utils.warning_message(), service_name, "is potentially a SMB share on Windows")
                else:
                    print(utils.warning_message(), service_name, "is potentially a SMB share on Windows. Will commence"
                                                             " enumeration using smbclient...")
                smb.smb_client(config.args.verbose)
            if service_name == "mysql":
                print(utils.warning_message(), service_name, "is recognised by nmap as a MySQL server...")
        else:
            print(utils.warning_message(), "Skipping", service_name, "(port", str(port) + ") as it has been specified "
                                                                                          "as a port to skip")
        print("")