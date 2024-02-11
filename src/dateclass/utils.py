import re

from enum import Enum
from datetime import datetime, timedelta


class Actions(Enum):
    delete = 1
    output = 2

    def __str__(self):
        return self.name


_timedelta_format = re.compile(
    r"((?P<days>\d+?)d)?((?P<hours>\d+?)h)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?"
)


def parse_timedelta(time_str):
    parts = _timedelta_format.match(time_str)
    if not parts:
        return
    parts = parts.groupdict()
    time_params = {}
    for name, param in parts.items():
        if param:
            time_params[name] = int(param)
    return timedelta(**time_params)


_groupdict_transforms = {
    "Year": lambda x: ("year", int(x)),
    "Month": lambda x: ("month", int(x)),
    "Day": lambda x: ("day", int(x)),
    "Hour": lambda x: ("hour", int(x)),
    "Minute": lambda x: ("minute", int(x)),
    "Second": lambda x: ("second", int(x)),
}


def date_from_groupdict(d):
    return datetime(**dict(_groupdict_transforms[k](v) for k, v in d.items()))
