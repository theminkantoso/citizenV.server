-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 14, 2021 at 11:02 AM
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

--
-- Dumping data for table `account`
--

INSERT INTO `account` (`accountId`, `password`, `email`, `roleId`, `managerAccount`, `startTime`, `endTime`, `isLocked`) VALUES
('00', 'sha256$iUtOAp2l3Fot4W6j$e865a998d8ab5d9b98db60448d64b33892e4790863c80bfa42c0de4c80886595', NULL, 0, NULL, NULL, NULL, 0),
('0001', 'sha256$88rjkGooVrrixK6F$6d1dfda1d43bba75e2e215be70aae110c511455c49a24e2f122f63d974b12834', NULL, 1, '00', NULL, NULL, 1),
('000103', '123456', NULL, 2, '0001', NULL, NULL, 1),
('00010304', '123456', NULL, 3, '000103', NULL, NULL, 1),
('0002', '123456', NULL, 1, '00', '2021-12-14', '2021-12-15', 1),
('000204', '123456', NULL, 2, '0002', NULL, NULL, 1),
('0003', 'sha256$rRM7HfFHhtNoUhn3$ce8b24dc83f7ef30c8aab5e0e94ccd5296e6b8eedb671f3ffd5e3f1456918851', 'trangco19621962@gmail.com', 1, '00', NULL, NULL, 0);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
