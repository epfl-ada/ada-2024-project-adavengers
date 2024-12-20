# Pints & Politics: Analyzing Beer Preferences Across U.S. States


## Abstract
This study dives into the fascinating link between beer preferences and political identities in the U.S. By analyzing beer styles, emotions, sentiments, and key attributes through user reviews, we uncover patterns that go beyond taste. Using tools like LDA and sentiment analysis, we’ll map out how different states' beer choices align with political leanings. We'll also explore whether beer preferences shift during election years, especially in swing states. Can beer really reveal more than just flavour? Let's find out!


## Datastory
The datastory can be accessed on this [website](https://mikaelkalajdzic.github.io/adavengers-datastory/datastory) for free.


## Research Questions


Q1. How can beer preferences be categorized and visualized across different dimensions (such as style, emotion, sentiment, and key attributes) to provide a comprehensive understanding of beer types based on the US reviewers?

Q2. How do these beer preferences (referred to Q1) vary across different U.S. states, and can these preferences be linked to political ideologies? Are there specific beer preferences that correlate with Republican or Democratic voting patterns?

Q3. How do beer preferences change over time during election years, particularly in swing states? 



## Proposed datasets


### 1. U.S. President Dataset ([link](https://doi.org/10.7910/DVN/42MVDX))

This dataset contains presidential election results by state from 1976 to 2020.

It is complete with no missing values and includes all 50 states for each year. For our analysis, we focus on election years 2004, 2008, 2012, and 2016 (subset: 2001–2017) to align with our beer reviews. 

This lightweight dataset (501KB, 4288 lines) is easy to manipulate. So far we calculated vote proportions by party per state (party_winners_over_years.csv) and identified "swing" states (those changing party allegiance, party_winners.csv).


### 2. NY Times Exit Poll Dataset ([2004](https://www.nytimes.com/elections/2012/results/president/exit-polls.html), [2008](https://archive.nytimes.com/www.nytimes.com/elections/2008/results/president/national-exit-polls.html?mod=article_inline), [2012](https://www.nytimes.com/elections/2012/results/president/exit-polls.html), [2016](https://edition.cnn.com/election/2016/results/exit-polls))

These datasets provide the percentage of Democrat and Republican votes for age groups, 18-29, 30-44, and 45-64, across 17 states obtained from exit polls for the election years: 2004, 2008, 2012, and 2016. Exit poll data was not available for all states due to poll not being conducted, since conducting these surveys is costly, the consistently Democrat or Republican states are usually omitted. States we are left with are: Arizona, California, Florida, Georgia, Indiana, Iowa, Kentucky, Nevada, New York, New Hampshire, North Carolina, Pennsylvania, South Carolina, Texas, Virginia, Wisconsin.

## Methods


We have separated the project into 3 tasks, each of them corresponding to one of the research questions above.


### Part 1. Characterizing beer preferences

We analyzed the beer reviews dataset. To define diverse beer preferences, we will examine different dimensions such as beer style, sentiment and overall score of a beer. The goal in this part is to get a better sense of the general beer styles that we have.
We regrouped the 108 unique beer styles into 8 general common beer categories. We tried to use data to understand what those 8 categories of beer mean, what are the beer characteristics that differ? (we defined 5 semantical characteristics about a beer : ( 1. Hop Intensity 2. Malt Profile 3. Body/Texture 4. Alcohol Strength 5. Carbonation) 
To measure how a general beer style is having a specific characteristic we measured the cosine similarity between that characteristic and the average reviews of that general beer style in an embedding space. 
But before doing this we verified if the beer reviews talk about the beer characteristic or not? To do this we studied the topics that are expressed in the reviews using an LDA model.


### Task 2. Beer preferences and political affiliation - a lookalike analysis

Our goal is to analyze beer style preferences in terms of their average rating and positive sentiment in reviews, across states and their potential connection to political affiliations. We focus on the popular eight beer styles and account for confounding factors like age, and geographical location, which may influence both beer preferences and political leanings.

Given the limitations of our dataset, we are not able to estimate factors like education, wealth, or ethnicity based on text alone. For instance, it's tricky to infer education levels or ethnicity from English-written reviews with “random” usernames. Therefore, we focus on age, and location as confounding factors, using state-level estimates.

We assume review user ages are uniformly distributed in the range from 18 to 64. And for political data, we extract 3 age groups from exit polls: 18-29, 30-44, and 45-64. We got the percentage of Democrat and Republican votes for each age group across the 17 states of the dataset.

All the data is available for years 2004-2016, with which we construct a time-series of voting and beer preference trend. We perform K-Means clustering to determine states with similar voting patterns and examine their beer preference trends.

By performing a "lookalike" analysis, we aim to determine influence of confounding factors on beer preference. 


### Task 3. Time series analysis of beer preferences over election years in swing states

We investigate how beer preferences change over time during and in between election years in swing states. By analyzing average rating trends for 3 most popular beer styles in the U.S., from the period 2004-2016, and tracking party affiliation changes by state, we explore the change in beer preference trends with the aim of linking it to the change of political climate.

## Contribution of team members

- Sara: Problem formulation, plotting graphs (task 2), data story writing
- Marija: Problem formulation, plotting graphs during data analysis (task 2&3), data story writing
- Luc: Initial dataset search, preliminary data analysis, coding task 3, writing data story
- David: Problem formulation, coding plotting graphs during data analysis (task 1), final result analysis
- Mikael: Preliminary data analysis, coding task 3, writing the data story

___
## Quickstart

```bash
# clone project
git clone https://github.com/epfl-ada/ada-2024-project-adavengers.git
cd ada-2024-project-adavengers

# [OPTIONAL] create conda environment
conda create -n <env_name> python=3.11
conda activate <env_name>


# install requirements
pip install -r pip_requirements.txt
```



## Project Structure

The directory structure of the project looks like this:

```
├── data                        <- Project data files (original data)
│   ├──BeerAdvocate                     <- Placeholder for BeerAdvocate dataset
│   ├── generated                       <- Generated csv/pickle files
│
├── fonts                       <- Addtional fonts
│
├── images                      <- Images (mask for cloud of words)
│
├── src                         <- Source code
│   ├── data                            <- Data directory (data processing, results stored in data/generated)
│   ├── ipynb scripts                   <- Jupyter Notebooks for analyzing additional datasets
│   ├── models                          <- Model directory
│   ├── plots                           <- Scripts generating interactive plots
│
├── results.ipynb               <- a well-structured notebook showing the results
│
├── .gitignore                  <- List of files ignored by git
├── pip_requirements.txt        <- File for installing python dependencies
└── README.md
```

