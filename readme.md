# Security Clearance Stats Parser

Pulls the content of http://www.dod.gov/dodgc/doha/industrial/ and each year (currently 1997-2016), and prints a count for rationals (such as financial, criminal, etc.).

```python parse.py```
This will grab all 11 years worth (and will take some time).  To change what years are grabbed, edit parse.py and change `START_YEAR` and `END_YEAR` constants.

## How it works
The text is scanned for keywords and each case is binned using the following heuristic:
```
        favorable = ["clearance is granted",
                "adverse decision remanded",
                "adverse decision reversed",
                "adverse decision is unsupported",
                "adverse decision is unsupportable",
                "clearance continued",
                "is granted",
                "clearance granted",
                "public trust postition granted",
                'favorable decision affirmed']

        unfavorable = ['clearance is denied',
                'clearance denied',
                'clearance is revoked',
                'information is revoked',
                'adverse decision is supported',
                'adverse decision is supportable',
                'adverse decision affirmed',
                'favorable decision reversed',
                'favorable decision remanded',
                'clearance revoked',
                'is denied',
                'fails to mitigate',
                'are not mitigated',
                'did not mitigate',
                'position denied']

        indeterminate = ['case remanded with instruction', 'unfavorable decision is vacated']
```
