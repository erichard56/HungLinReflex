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
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$260000$QgzpDYroyqPGzc43L3eRyk$RyBpUaJ/yIc/qFOKaCMc5CETHCQnhjExQ+G0KlZ0s9E=','2025-04-07 13:15:47.015209',1,'hunglin','','','',1,1,'2024-05-23 14:44:33.639650'),(2,'pbkdf2_sha256$260000$9MusHQQiRC0JAtB3YxtsQE$dBIz9HhHCAAFp9MwuiotK9kcsxLmSZXiHbZi5j9C1eE=','2025-04-08 15:07:03.643733',1,'erichard','Enrique','Richard','enrique.richard@gmail.com',1,1,'2024-05-23 17:19:42.989190'),(3,'pbkdf2_sha256$260000$iI7kj8G1aUEId9SEwiovHy$3AarMquvmY0jhVdLvnyq+ea/fAmubMH+iTzmdjV5dQs=','2025-07-11 18:49:54.631646',1,'dpijuan','Daniel','Pijuan','dpijuan@gmail.com',1,1,'2024-06-03 14:54:37.749138'),(4,'pbkdf2_sha256$260000$2jfZN0BeATncsc6S1ogFI9$rEzbo16ezONki5aDf5sZQNNYFRTPoZOr1nD7WBETZ/g=','2025-04-06 16:35:28.761581',0,'hduran','Héctor','Durán Agra','hduranagra@gmail.com',1,1,'2024-06-17 22:14:58.790275'),(5,'pbkdf2_sha256$260000$XcsrGPURZItbO8FYjio27r$nLTlkELe2q/ij27LDTzOgPdcBbUYu3Mv5lOoRIGGhF4=','2025-02-03 14:50:22.760908',1,'rgsilberberg','Roxana','Silberberg','rgsilberberg@gmail.com',1,1,'2024-06-17 22:37:54.000000'),(6,'pbkdf2_sha256$260000$M1Quz8LQLnI9P2HBL9mYas$ubCVUzO/xTr7jY2H/6WVahf3K7U0Qc2sVHFBS/9cyLI=','2025-04-06 16:13:59.881871',0,'deguren','Diego','Eduren','egurendiegomax@gmail.com',1,1,'2025-04-06 16:04:10.932938'),(10,'pbkdf2_sha256$260000$b9FCkwcB7fBIlFbnLkdFGD$eQt7BDrfr8xN/O0DpR+u2VJsNihQSBIqhVbUuVj6DdE=','2025-07-14 18:13:00.773430',0,'pakot','Pablo','Kot','pablokot@gmail.com',1,1,'2025-04-06 16:30:53.087417'),(11,'pbkdf2_sha256$260000$w2hcvG4vNzg3MGVZ0DJOkY$1QG5YxTFuRCFjGM3MHKrgz8dYLwNzeOojx5HZV1nQZU=','2025-04-07 13:35:03.193385',0,'hsaboundji','Hilda','Saboundji','taichilda51@gmail.com',1,1,'2025-04-06 16:48:40.614740'),(12,'pbkdf2_sha256$260000$YqGdo6TIR49T6xFh2Vqf5C$s3eb+xZ6D8MH82TuUmCducD9DFq8+XEoJ9OoP/yg1tM=','2025-04-06 17:32:52.797679',0,'rcohen','Raquel','Cohen','rcbambu@gmail.com',1,1,'2025-04-06 16:50:04.708261'),(13,'pbkdf2_sha256$260000$V4apkDqaaGZAMpJW2V6dqc$eRSkH1ZgnAdY7Zk2AroXa9Cv1n1F3McbgTfaA5Uy3Mw=','2025-04-16 13:13:17.407165',0,'mdemelli','Marcela','Demelli','mademelli@gmail.com',1,1,'2025-04-06 17:20:44.863574'),(14,'pbkdf2_sha256$260000$jcWspnYOgB0h8QAStQsUHG$4aVEfBTu9wJSiXBLlKKWgD+SzfSd9OytNvo/D1MeImk=','2025-04-08 13:53:50.340030',0,'epantarotto','Esteban','Pantarotto','esteban.pantarotto2018@gmail.com',1,1,'2025-04-06 17:22:23.722721'),(15,'pbkdf2_sha256$260000$cjqhlPXtWzJQ37TLhU2oO0$HAX74siKpksKlz/WFP2TkI/ET3s4ebp6iNCY5l1cYpg=','2025-04-06 20:27:08.590326',0,'gmaidana','Gabriela','Maidana','magama2374@gmail.com',1,1,'2025-04-06 20:26:36.721697');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-17 19:16:30
