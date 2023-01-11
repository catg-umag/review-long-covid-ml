library(tidyverse)
library(circlize)


df <- read.csv("long_covid_sym.csv") %>%
  mutate(Observation = ifelse(Observation == "Has U09.9 in Record", "Tested positive", Observation)) %>%
  filter(
    Age != "Unknown",
    Sex != "unknown"
  ) %>%
  select(-Ethnicity, -Race) %>%
  group_by(Observation, Age, Sex, Symptom) %>%
  summarize(patient_count = sum(patient_count)) %>%
  mutate(Symptom = as.factor(Symptom)) %>%
  ungroup()


categories <- df %>%
  group_by(Observation, Age) %>%
  summarize(n = sum(patient_count)) %>%
  unite("category", -n, sep = ":")
# custom order
categories <- c(
  "Has not tested positive:<18", "Has not tested positive:18-64", "Has not tested positive:65+",
  "Tested positive:65+", "Tested positive:18-64", "Tested positive:<18"
)

labels <- list(
  "Fatigue" = "F",
  "Mental Health Condition" = "MHC",
  "Shortness of breath" = "SoB"
)


make_plot <- function() {
  circos.par(start.degree = 85, gap.degree = c(0, 0, 10, 0, 0, 10))
  circos.initialize(categories, xlim = c(0, 6))

  # highlights
  draw.sector(95, -95, clock.wise = FALSE, rou1 = 0.3, rou2 = 0.22, col = "#b8e0e9bb", border = NA)
  draw.sector(-85, 85, clock.wise = FALSE, rou1 = 0.3, rou2 = 0.22, col = "#b5e5dabb", border = NA)

  # barplots
  circos.track(
    categories,
    ylim = c(0, 1300000),
    bg.border = NA, track.height = 0.65, track.margin = c(0, 0),
    panel.fun = function(x, y) {
      variables <- unlist(strsplit(CELL_META$sector.index, ":"))
      colors <- c("#f5b3b3", "#b1b2f5")

      subdf <- df %>%
        filter(Observation == variables[1], Age == variables[2])

      if (variables[1] == "Has not tested positive") {
        subdf <- subdf %>% arrange(Symptom, Sex)
      } else {
        subdf <- subdf %>% arrange(desc(Symptom), desc(Sex))
        colors <- rev(colors)
      }

      max_counts <- subdf %>%
        group_by(Symptom) %>%
        summarise(patient_count = max(patient_count))

      circos.barplot(
        subdf$patient_count,
        c(1.1, 1.9, 3.1, 3.9, 5.1, 5.9) - 0.5,
        col = colors,
        border = NA, bar_width = 0.8
      )
    }
  )

  circos.track(
    categories,
    ylim = c(0, 1),
    bg.border = NA, track.height = 0.03, cell.padding = c(0, 0), track.margin = c(0, 0),
    panel.fun = function(x, y) {
      variables <- unlist(strsplit(CELL_META$sector.index, ":"))
      colors <- c("#518b96", "#ff7879", "#ebdb74")

      if (variables[1] == "Tested positive") {
        colors <- rev(colors)
      }

      circos.barplot(
        c(1, 1, 1),
        c(1, 3, 5),
        col = colors,
        border = NA, bar_width = 1.8
      )
    }
  )

  # age text
  circos.track(categories,
    ylim = c(0, 1), bg.border = NA, track.height = 0.1,
    panel.fun = function(x, y) {
      variables <- unlist(strsplit(CELL_META$sector.index, ":"))
      circos.text(3, 0.5, variables[2], niceFacing = TRUE, cex = 0.75)
    }
  )

  circos.track(categories,
    ylim = c(0, 1), bg.border = NA, track.height = 0.16
  )

  # observation text
  highlight.sector(categories[1:3],
    track.index = 4, col = NA, text = "Not\ntested",
    facing = "clockwise", niceFacing = TRUE, text.vjust = 0.5, cex = 0.8
  )
  highlight.sector(categories[4:6],
    track.index = 4, col = NA, text = "Tested\npositive",
    facing = "clockwise", niceFacing = TRUE, text.vjust = 0.5, cex = 0.8
  )

  circos.clear()
}


# plot and save
pdf("Figure4.pdf")
par(mar = c(0, 0, 0, 0))
make_plot()
dev.off()
