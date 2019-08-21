from utils import *

import argparse
import sys
import time


def parse_arguments(args):

    parser = create_parser()

    if len(args) is 0:
        print(error_message(), "No arguments supplied, showing help...\n")
        time.sleep(0.5)
        parser.print_help()
        sys.exit(1)

    config.args = parser.parse_args(args)


def create_parser():
    example = 'Examples:\n\n'
    example += '$ python lancer.py -T 10.10.10.100 --verbose\n'
    example += '$ python lancer.py --target-file targets --skip-ports 445 8080 --show-program-output\n'
    example += '$ python lancer.py --target 192.168.1.10 --nmap nmap/bastion.xml /' \
               '\n  -wW /usr/share/wordlists/dirbuster/directory-2.3-small.txt /\n  -fD HTB -fU L4mpje -fP P@ssw0rd'

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="Lancer - system vulnerability scanner\n\nThis tool is designed to"
                                                 " aid the recon phase of a pentest or any legal & authorised attack"
                                                 " against a device or network. The author does not take any liability"
                                                 " for use of this tool for illegal use.", epilog=example)

    main_args = parser.add_argument_group("Main arguments")
    mex_group = main_args.add_mutually_exclusive_group(required=True)
    mex_group.add_argument("-T", "--target", metavar="TARGET", dest='target', type=str, help="IP of target")
    mex_group.add_argument("--target-file", metavar="FILE", dest="hostfile", type=argparse.FileType('r'),
                           help="File containing a list of target IP addresses")
    main_args.add_argument("-q", "--quiet", dest='quiet', action="store_true", default='',
                           help="Do a quiet nmap scan. This will help reduce the footprint of the scan in logs and on"
                                " IDS which may be present in a network.")
    main_args.add_argument("-v", "--verbose", dest='verbose', action="store_true", default='',
                           help="Use a more verbose output. This will output more detailed information and may help to"
                                " diagnose any issues")
    main_args.add_argument("-sd", "--skip-disclaimer", dest='skipDisclaimer', action="store_true", default='',
                           help="Skip the legal disclaimer. By using this flag, you agree to use the program for legal"
                                " and authorised use")
    main_args.add_argument("--skip-ports", nargs='+', type=int, metavar="PORTS", dest='skipPorts', default=[],
                           help="Set the ports to ignore. These ports will have no enumeration taken against them,"
                                " except for the initial discovery via nmap. This can be used to run a custom scan and"
                                " pass the results to Lancer.")
    main_args.add_argument("--show-output", dest='show_output', action="store_true", default='',
                           help="Show the output of the programs which are executed, such as nmap, nikto, smbclient"
                                " and gobuster")
    main_args.add_argument("--nmap", metavar="FILE", dest='nmapFile', type=str,
                           help="Skip an internal nmap scan by providing the path to an nmap XML file")

    sgroup2 = parser.add_argument_group("Web Services", "Options for targeting web services")
    sgroup2.add_argument("-wW", metavar="WORDLIST", dest='webWordlist',
                         default='/usr/share/wordlists/dirbuster/directory-2.3-medium.txt',
                         help="The wordlist to use. Defaults to the directory-2.3-medium.txt file found in"
                              " /usr/share/wordlists/dirbuster")

    sgroup3 = parser.add_argument_group("File Services", "Options for targeting file services")
    sgroup3.add_argument("-fD", metavar="DOMAIN", dest='fileDomain',
                         help="Domain to use during the enumeration of file services")
    sgroup3.add_argument("-fU", metavar="USERNAME", dest='fileUsername',
                         help="Username to use during the enumeration of file services")
    sgroup3.add_argument("-fP", metavar="PASSWORD", dest='filePassword',
                         help="Password to use during the enumeration of file services")
    return parser