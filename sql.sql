CREATE SCHEMA `link_short` DEFAULT CHARACTER SET utf8 ;

CREATE TABLE `link_short`.`link_short` (
  `idlink_short` INT NOT NULL AUTO_INCREMENT,
  `DateCreat` VARCHAR(45) NULL,
  `Link` VARCHAR(145) NULL,
  `LinkShort` VARCHAR(45) NULL,
  `User` VARCHAR(45) NULL,
  `linkscol` VARCHAR(45) NULL,
  PRIMARY KEY (`idlink_short`));


CREATE TABLE `link_short`.`users` (
  `idusers` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `password` VARCHAR(145) NULL,
  PRIMARY KEY (`idusers`));
  
  INSERT INTO `link_short`.`users` (name, password) VALUES ('evgen', '202cb962ac59075b964b07152d234b70') 