
# Pints & Politics: Analyzing Beer Preferences Across U.S. States

## Abstract

The US election season is back! This is the time to explore how cultural habits intersect with political identities. With an annual consumption of around 100L/person, beer is central to American culture.
But what exactly are they drinking? What aspects of a beer are composing a beer preference (only the taste? the alcohol percentage?) What are their preferences, and do they vary by state? Could these differences align with political divisions?
The beer review dataset is ideal for our investigation because it includes user-generated ratings from all around the US. Coupled with data on political opinions (vote statistics, surveys,...), we can search for correlations between beer preferences and political position.
By analyzing beer preferences over time—using more than 15 years of reviews—there is opportunity to examine shifts in tastes and determine if political context influence beer culture in the US.

## Research Questions

0. How can we define diverse beer preferences? Our analysis will explore preferences through various dimensions, including beer style, its origin, and the most defining attributes.
1. How do beer preferences vary across different U.S. states, and can these preferences be linked to political ideologies? Are there specific beer preferences (e.g., style, origin, aspect) that correlate with Republican or Democratic voting patterns, i.e. *what makes a beer liberal/democratic*?
2. How do beer preferences change over time during election years in these states, especially in states which changed the overall political affiliation between two consecutive election years, i.e. swing states? Can these changes in beer preference serve as indicators of political shifts?
3. Is there such a thing as an *election beer*? Over what beers do people gather and discuss their political views, i.e. what are the most reviewed beers during the election period? 
4. How does the sentiment in beer reviews vary across regions with different political leanings?

## Proposed additional datasets

### 1. U.S. President Dataset

> MIT Election Data and Science Lab, 2017, "U.S. President 1976–2020", https://doi.org/10.7910/DVN/42MVDX, Harvard Dataverse, V8; 1976-2020-president.tab

This dataset contains results of presidental elections (number of votes per each candidate) per state from 1976 to 2020.

After analyzing the dataset, we first assessed its completeness. We found that it includes data for all 50 states for each year, with no missing or empty values.
For our analysis, we will use only a subset of this dataset, focusing on the entries from 2001 to 2017, specifically the election years 2004, 2008, 2012, and 2016, to align with the beer reviews we have.

This dataset has the advantage to be quite lightweight (501KB CSV file with 4288 lines) and easy to manipulate.
Our first idea to play with this dataset is to calculate some statistics.
We were first interested in the proportion of votes for each party per state over the years.
Then we were curious to evaluate what are the "swing" states this dataset would give (states that changed party).

### 2. The Correlates of State Policy Dataset

> Grossmann, M., Jordan, M. P. and McCrain, J. (2021) “The Correlates of State Policy and the Structure of State Panel Data,” State Politics & Policy Quarterly. Cambridge University Press, pp. 1–21. doi: 10.1017/spq.2021.17.

The Correlates of State Policy dataset includes more than 3000 variables, with observations across the 50 U.S. states and across time (1900–2019, approximately).
These variables represent policy outputs, as well as political, social, and economic factors that may influence policy differences.

For our analysis, we are particularly interested in variables such as:
- the population within certain age groups (e.g., 18-24 years old, 25-44 years old, etc.)
- the minimum legal drinking age per state
- personal income per capita

The dataset is provided as a CSV file (~70 MB). Upon first inspection, we observed that it contains a lot of missing ("NA") values. Along this dataset, there is a PDF document that gives clear definitions for each of the 3000+ variables, along with information on the years for which data is available.
Given that some variables include data going back to the early 20th century, it is likely that this is the reason why there is a large number of "NA" values.
However, after reviewing the documentation, we confirmed that the variables we are interested in have data available for our timeframe (2001-2017).

Additionally, the dataset's website provides a nice interactive web application for visualizing and exploring the data: [CSPP Interactive Tool](https://cspp.ippsr.msu.edu/cspp/).

## Methods

We have separated the project in 5 tasks, each of them corresponding to one of the research questions above.

### Task 0. Characterizing beer preferences

