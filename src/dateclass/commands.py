import argparse
import os
import re

from glob import glob
from datetime import datetime, timedelta
from .utils import date_from_groupdict, Actions, parse_timedelta


def run(fname, keep_deltas, action):
    current_keep_files = {k: (None, None) for k in keep_deltas}
    files = set()

    now = datetime.utcnow()
    for f in glob("*"):
        if mro := fname.match(f):
            files.add(f)

            date = date_from_groupdict(mro.groupdict())
            delta = now - date

            for k in keep_deltas:
                if delta < k:
                    continue
                current, _ = current_keep_files[k]

                if current is None or current > delta:
                    current_keep_files[k] = (delta, f)

    keep_files = set(v for _, v in current_keep_files.values())
    remove_files = files - keep_files

    if action == Actions.output:
        print("\n".join(remove_files))
    else:
        for f in remove_files:
            os.remove(f)


def main():
    parser = argparse.ArgumentParser(
        prog="dateclass",
        description="Classifies files based on date",
    )

    parser.add_argument(
        "fileregex", type=re.compile, help="Match files with this python regex"
    )
    parser.add_argument(
        "-k",
        "--keep",
        type=parse_timedelta,
        action="append",
        help="Time difference for which to store the newest version older than specified",
    )
    parser.add_argument(
        "-n",
        "--newest",
        action="append_const",
        const=timedelta(days=0),
        help="Store newest version",
    )
    parser.add_argument(
        "-a",
        "--action",
        choices=Actions,
        type=Actions.__getitem__,
        default=Actions.output,
        help="What to do with the unnecessary files",
    )
    parser.add_argument(
        "-d",
        "--delete",
        action="store_const",
        dest="action",
        const=Actions.delete,
        help="Delete all unnecessary files",
    )
    parser.add_argument(
        "-o",
        "--output",
        action="store_const",
        dest="action",
        const=Actions.output,
        help="Output all unnecessary files",
    )
    args = parser.parse_args()

    run(args.fileregex, args.keep, args.action)
