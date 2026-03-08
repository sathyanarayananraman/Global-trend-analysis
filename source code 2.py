import pandas as pd

adult= pd.read_csv("https://ourworldindata.org/grapher/literacy-rate-adults.csv?v=1&csvType=full&useColumnShortNames=true",
                    storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'})
youth=pd.read_csv("https://ourworldindata.org/grapher/literacy-rate-of-young-men-and-women.csv?v=1&csvType=full&useColumnShortNames=true",storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'})

illiteracy = pd.read_csv("https://ourworldindata.org/grapher/literate-and-illiterate-world-population.csv",
                            storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'})
GDP = pd.read_csv("https://ourworldindata.org/grapher/gdp-per-capita-worldbank.csv?v=1&csvType=full&useColumnShortNames=true",
                            storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'})
avg_school_years = pd.read_csv("https://ourworldindata.org/grapher/literacy-rates-vs-average-years-of-schooling.csv?v=1&csvType=full&useColumnShortNames=true",storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'})

#cleaning dataframes: 
adult= adult.rename(columns={"entity": "country",
    "adult_literacy_rate__population_15plus_years__both_sexes__pct__lr_ag15t99":"adult_literacy_rate"})

youth= youth.rename(columns={"entity": "country",
    "youth_literacy_rate__population_15_24_years__male__pct__lr_ag15t24_m": "youth_literacy_male",
    "youth_literacy_rate__population_15_24_years__female__pct__lr_ag15t24_f":"youth_literacy_female"})

illiteracy= illiteracy.rename(columns={"Entity": "country","Code":"code","Year":"year",
                                      "Illiterate":"illiteracy_rate","Literate":"literacy_rate"})

GDP= GDP.rename(columns={"entity": "country",
    "ny_gdp_pcap_pp_kd": "gdp_per_capita"})

avg_school_years= avg_school_years.rename(columns={"entity": "country",
    "mf_youth_and_adults__15_64_years__average_years_of_education":"avg_years_of_education"})

adult = adult.dropna(subset=["code"])
youth = youth.dropna(subset=["code", "youth_literacy_male","owid_region"])
GDP = GDP.dropna(subset=["code","owid_region"])
avg_school_years = avg_school_years.dropna(subset=["code", "avg_years_of_education",'literacy_rate',"owid_region"])
illiteracy=illiteracy.dropna(subset=["code"])

#creating data frames:

df_literacy = ( pd.merge(adult,youth,
             on=["country", "code", "year"],
             how="inner")
      .drop_duplicates()
      .query("year >= 1990")
      .sort_values("year", ascending=False))
df_literacy = df_literacy[df_literacy["code"] != 0]
df_illiteracy =illiteracy.drop_duplicates().query("year >= 1990").sort_values("year", ascending=False)
df_illiteracy = df_illiteracy[df_illiteracy["code"] != 0]
df_gdp_schooling =(pd.merge(GDP,avg_school_years,
             on=["country", "code", "year","owid_region"],
             how="inner")
      .drop_duplicates()
      .query("year >= 1990")
      .sort_values("year", ascending=False))
df_gdp_schooling = df_gdp_schooling[df_gdp_schooling["code"] != 0]

#feature engineering:

df_literacy["Literacy_Gender_Gap"]=abs(df_literacy['youth_literacy_male']-df_literacy['youth_literacy_female'])
df_gdp_schooling['GDP_per_Schooling_Year']=(df_gdp_schooling['gdp_per_capita']-df_gdp_schooling['year'])
df_gdp_schooling['Education_Index'] = (
    (df_gdp_schooling['literacy_rate'] / 100) +
    (df_gdp_schooling['avg_years_of_education'] /
     df_gdp_schooling['avg_years_of_education'].max())
    ) / 2
df_literacy['Youth_Literacy_Average']= (df_literacy['youth_literacy_male']+ df_literacy['youth_literacy_female'])/2
df_literacy["Literacy_Growth_Rate"] = (
    df_literacy.groupby("country")["adult_literacy_rate"]
    .pct_change() * 100)
df_literacy = df_literacy.sort_values(["country", "year"])
df_literacy["Literacy_Growth_Rate"] = (df_literacy["Literacy_Growth_Rate"].fillna(0))

#SQL CONNECTION:
import pymysql
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='Sathya1234',
    database='guvi_project')
cursor = connection.cursor()
print(" Connected using pymysql")

# CREATE TABLE LITERACY RATE: 
cursor.execute('use guvi_project')
cursor.execute("""CREATE TABLE if not exists literacy_rates(
country varchar(30),
code VARCHAR(10),
year int,
adult_literacy_rate float,
youth_literacy_male float ,
youth_literacy_female float, 
owid_region varchar(30) , 
Literacy_Gender_Gap float,
Youth_Literacy_Average float, 
Literacy_Growth_Rate float,
PRIMARY KEY(country,year))
""")
print("Table created successfully ")

#data Ingestion:

from sqlalchemy import create_engine
import pandas as pd
engine = create_engine("mysql+pymysql://root:Sathya1234@localhost/guvi_project")
df_literacy.to_sql(
    name="literacy_rates",
    con=engine,
    if_exists="append",  
    index=False
)
print("Data inserted successfully ")

#CREATE TABLE illiteracy_population: 
cursor.execute('use guvi_project')
cursor.execute("""CREATE TABLE if not exists illiteracy_population(
country varchar(30),
code VARCHAR(10),
year int,
illiteracy_rate float,
literacy_rate float ,
PRIMARY KEY(country,year))
""")
print("Table created successfully ")

#data Ingestion:
 
from sqlalchemy import create_engine
import pandas as pd
engine = create_engine("mysql+pymysql://root:Sathya1234@localhost/guvi_project")
df_illiteracy.to_sql(
    name="illiteracy_population",
    con=engine,
    if_exists="replace",  
    index=False
)
print("Data inserted successfully ")

#CREATE TABLE gdp_schooling:
cursor.execute('use guvi_project')
cursor.execute("""CREATE TABLE if not exists gdp_schooling(
country varchar(30),
code VARCHAR(10),
year int,
gdp_per_capita bigint , 
owid_region_x varchar(30),
literacy_rate float, 
avg_years_of_education float, 
population_historical bigint ,
owid_region_y varchar(30), 
GDP_per_Schooling_Year float, 
Education_Index float,
PRIMARY KEY(country,year))
""")
print("Table created successfully ")

#data Ingestion:
from sqlalchemy import create_engine
import pandas as pd
engine = create_engine("mysql+pymysql://root:Sathya1234@localhost/guvi_project")
df_gdp_schooling.to_sql(
    name="gdp_schooling",
    con=engine,
    if_exists="replace",  
    index=False
)

print("Data inserted successfully ")

#SQL QUERRIES: LITERACY RATE

#Get top 5 countries with highest adult literacy in 2020.
cursor.execute("""
    select country ,code,year,adult_literacy_rate from literacy_rates WHERE YEAR=2020 
    order by adult_literacy_rate desc
    limit 5;
    """)
rows = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]
df = pd.DataFrame(rows, columns=columns)
print(df)

# Find countries where female youth literacy < 80%.
cursor.execute("""
    select country,code,year,youth_literacy_female from literacy_rates WHERE youth_literacy_female < 80
    order by youth_literacy_female desc,year desc;  
    """)
rows = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]
df = pd.DataFrame(rows, columns=columns)
print(df)

# Average adult literacy per continent (owid region).
cursor.execute("""
    select owid_region,avg(adult_literacy_rate) from literacy_rates 
    group by owid_region
    order by owid_region desc
    """)
rows = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]
df = pd.DataFrame(rows, columns=columns)
print(df)

#SQL QUERRIES: ILLITERACY POPULATION

# Countries with illiteracy % > 20% in 2000.
cursor.execute("""
    select country,year,illiteracy_rate from illiteracy_population where illiteracy_rate > 20 and year=2000
    order by illiteracy_rate desc;
    """)
rows = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]
df = pd.DataFrame(rows, columns=columns)
print(df)

