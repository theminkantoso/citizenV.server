-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Máy chủ: 127.0.0.1
-- Thời gian đã tạo: Th12 17, 2021 lúc 05:05 PM
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

--
-- Đang đổ dữ liệu cho bảng `account`
--

INSERT INTO `account` (`accountId`, `password`, `email`, `roleId`, `managerAccount`, `startTime`, `endTime`, `isLocked`) VALUES
('0', 'sha256$iUtOAp2l3Fot4W6j$e865a998d8ab5d9b98db60448d64b33892e4790863c80bfa42c0de4c80886595', NULL, 0, NULL, NULL, NULL, 0),
('1', 'sha256$iUtOAp2l3Fot4W6j$e865a998d8ab5d9b98db60448d64b33892e4790863c80bfa42c0de4c80886595', NULL, 1, '0', NULL, NULL, 0),
('29', 'sha256$iUtOAp2l3Fot4W6j$e865a998d8ab5d9b98db60448d64b33892e4790863c80bfa42c0de4c80886595', NULL, 2, '1', NULL, NULL, 0),
('2901', 'sha256$iUtOAp2l3Fot4W6j$e865a998d8ab5d9b98db60448d64b33892e4790863c80bfa42c0de4c80886595', NULL, 3, '29', NULL, NULL, 0),
('290101', 'sha256$iUtOAp2l3Fot4W6j$e865a998d8ab5d9b98db60448d64b33892e4790863c80bfa42c0de4c80886595', NULL, 4, '2901', '2021-12-16', '2021-12-22', 0),
('29010101', 'sha256$iUtOAp2l3Fot4W6j$e865a998d8ab5d9b98db60448d64b33892e4790863c80bfa42c0de4c80886595', NULL, 5, '290101', NULL, NULL, 0),
('36', 'sha256$iUtOAp2l3Fot4W6j$e865a998d8ab5d9b98db60448d64b33892e4790863c80bfa42c0de4c80886595', '', 2, '1', NULL, NULL, 0),
('3601', 'sha256$iUtOAp2l3Fot4W6j$e865a998d8ab5d9b98db60448d64b33892e4790863c80bfa42c0de4c80886595', NULL, 3, '36', NULL, NULL, 0),
('360101', 'sha256$iUtOAp2l3Fot4W6j$e865a998d8ab5d9b98db60448d64b33892e4790863c80bfa42c0de4c80886595', NULL, 4, '3601', NULL, NULL, 0),
('36010101', 'sha256$iUtOAp2l3Fot4W6j$e865a998d8ab5d9b98db60448d64b33892e4790863c80bfa42c0de4c80886595', NULL, 5, '360101', NULL, NULL, 0),
('360102', 'sha256$iUtOAp2l3Fot4W6j$e865a998d8ab5d9b98db60448d64b33892e4790863c80bfa42c0de4c80886595', NULL, 4, '3601', NULL, NULL, 0);

--
-- Đang đổ dữ liệu cho bảng `citizen`
--