To characterize beer preferences, we will first map the diverse beer styles in our dataset to the five most common styles based on popularity or frequency. Also, we will analyze beer reviews to identify the aspects that consistently receive the highest ratings. Finally, we will classify the beers by their origin, distinguishing between those produced by local U.S. breweries and international ones. This approach provides a comprehensive understanding of preferences across style, quality, and origin.

### Task 1. Beer preferences and political affiliation

First of all, we want to determine the beer style preferences among different states, and whether it has something to do with the political affiliation of that state. We would consider some of the most popular beer styles in the U.S., i.e. the ones that are most reviewed.  
In order to rightfully present our findings, we will have to take into account several confounding factors that could also influence beer preference as well as political leaning, such as *age, wealth, education*, *ethnicity* as well as geographical location of the state. Since those are unobservable confounding factors, we will take a specific approach in order to estimate them. To the best of our knowledge, there is no work done in estimating the level of education based on written text, especially reviews. We believe that even Sheakspere wouldn't write a very eloquent and elaborate beer review, thus, unfortunately we would have to disregard studying the influence of this factor. For ethnicity it is the similar issue, since we don't have a reasonable way to estimate the ethnicity of a person from reviews written in English, based in US and with relatevily random usernames of beer reviewers. Because of this, we will consider only age, wealth and location of a state as our confounding factor to the political affiliation and beer preference. We estimate those factors on the basis of a whole state since we aim to determine whether beer style taste differs from state to state, based on it's majority political stance.
As for age, we aim to determine the mean age of a state by estimating the age of users that leave reviews are registered in that state. To attain this, we will take the following approach. We will consider the minimal legal drinking age for each state and consider it as the time the user has registered to the beer rating platform. Then, we will substract the date of a review with the registration date and add the amount of passed time to the legal drinking age.  Or age from the dataset??
As for wealth, we will use the mean income per capita of that state, which can be found in the additional dataset #2. 


![Confounding factors graph](confounding_factors.JPG)

### Task 2. Time Series Analysis of Beer Preferences During Election Years

How does beer preference change over the years, and specifically over the election years? Does it change in the swing states, could the change in beer preference determine the swing state? To this end, we will have to extract information from beer reviews from the election years in that period, as well as determine the states that have changed the winning party over the election years. 
To analyze shifts in beer preferences, we’ll quantify the popularity of various beer styles by state during election years, using metrics such as the number of reviews and average ratings to investigate changes in taste over time. This time series analysis will examine whether fluctuations in beer preferences correspond with election cycles, especially around years when swing states shifted political affiliation. By comparing beer style trends in swing states to those in consistently aligned states, we can investigate whether swing states show unique shifts that could hint at a sociopolitical influence. Using regression or causal inference methods, we’ll further assess if beer style trends might correlate with political changes while adjusting for demographic factors like age and wealth to control for potential confounding influences.

### Task 3. Search for election beers

### Task 4. Sentiment analysis of beer reviews for different leaning states

## Proposed timeline

- 15.11. Search for Datasets, Data Handling and Preprocessing and Exploratory Data Analysis
- 29.11. Implementation of tasks, divided between team members
- 6.12. Initial result analysis, refining methods and combining data stories
- 13.12. Final analysis and website assembly
- 20.12. Final project deadline

## Organization within the team

## Questions for TAs (optional)


___
## Quickstart

```bash
# clone project
git clone <project link>
cd <project repo>

# [OPTIONAL] create conda environment
conda create -n <env_name> python=3.11 or ...
conda activate <env_name>


# install requirements
pip install -r pip_requirements.txt
```



### How to use the library
Tell us how the code is arranged, any explanations goes here.



## Project Structure

The directory structure of the project looks like this:

```
├── data                        <- Project data files
│
├── src                         <- Source code
│   ├── data                            <- Data directory
│   ├── models                          <- Model directory
│   ├── utils                           <- Utility directory
│   ├── scripts                         <- Shell scripts
│
├── tests                       <- Tests of any kind
│
├── results.ipynb               <- a well-structured notebook showing the results
│
├── .gitignore                  <- List of files ignored by git
├── pip_requirements.txt        <- File for installing python dependencies
└── README.md
```