# Trend of illiteracy % for India (2000–2020).
cursor.execute("""
    SELECT country,year,illiteracy_rate FROM illiteracy_population
    WHERE country = 'India'AND year BETWEEN 2000 AND 2020
    ORDER BY year;
    """)
rows = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]
df = pd.DataFrame(rows, columns=columns)
print(df)

# Top 10 countries with largest illiterate population in the last year.(2022)
cursor.execute("""
    SELECT country,year,illiteracy_rate FROM illiteracy_population
    where year=2022 order by year desc, illiteracy_rate desc
    limit 10;
    """)
rows = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]
df = pd.DataFrame(rows, columns=columns)
print(df)

# SQL QUERRIES ON GDP_SCHOOLING:

# Find countries with avg_years_schooling > 7 and gdp_per_capita < 5000.
cursor.execute("""
    select country,year,gdp_per_capita,avg_years_of_education,owid_region from gdp_schooling
    where avg_years_of_education >7 AND  gdp_per_capita < 5000
    order by  gdp_per_capita desc,year desc;
    """)
rows = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]
df = pd.DataFrame(rows, columns=columns)
print(df)

# Rank countries by GDP per schooling for the year 2020
cursor.execute("""
        SELECT 
        country, year, gdp_per_capita,avg_years_of_education,
        (gdp_per_capita / avg_years_of_education) AS gdp_per_schooling,
        RANK() OVER (ORDER BY (gdp_per_capita / avg_years_of_education) DESC) AS gdp_per_schooling_rank
        FROM gdp_schooling
        WHERE year = 2020
        ORDER BY gdp_per_schooling DESC
        """)
rows = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]
df = pd.DataFrame(rows, columns=columns)
print(df)

