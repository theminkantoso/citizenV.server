-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 19, 2021 at 12:21 PM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 8.0.13

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

-- --------------------------------------------------------

--
-- Table structure for table `account`
--

CREATE TABLE `account` (
  `accountId` varchar(10) NOT NULL,
  `password` varchar(10000) NOT NULL,
  `email` varchar(1000) DEFAULT NULL,
  `roleId` int(10) NOT NULL,
  `managerAccount` varchar(10) DEFAULT NULL,
  `startDate` date DEFAULT NULL,
  `endDate` date DEFAULT NULL,
  `isLocked` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `citizen`
--

CREATE TABLE `citizen` (
  `CCCD` varchar(12) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `DOB` date NOT NULL,
  `sex` enum('Nam','Nu') NOT NULL,
  `maritalStatus` varchar(50) NOT NULL,
  `nation` varchar(50) NOT NULL,
  `religion` varchar(50) NOT NULL,
  `permanentResidence` varchar(100) DEFAULT NULL,
  `temporaryResidence` varchar(100) DEFAULT NULL,
  `educationalLevel` varchar(10) DEFAULT NULL,
  `job` varchar(50) DEFAULT NULL,
  `cityProvinceId` varchar(2) NOT NULL,
  `districtId` varchar(4) NOT NULL,
  `wardId` varchar(6) NOT NULL,
  `groupId` varchar(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `cityprovince`
--

CREATE TABLE `cityprovince` (
  `cityProvinceId` varchar(2) NOT NULL,
  `cityProvinceName` varchar(30) NOT NULL,
  `completed` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `district`
--

CREATE TABLE `district` (
  `districtId` varchar(4) NOT NULL,
  `districtName` varchar(30) NOT NULL,
  `cityProvinceId` varchar(2) NOT NULL,
  `completed` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Triggers `district`
--
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
-- Table structure for table `residentialgroup`
--

CREATE TABLE `residentialgroup` (
  `groupId` varchar(8) NOT NULL,
  `groupName` varchar(30) NOT NULL,
  `wardId` varchar(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `revoked_tokens`
--

CREATE TABLE `revoked_tokens` (
  `id` int(11) NOT NULL,
  `jti` varchar(120) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `ward`
--

CREATE TABLE `ward` (
  `wardId` varchar(6) NOT NULL,
  `wardName` varchar(30) NOT NULL,
  `districtId` varchar(4) NOT NULL,
  `completed` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Triggers `ward`
--
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
-- Indexes for dumped tables
--

--
-- Indexes for table `account`
--
ALTER TABLE `account`
  ADD PRIMARY KEY (`accountId`),
  ADD KEY `fk_account_account` (`managerAccount`);

--
-- Indexes for table `citizen`
--
ALTER TABLE `citizen`
  ADD PRIMARY KEY (`CCCD`),
  ADD KEY `fk_citizen_cityprovince` (`cityProvinceId`),
  ADD KEY `fk_citizen_district` (`districtId`),
  ADD KEY `fk_citizen_ward` (`wardId`),
  ADD KEY `fk_citizen_residentialgroup` (`groupId`);

--
-- Indexes for table `cityprovince`
--
ALTER TABLE `cityprovince`
  ADD PRIMARY KEY (`cityProvinceId`);

--
-- Indexes for table `district`
--
ALTER TABLE `district`
  ADD PRIMARY KEY (`districtId`),
  ADD KEY `fk_district_cityprovince` (`cityProvinceId`);

--
-- Indexes for table `residentialgroup`
--
ALTER TABLE `residentialgroup`
  ADD PRIMARY KEY (`groupId`),
  ADD KEY `fk_residentialgroup_ward` (`wardId`);

--
-- Indexes for table `revoked_tokens`
--
ALTER TABLE `revoked_tokens`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `ward`
--
ALTER TABLE `ward`
  ADD PRIMARY KEY (`wardId`),
  ADD KEY `fk_ward_district` (`districtId`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `revoked_tokens`
--
ALTER TABLE `revoked_tokens`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

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
