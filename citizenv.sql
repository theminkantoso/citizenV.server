-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Máy chủ: 127.0.0.1
-- Thời gian đã tạo: Th12 18, 2021 lúc 02:49 PM
-- Phiên bản máy phục vụ: 10.4.17-MariaDB
-- Phiên bản PHP: 7.4.15

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `citizenv`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `account`
--

CREATE TABLE `account` (
  `accountId` varchar(10) NOT NULL,
  `password` varchar(10000) NOT NULL,
  `email` varchar(1000) DEFAULT NULL,
  `roleId` int(10) NOT NULL,
  `managerAccount` varchar(10) DEFAULT NULL,
  `startTime` date DEFAULT NULL,
  `endTime` date DEFAULT NULL,
  `isLocked` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `citizen`
--

CREATE TABLE `citizen` (
  `CCCD` varchar(12) NOT NULL,
  `name` varchar(50) NOT NULL,
  `DOB` date NOT NULL,
  `sex` varchar(3) NOT NULL,
  `maritalStatus` varchar(50) NOT NULL,
  `nation` varchar(50) NOT NULL,
  `religion` varchar(50) NOT NULL,
  `permanentResidence` varchar(100) DEFAULT NULL,
  `temporaryResidence` varchar(100) DEFAULT NULL,
  `educationalLevel` varchar(10) NOT NULL,
  `job` varchar(50) DEFAULT NULL,
  `cityProvinceId` varchar(2) NOT NULL,
  `districtId` varchar(4) NOT NULL,
  `wardId` varchar(6) NOT NULL,
  `groupId` varchar(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `cityprovince`
--

CREATE TABLE `cityprovince` (
  `cityProvinceId` varchar(2) NOT NULL,
  `cityProvinceName` varchar(30) NOT NULL,
  `completed` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `district`
--

CREATE TABLE `district` (
  `districtId` varchar(4) NOT NULL,
  `districtName` varchar(30) NOT NULL,
  `cityProvinceId` varchar(2) NOT NULL,
  `completed` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Bẫy `district`
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
-- Cấu trúc bảng cho bảng `residentialgroup`
--

CREATE TABLE `residentialgroup` (
  `groupId` varchar(8) NOT NULL,
  `groupName` varchar(30) NOT NULL,
  `wardId` varchar(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `revoked_tokens`
--

CREATE TABLE `revoked_tokens` (
  `id` int(11) NOT NULL,
  `jti` varchar(120) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `ward`
--

CREATE TABLE `ward` (
  `wardId` varchar(6) NOT NULL,
  `wardName` varchar(30) NOT NULL,
  `districtId` varchar(4) NOT NULL,
  `completed` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Bẫy `ward`
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
-- Chỉ mục cho các bảng đã đổ
--

--
-- Chỉ mục cho bảng `account`
--
ALTER TABLE `account`
  ADD PRIMARY KEY (`accountId`),
  ADD KEY `fk_account_account` (`managerAccount`);

--
-- Chỉ mục cho bảng `citizen`
--
ALTER TABLE `citizen`
  ADD PRIMARY KEY (`CCCD`),
  ADD KEY `fk_citizen_cityprovince` (`cityProvinceId`),
  ADD KEY `fk_citizen_district` (`districtId`),
  ADD KEY `fk_citizen_ward` (`wardId`),
  ADD KEY `fk_citizen_residentialgroup` (`groupId`);

--
-- Chỉ mục cho bảng `cityprovince`
--
ALTER TABLE `cityprovince`
  ADD PRIMARY KEY (`cityProvinceId`);

--
-- Chỉ mục cho bảng `district`
--
ALTER TABLE `district`
  ADD PRIMARY KEY (`districtId`),
  ADD KEY `fk_district_cityprovince` (`cityProvinceId`);

--
-- Chỉ mục cho bảng `residentialgroup`
--
ALTER TABLE `residentialgroup`
  ADD PRIMARY KEY (`groupId`),
  ADD KEY `fk_residentialgroup_ward` (`wardId`);

--
-- Chỉ mục cho bảng `revoked_tokens`
--
ALTER TABLE `revoked_tokens`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `ward`
--
ALTER TABLE `ward`
  ADD PRIMARY KEY (`wardId`),
  ADD KEY `fk_ward_district` (`districtId`);

--
-- AUTO_INCREMENT cho các bảng đã đổ
--

--
-- AUTO_INCREMENT cho bảng `revoked_tokens`
--
ALTER TABLE `revoked_tokens`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Các ràng buộc cho các bảng đã đổ
--

--
-- Các ràng buộc cho bảng `citizen`
--
ALTER TABLE `citizen`
  ADD CONSTRAINT `fk_citizen_cityprovince` FOREIGN KEY (`cityProvinceId`) REFERENCES `cityprovince` (`cityProvinceId`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_citizen_district` FOREIGN KEY (`districtId`) REFERENCES `district` (`districtId`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_citizen_residentialgroup` FOREIGN KEY (`groupId`) REFERENCES `residentialgroup` (`groupId`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_citizen_ward` FOREIGN KEY (`wardId`) REFERENCES `ward` (`wardId`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Các ràng buộc cho bảng `residentialgroup`
--
ALTER TABLE `residentialgroup`
  ADD CONSTRAINT `fk_residentialgroup_ward` FOREIGN KEY (`wardId`) REFERENCES `ward` (`wardId`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Các ràng buộc cho bảng `ward`
--
ALTER TABLE `ward`
  ADD CONSTRAINT `fk_ward_district` FOREIGN KEY (`districtId`) REFERENCES `district` (`districtId`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
