-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Máy chủ: 127.0.0.1
-- Thời gian đã tạo: Th12 14, 2021 lúc 10:21 AM
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

--
-- Đang đổ dữ liệu cho bảng `account`
--

INSERT INTO `account` (`accountId`, `password`, `email`, `roleId`, `managerAccount`, `startTime`, `endTime`, `isLocked`) VALUES
('00', 'sha256$iUtOAp2l3Fot4W6j$e865a998d8ab5d9b98db60448d64b33892e4790863c80bfa42c0de4c80886595', NULL, 0, NULL, NULL, NULL, 0);

--
-- Bẫy `account`
--
DELIMITER $$
CREATE TRIGGER `disableAccount` AFTER UPDATE ON `account` FOR EACH ROW BEGIN
 IF new.isLocked = 1 THEN
	UPDATE account SET isLocked = 1 WHERE managerAccount = old.accountId;
END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `citizen`
--

CREATE TABLE `citizen` (
  `citizenId` int(8) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `DOB` varchar(10) DEFAULT NULL,
  `sex` varchar(3) DEFAULT NULL,
  `maritalStatus` varchar(15) DEFAULT NULL,
  `nation` varchar(15) DEFAULT NULL,
  `religion` varchar(50) DEFAULT NULL,
  `CMND` varchar(11) DEFAULT NULL,
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
-- Cấu trúc bảng cho bảng `cityprovince`
--

CREATE TABLE `cityprovince` (
  `cityProvinceId` varchar(2) NOT NULL,
  `cityProvinceName` varchar(30) NOT NULL,
  `created` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `district`
--

CREATE TABLE `district` (
  `districtId` varchar(4) NOT NULL,
  `districtName` varchar(30) NOT NULL,
  `cityProvinceId` varchar(2) NOT NULL,
  `created` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `residentialgroup`
--

CREATE TABLE `residentialgroup` (
  `groupId` varchar(8) NOT NULL,
  `groupName` varchar(30) NOT NULL,
  `wardId` varchar(6) NOT NULL,
  `created` tinyint(1) DEFAULT NULL
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
  `created` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
  ADD PRIMARY KEY (`citizenId`),
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
-- AUTO_INCREMENT cho bảng `citizen`
--
ALTER TABLE `citizen`
  MODIFY `citizenId` int(8) NOT NULL AUTO_INCREMENT;

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
  ADD CONSTRAINT `fk_citizen_cityprovince` FOREIGN KEY (`cityProvinceId`) REFERENCES `cityprovince` (`cityProvinceId`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_citizen_district` FOREIGN KEY (`districtId`) REFERENCES `district` (`districtId`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_citizen_residentialgroup` FOREIGN KEY (`groupId`) REFERENCES `residentialgroup` (`groupId`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_citizen_ward` FOREIGN KEY (`wardId`) REFERENCES `ward` (`wardId`) ON UPDATE CASCADE;

--
-- Các ràng buộc cho bảng `district`
--
ALTER TABLE `district`
  ADD CONSTRAINT `fk_district_cityprovince` FOREIGN KEY (`cityProvinceId`) REFERENCES `cityprovince` (`cityProvinceId`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Các ràng buộc cho bảng `residentialgroup`
--
ALTER TABLE `residentialgroup`
  ADD CONSTRAINT `fk_residentialgroup_ward` FOREIGN KEY (`wardId`) REFERENCES `ward` (`wardId`) ON UPDATE CASCADE;

--
-- Các ràng buộc cho bảng `ward`
--
ALTER TABLE `ward`
  ADD CONSTRAINT `fk_ward_district` FOREIGN KEY (`districtId`) REFERENCES `district` (`districtId`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
