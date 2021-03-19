import datetime
import re


class TimepointFormatter:
    def __init__(self, timepoint):
        self.timepoint = timepoint

    @classmethod
    def now(cls):
        return cls(datetime.datetime.now(tz=datetime.timezone.utc))

    @property
    def translation (self):
        return {
            "{year}": "%Y",
            "{YYYY}": "%Y",
            "{year:short}": "%y",
            "{YY}": "%Y",
            "{month}": "%m",
            "{MM}": "%m",
            "{month:short}": "%b",
            "{month:long}": "%B",
            "{day}": "%d",
            "{DD}": "%d",

            "{hour}": "%H",
            "{hh}": "%H",
            "{minute}": "%M",
            "{min}": "%M",
            "{mm}": "%M",
            "{second}": "%S",
            "{ss}": "%S",

            "{day:year}": "%j",

            "{week}": "%V",  # not %U, #W
            "{weekday}": "%u",  # not %w
            "{weekday:short}": "%a",
            "{weekday:long}": "%A",

            "{timezone}": "%Z",
            "{tz}": "%z",
            "{date}": "%F",
            "{time}": "%T",
            "{date:unix}": self._date_unix,
            "{year:unix}": self._year_unix,
            "{quarter}": self._quarter,
            "{Q}": self._quarter,
        }

    @property
    def _year_unix(self):
        return f"U{self.timepoint.year - 1970}"

    @property
    def _date_unix(self):
        return self._year_unix + self.timepoint.strftime("-%m-%d")

    @property
    def _quarter(self):
        return str((self.timepoint.month-1)//3+1)

    def C1989(self, format):
        pass

    def full(self, format):
        # https://www.cplusplus.com/reference/ctime/strftime/
        # https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
        # https://strftime.org/

        table = self.translation

        return re.sub(
            "|".join(map(re.escape, table)),
            lambda x: table[x.group()],
            format,
        )

    def strftime(self, format):
        return self.timepoint.strftime(self.full(format))


if __name__ == "__main__":
    tp = TimepointFormatter.now().strftime("{year:unix}-Q{Q}")
    fmt = TimepointFormatter.now().full("{year}-77-{month}")

    print(tp)
    print(fmt)
