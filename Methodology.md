# Summary
This is a side project that presents a framework for pricing “Combined Total” player disposals markets (specifically in AFLM). 
By extracting implied probability parameters from player props from Pointsbet via TheOdds API , the model fits a joint Normal distribution to estimate the probability of two players reaching a certain disposal threshold. 
The system includes Monte Carlo simulations of wealth using Kelly staking to evaluate long term expectancy and risk adjusted returns of taking multiple bets in this market. 

# Background
I used to do EV betting, which would involve calculating the “true” odds of a bet and deciding whether it would benefit me in the long run. 
One of the markets these bets would include were combined totals, eg) “Player A and Player B to combine for X goals/points/disposals” which after asking another member, were found to be “impossible” to calculate (but approximated via rule of thumb). 

# Methodology
## Preprocessing and Devigging
The model scrapes real time data for upcoming matches via The Odds API, specifically Pointsbet (chosen arbitrarily). 

The API returns a JSON file which we then merge both “player_disposals” and “player_disposals_over” to create a probability map to each individual player. 

However, before you can fit a distribution, we note that we first have to remove the “vig” (vigorish) on the returned odds in order to get the “true” odds. 
Bookmakers bake [margins](https://www.aussportsbetting.com/guide/betting-agencies/bookmaker-margins/) into betting lines which is why punters lose money over the long run. 
A typical example would be a bookmaker pricing a coin flip at (1.91) instead of (2.00). The difference in the bookmaker odds and true odds is their profit margin. 

Standard devigging methods are under the assumption that bookmakers employ a linear margin across lines however it 
ignores the fact that higher risk premiums are applied to longshots as a result of [Favourite Longshot Bias](https://www.championbets.com.au/betting-academy-article/favourite-longshot-bias).
We assume that there must be some exponent factor which converts between bookmaker and true odds, implying that it would have the same effect on the true probability:

$$P_{fair} = (P_{implied})^k$$

To solve for this power, we refer back to a fixed anchor. We assume that the O/U line represents the exact middle $P_{o/u} = 0.5$. You can then solve for the exponent k via the O/U market odds ($Odds_{o/u}$):

$$ k = \dfrac{ln(0.5)}{ln(1/Odds_{o/u})} $$

## Parametric Calculations

We assume that the final count of disposals for each player follows a [Normal Distribution](https://en.wikipedia.org/wiki/Normal_distribution) $N(\mu\,\sigma\)$. Using the scraped data, we convert the disposals and their "true" implied probability into coordinates. 

1. $\mu\$ represents the player's O/U line 
2. $\sigma\$ is solved via [Least Square Optimisation](https://en.wikipedia.org/wiki/Least_squares) . This focuses on minimising the residual sum of squares between a theoretical Normal CDF and the devigged market data. :

 $$\min \sum_{i=1}^{n} (\Phi(x_i | \mu, \sigma) - P_{fair,i})^2$$

 However, on the off case where a player didn't have a O/U line or there wasn't enough data points, the standard deviation of a player's disposals would be calculated as a scalar multiple of the mean.
 To calculate this coefficient, we use the FitzRoy library and scrape data across the last three seasons. We then group by player name and use the built in R commands to calculate an average of ratios between a player's standard deviation of player disposals and their mean. 
 This comes out to about 0.3203 ( note that we filter players based on games played and if they are midfielder as those yield more accurate results). But to summarise, if there isn't enough data, we assume:

 $$\sigma\ = 0.3203 * \mu\$$ 
<p align = "center">
 <img src = "Images/image_2026-08-28_183037089.png" height = 400>
</p>

## Final Total Distribution

The sum of two R.Vs X and Y which are normally distributed, should also be normally distributed with parameters (see [Proof](https://en.wikipedia.org/wiki/Sum_of_normally_distributed_random_variables)):

  $$\mu_{total}\ = \mu_{X}\ +\mu_{Y}\$$  
  $$\sigma_{total} = \sqrt{\sigma_X^2 + \sigma_Y^2 + 2\rho\sigma_X\sigma_Y}$$
  
Player performances are correlated simply because they share the same ball. Once again, the FitzRoy library was used to scrape data from the last 3 seasons. Using built in R functions, we are able to calculate the correlation in disposals between two players which is further filtered by a minimum amount of games they are required to play together to reduce outliers.

This model would then output the probability of hitting 'X' disposals, which you can calculate the "true" odds by taking the reciprocal.

<p align = "center">
 <img src = "Images/image_2026-08-28_184919166.png" height = 400>
</p>

# Motivation

The point of this model is to evaluate whether or not a bet is worth taking. On occasion, some bookmakers do offer combined totals:

<p align = "center">
 <img src = "Images/image_2026-08-28_185616191.png" height = 200>
 <img src = "
</p>


 












