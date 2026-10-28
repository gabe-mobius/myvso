# MyVSO: Forms a veteran may need

The assistant may name only the forms in this file, and only rows marked `sourced`. Every `sourced` row links to an official page, quotes what supports the edition date and online option, and gives the date checked. A row marked `UNVERIFIED` has not been confirmed. Treat it as something to look into, not as a fact.

Restricted DBQs (hearing loss, tinnitus, initial PTSD) are intentionally not listed. MyVSO never recreates them (see VA_FACTS.md DBQ1).

**Online filing:** None of the listed VA claim forms is online-only. Each still has a PDF. Where Online says "Yes (online or paper)", VA offers an online tool and a PDF. SF-180 and the DoD forms (DD 2860, DD 3210, DD 149) are paper paths (eVetRecs is the online path for a DD 214).

Run `python3 check_forms.py` after any edit.

## Disability compensation and intent to file

| # | Form | Title | Purpose | Online | Source URL | Edition date and source quote | Date checked | Status |
|---|---|---|---|---|---|---|---|---|
| FM1 | 21-526EZ | Application for Disability Compensation and Related Compensation Benefits | Initial, increase, or secondary disability compensation claim. | Yes (online or paper) | https://www.va.gov/forms/21-526ez | Edition 2026-01-18. VA Forms API last_revision_on "2026-01-18"; form_tool_intro: "You can apply online instead of filling out and sending us the paper form." | 2026-10-15 | sourced |
| FM2 | 21-0966 | Intent to File a Claim for Compensation and/or Pension, or Survivors Pension and/or DIC | Sets a potential effective date for one year while the claim is prepared. | Yes (online or paper) | https://www.va.gov/forms/21-0966 | Edition 2026-05-21. VA Forms API last_revision_on "2026-05-21"; form_tool_intro: "You can submit your intent to file online instead of filling out and sending us the paper form." | 2026-10-15 | sourced |

## Supporting statements

| # | Form | Title | Purpose | Online | Source URL | Edition date and source quote | Date checked | Status |
|---|---|---|---|---|---|---|---|---|
| FM3 | 21-4138 | Statement in Support of Claim | Veteran's own written statement supporting a claim. | Yes (online or paper) | https://www.va.gov/forms/21-4138 | Edition 2024-07-28. VA Forms API last_revision_on "2024-07-28"; form_tool_intro: "You can submit your statement in support of claim online instead of filling out and sending us the paper form." | 2026-10-15 | sourced |
| FM4 | 21-10210 | Lay/Witness Statement | Buddy or witness statement about what they know of the veteran's condition. | Yes (online or paper) | https://www.va.gov/forms/21-10210 | Edition 2021-06-28. VA Forms API last_revision_on "2021-06-28"; form_tool_intro: "You can submit your statement online instead of sending us the paper form." | 2026-10-15 | sourced |
| FM5 | 21-0781 | Statement in Support of Claimed Mental Health Disorder(s) Due to an In-Service Traumatic Event(s) | Optional statement about a mental-health condition tied to an in-service traumatic event (including PTSD). | Paper PDF; online claim may collect the same answers | https://www.va.gov/forms/21-0781 | Edition 2024-03-18. VA Forms API last_revision_on "2024-03-18"; form_tool_intro: "We'll ask you to complete an online application for disability compensation (VA Form 21-526EZ) and answer questions about your mental health condition"; form_usage: "This form is optional." | 2026-10-15 | sourced |

## Records release

| # | Form | Title | Purpose | Online | Source URL | Edition date and source quote | Date checked | Status |
|---|---|---|---|---|---|---|---|---|
| FM6 | 21-4142 | Authorization to Disclose Information to the Department of Veterans Affairs (VA) | Lets VA request private medical records on the veteran's behalf. | Yes (online or paper) | https://www.va.gov/forms/21-4142 | Edition 2024-08-18. VA Forms API last_revision_on "2024-08-18"; form_tool_intro: "You can submit your authorization online instead of sending us the paper form." | 2026-10-15 | sourced |
| FM7 | 21-4142a | General Release for Medical Provider Information to the Department of Veterans Affairs (VA) | Companion release listing the medical providers for 21-4142. | Yes (online or paper) | https://www.va.gov/forms/21-4142a | Edition 2024-08-18. VA Forms API last_revision_on "2024-08-18"; form_tool_intro: "You can submit your authorization online instead of sending us the paper form." | 2026-10-15 | sourced |

## Unemployability

