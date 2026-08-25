
library(tidyverse)
library(fitzRoy)

seasons = c(2024,2025,2026)

data = fetch_player_stats(season = 2025,source = "fryzigg")

data = seasons %>%
  map_df(~fetch_player_stats(season = .x, source = "fryzigg"))

data = data %>%
  mutate(full_name = paste(player_first_name,player_last_name, sep = " " ))

calc_corr = function(dataset, p1,p2){
  
  correlation_data = dataset %>%
    filter(full_name %in% c(p1,p2))%>%
    group_by(match_date,full_name) %>%
    summarise(disposals = sum(disposals, na.rm = TRUE), .groups = "drop")%>%
    pivot_wider(names_from = full_name, values_from = disposals) %>%
    drop_na()
  
  print(paste("Shared Games: ",nrow(correlation_data)))
  
  if(nrow(correlation_data) < 5){
    return(-0.1)
  }
    
  correlation = cor(correlation_data[[p1]], correlation_data[[p2]])
  
  return(correlation)
}

test1 = calc_corr(data,"Nick Daicos","Jack Ginnivan")
test2 = calc_corr(data, "Nick Daicos", "Josh Worrell")
test3 = calc_corr(data, "Izak Rankine", "Josh Rachele")
test4 = calc_corr(data, "Noah Anderson","Max Gawn")

print(test1)
print(test2)
print(test3)
print(test4)