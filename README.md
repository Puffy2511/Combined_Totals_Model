
## About
Model that calculates the implied probability and true odds of player A and player B to combine for 'X' disposals (in AFLM), based off bookmaker odds.

<p align = "center">
  <img src = "https://github.com/Puffy2511/Combined_Totals_Model/blob/e8331cd92d7be84300eae3c395605f41ebac2c0c/image_2026-08-27_200114594.png" width = "500">
</p>
  
## Features

| Feature                     | Description                                                                                  |
|-----------------------------|----------------------------------------------------------------------------------------------|
| **Devig Function**      | Power method devigging to remove favourite-longshot bias |
| **Individual Player Modelling**      | Uses bookmaker lines and least squares optimisation to fit individual player models |
| **Customisable Monte Carlo Risk Simulation**      | Includes modifiable parameters such as controlling Kelly portion and test odds |

## Example
This example uses this model to calculate the true odds and probability of the offer above (Nick and Josh Daicos to combine for 70+ disposals)

The model scrapes Pointsbet and returns upcoming AFL matches. You choose the indice corresponding to whatever game. 

<img src = "Images/image_2026-08-27_212435209.png">

You can use the [View Correlation Calculator](Correlation%20Calculator.R) to calculate the historical correlation between player A and player B 

<img src = "Images/image_2026-08-27_213014948.png">

Select player A and B via indices as well as a target total to hit. The model outputs their individual distributions as well as their joint distributions (assumed both to be Normal). 
The model also returns the fair odds and implied probability of the event occurring. 

<img src = "Images/image_2026-08-27_203026470.png">

You can also choose to run risk simulations with parameters based on the previous probabilities. Parameters include a starting bankroll, payout odds, number of bets, number of simulations and Kelly proportion. The model outputs the expected final wealth, EV per bet for $1 stake, Average max drawdown and the sharpe ratio.

<img src = "Images/image_2026-08-27_203046732.png">

## Visualisations

Joint Normal Distribution for Player A and B
<p align = "center">
  <img src = "Images/image_2026-08-27_203056452.png">
</p>

Monte Carlo simulations on $1000 bankroll across 1000 bets with 50 simulations at Tab odds
<p align = "center">
  <img src = "Images/image_2026-08-27_203105781.png" height = "400">
</p>  

Monte Carlo simulations on a $1000 bankroll across 1000 bets with 50 simulations at boosted odds
