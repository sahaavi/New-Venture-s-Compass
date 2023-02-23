# New Venture(s) Compass - Product Discovery

We discuss the motivation, purpose and perceived user experience and benefits of New Venture(s) Compass dashboard in this document.

We also briefly introduce the dataset used for the dashboard.

## Motivation and purpose:

**Our role:** Data scientist consultancy and business advisory firm
**Target audience:** Entrepreneurs who want to start a new global business
This is an era of global economy and good hearts who want to bridge the gap in development between countries. Entrepreneurs are interested in creating new initiatives/ventures and contribute to global economy including developing countries. There are several unknowns in starting a business in a country and the requirements vary by country. This is a risk to any business as they are threat to success and risk to countries as well who could potentially miss new opportunities.
Our app is intended to help entrepreneurs select countries suitable for their needs and go more informed into these countries. Our app indirectly helps different countries as they can benefit from new opportunities. In these ways, our app reduces risk of failure for businesses and helps countries benefit from new opportunities.

## Expanded EDA and description of the data:
Original dataset has 5852 rows with data from 2003-2019 (Column name: example: 2003 [YR2003] for year 2003) of 266 different countries (has both Country Name, Country Code) in the world. 22 different world development indicators (Column name: Series Name) as tracked by Worldbank are in scope. This means, there are a total of 22 rows for each country in the dataset.
Due to non-availability of data, around 30 countries and years 2003-2013 are dropped and the resulting dataset is approximately 3000 records. There are a total of 9 columns in the dataset and are: Country Name, Country Code, Series Name, date column for each year from 2014 to 2019 (6 columns).
We will be visualizing data for around 200 countries in the main dashboard. Data and records are retained in the dataset based on whether the two important indicators – 1. Time to start a business and 2. Cost to start a business are available. If any of the other parameters are not available, those will be reported in remainder of the graphs in “resources” and “logistics” tabs as not available.
Worldbank is working on a new methodology and is currently planned to be available in April 2024. Dashboard will be revisited for enhancements after this is released.
Using Country code, we will derive a new variable (“continent”) for use in the map representation.

## Research question(s) that are explored:

Jupiter is a budding business owner who wants to expand current venture/idea in new countries to help in growth of their economies and also to capture benefits through global comparative advantage or offshoring. Jupiter wants to [explore] different countries and their ranking to easily start a new business using reliable world development indicators from Worldbank. This enables Jupiter to [compare] nuances and dynamics of different countries and [identify/select] the most preferred or ideal countries for starting or expanding the business.
When Jupiter logs on to the “New Venture(s) Compass” app, Jupiter can see an overview of selected world development indicators that are used in guiding the selection process. Jupiter can see that the app has structured data into three tabs – 1. Home 2. Resources 3. Logistics. Jupiter will be able to
1.	Home:
* Primarily provide/input preference for new business countries by selecting following inputs – 1. Cost to start a business 2. Time required to start a business on the Home tab.
* Narrow down selection further (fine tune) using,
  *   Year: Data available from 2003-2019. Allowed selection: Multiple years in given range (Min:1, Max: 10 years (both inclusive)
  *   Gender: For development indicators available based on Gender. Allowed selection: All, Male, Female
  *   Country: (Min:1, Max: 6 countries (both inclusive)
*   View and assess cost factors to start a new business and time requirements in days to start a new business for selected countries, year, gender
2.	Resources:
* View details on different resource availability in the selected countries, year carried forward from Home tab.
* Narrow down selection further (fine tune) using,
  *   Year: Years as selected in Home tab can be further reduced if required. Allowed selection: Multiple years in given range (Min:Home tab minimum, Max: Home tab maximum (both inclusive)
  *   Gender: For development indicators available based on Gender. Allowed selection: All, Male, Female
  *   Average interest rate prevailing in the country based on historical data.
* View and assess resource related factors to start a new business for selected country, year, gender. Resource related factors present are 1. Interest rate variation over selected years 2. Unemployment rates 3. Labor force participation for ages 15-24 (provide insights into the level of participation of young people in the labor market).
3.	Logistics:
* View details on different logistic aspected in the selected countries, year carried forward from Home tab.
* Narrow down selection further (fine tune) using,
  *   Year: Years as selected in Home tab can be further reduced if required. Allowed selection: Multiple years in given range (Min:Home tab minimum, Max: Home tab maximum (both inclusive)
  *   Time required to export or import goods.
  *   Time required to clear clearance for goods.
* View and assess logistics related factors to start a new business for selected country, year. Logistics related factors present are 1. Logistics overall performance index 2. Average time to clear customs 3. Time to export and import.


Jupiter, based on all the information gets an idea of countries preferable for starting business and proceeds with booking travel and writing a business plan 😊
