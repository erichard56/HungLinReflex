-- MySQL dump 10.13  Distrib 8.0.38, for macos14 (arm64)
--
-- Host: vxsct10016.avnam.net    Database: hunglin
-- ------------------------------------------------------
-- Server version	5.5.5-10.6.22-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bosquetaoista_cursante`
--

DROP TABLE IF EXISTS `bosquetaoista_cursante`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bosquetaoista_cursante` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `agenda_id` bigint(20) NOT NULL,
  `persona_id` bigint(20) NOT NULL,
  `tipocursante_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `bosquetaoista_cursan_agenda_id_dfdb539f_fk_bosquetao` (`agenda_id`),
  KEY `bosquetaoista_cursan_persona_id_d6340c67_fk_bosquetao` (`persona_id`),
  KEY `bosquetaoista_cursan_tipocursante_id_c0b997b2_fk_bosquetao` (`tipocursante_id`),
  CONSTRAINT `bosquetaoista_cursan_agenda_id_dfdb539f_fk_bosquetao` FOREIGN KEY (`agenda_id`) REFERENCES `bosquetaoista_agenda` (`id`),
  CONSTRAINT `bosquetaoista_cursan_persona_id_d6340c67_fk_bosquetao` FOREIGN KEY (`persona_id`) REFERENCES `bosquetaoista_persona` (`id`),
  CONSTRAINT `bosquetaoista_cursan_tipocursante_id_c0b997b2_fk_bosquetao` FOREIGN KEY (`tipocursante_id`) REFERENCES `bosquetaoista_tipocursante` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bosquetaoista_cursante`
--

LOCK TABLES `bosquetaoista_cursante` WRITE;
/*!40000 ALTER TABLE `bosquetaoista_cursante` DISABLE KEYS */;
INSERT INTO `bosquetaoista_cursante` VALUES (1,1,303,1),(7,1,76,1),(8,1,232,1),(9,1,87,1),(10,1,230,1),(11,1,318,1),(12,1,306,1),(13,1,308,1),(14,1,98,1),(15,1,328,1),(16,1,298,1),(17,1,90,1),(18,1,85,1),(19,1,1,1),(20,1,58,1),(21,1,159,1),(22,1,292,1),(23,1,152,1),(24,1,69,1),(25,1,274,1),(26,1,30,1),(27,1,204,1),(28,1,206,1),(29,1,33,1),(30,1,218,1);
/*!40000 ALTER TABLE `bosquetaoista_cursante` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-17 19:16:36
