CREATE DATABASE Hospital;
USE Hospital;


/* Creating and loading in tables */
CREATE TABLE hospital_visits(Encounter_ID BIGINT(50), 
                        Length_of_stay BIGINT(50),
                        Primary Key (Encounter_ID));



LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/hospital_visits10000.csv'
INTO TABLE hospital_visits
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

CREATE TABLE patients(Visit_ID BIGINT(50), 
                        Patient_ID BIGINT(50),
                        Race VARCHAR (250),
                        Gender VARCHAR (250),
                        Age BIGINT (50),
                        Primary Key (Patient_ID));



CREATE TABLE medication(Patient_Prescribed_ID BIGINT(50), 
                        Num_medications BIGINT (50),
						Num_diagnoses BIGINT (50),
                        DiabetesMed VARCHAR (250),
                        Primary Key (Patient_Prescribed_ID));
                        
CREATE TABLE admission_info(Visit_IDs BIGINT(50), 
                        Admission_type VARCHAR (100),
                        Discharge_disposition VARCHAR (255),
                        Admission_source VARCHAR (255),
                        Primary Key (Visit_IDs));

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/medication10000.csv'
INTO TABLE medication
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Admission_Info.csv'
INTO TABLE admission_info
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

CREATE TABLE procedures(Visit_ID BIGINT(50), 
                       Procedure_Type VARCHAR (250),
                        Primary Key (Visit_ID));

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Procedures10000.csv'
INTO TABLE procedures
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Patients10000.csv'
INTO TABLE patients
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

/* Adding Foreign key constraints */


/* Foreign key from patients to hospital visits */
ALTER TABLE `hospital`.`patients` 
ADD INDEX `Visit_idx` (`Visit_ID` ASC) VISIBLE;
;
ALTER TABLE `hospital`.`patients` 
ADD CONSTRAINT `Visit`
  FOREIGN KEY (`Visit_ID`)
  REFERENCES `hospital`.`hospital_visits` (`Encounter_ID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;
  
  /* Foreign key from hospital visits to admission info */
  
  ALTER TABLE `hospital`.`admission_info` 
ADD CONSTRAINT `Visit1`
  FOREIGN KEY (`Visit_IDs`)
  REFERENCES `hospital`.`hospital_visits` (`Encounter_ID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;
  
  
  /* Foreign key from patients to medication */
ALTER TABLE `hospital`.`medication` 
ADD CONSTRAINT `Patient_Prescribed`
  FOREIGN KEY (`Patient_Prescribed_ID`)
  REFERENCES `hospital`.`patients` (`Patient_ID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;
  
   /* Foreign key from hospital visits to procedures*/
   ALTER TABLE `hospital`.`procedures` 
ADD CONSTRAINT `Visit2`
  FOREIGN KEY (`Visit_ID`)
  REFERENCES `hospital`.`hospital_visits` (`Encounter_ID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;


/* Queries from checkpoint 4 */
Select p.Patient_ID, p.Age
 from patients p, procedures pr 
 WHERE p.Visit_ID=pr.Visit_ID AND pr.Procedure_Type='Cardiology\r';
 
Select p.Patient_ID, p.Gender,p.Race
 from patients p, procedures pr 
 WHERE p.Visit_ID=pr.Visit_ID AND pr.Procedure_Type='Cardiology\r'; 
 
 
Select * from Procedures;
Select * from Hospital_visits;
Select age,race from Patients;


/*create USER 'remote_user'@'localhost' identified WITH mysql_native_password BY 'pass123';
GRANT ALL PRIVILEGES ON hospital.* TO 'remote_user'@'localhost'; */


/*average num of medications used by diabetic patients vs non-diabetic patients */

SELECT AVG(m.Num_medications),m.DiabetesMed
FROM medication m
GROUP BY m.DiabetesMed;




/*
visit count of each type of admission source */

SELECT h.Admission_source,COUNT(*) as count
FROM admission_info h
GROUP BY h.Admission_source
ORDER BY count DESC;

/* stored procedures */
CALL AvgNumMedsByDiabetes;
call EmergencyAdmission;
call SelectAllPatients;

call VisitCountAdSource;





