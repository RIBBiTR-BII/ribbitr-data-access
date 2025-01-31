---
title: "ribbitr_db changelog"
author: "Cob Staines"
format: html
editor: source
---

# Change Log for RIBBiTR_DB

## 2025-01-27

## Changed
- reconcile microhabitat column names
  - survey_data.capture.microhabitat_detailed <- survey_data.capture.microhabitat_moredetail
  - survey_data.ves.microhabitat_detailed <- survey_data.ves.microhab_moredetail
  - survey_data.ves.microhabitat_type <- survey_data.ves.microhab
- bd_qpcr_results column name change
  - survey_data.bd_qpcr_results.replicate_detected <- survey_data.db_qpcr_results.replicate_results

## 2025-01-13

### Added

- table: survey_data.taxonomy
  - lookup table for all taxonomy columns which includes corresponding taxon reference IDs in external taxonomy databases (AmphibiaWeb, ITIS, NCBI, GBIF, IUCN), taxon hierarchies and ranks, and other metadata to support analysis accross taxa.
- table: survey_data.lab
  - lookup table for labs corresponding to project data, as well and contacts for consulting, interpreting and seeking permission to use these data for analysis and publication.
- column: survey_data.visit.visit_lab
  - column to track which lab is responsible for field visit data
### Changed
- column names changed from "species" to "taxon" to reflect that some data reflect taxa at higher ranks than species (genus, etc.)
  - survey_data.aural.taxon_aural <- survey_data.aural.species_aural
  - survey_data.capture.taxon_capture <- survey_data.capture.species_capture
  - survey_data.cmr.taxon_cmr <- survey_data.cmr.species_cmr
  - survey_data.ves.taxon_ves <- survey_data.ves.species_ves

## 2025-01-03

### Changed

- lat/lon coordinates calculated for all spatial data
  - site table
    - renamed:
      - site_utme <- utme
      - site_utmn <- utmn
      - site_utm_zone <- utm_zone
      - site_elevation_m <- elevation_m
    - new columns:
      - site_latitude
      - site_longitude
  - environmental table
    - renamed:
      - environmental_utme <- sample_location_utme
      - environmental_utmn <- sample_location_utmn
      - environmental_utm_zone <- sample_location_utm_zone
      - environmental_elevation_m <- sample_location_elevation_m
    - new columns:
        - environmental_latitude
        - environmental_longitude
  - capture table
    - new columns:
      - capture_utm_zone
      - capture_latitude
      - capture_longitude

## 2024-12-13

### Added

- bd qpcr results table updated with qPCR results from Richards-Zawacki lab through December 2023
- created sample table
  - capture_id
  - sample_id
  - sample_name
  - sample_type
      - one of: antibody, amps, bd, bacterial, crispr, genetic, microbiome, mucosome
- microclimate_data schema created with tables:
  - logger
  - sensor
  - time_series_01_raw

### Changed

- added/renamed metadata columns to bd_qpcr_results
  - results_id (unique results identifier)
-   sample_id
  - sample_name_bd <- bd_swab_id
  - replicate_count
  - extraction_plate_name
  - qpcr_plate_name
  - qpcr_well
  - qpcr_plate_run
- dropped sample name columns from capture table, to allow for any number of samples per capture
  - amps
  - amps_2
  - amps_3
  - amps_4
  - antibody
  - antibody_2
  - antibody_3
  - antibody_4
  - bd_swab_id
  - bacterial_swab_id
  - crispr_id
  - genetic_id
  - microbiome_id
  - mucosome_id

## 2024-12-02

### Added

- Panama survey data through October 2024

## 2024-11-25

