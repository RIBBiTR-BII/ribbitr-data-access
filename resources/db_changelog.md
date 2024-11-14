---
title: "ribbitr_db Changelog"
author: "Cob Staines"
format: html
editor: source
---

# Change Log for RIBBiTR_DB

## 2024-11-13

### Changed

- survey.start_time established as natural key (along with survey.visit_id and survey.detection_type)

## 2024-11-07

### Changed

- qpcr_bd_results -> bd_qpcr_results
- location -> country
  - location.location -> country.country_name
- survey
  - survey.percent_vegetation_cover -> survey.vegetation_cover_percent
  - survey.percent_cloud_cover coalesced with survey.cloud_cover_percent and dropped
  
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
    -   survey.observers -> survey.observers_survey
    -   survey.comments -> survey.comments_survey
    -   aural.observer -> aural.observer_aural
    -   aural.count -> aural.count_aural
    -   aural.comments -> aural.comments_aural
    -   capture.observer -> capture.observer_capture
    -   capture.comments -> capture.comments_capture
    -   ves.observer -> ves.observer_ves
    -   ves.count -> ves.count_ves
    -   ves.comments -> ves.comments_ves
    -   visit.comments -> visit.comments_visit

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