| # | Form | Title | Purpose | Online | Source URL | Edition date and source quote | Date checked | Status |
|---|---|---|---|---|---|---|---|---|
| FM8 | 21-8940 | Veteran's Application for Increased Compensation Based on Unemployability | Claim for individual unemployability (TDIU). | Yes (online or paper) | https://www.va.gov/forms/21-8940 | Edition 2024-07-01. VA Forms API last_revision_on "2024-07-01"; form_tool_intro: "You can fill out this form online instead of filling out and sending us the paper form." | 2026-10-15 | sourced |
| FM9 | 21-4192 | Request for Employment Information in Connection with Claim for Disability Benefits | Employer information used with an unemployability claim. | Yes (online or paper) | https://www.va.gov/forms/21-4192 | Edition 2024-08-28. VA Forms API last_revision_on "2024-08-28"; form_tool_intro: "You can fill out VA Form 21-4192 online instead of filling out and sending us the paper form." | 2026-10-15 | sourced |

## Decision review (AMA)

| # | Form | Title | Purpose | Online | Source URL | Edition date and source quote | Date checked | Status |
|---|---|---|---|---|---|---|---|---|
| FM10 | 20-0995 | Decision Review Request: Supplemental Claim | AMA supplemental claim with new and relevant evidence. | Yes (online or paper) | https://www.va.gov/forms/20-0995 | Edition 2024-05-28. VA Forms API last_revision_on "2024-05-28"; form_tool_intro: "You can file online instead of filling out and sending us the paper form." | 2026-10-15 | sourced |
| FM11 | 20-0996 | Decision Review Request: Higher-Level Review | AMA higher-level review by a more senior reviewer. | Yes (online or paper) | https://www.va.gov/forms/20-0996 | Edition 2024-03-18. VA Forms API last_revision_on "2024-03-18"; form_tool_intro: "You can apply online instead of filling out and sending us the paper form." | 2026-10-15 | sourced |
| FM12 | 10182 | Decision Review Request: Board Appeal (Notice of Disagreement) | AMA appeal to the Board of Veterans' Appeals. | Yes (online or paper) | https://www.va.gov/forms/10182 | Edition 2026-06-03. VA Forms API form_name "VA10182", last_revision_on "2026-06-03"; form_tool_intro: "You can request a Board Appeal online instead of sending us the paper form." | 2026-10-15 | sourced |

## Power of attorney (explained only; MyVSO never holds these)

| # | Form | Title | Purpose | Online | Source URL | Edition date and source quote | Date checked | Status |
|---|---|---|---|---|---|---|---|---|
| FM13 | 21-22 | Appointment of Veterans Service Organization as Claimant's Representative | Appoints a VA-recognized VSO as the veteran's representative (POA). MyVSO explains this form but never holds or files it. | Yes (online or paper) | https://www.va.gov/forms/21-22 | Edition 2023-07-28. VA Forms API last_revision_on "2023-07-28"; form_tool_intro: "You can fill out your form online, instead of filling out a paper form." | 2026-10-15 | sourced |
| FM14 | 21-22a | Appointment of Individual as Claimant's Representative | Appoints an accredited attorney or claims agent as the veteran's representative (POA). MyVSO explains this form but never holds or files it. | Yes (online or paper) | https://www.va.gov/forms/21-22a | Edition 2023-07-18. VA Forms API last_revision_on "2023-07-18"; form_tool_intro: "You can fill out your form online, instead of filling out a paper form." | 2026-10-15 | sourced |

## Dependents

| # | Form | Title | Purpose | Online | Source URL | Edition date and source quote | Date checked | Status |
|---|---|---|---|---|---|---|---|---|
| FM15 | 21-686c | Application Request to Add and/or Remove Dependents | Adds or removes dependents that can affect compensation. | Yes (online or paper) | https://www.va.gov/forms/21-686c | Edition 2025-08-18. VA Forms API last_revision_on "2025-08-18"; form_tool_intro: "You can submit your request online instead of filling out and sending us the paper form." | 2026-10-15 | sourced |

## Military records and DD 214

| # | Form | Title | Purpose | Online | Source URL | Edition date and source quote | Date checked | Status |
|---|---|---|---|---|---|---|---|---|
| FM16 | SF-180 | Request Pertaining to Military Records | Requests military personnel records (including DD 214) from the National Archives / NPRC. | Paper (mail or fax); online eVetRecs is an alternative path | https://www.gsa.gov/reference/forms/request-pertaining-to-military-records | Edition 06/2026. GSA form page: "Form Number: SF180"; "Current Revision Date: 06/2026". Archives: veterans can also use vetrecs.archives.gov. | 2026-10-15 | sourced |
| FM21 | DD 214 (request) | Request for DD Form 214 / Report of Separation | Veterans request a copy of their DD 214 through eVetRecs (online) or SF-180 (mail/fax). DD 214 itself is a separation document, not a claim form. | Online (eVetRecs) or SF-180 | https://www.archives.gov/veterans/military-service-records | Edition see SF-180 / eVetRecs. Archives: "most veterans and their next of kin can obtain free copies of their DD Form 214 (Report of Separation) ... any of the ways listed below"; "If you are unable to start the form online ... mail or Fax it" using SF-180. | 2026-10-15 | sourced |

