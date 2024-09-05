import pandas as pd
import csv
import altair as alt
import streamlit as st
import geopandas as gpd
alt.data_transformers.disable_max_rows()

# Reading the dataset
df = pd.read_csv('dfprojecte2.csv')

# Changes to the df

# Creating a new column for the month of the accident
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.strftime('%Y-%m')

# Renaming the column month with their names instead of date
df['Month'] = df[
    'Month'].replace({
    '2018-06': 'June',
    '2018-07': 'July',
    '2018-08': 'August',
    '2018-09': 'September'
})
# Changing from capital letters to lowercase
# Done after visualizing the plots
df['Vehicle Type'] = df['Vehicle Type'].replace({
    'TAXI': 'Taxi',
    'AMBULANCE': 'Ambulance',
    'FIRE': 'Fire'
})
# Creating a new column for the day of the accident
df['Day'] = df['Date'].apply(lambda x: x.isoweekday())

# Renaming the column day with their names instead of number+-
df['Day'] = df['Day'].replace({
    1: 'Monday',
    2: 'Tuesday',
    3: 'Wednesday',
    4: 'Thursday',
    5: 'Friday',
    6: 'Saturday',
    7: 'Sunday'
})
# Creating a new column for the hour of the accident
df["Hour"] = pd.to_datetime(df['Time'], format='%H:%M').dt.hour
# Renaming an attribute after seeing it is too long
df['Contributing factor'] = df['Contributing factor'].replace({
    'Passing or Lane Usage Improper': 'Improper Lane Usage'
})

# PLOTS
data_map = df[["ZipCode", "Borough", "Hour", "Month", "icon", "Day", "Vehicle Type"]].copy()
# selectors
multi_borough = alt.selection_point(fields=['Borough'])
select_hour = alt.selection_interval( encodings=['x'])
multi_vehicle = alt.selection_point(fields=['Vehicle Type'])
multi_day = alt.selection_point(fields=['Day'])
multi_month = alt.selection_point(fields=['Month'])
multi_icon = alt.selection_point(fields=['icon'])

