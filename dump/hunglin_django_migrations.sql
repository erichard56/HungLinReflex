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
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2024-05-23 14:44:03.298823'),(2,'auth','0001_initial','2024-05-23 14:44:03.988235'),(3,'admin','0001_initial','2024-05-23 14:44:04.167756'),(4,'admin','0002_logentry_remove_auto_add','2024-05-23 14:44:04.217124'),(5,'admin','0003_logentry_add_action_flag_choices','2024-05-23 14:44:04.252779'),(6,'contenttypes','0002_remove_content_type_name','2024-05-23 14:44:04.424260'),(7,'auth','0002_alter_permission_name_max_length','2024-05-23 14:44:04.488916'),(8,'auth','0003_alter_user_email_max_length','2024-05-23 14:44:04.538711'),(9,'auth','0004_alter_user_username_opts','2024-05-23 14:44:04.579666'),(10,'auth','0005_alter_user_last_login_null','2024-05-23 14:44:04.639087'),(11,'auth','0006_require_contenttypes_0002','2024-05-23 14:44:04.662286'),(12,'auth','0007_alter_validators_add_error_messages','2024-05-23 14:44:04.697655'),(13,'auth','0008_alter_user_username_max_length','2024-05-23 14:44:04.758125'),(14,'auth','0009_alter_user_last_name_max_length','2024-05-23 14:44:04.833676'),(15,'auth','0010_alter_group_name_max_length','2024-05-23 14:44:04.905332'),(16,'auth','0011_update_proxy_permissions','2024-05-23 14:44:05.014361'),(17,'auth','0012_alter_user_first_name_max_length','2024-05-23 14:44:05.071028'),(18,'bosquetaoista','0001_initial','2024-05-23 14:44:06.124582'),(19,'bosquetaoista','0002_tipos','2024-05-23 14:44:06.176723'),(20,'bosquetaoista','0003_rename_tipos_tablas','2024-05-23 14:44:06.346808'),(21,'bosquetaoista','0004_delete_tablas','2024-05-23 14:44:06.396368'),(22,'sessions','0001_initial','2024-05-23 14:44:06.492611'),(23,'bosquetaoista','0005_alter_personaextra_comentario','2024-05-28 21:25:31.939389'),(24,'bosquetaoista','0006_alter_personaextra_comentario','2024-05-28 21:27:54.782929'),(25,'bosquetaoista','0007_persona_imagen','2024-06-08 21:56:30.045431'),(26,'bosquetaoista','0008_alter_persona_imagen','2024-06-10 15:15:05.802884'),(27,'bosquetaoista','0009_alter_persona_imagen','2024-06-10 15:15:05.923279'),(28,'bosquetaoista','0010_alter_persona_imagen','2024-06-10 15:15:06.041828'),(29,'bosquetaoista','0011_alter_persona_imagen','2024-06-10 15:15:06.175839'),(30,'bosquetaoista','0012_alter_persona_imagen','2024-06-10 15:24:54.900642'),(31,'bosquetaoista','0013_alter_persona_imagen','2024-06-10 17:06:27.136512'),(32,'bosquetaoista','0014_alter_persona_imagen','2024-06-10 17:06:27.231906'),(33,'bosquetaoista','0015_rename_imagen_persona_foto','2024-06-10 17:06:27.304006'),(34,'bosquetaoista','0016_alter_agenda_orador','2024-06-12 14:39:07.773909'),(35,'bosquetaoista','0017_alter_agenda_orador','2024-06-12 14:39:07.956959'),(36,'bosquetaoista','0018_tabla','2024-06-13 18:56:42.039423'),(37,'bosquetaoista','0019_tabla_codigo','2024-06-13 18:56:42.139067'),(38,'bosquetaoista','0020_remove_tabla_codigo','2024-06-13 18:56:42.176992'),(39,'bosquetaoista','0021_tabla_codigo_tabla_nombre','2024-06-13 18:56:42.245025'),(40,'bosquetaoista','0022_delete_tabla','2024-06-13 18:56:42.298758'),(41,'bosquetaoista','0023_tabla','2024-06-15 18:45:31.718211'),(42,'bosquetaoista','0024_delete_tabla','2024-06-15 18:54:23.953073'),(43,'bosquetaoista','0025_alter_persona_foto','2024-06-19 18:27:03.528485'),(44,'bosquetaoista','0026_frase','2024-06-26 13:14:43.821535'),(45,'bosquetaoista','0027_alter_frase_detalle_alter_frase_frase','2024-06-26 14:41:20.889853'),(46,'bosquetaoista','0028_persona_foto2','2024-08-22 16:01:01.074449'),(47,'bosquetaoista','0029_remove_persona_foto','2024-08-22 20:27:41.023129'),(48,'bosquetaoista','0030_rename_foto2_persona_foto','2024-08-22 20:28:10.588778'),(49,'bosquetaoista','0031_auto_20240825_1746','2024-08-25 20:46:53.921155');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-17 19:16:34
