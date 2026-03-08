Global Literacy & Education Trends: An Analytical Study
📌 Project Overview

Literacy rates are a key indicator of a country's human development, economic growth, and educational progress.
This project analyzes adult literacy, youth literacy, illiteracy population, GDP per capita, and average years of schooling across countries and years to identify patterns, correlations, and global disparities in education.

The analysis combines Python, SQL, and Power BI to perform data cleaning, exploratory analysis, and dashboard creation for meaningful insights.

🎯 Skills Gained From This Project

📥 Data Collection & Cleaning

📊 Exploratory Data Analysis (EDA)

⚙️ Feature Engineering

🗄 SQL Database Design & Query Writing

📈 Power BI Dashboard Development

📖 Data Storytelling & Insight Presentation

🌍 Domain

Education Analytics & Socio-Economic Data Analysis

📝 Problem Statement

Literacy plays a crucial role in economic growth, workforce readiness, and societal development.
By analyzing global literacy and education data, this project aims to:

Identify trends in literacy and illiteracy

Explore the relationship between education and economic development

Detect gender gaps and regional disparities

Highlight countries with significant improvement or stagnation in education

📊 Real-World Business Use Cases
📊 Government Policy & Budget Allocation

Governments can analyze literacy vs GDP relationships to allocate education funding effectively.

Helps identify regions where investment in education yields higher economic returns.

🌍 International Development Programs

Organizations like UNESCO, UNICEF, and the World Bank can:

Identify regions with high illiteracy rates

Track progress toward Sustainable Development Goal (SDG 4 – Quality Education).

💼 Corporate Social Responsibility (CSR)

Corporations can:

Identify low-literacy regions for skill development programs

Improve future workforce readiness.

🏫 Education NGOs & Non-Profits

NGOs can:

Identify high-priority areas for literacy campaigns

Track year-to-year literacy improvements.

📈 Economic Forecasting & Workforce Planning

Businesses can analyze education and literacy trends to predict future talent availability.

🗺 Regional Disparity Analysis

Comparing literacy with GDP highlights socio-economic inequalities across countries and regions.

📚 EdTech Market Research

EdTech companies can identify regions with low literacy and low GDP to introduce affordable learning solutions.

🔄 Project Workflow
1️⃣ Dataset Collection

Datasets were collected from Our World in Data (OWID).

Base URL

https://ourworldindata.org/grapher/

⚠️ Data collection is performed in Google Colab because some dataset URLs may be blocked in local IDEs.

Datasets Used
Indicator	Dataset Link
Adult Literacy Rate	https://ourworldindata.org/grapher/literacy-rate-adults.csv

Youth Literacy Rate	https://ourworldindata.org/grapher/literacy-rate-of-young-men-and-women.csv

Illiterate Population	https://ourworldindata.org/grapher/literate-and-illiterate-world-population.csv

GDP per Capita	https://ourworldindata.org/grapher/gdp-per-capita-worldbank.csv

Average Years of Schooling	https://ourworldindata.org/grapher/literacy-rates-vs-average-years-of-schooling.csv
🔍 Data Understanding

Datasets were loaded into Pandas DataFrames and merged as follows:

df_literacy → Adult & Youth Literacy Rates

df_illiteracy → Illiterate Population Data

df_gdp_schooling → GDP per Capita & Average Years of Schooling

🧹 Data Cleaning

Key data preparation steps included:

Handling missing values (drop or impute)

Removing duplicate records

Standardizing country names

Renaming columns for clarity

Identifying unusual values

Filtering data between 1990 – 2023

⚙️ Feature Engineering

Additional features were created to improve analysis.

Feature	Purpose
Illiteracy %	Percentage of population that is illiterate
Literacy Gender Gap	Difference between male & female literacy
GDP per Schooling Year	Economic output per year of education
Education Index	Combined indicator of literacy & schooling
Youth Literacy Average	Average youth literacy across genders
Literacy Growth Rate	Year-over-year literacy improvement
📊 Exploratory Data Analysis (EDA)

EDA was performed using Matplotlib and Seaborn.

Univariate Analysis

Distribution of literacy rates

GDP per capita trends

Years of schooling distribution

Bivariate Analysis

Literacy vs GDP relationship

Literacy vs schooling correlation

Gender literacy gap

Insights

Identification of trends, outliers, and correlations

Detection of regional disparities in education

🗄 Data Storage (SQL)

Three tables were created in MySQL:

1️⃣ literacy_rates
2️⃣ illiteracy_population
3️⃣ gdp_schooling

Composite key used:

(country, year)
🧮 SQL Queries
Literacy Rates

Top 5 countries with highest adult literacy in 2020

Countries where female youth literacy < 80%

Average adult literacy per continent

Illiteracy Population

Countries with illiteracy % > 20% in 2000

Illiteracy trend for India (2000–2020)

Top 10 countries with largest illiterate population

GDP & Schooling

Countries with schooling > 7 years and GDP < $5000

Rank countries by GDP per schooling year (2020)

Global average schooling years per year

Join Queries

Countries with highest GDP but lowest schooling (<6 years)

Countries with high illiteracy despite >10 schooling years

Literacy vs GDP growth for a selected country

Youth literacy gender gap for countries with GDP > $30,000

📊 Power BI Dashboard

Interactive dashboards were created using Power BI.

Dashboard Features

Literacy vs Illiteracy trend analysis

Gender literacy gap visualization

GDP vs Literacy correlation

Global literacy ranking

Regional literacy comparisons

Example Visualizations

Line Charts (Literacy trends)

Scatter Plots (GDP vs Literacy)

Heatmaps (Country comparisons)

Ranking charts

Slicers for Year & Country

📦 Project Deliverables

✅ 3 Cleaned DataFrames

✅ SQL table creation & insertion scripts

✅ Jupyter Notebook with EDA & visualizations

✅ Power BI Dashboard

✅ Final insights and conclusions

🛠 Tech Stack

Python

Pandas

NumPy

Matplotlib

Seaborn

SQL / MySQL

Power BI

🏷 Tags

Python Pandas NumPy SQL MySQL EDA Data Cleaning Power BI Data Visualization Feature Engineering Education Analytics Socio-Economic Analysis
