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
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add casa',7,'add_casa'),(26,'Can change casa',7,'change_casa'),(27,'Can delete casa',7,'delete_casa'),(28,'Can view casa',7,'view_casa'),(29,'Can add evento',8,'add_evento'),(30,'Can change evento',8,'change_evento'),(31,'Can delete evento',8,'delete_evento'),(32,'Can view evento',8,'view_evento'),(33,'Can add grado',9,'add_grado'),(34,'Can change grado',9,'change_grado'),(35,'Can delete grado',9,'delete_grado'),(36,'Can view grado',9,'view_grado'),(37,'Can add tipo cursante',10,'add_tipocursante'),(38,'Can change tipo cursante',10,'change_tipocursante'),(39,'Can delete tipo cursante',10,'delete_tipocursante'),(40,'Can view tipo cursante',10,'view_tipocursante'),(41,'Can add tipo doc',11,'add_tipodoc'),(42,'Can change tipo doc',11,'change_tipodoc'),(43,'Can delete tipo doc',11,'delete_tipodoc'),(44,'Can view tipo doc',11,'view_tipodoc'),(45,'Can add tipo estado',12,'add_tipoestado'),(46,'Can change tipo estado',12,'change_tipoestado'),(47,'Can delete tipo estado',12,'delete_tipoestado'),(48,'Can view tipo estado',12,'view_tipoestado'),(49,'Can add tipo evento',13,'add_tipoevento'),(50,'Can change tipo evento',13,'change_tipoevento'),(51,'Can delete tipo evento',13,'delete_tipoevento'),(52,'Can view tipo evento',13,'view_tipoevento'),(53,'Can add tipo extra',14,'add_tipoextra'),(54,'Can change tipo extra',14,'change_tipoextra'),(55,'Can delete tipo extra',14,'delete_tipoextra'),(56,'Can view tipo extra',14,'view_tipoextra'),(57,'Can add persona',15,'add_persona'),(58,'Can change persona',15,'change_persona'),(59,'Can delete persona',15,'delete_persona'),(60,'Can view persona',15,'view_persona'),(61,'Can add agenda',16,'add_agenda'),(62,'Can change agenda',16,'change_agenda'),(63,'Can delete agenda',16,'delete_agenda'),(64,'Can view agenda',16,'view_agenda'),(65,'Can add cursante',17,'add_cursante'),(66,'Can change cursante',17,'change_cursante'),(67,'Can delete cursante',17,'delete_cursante'),(68,'Can view cursante',17,'view_cursante'),(69,'Can add persona extra',18,'add_personaextra'),(70,'Can change persona extra',18,'change_personaextra'),(71,'Can delete persona extra',18,'delete_personaextra'),(72,'Can view persona extra',18,'view_personaextra'),(73,'Can add tabla',19,'add_tabla'),(74,'Can change tabla',19,'change_tabla'),(75,'Can delete tabla',19,'delete_tabla'),(76,'Can view tabla',19,'view_tabla'),(77,'Can add frase',20,'add_frase'),(78,'Can change frase',20,'change_frase'),(79,'Can delete frase',20,'delete_frase'),(80,'Can view frase',20,'view_frase');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-17 19:16:25
