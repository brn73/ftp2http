#!/usr/bin/env python


import argparse
import bcrypt
import ftp2http
import getpass
import os
import sys


from .version import version


def main():
    parser = argparse.ArgumentParser(version=version)
    parser.add_argument(
        "-f", "--configuration-file",
        default="/etc/ftp2http.conf",
        help="Specifies the configuration file path.",
    )
    parser.add_argument(
        "-a", "--generate-account",
        action="store_true",
        help="Generate details for adding a user account."
    )
    parser.add_argument(
        "--fd",
        type=int, default=-1,
        help="Specifies a socket file descriptor.",
    )
    args = parser.parse_args()

    if args.generate_account:

        name = raw_input("Enter a username: ")
        password = getpass.getpass("Enter a password: ")
        password_repeated = getpass.getpass("Confirm password: ")

        if password != password_repeated:
            sys.stderr.write("Error! The passwords did not match.\n")
            sys.exit(1)

        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        print
        print "Add the following line to your configuration file."
        print "user: %s:%s" % (name, hashed_password)
        print

    else:

        configuration_path = os.path.abspath(args.configuration_file)
        config = ftp2http.read_configuration_file(configuration_path)
        config["listen_fd"] = args.fd
        ftp2http.start_ftp_server(**config)


if __name__ == "__main__":
    main()