- created environmental table
  - moved environmental survey data from survey table to environmental table. This includes the following columns:
    - "wind_speed_m_s",
    - "air_temp_c",
    - "water_temp_c",
    - "p_h",
    - "tds_ppm",
    - "wind",
    - "sky",
    - "air_time",
    - "water_time",
    - "samp_loc",
    - "pressure_psi",
    - "dissolved_o2_percent",
    - "salinity_ppt",
    - "cloud_cover_percent",
    - "precip",
    - "soil_humidity_m3m3",
    - "wind_speed_scale",
    - "precipitation_during_visit",
    - "precipitation_last_48_h",
    - "temperature_last_48_h",
    - "weather_condition_notes",
    - "pressure_psi_drop",
    - "relative_humidity_percent",
    - "wind_speed_min_m_s",
    - "wind_speed_max_m_s",
    - "air_temp_c_drop",
    - "densiometer_d1_num_covered",
    - "d1_n",
    - "d1_s",
    - "d1_e",
    - "d1_w",
    - "d1_percent_cover",
    - "densiometer_d2_num_covered",
    - "d2_n",
    - "d2_s",
    - "d2_e",
    - "d2_w",
    - "d2_percent_cover",
    - "depth_of_water_from_d2_cm",
    - "vegetation_cover_percent",
    - "vegetation_notes",
    - "secchi_depth_cm",
    - "conductivity_us_cm",
    - "fish"

## 2024-11-19

### Added

- Pennsylvania survey data through October 2024
- cmr table columns added
  - cmr.species_cmr
  - cmr.site_id_tagged
  - cmr.date_tagged
  - cmr.id_type
- region table
  - region.time_zone

### Changed

- visit.time_of_day \<- visit.survey_time
  - to clarify as descriptor of visit, not of survey
- recalculated survey.duration_minutes, flipping survey.start_time and survey.end_time when duration exceeded 18 hours
- capture.cmr_id \<- capture.capture_mark_recapture
- cmr table
  - cmr.cmr_id \<- cmr.capture_mark_recapture
  - cmr.local_cmr_id \<- cmr.cmr_id

## 2024-11-13

### Changed

- survey.start_time established as natural key (along with survey.visit_id and survey.detection_type)

## 2024-11-07

### Changed

- bd_qpcr_results \<- qpcr_bd_results
- country \<- location
  - country.country_name \<- location.location
- survey
  - survey.vegetation_cover_percent \<- survey.percent_vegetation_cover
  - survey.percent_cloud_cover coalesced with survey.cloud_cover_percent, former dropped
  - survey.relative_humidty_percent coalesced with survey.relative_humidity_percent, former dropped
  - survey.relative_humidity_drop_percent dropped

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

- Upgraded postgreSQL engine from version 13.15 to 16.3

## 2024-10-17

### Changed

- Renamed possibly ambiguous columns in multiple tables in survey_data schema
  - survey.observers_survey \<- survey.observers
  - survey.comments_survey s\<- urvey.comments
  - aural.observer_aural \<- aural.observer
  - aural.count_aural \<- aural.count
  - aural.comments_aural \<- aural.comments
  - capture.observer_capture \<- capture.observer
  - capture.comments_capture \<- capture.comments
  - ves.observer_ves \<- ves.observer
  - ves.count_ves \<- ves.count
  - ves.comments_ves \<- ves.comments
  - visit.comments_visit \<- visit.comments

## 2024-10-11

### Added

- Unique constraints for natural keys on survey_data schema for the following columns:
  - location table: location
  - region table: region
  - site table: site
  - survey table: visit_id, detection_type
  - visit table: site_id, date, survey_time
- public schema views of all database metadata:
  - public.all_tables
  - public.all_columns

## 2024-10-09

### Server maintenance

- Upgraded postgreSQL engine from version 13.9 to 13.15
- Updated certificate authority to rds-ca-rsa2048-g1. If connecting to server using SSL, [download certificate bundle here](https://truststore.pki.rds.amazonaws.com/us-west-1/us-west-1-bundle.pem)
- Set "track_commit_timestamp = on" for easier troubleshooting or and rollbacks
- Created public schema
- Enabled extensions postgis and uuid-ossp on public schema

## 2024-10-08

### Added

- changelog to track and share database changes
- metadata tables: Metadata to help with documentation, communication of table and column purposes, and automation of data management. Each schema in RIBBiTR_DB now has two metadata tables:
  - metadata_tables: provides lookup details on each table in the schema. All columns are derived from postgres information_schema.
  - metadata_columns: provides lookup details on each column in each table in the schema. Some columns are derived from postgres information_schema, others are defined manually (see metadata_columns to see which specific metadata columns are user-defined).

## 2024-10-01

### Server maintenance

- Set "log_statement = mod" to log all database modifications for accountability and troubleshooting
