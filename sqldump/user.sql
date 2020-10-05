-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Oct 05, 2020 at 09:23 AM
-- Server version: 5.7.26
-- PHP Version: 7.3.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `homebiz_user`
--
CREATE DATABASE IF NOT EXISTS `homebiz_user` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `homebiz_user`;

-- --------------------------------------------------------

--
-- Table structure for table `user_login`
--

CREATE TABLE `user_login` (
  `id` bigint(20) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `type` tinyint(1) DEFAULT NULL,
  `created` timestamp NULL DEFAULT NULL,
  `updated` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `user_login`
--

INSERT INTO `user_login` (`id`, `email`, `password`, `type`, `created`, `updated`) VALUES
(3, 'er@homebiz.app', '708d3812b3e90cbc4b0751ec1afab7b7', 0, '2020-10-04 21:54:04', NULL),
(4, 'jr@homebiz.app', 'de2c9f8839385b3fcf939952de28bb01', 0, '2020-10-04 21:58:38', NULL),
(5, 'vv@homebiz.app', '574732e83b6fa9736aedcce9bf644854', 0, '2020-10-04 22:01:49', NULL),
(6, 'yx@homebiz.app', '8f4815062be162a55ec2cd1cff8a0d3c', 0, '2020-10-04 22:06:06', NULL),
(7, 'qj@homebiz.app', 'fb2dc60361c7a51d48ffaf30a05ac4d0', 0, '2020-10-04 22:06:39', NULL),
(8, 'boss@homebiz.app', 'f57611add43f15fbaa6bd04331da3019', 3, '2020-10-04 22:10:13', NULL),
(9, 'hello@songla.com', 'c8c6b8378b28e605be4a86420e097082', 2, '2020-10-04 22:11:49', NULL),
(18, 'hs@homebiz.app', 'a3ec33759a997a9bb6489846ddc81081', 0, '2020-10-05 00:41:13', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `user_profile`
--

CREATE TABLE `user_profile` (
  `userID` bigint(20) NOT NULL,
  `nric` varchar(10) DEFAULT NULL,
  `firstName` varchar(255) DEFAULT NULL,
  `lastName` varchar(255) DEFAULT NULL,
  `gender` tinyint(1) DEFAULT NULL,
  `birthday` datetime DEFAULT NULL,
  `profilePhotoURL` varchar(255) DEFAULT NULL,
  `description` longtext,
  `addressLine1` varchar(255) DEFAULT NULL,
  `addressLine2` varchar(255) DEFAULT NULL,
  `postalCode` varchar(11) DEFAULT NULL,
  `phoneNo` varchar(15) DEFAULT NULL,
  `telegramToken` bigint(10) DEFAULT NULL,
  `created` timestamp NULL DEFAULT NULL,
  `updated` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `user_profile`
--

INSERT INTO `user_profile` (`userID`, `nric`, `firstName`, `lastName`, `gender`, `birthday`, `profilePhotoURL`, `description`, `addressLine1`, `addressLine2`, `postalCode`, `phoneNo`, `telegramToken`, `created`, `updated`) VALUES
(3, NULL, 'Emmanuel', 'Rayendra', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2020-10-04 21:54:04', NULL),
(4, NULL, 'Jia Rong', 'Chew', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2020-10-04 21:58:38', NULL),
(5, NULL, 'Vi Vo', 'Pham', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2020-10-04 22:01:49', NULL),
(6, NULL, 'Vi Vo', 'Pham', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2020-10-04 22:06:06', NULL),
(7, NULL, 'Qi Jin', 'Tay', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2020-10-04 22:06:39', NULL),
(8, NULL, 'Barak', 'Osama', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2020-10-04 22:10:13', NULL),
(9, NULL, 'Song La', 'Lim', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2020-10-04 22:11:49', NULL),
(18, NULL, 'Hong Seng', 'Ong', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2020-10-05 00:41:13', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `user_login`
--
ALTER TABLE `user_login`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `user_profile`
--
ALTER TABLE `user_profile`
  ADD PRIMARY KEY (`userID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `user_login`
--
ALTER TABLE `user_login`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `user_profile`
--
ALTER TABLE `user_profile`
  MODIFY `userID` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `user_profile`
--
ALTER TABLE `user_profile`
  ADD CONSTRAINT `userID` FOREIGN KEY (`userID`) REFERENCES `user_login` (`id`);