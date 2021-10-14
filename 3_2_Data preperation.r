require("xtable")

languages = c('Arabic', 'Basque', 'Catalan', 'Chinese', 'Czech', 'English', 'Greek', 'Hungarian', 'Italian', 'Turkish')
data <- lapply(
  languages,
  function (x) read.table(
      paste("./dependency_networks/", x, "_syntactic_dependency_network.txt", sep = ""),
      header = FALSE, quote = "", fill=TRUE)
)

node_counts <- as.integer( unlist(lapply(data, function (x) x[["V1"]][1])) )
edge_counts <- as.integer( unlist(lapply(data, function (x) x[["V2"]][1])) )
mean_degrees <- 2*edge_counts / node_counts
delta <- mean_degrees / (node_counts - 1)

lang_df <- data.frame(language = languages, N = node_counts, E = edge_counts, mean_degrees = mean_degrees, delta = delta)
xtable(lang_df, digits=-3)
