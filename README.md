# dateclass

Used to remove backups or logs based on dates.

## usage

```
usage: dateclass [-h] [-k KEEP] [-n] [-a {delete,output}] [-d] [-o] fileregex

Classifies files based on date

positional arguments:
  fileregex             Match files with this python regex

options:
  -h, --help            show this help message and exit
  -k KEEP, --keep KEEP  Time difference for which to store the newest version older than specified
  -n, --newest          Store newest version
  -a {delete,output}, --action {delete,output}
                        What to do with the unnecessary files
  -d, --delete          Delete all unnecessary files
  -o, --output          Output all unnecessary files
```
