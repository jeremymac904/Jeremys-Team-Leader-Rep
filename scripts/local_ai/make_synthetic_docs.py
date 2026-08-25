#!/usr/bin/env python3
"""Generate fictional mortgage documents for testing the local pipeline.

Everything produced is invented. Every page is stamped FICTIONAL TEST DATA.
No real borrower information is used, and the layouts are plain generic
constructions rather than copies of any lender's or agency's forms.

    python3 scripts/local_ai/make_synthetic_docs.py

Writes PDFs to examples/synthetic-documents/. These ARE committed, because
they contain nothing private and the test suite depends on them.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
OUT = ROOT / "examples" / "synthetic-documents"

BANNER = "*** FICTIONAL TEST DATA - NOT A REAL DOCUMENT - DO NOT USE FOR LENDING ***"


def build(name: str, title: str, lines: list[str]) -> Path:
    import pymupdf

    doc = pymupdf.open()
    page = doc.new_page()
    y = 50

    page.insert_text((40, y), BANNER, fontsize=8, color=(0.8, 0, 0))
    y += 28
    page.insert_text((40, y), title, fontsize=15)
    y += 26

    for line in lines:
        if y > 760:
            page = doc.new_page()
            y = 50
            page.insert_text((40, y), BANNER, fontsize=8, color=(0.8, 0, 0))
            y += 28
        page.insert_text((40, y), line, fontsize=9.5)
        y += 14

    y = min(y + 16, 770)
    page.insert_text((40, y), BANNER, fontsize=8, color=(0.8, 0, 0))

    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{name}.pdf"
    doc.save(path)
    doc.close()
    return path


DOCS = {
    "synthetic-paystub": ("EARNINGS STATEMENT - PAY STUB", [
        "Employer: Northwind Fictional Manufacturing LLC",
        "Employer Address: 100 Invented Way, Sampleton, FL 32000",
        "Employee: Jordan A. Testcase",
        "Employee ID: FAKE-00417",
        "",
        "Pay Period Start: 07/01/2026",
        "Pay Period End:   07/15/2026",
        "Pay Date:         07/20/2026",
        "Pay Frequency:    Semi-Monthly",
        "",
        "EARNINGS           RATE      HOURS      CURRENT        YEAR TO DATE",
        "Regular            32.50     86.67      2,816.78       39,434.92",
        "Overtime           48.75      6.00        292.50        3,412.50",
        "Bonus                 -          -          0.00        2,500.00",
        "Commission            -          -          0.00            0.00",
        "Gross Pay                              3,109.28       45,347.42",
        "",
        "DEDUCTIONS                              CURRENT        YEAR TO DATE",
        "Federal Income Tax                        412.15        6,004.18",
        "Social Security                           192.78        2,811.54",
        "Medicare                                   45.08          657.54",
        "State Income Tax                            0.00            0.00",
        "401(k) Contribution                       155.46        2,267.37",
        "Health Insurance                          142.00        2,059.00",
        "Total Deductions                          947.47       13,799.63",
        "",
        "Net Pay                                 2,161.81       31,547.79",
    ]),
    "synthetic-w2": ("FORM W-2 WAGE AND TAX STATEMENT (FICTIONAL)", [
        "Tax Year: 2025",
        "",
        "Employer: Northwind Fictional Manufacturing LLC",
        "Employer EIN: 00-0000000  (fictional)",
        "Employer Address: 100 Invented Way, Sampleton, FL 32000",
        "",
        "Employee: Jordan A. Testcase",
        "Employee SSN: XXX-XX-0000  (redacted, fictional)",
        "Employee Address: 42 Example Street, Sampleton, FL 32000",
        "",
        "Box 1  Wages, tips, other compensation:      74,218.66",
        "Box 2  Federal income tax withheld:           9,884.20",
        "Box 3  Social security wages:                76,905.12",
        "Box 4  Social security tax withheld:          4,768.12",
        "Box 5  Medicare wages and tips:              76,905.12",
        "Box 6  Medicare tax withheld:                 1,115.12",
        "Box 12a D  401(k) elective deferrals:         3,686.46",
        "Box 13 Retirement plan: X",
        "Box 16 State wages:                          74,218.66",
        "Box 17 State income tax:                          0.00",
    ]),
    "synthetic-bank-statement": ("MONTHLY ACCOUNT STATEMENT (FICTIONAL)", [
        "Institution: First Imaginary Savings Bank",
        "Account Owner: Jordan A. Testcase",
        "Account Type: Personal Checking",
        "Account Number: ****0000  (masked, fictional)",
        "Statement Period: 06/01/2026 through 06/30/2026",
        "",
        "Beginning Balance:                           8,412.55",
        "Total Deposits and Additions:               10,338.62",
        "Total Withdrawals and Debits:                9,127.44",
        "Ending Balance:                              9,623.73",
        "Average Daily Balance:                       8,904.11",
        "",
        "DATE        DESCRIPTION                        AMOUNT      BALANCE",
        "06/05/2026  DIRECT DEP NORTHWIND PAYROLL      2,161.81     10,574.36",
        "06/08/2026  MORTGAGE PAYMENT ACH             -1,847.22      8,727.14",
        "06/11/2026  TRANSFER FROM SAVINGS             1,000.00      9,727.14",
        "06/14/2026  DEPOSIT - CHECK                   4,850.00     14,577.14",
        "06/15/2026  AUTO LOAN ACH                      -512.40     14,064.74",
        "06/20/2026  DIRECT DEP NORTHWIND PAYROLL      2,161.81     16,226.55",
        "06/22/2026  CREDIT CARD PAYMENT                -975.00     15,251.55",
        "06/24/2026  UNKNOWN TRANSFER IN                 165.00     15,416.55",
        "06/26/2026  RENT/MISC DEBIT                  -3,200.00     12,216.55",
        "06/28/2026  PERSONAL LOAN PMT ACH              -418.66     11,797.89",
        "06/30/2026  MISC DEBITS                      -2,174.16      9,623.73",
        "",
        "NOTE: The 06/14 deposit of 4,850.00 is a non-payroll deposit.",
        "NOTE: A recurring 418.66 personal loan debit appears monthly.",
    ]),
    "synthetic-purchase-contract": ("RESIDENTIAL PURCHASE AGREEMENT (FICTIONAL EXCERPT)", [
        "This is a simplified fictional contract excerpt for software testing.",
        "",
        "Buyer:  Jordan A. Testcase and Riley B. Testcase",
        "Seller: Morgan C. Fictional",
        "Property Address: 42 Example Street, Sampleton, FL 32000",
        "County: Sample County",
        "",
        "Purchase Price:                             425,000.00",
        "Earnest Money Deposit:                        5,000.00",
        "Additional Deposit Due 08/15/2026:            5,000.00",
        "Down Payment:                                42,500.00",
        "Loan Amount (approx):                       382,500.00",
        "Financing Type: Conventional",
        "Seller Concessions Toward Buyer Costs:        8,500.00",
        "",
        "Effective Date:                             08/01/2026",
        "Inspection Period Ends:                     08/12/2026",
        "Loan Application Deadline:                  08/08/2026",
        "Financing Contingency Deadline:             09/05/2026",
        "Appraisal Contingency Deadline:             09/05/2026",
        "Closing Date:                               09/20/2026",
        "",
        "Occupancy: Buyer to occupy as primary residence.",
        "Personal Property Included: refrigerator, washer, dryer, window treatments.",
        "HOA: Property is subject to Sampleton Fictional HOA, dues 145.00 monthly.",
        "",
        "Addenda Attached:",
        "  - Financing Addendum",
        "  - HOA Disclosure Addendum",
        "  - Inspection Addendum",
        "",
        "Signatures: Buyer ____________  Seller ____________",
    ]),
    "synthetic-loan-estimate": ("LOAN ESTIMATE (FICTIONAL SAMPLE DATA)", [
        "Applicant: Jordan A. Testcase",
        "Property: 42 Example Street, Sampleton, FL 32000",
        "Date Issued: 08/03/2026",
        "",
        "LOAN TERMS",
        "Loan Amount:                                382,500.00",
        "Interest Rate:                                   6.375%",
        "Loan Term: 30 years",
        "Loan Type: Conventional",
        "Loan Purpose: Purchase",
        "Rate Lock: NO - rate not locked as of issue date",
        "Monthly Principal & Interest:                 2,386.94",
        "Prepayment Penalty: None",
        "Balloon Payment: None",
        "",
        "PROJECTED PAYMENTS",
        "Estimated Property Taxes:                       425.00",
        "Estimated Homeowners Insurance:                 210.00",
        "Estimated HOA Dues:                             145.00",
        "Mortgage Insurance:                             112.00",
        "Estimated Total Monthly Payment:              3,278.94",
        "",
        "CLOSING COST DETAILS",
        "A. Origination Charges:                       2,868.75",
        "   Points (0.5%):                             1,912.50",
        "   Application Fee:                             500.00",
        "   Underwriting Fee:                            456.25",
        "B. Services You Cannot Shop For:              1,145.00",
        "C. Services You Can Shop For:                 2,310.00",
        "D. Total Loan Costs:                          6,323.75",
        "E. Taxes and Government Fees:                 2,677.50",
        "F. Prepaids:                                  1,984.00",
        "G. Initial Escrow Payment:                    1,560.00",
        "H. Other:                                       525.00",
        "I. Total Other Costs:                         6,746.50",
        "J. Total Closing Costs:                      13,070.25",
        "Lender Credits:                                -750.00",
        "",
        "Estimated Cash to Close:                     46,820.25",
        "APR:                                             6.518%",
    ]),
    "synthetic-mortgage-statement": ("MONTHLY MORTGAGE STATEMENT (FICTIONAL)", [
        "Servicer: Imaginary Loan Servicing Company",
        "Borrower: Morgan C. Fictional",
        "Property: 88 Placeholder Lane, Sampleton, FL 32000",
        "Loan Number: 000000000  (fictional)",
        "Statement Date: 07/01/2026",
        "",
        "Payment Due Date:                            08/01/2026",
        "Amount Due:                                    1,847.22",
        "",
        "Outstanding Principal Balance:               238,411.09",
        "Interest Rate:                                    4.250%",
        "Escrow Balance:                                2,145.663",
        "",
        "EXPLANATION OF AMOUNT DUE",
        "Principal:                                       512.88",
        "Interest:                                        844.34",
        "Escrow (Taxes and Insurance):                    490.00",
        "Total Payment Amount:                          1,847.22",
        "",
        "PAST PAYMENTS BREAKDOWN (YTD)",
        "Total Principal Paid:                          3,441.22",
        "Total Interest Paid:                           5,972.18",
        "Total Escrow Paid:                             3,430.00",
    ]),
    "synthetic-tax-return": ("FORM 1040 U.S. INDIVIDUAL INCOME TAX RETURN (FICTIONAL)", [
        "Tax Year: 2025",
        "Filing Status: Married Filing Jointly",
        "",
        "Taxpayer: Priya R. Testcase",
        "Spouse:   Alex T. Testcase",
        "SSN: XXX-XX-0000  (redacted, fictional)",
        "Address: 71 Imaginary Road, Sampleton, FL 32000",
        "",
        "INCOME",
        "Line 1z  Wages, salaries, tips:                    48,200.00",
        "Line 2b  Taxable interest:                            412.00",
        "Line 3b  Ordinary dividends:                          865.00",
        "Line 7   Capital gain or loss:                       3,150.00",
        "Line 8   Additional income from Schedule 1:         62,480.00",
        "Line 9   Total income:                             115,107.00",
        "Line 11  Adjusted gross income:                     110,894.00",
        "Line 15  Taxable income:                             81,594.00",
        "",
        "SCHEDULES ATTACHED",
        "Schedule 1 - Additional Income and Adjustments",
        "Schedule C - Profit or Loss From Business",
        "Schedule E - Supplemental Income and Loss",
        "Schedule SE - Self-Employment Tax",
        "",
        "SCHEDULE C SUMMARY (Sole Proprietorship)",
        "Business: Testcase Consulting LLC",
        "Gross receipts:                                     148,300.00",
        "Total expenses:                                      96,420.00",
        "Depreciation (Line 13):                              11,850.00",
        "Business use of home (Line 30):                       3,200.00",
        "Net profit (Line 31):                                51,880.00",
        "",
        "SCHEDULE E SUMMARY (Rental Real Estate)",
        "Property: 12 Placeholder Street, Sampleton, FL",
        "Rents received:                                      24,000.00",
        "Total expenses:                                      13,400.00",
        "Depreciation:                                         7,200.00",
        "Net rental income (loss):                            10,600.00",
        "",
        "NOTE: Depreciation and business-use-of-home are commonly reviewed",
        "as potential add-backs. That determination is made by underwriting.",
    ]),
    "synthetic-closing-disclosure": ("CLOSING DISCLOSURE (FICTIONAL SAMPLE DATA)", [
        "Borrower: Jordan A. Testcase and Riley B. Testcase",
        "Seller:   Morgan C. Fictional",
        "Property: 42 Example Street, Sampleton, FL 32000",
        "",
        "Date Issued:        09/14/2026",
        "Closing Date:       09/20/2026",
        "Disbursement Date:  09/20/2026",
        "",
        "LOAN TERMS",
        "Loan Amount:                                382,500.00",
        "Interest Rate:                                   6.375%",
        "Loan Term: 30 years",
        "Loan Type: Conventional",
        "Monthly Principal & Interest:                 2,386.94",
        "Prepayment Penalty: None",
        "Balloon Payment: None",
        "",
        "PROJECTED PAYMENTS",
        "Estimated Escrow (taxes and insurance):         635.00",
        "Mortgage Insurance:                             112.00",
        "Estimated Total Monthly Payment:              3,278.94",
        "",
        "LOAN COSTS",
        "A. Origination Charges:                       2,868.75",
        "B. Services Borrower Did Not Shop For:        1,145.00",
        "C. Services Borrower Did Shop For:            2,190.00",
        "D. TOTAL LOAN COSTS:                          6,203.75",
        "",
        "OTHER COSTS",
        "E. Taxes and Other Government Fees:           2,677.50",
        "F. Prepaids:                                  2,104.00",
        "G. Initial Escrow Payment at Closing:         1,905.00",
        "H. Other:                                       525.00",
        "I. TOTAL OTHER COSTS:                         7,211.50",
        "",
        "J. TOTAL CLOSING COSTS:                      13,415.25",
        "Lender Credits:                                -750.00",
        "",
        "CALCULATING CASH TO CLOSE",
        "Total Closing Costs:                         13,415.25",
        "Down Payment:                                42,500.00",
        "Deposit (earnest money):                    -10,000.00",
        "Seller Credits:                              -8,500.00",
        "Adjustments and Other Credits:                 -420.00",
        "CASH TO CLOSE:                               36,995.25",
        "",
        "COMPARISON TO LOAN ESTIMATE",
        "Loan Estimate Total Closing Costs:           13,070.25",
        "Closing Disclosure Total Closing Costs:      13,415.25",
        "Difference:                                     345.00",
        "",
        "NOTE: Section C increased from 2,310.00 to 2,190.00 and Section G",
        "increased from 1,560.00 to 1,905.00. Tolerance rules determine whether",
        "any increase requires a cure. That review is performed by a human.",
    ]),
    "synthetic-appraisal-excerpt": ("APPRAISAL REPORT EXCERPT (FICTIONAL)", [
        "Uniform Residential Appraisal - Simplified Fictional Excerpt",
        "",
        "Subject Property: 42 Example Street, Sampleton, FL 32000",
        "Borrower: Jordan A. Testcase",
        "Lender/Client: Fictional Mortgage Lending Co.",
        "Effective Date of Appraisal: 08/28/2026",
        "",
        "Appraised Value:                            428,000.00",
        "Contract Price:                             425,000.00",
        "",
        "Property Type: Single Family Detached",
        "Year Built: 2004",
        "Gross Living Area: 2,145 sq ft",
        "Bedrooms: 4   Bathrooms: 2.5",
        "Site Size: 0.24 acres",
        "Condition Rating: C3",
        "",
        "COMPARABLE SALES",
        "Comp 1: 51 Invented Court   - Sold 06/2026 - 418,000 - 2,090 sq ft",
        "Comp 2: 17 Placeholder Ave  - Sold 05/2026 - 435,000 - 2,210 sq ft",
        "Comp 3: 9 Nonexistent Drive - Sold 07/2026 - 424,500 - 2,155 sq ft",
        "",
        "Conditions of Appraisal: Appraisal made 'as is'.",
        "Note: Fictional data generated for software testing only.",
    ]),
}


def main() -> int:
    try:
        import pymupdf  # noqa: F401
    except ImportError:
        print("pymupdf is required. Install it with:")
        print("  ./vendor/hermes-venv/bin/python -m pip install pymupdf")
        return 1

    print("Generating fictional test documents\n")
    for name, (title, lines) in DOCS.items():
        path = build(name, title, lines)
        print(f"  {path.relative_to(ROOT)}")
    print(f"\n{len(DOCS)} documents written to {OUT.relative_to(ROOT)}/")
    print("Every page is stamped FICTIONAL TEST DATA.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