# Plot accidents per borough
bar_borough = alt.Chart(data_map).mark_bar(color = '#328dad').encode(
    x=alt.X('Borough:N', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('count():Q', scale=alt.Scale(domain=[0,2000])),
    tooltip='count():Q',
    opacity=alt.condition(multi_borough, alt.value(1), alt.value(0.4))
).add_params(multi_borough).properties(
    width=450, height=290, title='Number of accidents per borough'
).transform_filter(select_hour).transform_filter(multi_vehicle).transform_filter(multi_day).transform_filter(multi_month).transform_filter(multi_icon)

# Plot accidents per hour
bar_hour= alt.Chart(data_map).mark_area(color = '#328dad',opacity=0.4).encode(
    x=alt.X('Hour:Q', scale=alt.Scale(domain=[0,23])),
    y=alt.Y('count():Q', scale=alt.Scale(domain=[0,220])),
    tooltip=['Hour', 'count()'],
).add_params(select_hour).properties(
    width=400, height=290, title='Number of accidents per hour'
).transform_filter(multi_borough).transform_filter(multi_vehicle).transform_filter(multi_day).transform_filter(multi_month).transform_filter(multi_icon)

bar_hour_top= alt.Chart(data_map).mark_area(color = '#328dad',).encode(
    x=alt.X('Hour:Q', scale=alt.Scale(domain=[0,23])),
    y=alt.Y('count():Q', scale=alt.Scale(domain=[0,220])),
    tooltip=['Hour', 'count()'],
).properties(
    width=400, height=290, title='Number of accidents per hour'
).transform_filter(select_hour).transform_filter(multi_borough).transform_filter(multi_vehicle).transform_filter(multi_day).transform_filter(multi_month).transform_filter(multi_icon)

bar_hour_final=bar_hour+bar_hour_top

# Plot accidents per vehicle
palette_vehicle = alt.Scale(
    domain=['Fire', 'Ambulance', 'Taxi'],
    range=['#fce9a6', '#4a74b4', '#acdfbb']
)

bar_vehicle = alt.Chart(data_map).mark_arc(innerRadius=50).encode(
    theta='count():Q',
    tooltip=['Vehicle Type', 'count()'],
    color=alt.Color('Vehicle Type:N', scale=palette_vehicle),
    opacity=alt.condition(multi_vehicle, alt.value(1), alt.value(0.4))
).add_params(multi_vehicle).properties(
    width=400, height=290, title='Number of accidents per type of vehicle'
).transform_filter(multi_borough).transform_filter(select_hour).transform_filter(multi_day).transform_filter(multi_month).transform_filter(multi_icon)

# Plot accidents per day
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
bar_day = alt.Chart(data_map).mark_bar(color = '#328dad').encode(
    x=alt.X('count():Q', scale=alt.Scale(domain=[0,525])),
    y=alt.Y('Day:N',sort=day_order),
    tooltip=['Day', 'count()'],
    opacity=alt.condition(multi_day, alt.value(1), alt.value(0.4))
).add_params(multi_day).properties(
    width=450, height=290, title='Number of accidents per day'
).transform_filter(multi_borough).transform_filter(select_hour).transform_filter(multi_vehicle).transform_filter(multi_month).transform_filter(multi_icon)

# Plot accidents per month
palette_month = alt.Scale(
    domain=['June', 'July', 'August', 'September'],
    range=['#93d5bd', '#fedd90', '#abd6e8', '#4a74b4']
)
bar_month = alt.Chart(data_map).mark_area().encode(
    x=alt.X('Hour:N', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('count():Q', axis=alt.Axis(title=" "), scale=alt.Scale(domain=[0,70])),
    tooltip=['Month', 'count()'],
    opacity=alt.condition(multi_month, alt.value(1), alt.value(0.4)),
    color=alt.Color('Month:N', scale=palette_month),
    row=alt.Row("Month:N").sort(['June', 'July', 'August', 'September'])
).add_params(multi_month).properties(
    width=600, height=80, title='Number of accidents per month'
).transform_filter(multi_borough).transform_filter(select_hour).transform_filter(multi_vehicle).transform_filter(multi_day).transform_filter(multi_icon)

# Plot accidents per weather condition
bar_icon = alt.Chart(data_map).mark_bar(color = '#328dad').encode(
    x=alt.X('icon:N', axis=alt.Axis(title="Weather condition", labelAngle=0)),
    y=alt.Y('count():Q', scale=alt.Scale(domain=[0,2200])),
    tooltip=['icon', 'count()'],
    opacity=alt.condition(multi_icon, alt.value(1), alt.value(0.4))
).add_params(multi_icon).properties(
    width=450, height=290, title='Number of accidents per weather condition'
).transform_filter(multi_borough).transform_filter(select_hour).transform_filter(multi_vehicle).transform_filter(multi_day).transform_filter(multi_month)


# Choropleth map showing total accidents
url_c = 'https://gist.githubusercontent.com/AndreaTomas00/961de0242315af50dab7038186dcde0b/raw/f8a8085082ee844414694ab89c24c57bd51e3767/boroughs.geojson'
county_map = alt.Data(url=url_c, format=alt.DataFormat(property="features"))
data_map['Count'] = 1 #adding this column to be able to perform the addition in the groupby
url_zc = 'https://raw.githubusercontent.com/fedhere/PUI2015_EC/master/mam1612_EC/nyc-zip-code-tabulation-areas-polygons.geojson'
gdf_zc = alt.Data(url=url_zc, format=alt.DataFormat(property="features"))
c_base = alt.Chart(county_map).mark_geoshape(
    fill='lightgrey',
    tooltip=True
).interactive().project("mercator").properties(height=600, width=500)
zc_base = alt.Chart(gdf_zc).mark_geoshape(
    stroke='grey',
    fill='lightgrey',
    opacity = 0.6,
    tooltip=False
)
blue_scale = alt.Scale(scheme='greenblue', domain=[0, 2000])
c_map = alt.Chart(data_map).mark_geoshape(stroke='black').transform_filter(multi_day).transform_filter(select_hour).transform_filter(multi_vehicle).transform_filter(
    multi_month).transform_filter(multi_icon).transform_aggregate(
    Accidents='sum(Count)',
    groupby=['Borough']
).interactive().transform_lookup(
    lookup='Borough',
    from_=alt.LookupData(county_map, key='properties.name', fields=['geometry', 'type', 'properties'])
).encode(
    color= alt.Color('Accidents:Q', title="Num accidents", scale=blue_scale),
    opacity=alt.condition(multi_borough, alt.value(0.8), alt.value(0)),
    tooltip = ['Borough:N', 'Accidents:Q'],
).project('mercator')


final_vis = alt.vconcat(alt.hconcat(alt.layer(c_base, zc_base, c_map).properties(title="Distribution of accidents by borough"), bar_day, bar_month).resolve_legend(color = "independent", size = "independent").resolve_scale(
    color = "independent"), alt.hconcat(bar_hour_final, bar_icon, bar_vehicle, bar_borough)).configure_title(fontSize=20).configure_axis(
    titleFontSize=16,
    labelFontSize=12
).configure_header(
    titleFontSize=16,
    labelFontSize=14
).configure_legend(
    titleFontSize=16,
    labelFontSize=14
).resolve_legend(color = "independent", size = "independent").resolve_scale(color = "independent")
st.set_page_config(
    page_title = "VI - Projecte 2",
    layout = "wide"
)
st.altair_chart(final_vis)