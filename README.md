# Page Load time Analysis

This is the Project was done as a part of the course work during my Doctoral course-work at SBU.
Here the goal was to observe how advertisments served at page load impact loading time. Overall methodology:
- We have a curated list of websites we want to analyze.
- We have an available adblock extension foe chrome.
- We invoke selenium testing framework, through our python framework and hit our list of websites.
- We re-invoke selenium framework, also install the adblock and hit the websites.
- We generate the audit trails for both cases, and compile our reports.

Brief description of files in this project:
- TestBed.py This is the starting point. Creates a csv dump of comparisons from hitting websites with and without adblocks, it uses components TestDriver and analyze from Analyzer.
- Analyzer.py contains Testdriver and analyze classes which uses WebsiteClass to generate statistics about each endpoint being hit by the TestBed
- WebsiteClass.py encapsulates the particulars of a website with and without adblock 
- test_list.txt contains list of websites to be tested
- workbook1.ipynb holds the analysis from the data
