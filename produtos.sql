-- phpMyAdmin SQL Dump
-- version 4.9.5deb2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Sep 18, 2021 at 07:21 PM
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
-- Table structure for table `produtos`
--

CREATE TABLE `produtos` (
  `codigo` int NOT NULL,
  `produto` varchar(30) NOT NULL,
  `categoria` varchar(20) NOT NULL,
  `estoque_minimo` int NOT NULL,
  `quantidade` int NOT NULL,
  `preco` float(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `produtos`
--

INSERT INTO `produtos` (`codigo`, `produto`, `categoria`, `estoque_minimo`, `quantidade`, `preco`) VALUES
(1, 'CADERNO', 'ESCOLAR', 10, 80, 19.90),
(2, 'LAPIS', 'ESCOLAR', 20, 200, 1.50),
(3, 'CANETA', 'ESCOLAR', 20, 150, 2.00),
(4, 'CLIPS', 'ESCRITORIO', 50, 500, 4.50),
(5, 'SULFITE(100)', 'ESCRITORIO', 10, 100, 6.50),
(6, 'REGUA ACRILICA', 'ESCOLAR', 5, 40, 3.50),
(7, 'LAPIS DE COR 12 CORES', 'ESCOLAR', 20, 80, 12.90),
(8, 'AGENDA', 'ESCRITORIO', 10, 40, 19.90),
(9, 'GRAMPO CX 100', 'ESCRITORIO', 5, 20, 8.90),
(10, 'Pincel marca texto', 'escolar', 5, 30, 3.50),
(11, 'Cola em bastão', 'escolar', 5, 12, 2.00),
(12, 'Bloco desenho A4', 'escolar', 5, 15, 10.00),
(13, 'Borracha', 'escolar', 5, 4, 0.80),
(14, 'Aquarela 12 cores', 'escolar', 5, 20, 12.90),
(15, 'Apontador com depósito', 'escolar', 5, 10, 1.90),
(16, 'Estojo escolar plástico', 'escolar', 5, 15, 4.50),
(17, 'Organizador de escritorio', 'escritorio', 3, 10, 18.50),
(18, 'Prancheta poliestireno', 'escritorio', 3, 10, 9.80),
(19, 'Caneta tinteiro', 'escritorio', 5, 2, 9.90),
(20, 'Refiladora', 'escritorio', 2, 10, 15.00),
(21, 'Espeto p/papel', 'escritorio', 5, 15, 3.90),
(22, 'HD externo', 'informatica', 5, 10, 100.00),
(23, 'Cadeira de escritório', 'escritorio', 2, 5, 249.80),
(24, 'Luminária de mesa', 'escritorio', 2, 10, 49.90),
(25, 'Luminária de emergência', 'escritorio', 5, 20, 20.00),
(26, 'Caixa de som 6w', 'informatica', 2, 10, 29.90),
(27, 'Mouse sem fio usb', 'informatica', 5, 15, 60.00),
(28, 'Teclado usb slim', 'informatica', 5, 10, 50.00),
(29, 'Nobreak Station II', 'informatica', 2, 1, 120.00),
(30, 'Webcam Full HD', 'informatica', 8, 10, 119.90);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `produtos`
--
ALTER TABLE `produtos`
  ADD UNIQUE KEY `codigo` (`codigo`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `produtos`
--
ALTER TABLE `produtos`
  MODIFY `codigo` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