INSERT INTO `citizen` (`CCCD`, `name`, `DOB`, `sex`, `maritalStatus`, `nation`, `religion`, `permanentResidence`, `temporaryResidence`, `educationalLevel`, `job`, `cityProvinceId`, `districtId`, `wardId`, `groupId`) VALUES
('027323453457', 'Le', '2021-04-12', 'Nu', 'Chưa kết hôn', 'Kinh', 'Không', 'Thống Nhất1,Xã HN1,Cầu Giấy1,Hà Nội', NULL, '9/12', NULL, '29', '2901', '290101', '29010101'),
('027323453458', 'Le', '2021-04-12', 'Nu', 'Chưa kết hôn', 'Kinh', 'Không', 'Thống Nhất1,Xã HN1,Cầu Giấy1,Hà Nội', NULL, '9/12', NULL, '29', '2901', '290101', '29010101'),
('027323453459', 'Le', '2021-04-12', 'Nu', 'Chưa kết hôn', 'Kinh', 'Không', 'Thống Nhất1,Xã HN1,Cầu Giấy1,Hà Nội', NULL, '9/12', NULL, '29', '2901', '290101', '29010101'),
('028323453457', 'Le', '2021-04-12', 'Nu', 'Chưa kết hôn', 'Kinh', 'Không', 'Thống Nhất3,Xã HN1,Cầu Giấy1,Hà Nội', NULL, '9/12', NULL, '29', '2901', '290101', '29010103'),
('028323453458', 'Le', '2021-04-12', 'Nu', 'Chưa kết hôn', 'Kinh', 'Không', 'Thống Nhất3,Xã HN1,Cầu Giấy1,Hà Nội', NULL, '9/12', NULL, '29', '2901', '290101', '29010103'),
('028323453459', 'Le', '2021-04-12', 'Nu', 'Chưa kết hôn', 'Kinh', 'Không', 'Thống Nhất3,Xã HN1,Cầu Giấy1,Hà Nội', NULL, '9/12', NULL, '29', '2901', '290101', '29010103'),
('036013453459', 'Le', '2021-04-12', 'Nu', 'Chưa kết hôn', 'Kinh', 'Không', 'Nc1,TH1,Cầu Giấy,Thanh Hoá', NULL, '9/12', NULL, '36', '3601', '360101', '36010101'),
('036323453457', 'Le MT', '2021-04-12', 'Nu', 'Chưa kết hôn', 'Kinh', 'Không', 'Nc1,TH1,Cầu Giấy,Thanh Hoá', NULL, '12/12', NULL, '36', '3601', '360101', '36010101'),
('036323453458', 'Le', '2021-04-12', 'Nu', 'Chưa kết hôn', 'Kinh', 'Không', 'Nc1,TH1,Cầu Giấy,Thanh Hoá', NULL, '9/12', NULL, '36', '3601', '360101', '36010101'),
('036323453459', 'Le', '2021-04-12', 'Nu', 'Chưa kết hôn', 'Kinh', 'Không', 'Nc1,TH1,Cầu Giấy,Thanh Hoá', NULL, '9/12', NULL, '36', '3601', '360101', '36010101'),
('038323453457', 'Le', '2021-04-12', 'Nu', 'Chưa kết hôn', 'Kinh', 'Không', 'Thống Nhất1,Xã HN1,Cầu Giấy1,Hà Nội', NULL, '9/12', NULL, '29', '2901', '290101', '29010101'),
('038323453458', 'Le', '2021-04-12', 'Nu', 'Chưa kết hôn', 'Kinh', 'Không', 'Thống Nhất1,Xã HN1,Cầu Giấy1,Hà Nội', NULL, '9/12', NULL, '29', '2901', '290101', '29010101'),
('038323453459', 'Le', '2021-04-12', 'Nu', 'Chưa kết hôn', 'Kinh', 'Không', 'Hà Nội,Cầu Giấy1,Xã HN1,Thống Nhất1', NULL, '9/12', NULL, '29', '2901', '290101', '29010101');

--
-- Đang đổ dữ liệu cho bảng `cityprovince`
--

INSERT INTO `cityprovince` (`cityProvinceId`, `cityProvinceName`, `completed`) VALUES
('29', 'Hà Nội', 1),
('36', 'Thanh Hoá', NULL);

--
-- Đang đổ dữ liệu cho bảng `district`
--

INSERT INTO `district` (`districtId`, `districtName`, `cityProvinceId`, `completed`) VALUES
('2901', 'Cầu Giấy1', '29', 1),
('2902', 'Hà Đông', '29', 1),
('3601', 'Cầu Giấy', '36', NULL),
('3602', 'Nông Cống', '36', NULL);

--
-- Đang đổ dữ liệu cho bảng `residentialgroup`
--

INSERT INTO `residentialgroup` (`groupId`, `groupName`, `wardId`, `completed`) VALUES
('29010101', 'Thống Nhất1', '290101', 1),
('29010103', 'Thống Nhất3', '290101', 1),
('36010101', 'Nc1', '360101', NULL),
('36010102', 'Nc2', '360101', NULL);

--
-- Đang đổ dữ liệu cho bảng `ward`
--

INSERT INTO `ward` (`wardId`, `wardName`, `districtId`, `completed`) VALUES
('290101', 'Xã HN1', '2901', 1),
('290102', 'Xã HN2', '2901', 1),
('360101', 'TH1', '3601', NULL),
('360102', 'TH2', '3601', NULL);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
