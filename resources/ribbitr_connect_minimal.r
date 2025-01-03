# install and load "librarian" R package
install.packages("librarian")
# minimal packages for establishing RIBBiTR DB connection
librarian::shelf(tidyverse, dbplyr, RPostgres, DBI, RIBBiTR-BII/ribbitrrr)
# establish database connection
dbcon <- hopToDB("ribbitr")
