
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

