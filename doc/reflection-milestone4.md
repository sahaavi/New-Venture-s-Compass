# New Venture(s) Compass

## Team Reflection
This document lists feedback and details on our New Venture(s) Compass app for final milestone Milestone 4.

## Background
The default view provides data for 6 countries, with each country randomly chosen from a different continent (excluding Antarctica) using the World Bank database. The data helps to gain insights on different indicators and areas one need to gain knowledge on to start a new business in a country.

The app has three different tabs for different functions – 1. Main: This gives brief recommendation on countries suitable for new ventures as per user’s expectations with respect to the cost for starting business and time required for starting business. 2. Resources: This page gives detailed information regarding financial instruments and labor resource status for the countries selected in Main page. 3. Logistics: This page gives detailed information regarding status of imports, exports and overall logistics picture for the countries selected in Main page. Users can view and compare macro and micro economic statuses of different countries by navigating through different pages. 

For specific inputs, a dropdown menu is provided that allows multiple countries or years selection. Sliders are present on the side to further fine tune parameters for selected countries. Final goal is that these provide information for user to be able to finalize the exact country or countries for their new ventures and investments that meets their expectations. 

## Development and Implementation - First release 
a. Dashboard in dash and Python and hosted on heroku cloud platform.
b. Default view with user training video.
c. Various types of graphs and interactivity between graphs, input dropdowns and sliders (attention to consistency).
d. Data sources and details.
e. TA feedback - added training video, expanded size of map chart, added default for Time to Import (hours) and Time to Export graphs.

### Development and Implementation - The road ahead

e. Restrict inputs systematically to 10 countries (nice to have feature so deprioritized due to timelines).
f. Background color or logistics index chart (known issue).

### Dashboard Advantages
a. There is text embedded above each tab which gives the reader a sense of what they are looking for and why its necessary. 
This story telling approach will guide user interactively and with rationale to select countries.

b. Dashboard has a default view with 10 countries, this makes anyone get quickly familiar with what the dashboard can deliver in an intuitive way. There is no such application that exists today that we know of.
 
## Dashboard Limitations
a. Data is available only till 2019, new data will be available only in 2024. Till then, history is limited for decision.

b. Some data is not available in the database, graph would report NA. NA is imputed to 0 in Average time to clear Exports chart.


## Dashboard Open Issues
Please refer to the GitHub issues list and road ahead section. 

We hope, one can appreciate the purpose and the functions built and imagined so far of the app.