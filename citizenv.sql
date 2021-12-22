-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 21, 2021 at 04:55 PM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 8.1.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `citizenv`
--
CREATE DATABASE IF NOT EXISTS `citizenv` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `citizenv`;

-- --------------------------------------------------------

--
-- Table structure for table `account`
--

DROP TABLE IF EXISTS `account`;
CREATE TABLE IF NOT EXISTS `account` (
  `accountId` varchar(100) NOT NULL,
  `password` varchar(10000) NOT NULL,
  `email` varchar(1000) DEFAULT NULL,
  `roleId` int(10) NOT NULL,
  `managerAccount` varchar(100) DEFAULT NULL,
  `startDate` date DEFAULT NULL,
  `endDate` date DEFAULT NULL,
  `isLocked` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`accountId`),
  KEY `fk_account_account` (`managerAccount`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `citizen`
--

DROP TABLE IF EXISTS `citizen`;
CREATE TABLE IF NOT EXISTS `citizen` (
  `CCCD` varchar(12) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `DOB` date NOT NULL,
  `sex` enum('Nam','Nu') NOT NULL,
  `maritalStatus` enum('Chua ket hon','Da ket hon','Ly hon','') NOT NULL,
  `nation` varchar(50) NOT NULL,
  `religion` varchar(50) NOT NULL,
  `permanentResidence` varchar(100) DEFAULT NULL,
  `temporaryResidence` varchar(100) DEFAULT NULL,
  `educationalLevel` varchar(10) DEFAULT NULL,
  `job` varchar(50) DEFAULT NULL,
  `cityProvinceId` varchar(2) NOT NULL,
  `districtId` varchar(4) NOT NULL,
  `wardId` varchar(6) NOT NULL,
  `groupId` varchar(8) NOT NULL,
  PRIMARY KEY (`CCCD`),
  KEY `fk_citizen_cityprovince` (`cityProvinceId`),
  KEY `fk_citizen_district` (`districtId`),
  KEY `fk_citizen_ward` (`wardId`),
  KEY `fk_citizen_residentialgroup` (`groupId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `cityprovince`
--

DROP TABLE IF EXISTS `cityprovince`;
CREATE TABLE IF NOT EXISTS `cityprovince` (
  `cityProvinceId` varchar(2) NOT NULL,
  `cityProvinceName` varchar(30) NOT NULL,
  `completed` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`cityProvinceId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `district`
--

DROP TABLE IF EXISTS `district`;
CREATE TABLE IF NOT EXISTS `district` (
  `districtId` varchar(4) NOT NULL,
  `districtName` varchar(30) NOT NULL,
  `cityProvinceId` varchar(2) NOT NULL,
  `completed` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`districtId`),
  KEY `fk_district_cityprovince` (`cityProvinceId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Triggers `district`
--
DROP TRIGGER IF EXISTS `updateCompletedDistrict`;
DELIMITER $$
CREATE TRIGGER `updateCompletedDistrict` AFTER UPDATE ON `district` FOR EACH ROW BEGIN 
	DECLARE countCompleted INT DEFAULT 0;
    DECLARE total INT DEFAULT 0;
    SELECT COUNT(*) INTO countCompleted FROM district WHERE cityProvinceId = new.cityProvinceId AND completed = 1;
    SELECT COUNT(*) INTO total FROM district WHERE cityProvinceId = new.cityProvinceId;
    IF total = countCompleted THEN
    	UPDATE cityprovince SET cityprovince.completed = 1 WHERE cityprovince.cityProvinceId = new.cityProvinceId;
    ELSEIF total > countCompleted THEN
    	UPDATE cityprovince SET cityprovince.completed = 0 WHERE cityprovince.cityProvinceId = new.cityProvinceId;
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `file`
--

DROP TABLE IF EXISTS `file`;
CREATE TABLE IF NOT EXISTS `file` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `data` mediumblob NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `residentialgroup`
--

DROP TABLE IF EXISTS `residentialgroup`;
CREATE TABLE IF NOT EXISTS `residentialgroup` (
  `groupId` varchar(8) NOT NULL,
  `groupName` varchar(30) NOT NULL,
  `wardId` varchar(6) NOT NULL,
  PRIMARY KEY (`groupId`),
  KEY `fk_residentialgroup_ward` (`wardId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `revoked_tokens`
--

DROP TABLE IF EXISTS `revoked_tokens`;
CREATE TABLE IF NOT EXISTS `revoked_tokens` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `jti` varchar(120) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `ward`
--

DROP TABLE IF EXISTS `ward`;
CREATE TABLE IF NOT EXISTS `ward` (
  `wardId` varchar(6) NOT NULL,
  `wardName` varchar(30) NOT NULL,
  `districtId` varchar(4) NOT NULL,
  `completed` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`wardId`),
  KEY `fk_ward_district` (`districtId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Triggers `ward`
--
DROP TRIGGER IF EXISTS `updateCompletedWard`;
DELIMITER $$
CREATE TRIGGER `updateCompletedWard` AFTER UPDATE ON `ward` FOR EACH ROW BEGIN 
	DECLARE countCompleted INT DEFAULT 0;
    DECLARE total INT DEFAULT 0;
    SELECT COUNT(*) INTO countCompleted FROM ward WHERE districtId = new.districtId AND completed = 1;
    SELECT COUNT(*) INTO total FROM ward WHERE districtId = new.districtId;
    IF total = countCompleted THEN
    	UPDATE district SET district.completed = 1 WHERE district.districtId = new.districtId;
    ELSEIF total > countCompleted THEN
    	UPDATE district SET district.completed = 0 WHERE district.districtId = new.districtId;
    END IF;
END
$$
DELIMITER ;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `citizen`
--
ALTER TABLE `citizen`
  ADD CONSTRAINT `fk_citizen_cityprovince` FOREIGN KEY (`cityProvinceId`) REFERENCES `cityprovince` (`cityProvinceId`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_citizen_district` FOREIGN KEY (`districtId`) REFERENCES `district` (`districtId`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_citizen_residentialgroup` FOREIGN KEY (`groupId`) REFERENCES `residentialgroup` (`groupId`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_citizen_ward` FOREIGN KEY (`wardId`) REFERENCES `ward` (`wardId`) ON UPDATE CASCADE;

--
-- Constraints for table `district`
--
ALTER TABLE `district`
  ADD CONSTRAINT `fk_district_cityprovince` FOREIGN KEY (`cityProvinceId`) REFERENCES `cityprovince` (`cityProvinceId`) ON UPDATE CASCADE;

--
-- Constraints for table `residentialgroup`
--
ALTER TABLE `residentialgroup`
  ADD CONSTRAINT `fk_residentialgroup_ward` FOREIGN KEY (`wardId`) REFERENCES `ward` (`wardId`) ON UPDATE CASCADE;

--
-- Constraints for table `ward`
--
ALTER TABLE `ward`
  ADD CONSTRAINT `fk_ward_district` FOREIGN KEY (`districtId`) REFERENCES `district` (`districtId`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
