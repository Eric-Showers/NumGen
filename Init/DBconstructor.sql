SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


--
-- Table structure for table `product_numbers`
--

CREATE TABLE IF NOT EXISTS `product_numbers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL DEFAULT '',
  `last_generated` bigint(20) DEFAULT NULL,
  `is_default` tinyint(1) DEFAULT NULL,
  `barcode_type` varchar(30) DEFAULT NULL,
  `first_digits` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=6 ;

-- To initialize product_numbers table for use, ensure that the `last_generated` 
-- values for each product type matches the real world availability


INSERT INTO `product_numbers` (`id`, `name`, `last_generated`, `is_default`, `barcode_type`, `first_digits`) VALUES
(1, '233...', 234477, NULL, 'upca', 885150),
(2, '600...', 600449, NULL, 'ean13', 405379),
(3, 'Digital', 285232, NULL, 'upca', 885150),
(5, 'Fremdlabel', 270009, NULL, 'upca', 885150);


--
-- Table structure for table `isrc_numbers`
--

CREATE TABLE IF NOT EXISTS `isrc_numbers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL DEFAULT '',
  `country_code` varchar(2) NOT NULL DEFAULT 'DE',
  `registrant_code` varchar(3) NOT NULL DEFAULT '',
  `last_generated` int(11) DEFAULT NULL,
  `last_gen_year` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;


-- To initialize isrc_numbers table for use, ensure that the `last_generated`
-- value matches the real world availability


INSERT INTO `isrc_numbers` (`id`, `name`, `registrant_code`, `country_code`, `last_generated`, `last_gen_year`) VALUES
(1, 'Membran', 'U24', 'DE', 0, 17);
