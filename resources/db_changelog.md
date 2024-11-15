---
title: "ribbitr_db Changelog"
author: "Cob Staines"
format: html
editor: source
---

# Change Log for RIBBiTR_DB

## 2024-11-15

### Added

- Pennsylvania survey data through 2024

### Changed

- visit.time_of_day <- visit.survey_time
  - to clarify as descriptor of visit, not of survey
- recalculated survey.duration_minutes, flipping survey.start_time and survey.end_time when duration exceeded 18 hours


## 2024-11-13

### Changed

- survey.start_time established as natural key (along with survey.visit_id and survey.detection_type)

## 2024-11-07

### Changed

- bd_qpcr_results <- qpcr_bd_results 
- country <- location
  - country.country_name <- location.location
- survey
  - survey.vegetation_cover_percent <- survey.percent_vegetation_cover
  - survey.percent_cloud_cover coalesced with survey.cloud_cover_percent, former dropped
  
### Added
- country.iso_country_code

## 2024-10-31

### Changed

- Dropped visits with NULL date
- Created not null constraint on
    - visit.date
    - visit.site_id
    - site.site
    - location.location

## 2024-10-18

### Server maintenance

-   Upgraded postgreSQL engine from version 13.15 to 16.3

## 2024-10-17

### Changed

-   Renamed possibly ambiguous columns in multiple tables in survey_data schema
    -   survey.observers_survey <- survey.observers
    -   survey.comments_survey s<- urvey.comments
    -   aural.observer_aural <- aural.observer
    -   aural.count_aural <- aural.count
    -   aural.comments_aural <- aural.comments
    -   capture.observer_capture <- capture.observer
    -   capture.comments_capture <- capture.comments
    -   ves.observer_ves <- ves.observer
    -   ves.count_ves <- ves.count
    -   ves.comments_ves <- ves.comments
    -   visit.comments_visit <- visit.comments

## 2024-10-11

### Added

-   Unique constraints for natural keys on survey_data schema for the following columns:
    -   location table: location
    -   region table: region
    -   site table: site
    -   survey table: visit_id, detection_type
    -   visit table: site_id, date, survey_time
-   public schema views of all database metadata:
    -   public.all_tables
    -   public.all_columns

## 2024-10-09

### Server maintenance

-   Upgraded postgreSQL engine from version 13.9 to 13.15
-   Updated certificate authority to rds-ca-rsa2048-g1. If connecting to server using SSL, [download certificate bundle here](https://truststore.pki.rds.amazonaws.com/us-west-1/us-west-1-bundle.pem)
-   Set "track_commit_timestamp = on" for easier troubleshooting or and rollbacks
-   Created public schema
-   Enabled extensions postgis and uuid-ossp on public schema

## 2024-10-08

### Added

-   changelog to track and share database changes
-   metadata tables: Metadata to help with documentation, communication of table and column purposes, and automation of data management. Each schema in RIBBiTR_DB now has two metadata tables:
    -   metadata_tables: provides lookup details on each table in the schema. All columns are derived from postgres information_schema.
    -   metadata_columns: provides lookup details on each column in each table in the schema. Some columns are derived from postgres information_schema, others are defined manually (see metadata_columns to see which specific metadata columns are user-defined).

## 2024-10-01

### Server maintenance

-   Set "log_statement = mod" to log all database modifications for accountability and troubleshooting