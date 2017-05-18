# Security Clearance Stats Parser

Pulls the content of http://ogc.osd.mil/doha/industrial/ and each year (currently 1996-2017), and prints a count for rationals (such as financial, criminal, etc.).

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

## Explanation of 'Guidelines'
Taken from DoD Directive 5220.06 - Defense Industrial Personnel Security Clearance Review Program (http://www.dtic.mil/whs/directives/corres/pdf/522006p.pdf)
Excerpted here, from Enclosure 2, Section 2.3:
* E2.2.3.1. Guideline A: Allegiance to the United States
* E2.2.3.2. Guideline B: Foreign influence
* E2.2.3.3. Guideline C: Foreign preference
* E2.2.3.4. Guideline D: Sexual behavior
* E2.2.3.5. Guideline E: Personal conduct
* E2.2.3.6. Guideline F: Financial considerations
* E2.2.3.7. Guideline G: Alcohol consumption
* E2.2.3.8. Guideline H: Drug involvement
* E2.2.3.9. Guideline I: Emotional, mental, and personality disorders
* E2.2.3.10. Guideline J: Criminal conduct
* E2.2.3.11. Guideline K: Security violations
* E2.2.3.12. Guideline L: Outside activities
* E2.2.3.13. Guideline M: Misuse of Information Technology Systems
