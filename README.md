
# Pints & Politics: Analyzing Beer Preferences Across U.S. States

## Abstract

The US election season is back! This is the time to explore how cultural habits intersect with political identities. With an annual consumption of around 100L/person, beer is central to American culture.
But what exactly are they drinking? What aspects of a beer are composing a beer preference (only the taste? the alcohol percentage?) What are their preferences, and do they vary by state? Could these differences align with political divisions?
The beer review dataset is ideal for our investigation because it includes user-generated ratings from all around the US. Coupled with data on political opinions (vote statistics, surveys,...), we can search for correlations between beer preferences and political position. NLP techniques such as sentiment analysis, can reveal if reviews in a state exhibit higher variance and therefore correspond to a "swing state".
By analyzing beer preferences over time—using more than 15 years of reviews—there is opportunity to examine shifts in tastes and determine if political context influence beer culture in the US.

## Research Questions

1. How do beer preferences vary across different U.S. states, and can these preferences be linked to political ideologies?
2. Are there specific beer styles (e.g., IPAs, lagers, stouts) that correlate with Republican or Democratic voting patterns?
3. How does the sentiment in beer reviews vary across regions with different political leanings?

## Proposed additional datasets

### 1. President Dataset

> MIT Election Data and Science Lab, 2017, "U.S. President 1976–2020", https://doi.org/10.7910/DVN/42MVDX, Harvard Dataverse, V8; 1976-2020-president.tab

This dataset contains results of presidental elections (number of votes per each candidate) per state from 1976 to 2020.

After analyzing the dataset, we first assessed its completeness. We found that it includes data for all 51 states for each year, with no missing or empty values. For our analysis, we will use only a subset of this dataset, focusing on the entries from 2001 to 2017, specifically the election years 2004, 2008, 2012, and 2016, to align with the beer reviews we have.


> some ideas on how you expect to get, manage, process, and enrich it/them. Show us that you’ve read the docs and some examples, and that you have a clear idea on what to expect. Discuss data size and format if relevant. It is your responsibility to check that what you propose is feasible.

This dataset has the advantage to be quite lightweight (501KB CSV file with 4288) and easy to manipulate.
Our first idea to play with this dataset is to calculate some statistics.

First, we were interested in the proportion of votes for each party per state over the years.
Then we were curious to evaluate what are the "swing" states this dataset would give. 

### 2. Another dataset???

## Methods

## Proposed timeline

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

