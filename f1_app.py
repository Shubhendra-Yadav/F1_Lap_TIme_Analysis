import pandas as pd
import numpy as np
import streamlit as st
import pickle
import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import seaborn as sns


# loading the years list
years = []
for i in range(2023, 2025, 1):
    years.append(i)

# setting the title
st.title("F1 Lap Time Analysis")

# selecting the year for the season
selected_season = st.selectbox(
    "Select the F1 Season:",
    years
)

# selecting the race from the season
schedule = fastf1.get_event_schedule(selected_season)
schedule = pd.DataFrame(schedule)
races = schedule['EventName']

selected_race = st.selectbox(
    "Select the race:",
    races
)

# loading the drivers in the race
session = fastf1.get_session(selected_season, str(selected_race), 'R')
session.load()
drivers = pd.DataFrame(session.results['FullName'])

# selecting the drivers
compare_drivers = st.multiselect(
    "Select drivers to view lap times:",
    drivers,
)
fig, ax = plt.subplots(figsize=(8, 8))

# get the driver number for lap times
for i in compare_drivers:
    driver_number = drivers.index[drivers['FullName'] == i]
    driver_number = int(driver_number[0])
    driver_number

    # lap times of the drivers
    driver_laps = session.laps.pick_drivers(driver_number).pick_quicklaps().reset_index()
    
    fastf1.plotting.setup_mpl(mpl_timedelta_support=True, misc_mpl_mods=False, color_scheme='fastf1')

    ax.plot("LapNumber", "LapTime", '--o', data=driver_laps, label=driver_number)
    
    ax.invert_yaxis()
    ax.legend()
    # ax.invert_yaxis() #####can't figure out the need to invert y-axis twice.#####
    
    plt.xlabel("Lap Number")
    plt.ylabel("Lap Time")
    plt.title(f"{selected_race} - {selected_season}")
    plt.tight_layout()


if st.button("Generate Lap Times Plot", type="primary"):
    st.pyplot(fig)