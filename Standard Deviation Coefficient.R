
library(tidyverse)
library(fitzRoy)

seasons = c(2024,2025,2026)

data = seasons %>%
  map_df(~fetch_player_stats(season = .x))

cleaned_data = data %>%
  
  group_by(player.givenName)%>%
  summarise(
    games_played = n(),
    avg_disposals = mean(disposals,na.rm = TRUE),
    sd_disposals = sd(disposals, na.rm = TRUE)
  ) %>%
  
  filter(games_played >=5, avg_disposals >= 18)%>%
  mutate(sd_coef = sd_disposals/avg_disposals)

Std_dev_coef = mean(cleaned_data$sd_coef)

print(paste("Std Dev Coefficient(Midfielders) 2024-2026: ", round(Std_dev_coef,4)))


ggplot(cleaned_data, aes(x = avg_disposals, y = sd_disposals)) + 
  geom_point(alpha = 0.5)+
  geom_abline(slope = Std_dev_coef, intercept = 0, color = "red")+
  labs(title = "AFL Disposals: Mean vs Standard Deviation", x = "Mean Disposals", y = "Standard Deviation",
       subtitle = paste("Slope of the line is historical std_coef avg:", round(Std_dev_coef,4)))+
  theme_minimal()
  