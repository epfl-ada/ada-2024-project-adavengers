import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_beer_pref_trends(beer_ratings, states):
    """ For the specified states plot beer trends for each beer styles. """
    styles = ['IPA', 'Lager', 'Other Ale', 'Pale Ale', 'Pilsner', 'Porter', 'Red/Amber Ale', 'Stout']
    year_list = list(np.arange(2004, 2017, 1, dtype=int))

    # Identify the states of interest
    states_interest = beer_ratings.loc[states]

    # Create grid for plotting 
    _, axes = plt.subplots(4, 2, figsize=(12, 14))
    axes = axes.flatten()

    for i, style in enumerate(styles):
        
        # Set the ax where we are plotting
        ax = axes[i]
        
        # Identify the styles
        style_names = [f"{style}_{year}" for year in year_list]
        beer_styles = states_interest[style_names]
        
        for index, row in beer_styles.iterrows():
            ax.plot(year_list, row, label=f"{index}")
            
        ax.set_title(f"Trend in average ratings of {style} beer preferences")
        ax.set_xlabel('Years')
        ax.set_ylabel('Average ratings')
        ax.legend(title='States', fontsize=8, loc='upper left')
        ax.grid(True)
        
    # Adjust layout
    plt.tight_layout()
    plt.show()