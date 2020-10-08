-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Oct 08, 2020 at 06:32 PM
-- Server version: 5.7.23
-- PHP Version: 7.2.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `shop`
--

-- --------------------------------------------------------

--
-- Table structure for table `shop`
--

CREATE TABLE `shop` (
  `shopId` int(11) NOT NULL,
  `shopName` varchar(255) NOT NULL,
  `shopDesc` longtext,
  `shopImageURL` longtext,
  `contactNo` varchar(30) DEFAULT NULL,
  `address` longtext,
  `email` varchar(255) DEFAULT NULL,
  `website` varchar(255) DEFAULT NULL,
  `createdAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `shop`
--

INSERT INTO `shop` (`shopId`, `shopName`, `shopDesc`, `shopImageURL`, `contactNo`, `address`, `email`, `website`, `createdAt`) VALUES
(1, 'Yummy Cakes', 'Yummy Cakes for the tummy', 'http://canadianhometrends.com/wp-content/uploads/2013/12/77611H.jpg', '91234567', 'Singapore Management University\r\n80 Stamford Road \r\nSingapore 178902', 'sis_ugrad@smu.edu.sg', 'https://sis.smu.edu.sg/about/contact/visit/us', '2020-10-08 14:45:31'),
(2, 'The Shao Rou Store', 'The one and only Shao Rou store. You may ask, what is shao rou? It is roasted meat. Try one of our delicious shao rou today, we have chicken rice and char siew noodles, more stuff in the future ! ', 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.WkbMXwABR4gBGxMz5H0h7AHaE7%26pid%3DApi&f=1', NULL, 'Office of the President of the Republic of Singapore\r\nOrchard Road, Singapore 238823', 'istana_feedback@istana.gov.sg', 'https://www.istana.gov.sg/Pages/Contact', '2020-10-08 14:50:19'),
(3, 'Your Teeth', 'Your teeth, my problem, try our products today! From coolgates to dispensers, we have it all, call me now! I run a dropshipping business, need them moolah, call me now, its not MLM', 'https://media.istockphoto.com/photos/gimme-a-call-picture-id176036885', '+65 98339150', 'Block 94, Lorong 4 Toa Payoh, #01-10, Singapore 310094', 'mlm@iscamyou.com', 'https://www.tupperwarebrands.com', '2020-10-08 14:54:45');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `shop`
--
ALTER TABLE `shop`
  ADD PRIMARY KEY (`shopId`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `shop`
--
ALTER TABLE `shop`
  MODIFY `shopId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
