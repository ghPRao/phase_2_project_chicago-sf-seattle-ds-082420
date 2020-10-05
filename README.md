# Table of Contents

### Reports
- [Factors Influencing Homesale Prices in King County Area] (https://github.com/ghPRao/phase_2_project_chicago-sf-seattle-ds-082420/edit/master/notebooks/reports/index.ipynb "Report Notebook")
- [Presentation] (https://github.com/ghPRao/phase_2_project_chicago-sf-seattle-ds-082420/edit/master/reports/King_County_Home_Sales.pdf "Presentation Slides")

### Exploratory Notebooks
- [Data Cleanup] (https://github.com/ghPRao/phase_2_project_chicago-sf-seattle-ds-082420/edit/master/notebooks/exploratory/eda/EDA.ipynb "Data Cleanup and Porch Influence")
- [Influence of Waterfront and Porches on Homesale Price] (https://github.com/ghPRao/phase_2_project_chicago-sf-seattle-ds-082420/edit/master/notebooks/exploratory/eda/andrew_PR_EDA.ipynb "Waterfront and Porches")
- [Influence of Traffic Noise on Homesale Price] (https://github.com/ghPRao/phase_2_project_chicago-sf-seattle-ds-082420/edit/master/notebooks/exploratory/eda/sam_traffic_noise.ipynb "Traffic Noise")
- [Map Visualizations and Location of Housing by Price] (https://github.com/ghPRao/phase_2_project_chicago-sf-seattle-ds-082420/edit/master/notebooks/exploratory/eda/sam_mapping.ipynb "Map Visualizations")

## Analysis
__
The following contians analysis of select factors influencing homesale prices in the King County area. Influences explored in this report include the presence of waterfron ton the property, the existence of enclosed and open porches, and the influence of nuisances on homesale prices.

# Porches
---

Porches are a structure typically located near the front of a building, and are a common sight in numerous houses.  They typically cover the entrance of a house, and come in two main types: enclosed and open porches.  Enclosed porches are more like an extra room in front of the house, as they are surrounded by walls (though they are typically made of glass or screens).  On the other hand, open porches forgo the protection of the walls against the elements and the outside world in return for a more scenic experience to experience the outdoors.  

As they are a popular commodity in many houses, we want to see how the price will change between a house that does have a porch and does not have a porch.

<img src= ../reports/figures/porch_porch_area.png alt="Drawing" style="width: 400px;"/>

In the scatterplot above, we plot both the square feet of the house's enclosed porch area and their open porch area, and then classify their color based on their sale price,  with low-end housing at a gray color and luxury housing at a dark green color.  Common trends we can see are that the number of houses with an enclosed porch area is significantly less than houses with an open porch area.  We can assume this is so because of cheaper material costs as well as open porch areas being more aesthetically pleasing.  Another point we can take is that houses with porch size below 800 square feet, whether it be open porch or enclosed porch, have a wide variety of sale prices.  However the main point is that all houses with a large open porch area, or an open porch area above 800 square feet, are considered expensive housing.  With these points we can analzye that just having a porch does not correlate exactly to a high sale price, but you need a large porch to a certain degree.

<img src= ../reports/figures/porch_ols.png alt="Drawing" style="width: 400px;"/>

To get a rough estimate how much more a potential house owner is looking at paying if they decide that they must have a porch in their home, we will predict it using a very simple FSM.  As the sole feature is whether the home has a porch or not, there is a very small R^2 value and should not be taken as a serious indicator of sale price.

<img src = ../reports/figures/poch_avg_price.png width=400px>

To help visualize the FSM, we will compile the information into a plot.  We can view that on average, if we were looking for a house without a porch, we wil expect to pay around ~\\$650,000 dollars.  However if we attempt to instead look for a house with a porch, we will expect to pay around ~\\$195,000 dollars more.  This comes down to a 30% price increase.  As this exact number should not be taken literally, due to other factors such as porch size and porch materials, it should serve as a good rough estimate for a potential home buyer.

# Waterfront Housing
---

Unlike porches, beachfront and lakefront housing are significantly more rare.  Both are housing that contain access to a lake or beach on their property, and are typically considered a prized commodity due to people's fascination with water.  While normal houses can be built anywhere that there is suitable land, beachfront and lakefront housing requires access to limited space around a body of water, which leads to scarcity and low supply.  To simplify our terminology, we will combine the two phrases beachfront and lakefront into a singular term waterfront.

<img src=../reports/figures/wf_avg_breakdown.png width=400px>

To get a better sense of the difference in price range between different waterfronts, we will take a look at this plot here.  With our non-waterfront price range at the top, it is clear that it is quite limited in comparison to the properties in the other areas.  While not all non-waterfront properties are properly portrayed due to the removal of significant outliers, the majority of the properties in waterfront areas sit at a comfortably higher price range.  We do notice two glaring things that stand out, mainly the areas of Duwamish and Lake Wash.  Duwamish is a noticable case where its price range is significantly lower than all other areas, including non-waterfront properties.  We expect that this is due to the poor ecological state of the Duwamish river due to heavily pollution in the past, which makes it a poor choice to build houses for residential purposes.  On the other side of the spectrum, we have Lake Washington which has ridiculously high housing prices due to the prime real estate.  Many mansions and luxurious homes reside here, including one owned by Bill Gates himself.  As Duwamish and Lake Washington are clearly out of the norm, we will consider them as outliers and not include them unless specifically requested by a customer.

<img src=../reports/figures/wf_ols.png width=400px>

To get a rough estimate how much more a potential house owner is looking at paying if they decide that they must have a waterfront on their property, we will predict it using a very simple FSM.  As the sole feature is whether the home has a waterfront or not, there is a very small R^2 value and should not be taken as a serious indicator of sale price.

<img src = ../reports/figures/wf_avg_price.png width = 400px>

To help visualize the FSM, we will compile the information into a plot. We can view that on average, if we were looking for a house with a waterfront property, we wil expect to pay around ~\\$740,000 dollars. However if we attempt to instead look for a house with a porch, we will expect to pay around ~\\$813,000 dollars more. This is a staggering, ~110% increase in price.  While this exact number should not be taken literally, any potential home buyer should definitely prepare themselves to spend significantly more money if they truly desire a waterfront house.


## Traffic Noise
___

Nuisances come in many varieties. In this study, we focused on the severity of traffic noise and it's influence on homesale prices. In this case, we gave traffic noise three levels of severity, Moderate, High, and Extreme.

<img src = ../reports/figures/presence_nuisance.png width= 400px>

After running what's known as onehotencoding analysis on the data, there was a difference the mean sale value between Moderate and Extreme zones. When comparing Moderate and Extreme traffic noise, we find it has a negative impact on homesale price of over $20,000, or about 4\% of homesale price.


```python

```
