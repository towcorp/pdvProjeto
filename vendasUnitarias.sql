-- phpMyAdmin SQL Dump
-- version 4.9.5deb2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Sep 12, 2021 at 11:10 AM
-- Server version: 8.0.26-0ubuntu0.20.04.2
-- PHP Version: 7.4.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `estoque_produtos`
--

-- --------------------------------------------------------

--
-- Table structure for table `vendasUnitarias`
--

CREATE TABLE `vendasUnitarias` (
  `id` int NOT NULL,
  `codigo` int NOT NULL,
  `item` varchar(30) NOT NULL,
  `quantidade` int NOT NULL,
  `preco_unitario` float NOT NULL,
  `total` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `vendasUnitarias`
--

INSERT INTO `vendasUnitarias` (`id`, `codigo`, `item`, `quantidade`, `preco_unitario`, `total`) VALUES
(30, 1, 'bone', 1, 29.9, 29.9),
(31, 2, 'bone', 1, 29.9, 29.9),
(32, 2, 'bone', 1, 29.9, 29.9),
(33, 4, 'prod igual', 5, 23.5, 117.5);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `vendasUnitarias`
--
ALTER TABLE `vendasUnitarias`
  ADD UNIQUE KEY `id` (`id`) USING BTREE;

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `vendasUnitarias`
--
ALTER TABLE `vendasUnitarias`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
