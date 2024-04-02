#!/usr/bin/env python
"""This script uploads a plugin package to the plugin repository.
Authors: A. Pasotti, V. Picavet
git sha              : $TemplateVCSFormat
"""

import getpass
import sys
import xmlrpc.client
from optparse import OptionParser

standard_library.install_aliases()  # noqa

# Configuration
PROTOCOL = "https"
SERVER = "plugins.qgis.org"
PORT = "443"
ENDPOINT = "/plugins/RPC2/"
VERBOSE = False


def main(parameters, arguments):
    """Main entry point.

    :param parameters: Command line parameters.
    :param arguments: Command line arguments.
    """
    address = (
        "{protocol}://{username}:{password}@{server}:{port}{endpoint}".format(  # noqa
            protocol=PROTOCOL,
            username=parameters.username,
            password=parameters.password,
            server=parameters.server,
            port=parameters.port,
            endpoint=ENDPOINT,
        )
    )
    print("Connecting to: %s" % hide_password(address))  # noqa

    server = xmlrpc.client.ServerProxy(address, verbose=VERBOSE)

    try:
        with open(arguments[0], "rb") as handle:  # noqa
            plugin_id, version_id = server.plugin.upload(
                xmlrpc.client.Binary(handle.read())
            )
        print("Plugin ID: %s" % plugin_id)  # noqa
        print("Version ID: %s" % version_id)  # noqa
    except xmlrpc.client.ProtocolError as err:
        print("A protocol error occurred")  # noqa
        print("URL: %s" % hide_password(err.url, 0))  # noqa
        print("HTTP/HTTPS headers: %s" % err.headers)  # noqa
        print("Error code: %d" % err.errcode)  # noqa
        print("Error message: %s" % err.errmsg)  # noqa
    except xmlrpc.client.Fault as err:
        print("A fault occurred")  # noqa
        print("Fault code: %d" % err.faultCode)  # noqa
        print("Fault string: %s" % err.faultString)  # noqa


def hide_password(url, start=6):
    """Returns the http url with password part replaced with '*'.

    :param url: URL to upload the plugin to.
    :type url: str

    :param start: Position of start of password.
    :type start: int
    """
    start_position = url.find(":", start) + 1
    end_position = url.find("@")
    url_start = url[:start_position]
    hide_pass = "*" * (end_position - start_position)
    url_end = url[end_position:]
    return f"{url_start}{hide_pass}{url_end}"


if __name__ == "__main__":
    parser = OptionParser(usage="%prog [options] plugin.zip")
    parser.add_option(
        "-w",
        "--password",
        dest="password",
        help="Password for plugin site",
        metavar="******",
    )
    parser.add_option(
        "-u",
        "--username",
        dest="username",
        help="Username of plugin site",
        metavar="user",
    )
    parser.add_option(
        "-p",
        "--port",
        dest="port",
        help="Server port to connect to",
        metavar="80",
    )
    parser.add_option(
        "-s",
        "--server",
        dest="server",
        help="Specify server name",
        metavar="plugins.qgis.org",
    )
    options, args = parser.parse_args()
    if len(args) != 1:
        print("Please specify zip file.\n")  # noqa
        parser.print_help()
        sys.exit(1)
    if not options.server:
        options.server = SERVER
    if not options.port:
        options.port = PORT
    if not options.username:
        # interactive mode
        username = getpass.getuser()
        print("Please enter user name [%s] :" % username, end=" ")  # noqa

        res = input()
        if res != "":
            options.username = res
        else:
            options.username = username
    if not options.password:
        # interactive mode
        options.password = getpass.getpass()
    main(options, args)