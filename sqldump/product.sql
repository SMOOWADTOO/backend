-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Oct 05, 2020 at 03:19 AM
-- Server version: 5.7.23
-- PHP Version: 7.2.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `homebiz_product`
--

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE `product` (
  `productId` int(11) NOT NULL,
  `shopId` int(11) NOT NULL,
  `productName` varchar(255) NOT NULL,
  `productDesc` longtext NOT NULL,
  `unitPrice` double NOT NULL,
  `productPhotoURL` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`productId`, `shopId`, `productName`, `productDesc`, `unitPrice`) VALUES
(1, 1, 'Yam Cake', 'Cake made from yam', 2),
(2, 1, 'Pandan Cake', 'Cake made from pandan leaf', 3),
(3, 2, 'Chicken rice', 'Chicken rice with vegetable', 5),
(4, 2, 'Char siew noodle', 'Noodle with char siew, roasted pork, dumpling and vegetable', 4),
(5, 3, 'Coolgate toothpaste', 'Cooling your tooth with our special toothpaste', 4.5),
(6, 3, 'Toothpaste dispenser', 'Easily pump your toothpaste with our dispenser', 6.5);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`productId`,`shopId`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `product`
--
ALTER TABLE `product`
  MODIFY `productId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;