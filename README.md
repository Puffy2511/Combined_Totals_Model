
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

You then use the 