## Section 5103 evidence notice

| # | Form | Title | Purpose | Online | Source URL | Edition date and source quote | Date checked | Status |
|---|---|---|---|---|---|---|---|---|
| FM17 | (no separate form) | Section 5103 evidence notice | The statutory evidence notice. VA says the requirements are summarized in VA Form 21-526EZ; there is no standalone 5103 form in the VA Forms catalog. | N/A — content is in 21-526EZ | https://www.va.gov/disability/how-to-file-claim/evidence-needed/ | Edition see 21-526EZ. VA evidence-needed page: "The information on this page is a summary of evidence requirements (called \"section 5103 notice\"). You can review the official evidence requirements in VA Form 21-526EZ." VA Forms API query for "5103" returned no form. | 2026-10-15 | sourced |

## CRSC and military-record correction

| # | Form | Title | Purpose | Online | Source URL | Edition date and source quote | Date checked | Status |
|---|---|---|---|---|---|---|---|---|
| FM18 | DD 2860 | Claim for Combat-Related Special Compensation (CRSC) | Military-department claim for CRSC (not a VA form). | Paper (submit to the military department) | https://www.esd.whs.mil/Directives/forms/dd2500_2999/DD2860/ | Edition 08/12/2026. DoW forms page: "Form Number: DD 2860"; "Title: Claim for Combat-Related Special Compensation (CRSC)"; "Edition Date: 08/12/2026" | 2026-10-15 | sourced |
| FM19 | DD 3210 | Combat-Related Special Compensation (CRSC) Reconsideration Request | Asks the military department to reconsider a CRSC decision. | Paper (submit to the military department) | https://www.esd.whs.mil/Directives/forms/dd3000_3499/DD3210/ | Edition 08/13/2026. DoW forms page: "Form Number: DD 3210"; "Title: Combat-Related Special Compensation (CRSC) Reconsideration Request"; "Edition Date: 08/13/2026" | 2026-10-15 | sourced |
| FM20 | DD 149 | Application for Correction of Military Record Under the Provisions of Title 10, U.S. Code, Section 1552 | Asks a Board for Correction of Military Records to correct a military record (also the CRSC appeal path after reconsideration). | Paper (submit to the appropriate BCMR) | https://www.esd.whs.mil/Directives/forms/dd0001_0499/DD149/ | Edition 02/13/2025. DoW forms page: "Form Number: DD 149"; "Title: Application for Correction of Military Record Under the Provisions of Title 10, U.S. Code, Section 1552"; "Edition Date: 02/13/2025" | 2026-10-15 | sourced |

## Which forms do I need (decision table)

The assistant uses this table only after asking the situational questions in ASSISTANT_INSTRUCTIONS.md Part L, one at a time. It never shows this whole table or the full form list to the veteran. A "no" or "not sure" removes that row; the assistant never re-asks. Every form named here is a `sourced` row above.

| Step | Situation (the veteran's own answer) | Forms to list, in this order (FORMS.md rows) |
|---|---|---|
| 1 | Not asking VA to review a decision (any new or increase claim) | 21-0966 intent to file (FM2), listed first, unless the veteran says one is already active |
| 2 | Filing a claim: first claim, a condition VA already rated, or one the veteran says is caused by a rated condition | 21-526EZ (FM1). Same form for all three; the veteran names the claim type |
| 3 | Got a VA decision and wants it reviewed; the veteran picks the lane after hearing all three explained | Supplemental Claim 20-0995 (FM10), or Higher-Level Review 20-0996 (FM11), or Board Appeal 10182 (FM12): only the one picked |
| 4 | Wants VA to get records from private doctors | 21-4142 (FM6) and 21-4142a (FM7) |
| 5 | Says they cannot work because of their service-connected conditions | 21-8940 (FM8); 21-4192 (FM9) is for their former employer(s) to complete |
| 6 | Wants to send a written statement, a witness statement, or (only if the veteran said so) a statement about a mental-health condition from an in-service event | 21-4138 (FM3), 21-10210 (FM4), 21-0781 (FM5): only the ones that match what they said |
| 7 | Adding or removing a spouse, child, or dependent parent | 21-686c (FM15) |
| 8 | Needs copies of service records or a DD 214 | eVetRecs online or SF-180 (FM16, FM21) |
| 9 | Military retiree who says a condition is combat-related (CRSC is a military-department claim, not VA) | DD 2860 (FM18); if CRSC was already denied: DD 3210 (FM19), then DD 149 (FM20) |
| 10 | Asks to appoint a representative | 21-22 for a VSO (FM13) or 21-22a for an attorney or claims agent (FM14). MyVSO explains these only; it never holds or files them |