# Find global average schooling years per year.
cursor.execute("""
        SELECT year,avg(avg_years_of_education)global_avg_schooling 
        from gdp_schooling group by year
        order by year
        """)
rows = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]
df = pd.DataFrame(rows, columns=columns)
print(df)

# JOIN QUERRIES

# List top 10 countries in 2020 with highest GDP per capita but lowest average years of schooling(less than 6
cursor.execute("""
        SELECT country,year,gdp_per_capita,avg_years_of_education as lowest_avg_years_of_schooling
        from gdp_schooling where avg_years_of_education < 6 and year=2020
        order by gdp_per_capita desc
        limit 10
        """)

rows = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]
df = pd.DataFrame(rows, columns=columns)
print(df)

# Show countries where the illiterate population is high despite having more than 10 average years of schooling.
cursor.execute("""
        SELECT i.country, i.year,i.illiteracy_rate,g.avg_years_of_education
        from gdp_schooling g 
        inner join illiteracy_population i 
        on i.country=g.country and i.year=g.year
        where g.avg_years_of_education > 10 
        order by i.illiteracy_rate desc ,  i.year desc
        LIMIT 10
        """)

rows = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]
df = pd.DataFrame(rows, columns=columns)
print(df)

# Compare literacy rates and GDP per capita growth for a selected country over the last 20 years. (country of your choice)
cursor.execute("""
        SELECT l.country,l.year,l.adult_literacy_rate,g.gdp_per_capita
        FROM literacy_rates l
        JOIN gdp_schooling g ON l.country = g.country AND l.year = g.year
        WHERE l.country = 'spain' AND l.year >= YEAR(CURDATE()) - 20
        ORDER BY l.year;
        """)

rows = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]
df = pd.DataFrame(rows, columns=columns)
print(df)

# Show the difference between youth literacy male and female rates for countries with GDP per capita above $30,000 in 2020.
cursor.execute("""
        SELECT l.country,l.year,l.youth_literacy_male,l.youth_literacy_female,
        (l.youth_literacy_male - l.youth_literacy_female) AS literacy_gap,g.gdp_per_capita
        FROM literacy_rates l
        JOIN gdp_schooling g ON l.country = g.country 
        AND l.year = g.year
        WHERE g.gdp_per_capita > 30000 AND l.year = 2020
        ORDER BY literacy_gap DESC;
        """)

rows = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]
df = pd.DataFrame(rows, columns=columns)
print(df)

#Creating charts using MatPlotlib:
import matplotlib.pyplot as plt 
import seaborn as sns 

# Government Policy & Budget Allocation
# GDP Vs Literacy_growth Rate :
sns.scatterplot(data=df_gdp_schooling, x='gdp_per_capita', y='literacy_rate') 
plt.xlabel("GDP per Capita")
plt.ylabel("Literacy Rate (%)")
plt.title("Literacy Rate vs GDP per Capita")
plt.show()

 # International Development Programs : 
# step 1 : 
# Region wise illiteracy dta:
data=pd.merge(df_illiteracy,df_literacy, on=['country','code','year'], how='right')
grouped  = (  data.groupby(['owid_region'])['illiteracy_rate'].mean().reset_index())

plt.figure(figsize=(10,7))
sns.lineplot(data=grouped,x='owid_region',y='illiteracy_rate',sort=True,
             linewidth=2)
plt.xlabel("Region")
plt.ylabel("illiteracy (%)")
plt.title("illitaracy data (Region wise)")
plt.show()

# step 2:
# Gender Literacy gap region wise:
plt.figure(figsize=(10,7))
sns.lineplot(data=df_literacy,x='owid_region',y='Literacy_Gender_Gap',errorbar=None ,sizes=6 )
plt.title("Gender Literacy Gap (Region wise)", fontsize=10)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Literacy Gap", fontsize=12)

#  Corporate Social Responsibility (CSR) Planning :
# literacy_rate:
sns.histplot(df_illiteracy['literacy_rate','country'])
plt.xlabel("Literacy percentage")
plt.ylabel('No.Of.Countries') 
plt.title('Literacy chart')
plt.show() 

# Education NGOs & Non-Profits
sns.scatterplot(data=df_gdp_schooling,
x='avg_years_of_education',
y='literacy_rate',
hue='owid_region')

# Economic Forecasting & Workforce Planning:
sns.lineplot(data=df_gdp_schooling, x ='year' , y='Education_Index',errorbar=None)
plt.xlabel("year")
plt.ylabel('Education_Index') 
plt.title('Education trends')
plt.show() 

#converting Dataframes to CSV :
df_gdp_schooling.to_csv(r"D:\python projects\df_gdp_schooling.csv", index=False)
df_illiteracy.to_csv(r"D:\python projects\df_illiteracy.csv",index=False)
df_literacy.to_csv(r"D:\python projects\df_literacy.csv",index=False)