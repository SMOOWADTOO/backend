-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Oct 09, 2020 at 08:04 AM
-- Server version: 5.7.23
-- PHP Version: 7.2.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `order`
--

-- --------------------------------------------------------

--
-- Table structure for table `orderDetails`
--

CREATE TABLE `orderDetails` (
  `orderDetailId` int(11) NOT NULL,
  `orderId` int(11) NOT NULL,
  `productId` int(11) NOT NULL,
  `price` double NOT NULL,
  `quantity` int(11) NOT NULL,
  `total` double NOT NULL,
  `createdAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `orderDetails`
--

INSERT INTO `orderDetails` (`orderDetailId`, `orderId`, `productId`, `price`, `quantity`, `total`, `createdAt`) VALUES
(1, 1, 1, 2.5, 3, 7.5, '2020-10-09 07:37:35'),
(2, 1, 2, 5, 1, 5, '2020-10-09 07:38:40'),
(3, 2, 1, 2.5, 2, 5, '2020-10-09 08:04:03');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `orderId` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `pickupAddress` longtext NOT NULL,
  `deliveryAddress` longtext NOT NULL,
  `completed` tinyint(1) NOT NULL DEFAULT '0',
  `paid` tinyint(1) NOT NULL DEFAULT '0',
  `createdAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`orderId`, `username`, `pickupAddress`, `deliveryAddress`, `completed`, `paid`, `createdAt`, `updatedAt`) VALUES
(1, 'jrchew', 'Istana', 'SMU SIS', 0, 0, '2020-10-09 07:35:22', '2020-10-09 18:05:28'),
(2, 'qijintay', 'SMU SIS ', 'SMU SIS', 0, 0, '2020-10-09 07:40:00', '2020-10-09 18:05:28');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `orderDetails`
--
ALTER TABLE `orderDetails`
  ADD PRIMARY KEY (`orderDetailId`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`orderId`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `orderDetails`
--
ALTER TABLE `orderDetails`
  MODIFY `orderDetailId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `orderId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
