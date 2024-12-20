# Pints & Politics: Analyzing Beer Preferences Across U.S. States


## Abstract
This study dives into the fascinating link between beer preferences and political identities in the U.S. By analyzing beer styles, emotions, sentiments, and key attributes through user reviews, we uncover patterns that go beyond taste. Using tools like LDA and sentiment analysis, we’ll map out how different states' beer choices align with political leanings. We'll also explore whether beer preferences shift during election years, especially in swing states. Can beer really reveal more than just flavour? Let's find out!


## Research Questions


Q1. How can beer preferences be categorized and visualized across different dimensions (such as style, emotion, sentiment, and key attributes) to provide a comprehensive understanding of beer types based on the US reviewers?

Q2. How do these beer preferences (referred to Q1) vary across different U.S. states, and can these preferences be linked to political ideologies? Are there specific beer preferences that correlate with Republican or Democratic voting patterns?

Q3. How do beer preferences change over time during election years, particularly in swing states? Is there such a thing as an *election beer* in terms of style and emotion it brings?




## Proposed datasets


### 1. U.S. President Dataset ([link](https://doi.org/10.7910/DVN/42MVDX))

This dataset contains presidential election results by state from 1976 to 2020.

It is complete with no missing values and includes all 50 states for each year. For our analysis, we focus on election years 2004, 2008, 2012, and 2016 (subset: 2001–2017) to align with our beer reviews. 

This lightweight dataset (501KB, 4288 lines) is easy to manipulate. So far we calculated vote proportions by party per state (party_winners_over_years.csv) and identified "swing" states (those changing party allegiance, party_winners.csv).


### 2. NY Times Exit Poll Dataset ([2004](https://www.nytimes.com/elections/2012/results/president/exit-polls.html), [2008](https://archive.nytimes.com/www.nytimes.com/elections/2008/results/president/national-exit-polls.html?mod=article_inline), [2012](https://www.nytimes.com/elections/2012/results/president/exit-polls.html), [2016](https://edition.cnn.com/election/2016/results/exit-polls))

This dataset provides the percentage of Democrat and Republican votes for age groups, 18-29, 30-44, and 45-64, across 17 states obtained from exit polls for the election years: 2004, 2008, 2012, and 2016. Exit poll data was not available for all states due to poll not being conducted, since conducting these surveys is costly, the consistently Democrat or Republican states are usually omitted. States we are left with are: Arizona, California, Florida, Georgia, Indiana, Iowa, Kentucky, Nevada, New York, New Hampshire, North Carolina, Pennsylvania, South Carolina, Texas, Virginia, Wisconsin.

## Methods


We have separated the project into 3 tasks, each of them corresponding to one of the research questions above.


### Task 1. Characterizing beer preferences


### Task 2. Beer preferences and political affiliation
Our goal is to analyze beer style preferences across states and their potential connection to political affiliations. We focused on popular the eight beer styles and account for confounding factors like age, and geographical location, which may influence both beer preferences and political leanings.

Given the limitations of our dataset, we weren't able to estimate factors like education, wealth, or ethnicity based on text alone. For instance, it's tricky to infer education levels or ethnicity from English-written reviews with “random” usernames. Therefore, we focused on age, and location as confounding factors, using state-level estimates.

To estimate age, we'll assume review user ages are uniformly distributed in the range from 18 to 64. And for political data, we extracted 3 age groups from exit polls: 18-29, 30-44, and 45-64. We got the percentage of Democrat and Republican votes for each age group across the 17 states of the dataset.

For each beer preference category (defined in Task 1), we performed causal analysis by matching Democratic and Republican states to minimize propensity score on identified factors to determine whether there is any political association with beer preferences.


![Confounding factors graph](confounding_factors.JPG)


### Task 3. Time Series Analysis of Beer Preferences Over Election Years
We investigated how beer preferences change over time during election years, particularly in swing states, and whether certain beers emerge as an election beer. By analyzing beer reviews from election years and tracking party affiliation changes by state, we’ll explore the popularity of beer styles, using review counts, average ratings, and sentiment analysis. We will also examine the characteristics of an election beer, focusing on its style and the emotions it brings. A time series analysis will determine if these preferences align with election cycles, especially in swing states, and regression methods will help assess any correlation with political shifts, controlling for demographic factors like age and wealth.

## Proposed timeline

- 15.11. Search for Datasets, Data Handling and Preprocessing and Exploratory Data Analysis
- 29.11. Implementation of tasks divided between team members
- 06.12. Initial result analysis, refining methods and combining data stories
- 13.12. Final analysis and website assembly
- 20.12. Final project deadline


## Organization within the team

- Sara: Task 2
- Marija: Task 2
- Luc: Task 3
- David: Task 1
- Mikael: Task 3

Each team member will be responsible for creating the final visualization for their respective task, completing the data story.

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
│   ├── generated                        <- Generated csv/pickle files
│
├── src                         <- Source code
│   ├── data                            <- Data directory (data processing, results stored in data/generated)
│   ├── ipynb scripts                   <- Jupyter Notebooks for analyzing additional datasets
│   ├── models                          <- Model directory
│   ├── utils                           <- Utility directory
│
├── tests                       <- Tests of any kind
│
├── results.ipynb               <- a well-structured notebook showing the results
│
├── .gitignore                  <- List of files ignored by git
├── pip_requirements.txt        <- File for installing python dependencies
└── README.md
```

