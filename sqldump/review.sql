-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Oct 05, 2020 at 03:28 AM
-- Server version: 5.7.23
-- PHP Version: 7.2.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `homebiz_review`
--

-- --------------------------------------------------------

--
-- Table structure for table `review`
--

CREATE TABLE `review` (
  `reviewId` int(11) NOT NULL,
  `shopId` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `title` varchar(255) NOT NULL,
  `reviewDetail` longtext NOT NULL,
  `rating` int(5) NOT NULL,
  `publishedTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `review`
--

INSERT INTO `review` (`reviewId`, `shopId`, `username`, `title`, `reviewDetail`, `rating`, `publishedTime`) VALUES
(1, 1, 'vivocity', 'Fabulous Cake', 'cake is yummy, thanks shop', 5, '2020-10-05 03:28:19'),
(2, 2, 'johnny_chew', 'Best chicken rice ever', 'as title', 4, '2020-10-05 03:28:19'),
(3, 3, 'mouthcare123', 'Tasty toothpaste', 'My mouth smells better now', 5, '2020-10-05 03:28:19'),
(4, 3, 'vivocity', 'Good product, fast delivery', 'Ordered toothpaste and dispensers for my kids. Items were delivered next day. Good quality also', 5, '2020-10-05 03:28:19');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `review`
--
ALTER TABLE `review`
  ADD PRIMARY KEY (`reviewId`,`shopId`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `review`
--
ALTER TABLE `review`
  MODIFY `reviewId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
