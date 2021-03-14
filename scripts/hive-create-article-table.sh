

CREATE TABLE IF NOT EXISTS article (`date` Timestamp, category String, press String, title String, content String) COMMENT "Article storage" ROW FORMAT DELIMITED FIELDS TERMINATED BY "\t" LINES TERMINATED BY "\n" STORED AS TEXTFILE;