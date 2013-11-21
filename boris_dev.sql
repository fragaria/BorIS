-- MySQL dump 10.13  Distrib 5.1.72, for debian-linux-gnu (i486)
--
-- Host: localhost    Database: boris
-- ------------------------------------------------------
-- Server version	5.1.72-2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (1,'Terén');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_425ae3c4` (`group_id`),
  KEY `auth_group_permissions_1e014c8f` (`permission_id`)
) ENGINE=MyISAM AUTO_INCREMENT=155 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (145,1,111),(144,1,110),(143,1,109),(142,1,108),(141,1,107),(140,1,106),(139,1,105),(138,1,104),(137,1,103),(136,1,99),(135,1,98),(134,1,97),(133,1,96),(132,1,95),(131,1,94),(130,1,93),(129,1,92),(128,1,91),(127,1,90),(126,1,89),(125,1,88),(124,1,87),(123,1,86),(122,1,85),(121,1,84),(120,1,83),(119,1,82),(118,1,81),(117,1,80),(116,1,79),(115,1,78),(114,1,77),(113,1,76),(112,1,75),(111,1,74),(110,1,73),(109,1,72),(108,1,71),(107,1,70),(106,1,68),(105,1,65),(104,1,63),(103,1,62),(102,1,61),(101,1,60),(100,1,59),(99,1,58),(98,1,57),(97,1,56),(96,1,55),(95,1,53),(94,1,51),(93,1,50),(148,1,114),(147,1,113),(146,1,112),(92,1,49),(91,1,48),(90,1,47),(89,1,46),(88,1,44),(87,1,41),(86,1,38),(85,1,35),(84,1,32),(83,1,141),(82,1,140),(81,1,139),(80,1,135),(79,1,134),(78,1,133),(77,1,132),(76,1,131),(75,1,130),(149,1,115),(150,1,116),(151,1,117),(152,1,124),(153,1,125),(154,1,126);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_message`
--

DROP TABLE IF EXISTS `auth_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `auth_message_403f60f` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_message`
--

LOCK TABLES `auth_message` WRITE;
/*!40000 ALTER TABLE `auth_message` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_1bb8f392` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=142 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add message',5,'add_message'),(14,'Can change message',5,'change_message'),(15,'Can delete message',5,'delete_message'),(16,'Can add content type',6,'add_contenttype'),(17,'Can change content type',6,'change_contenttype'),(18,'Can delete content type',6,'delete_contenttype'),(19,'Can add session',7,'add_session'),(20,'Can change session',7,'change_session'),(21,'Can delete session',7,'delete_session'),(22,'Can add site',8,'add_site'),(23,'Can change site',8,'change_site'),(24,'Can delete site',8,'delete_site'),(25,'Can add redirect',9,'add_redirect'),(26,'Can change redirect',9,'change_redirect'),(27,'Can delete redirect',9,'delete_redirect'),(28,'Can add migration history',10,'add_migrationhistory'),(29,'Can change migration history',10,'change_migrationhistory'),(30,'Can delete migration history',10,'delete_migrationhistory'),(31,'Can add Droga',11,'add_drug'),(32,'Can change Droga',11,'change_drug'),(33,'Can delete Droga',11,'delete_drug'),(34,'Can add Rizikové chování',12,'add_riskybehavior'),(35,'Can change Rizikové chování',12,'change_riskybehavior'),(36,'Can delete Rizikové chování',12,'delete_riskybehavior'),(37,'Can add Kraj',13,'add_region'),(38,'Can change Kraj',13,'change_region'),(39,'Can delete Kraj',13,'delete_region'),(40,'Can add Okres',14,'add_district'),(41,'Can change Okres',14,'change_district'),(42,'Can delete Okres',14,'delete_district'),(43,'Can add Město',15,'add_town'),(44,'Can change Město',15,'change_town'),(45,'Can delete Město',15,'delete_town'),(46,'Can add Osoba',16,'add_person'),(47,'Can change Osoba',16,'change_person'),(48,'Can delete Osoba',16,'delete_person'),(49,'Can add Odborný kontakt',17,'add_practitionercontact'),(50,'Can change Odborný kontakt',17,'change_practitionercontact'),(51,'Can delete Odborný kontakt',17,'delete_practitionercontact'),(52,'Can add Anonym',18,'add_anonymous'),(53,'Can change Anonym',18,'change_anonymous'),(54,'Can delete Anonym',18,'delete_anonymous'),(55,'Can add Klient',19,'add_client'),(56,'Can change Klient',19,'change_client'),(57,'Can delete Klient',19,'delete_client'),(58,'Can add Anamnéza',20,'add_anamnesis'),(59,'Can change Anamnéza',20,'change_anamnesis'),(60,'Can delete Anamnéza',20,'delete_anamnesis'),(61,'Can add Poznámka',21,'add_clientnote'),(62,'Can change Poznámka',21,'change_clientnote'),(63,'Can delete Poznámka',21,'delete_clientnote'),(64,'Can add Užívaná droga',22,'add_drugusage'),(65,'Can change Užívaná droga',22,'change_drugusage'),(66,'Can delete Užívaná droga',22,'delete_drugusage'),(67,'Can add Rizikové chování',23,'add_riskymanners'),(68,'Can change Rizikové chování',23,'change_riskymanners'),(69,'Can delete Rizikové chování',23,'delete_riskymanners'),(70,'Can add Vyšetření onemocnění',24,'add_diseasetest'),(71,'Can change Vyšetření onemocnění',24,'change_diseasetest'),(72,'Can delete Vyšetření onemocnění',24,'delete_diseasetest'),(73,'Can add Kontakt',25,'add_encounter'),(74,'Can change Kontakt',25,'change_encounter'),(75,'Can delete Kontakt',25,'delete_encounter'),(76,'Can add service',26,'add_service'),(77,'Can change service',26,'change_service'),(78,'Can delete service',26,'delete_service'),(79,'Can add Harm Reduction',27,'add_harmreduction'),(80,'Can change Harm Reduction',27,'change_harmreduction'),(81,'Can delete Harm Reduction',27,'delete_harmreduction'),(82,'Can add Vstupní zhodnocení stavu klienta',26,'add_incomeexamination'),(83,'Can change Vstupní zhodnocení stavu klienta',26,'change_incomeexamination'),(84,'Can delete Vstupní zhodnocení stavu klienta',26,'delete_incomeexamination'),(85,'Can add Testování infekčních nemocí',28,'add_diseasetest'),(86,'Can change Testování infekčních nemocí',28,'change_diseasetest'),(87,'Can delete Testování infekčních nemocí',28,'delete_diseasetest'),(88,'Can add Asistenční služba',29,'add_asistservice'),(89,'Can change Asistenční služba',29,'change_asistservice'),(90,'Can delete Asistenční služba',29,'delete_asistservice'),(91,'Can add Informační servis',30,'add_informationservice'),(92,'Can change Informační servis',30,'change_informationservice'),(93,'Can delete Informační servis',30,'delete_informationservice'),(94,'Can add Kontaktní práce',26,'add_contactwork'),(95,'Can change Kontaktní práce',26,'change_contactwork'),(96,'Can delete Kontaktní práce',26,'delete_contactwork'),(97,'Can add Krizová intervence',31,'add_crisisintervention'),(98,'Can change Krizová intervence',31,'change_crisisintervention'),(99,'Can delete Krizová intervence',31,'delete_crisisintervention'),(141,'Can change phone usage',46,'change_phoneusage'),(140,'Can delete phone usage',46,'delete_phoneusage'),(139,'Can add phone usage',46,'add_phoneusage'),(103,'Can add Sociální práce',32,'add_socialwork'),(104,'Can change Sociální práce',32,'change_socialwork'),(105,'Can delete Sociální práce',32,'delete_socialwork'),(106,'Can add Další úkony',26,'add_utilitywork'),(107,'Can change Další úkony',26,'change_utilitywork'),(108,'Can delete Další úkony',26,'delete_utilitywork'),(109,'Can add Základní zdravotní ošetření',26,'add_basicmedicaltreatment'),(110,'Can change Základní zdravotní ošetření',26,'change_basicmedicaltreatment'),(111,'Can delete Základní zdravotní ošetření',26,'delete_basicmedicaltreatment'),(112,'Can add Individuální poradenství',26,'add_individualcounseling'),(113,'Can change Individuální poradenství',26,'change_individualcounseling'),(114,'Can delete Individuální poradenství',26,'delete_individualcounseling'),(115,'Can add Oslovení',26,'add_address'),(116,'Can change Oslovení',26,'change_address'),(117,'Can delete Oslovení',26,'delete_address'),(118,'Can add search encounter',40,'add_searchencounter'),(119,'Can change search encounter',40,'change_searchencounter'),(120,'Can delete search encounter',40,'delete_searchencounter'),(121,'Can add search service',41,'add_searchservice'),(122,'Can change search service',41,'change_searchservice'),(123,'Can delete search service',41,'delete_searchservice'),(124,'Can add syringe collection',42,'add_syringecollection'),(125,'Can change syringe collection',42,'change_syringecollection'),(126,'Can delete syringe collection',42,'delete_syringecollection'),(127,'Can add search syringe collection',43,'add_searchsyringecollection'),(128,'Can change search syringe collection',43,'change_searchsyringecollection'),(129,'Can delete search syringe collection',43,'delete_searchsyringecollection'),(130,'Can add Krizová intervence',26,'add_crisisintervention'),(131,'Can change Krizová intervence',26,'change_crisisintervention'),(132,'Can delete Krizová intervence',26,'delete_crisisintervention'),(133,'Can add Odkazy',36,'add_utilitywork'),(134,'Can change Odkazy',36,'change_utilitywork'),(135,'Can delete Odkazy',36,'delete_utilitywork');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'hynek','','','hynek.urban@fragaria.cz','sha1$20dc0$959c544ad9cd05a9dc117cf378140baddc86cd68',1,1,1,'2012-01-04 11:31:57','2012-01-03 20:52:31'),(2,'test','','','','sha1$a2b0c$ae35c5764e9f8f41da4f69a88e5c86bd6bf4ca3f',1,1,0,'2013-08-21 11:56:48','2012-01-04 11:32:09'),(3,'admin','','','admin@fragaria.cz','sha1$0dbbe$21668545ffae18551e361962baa6d9ddf96cf3be',1,1,1,'2013-11-18 09:57:22','2012-01-22 19:30:46'),(4,'OndrejSulc','Ondřej','Šulc','sulc@os-semiramis.cz','sha1$ab2a1$f6e04326a598065c6d8ad2bacd52fb34a83faa66',1,1,1,'2013-10-22 12:10:17','2012-03-02 11:02:40'),(8,'LukasVerner','Lukáš','Verner','','sha1$5a593$eb591ebd4080410626710a61d4b9f309ac1bd8ee',1,1,0,'2012-10-11 09:20:42','2012-09-20 12:38:23'),(9,'TerezaMullerova','Tereza','Müllerová','','sha1$85c64$7f125f23f541987eb981e401f3d9135f2726fa25',1,1,0,'2012-09-20 12:43:31','2012-09-20 12:42:08'),(10,'MonikaZaveska','Monika','Záveská','','sha1$77a76$8a05363a9d908ba1f2794dd7914f48db08d77a77',1,1,0,'2012-11-01 10:01:24','2012-09-20 12:42:56');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_403f60f` (`user_id`),
  KEY `auth_user_groups_425ae3c4` (`group_id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
INSERT INTO `auth_user_groups` VALUES (3,8,1),(4,9,1),(6,10,1);
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_403f60f` (`user_id`),
  KEY `auth_user_user_permissions_1e014c8f` (`permission_id`)
) ENGINE=MyISAM AUTO_INCREMENT=552 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
INSERT INTO `auth_user_user_permissions` VALUES (1,2,31),(2,2,32),(3,2,33),(4,2,34),(5,2,35),(6,2,36),(7,2,37),(8,2,38),(9,2,39),(10,2,40),(11,2,41),(12,2,42),(13,2,43),(14,2,44),(15,2,45),(16,2,46),(17,2,47),(18,2,48),(19,2,49),(20,2,50),(21,2,51),(22,2,52),(23,2,53),(24,2,54),(25,2,55),(26,2,56),(27,2,57),(28,2,58),(29,2,59),(30,2,60),(31,2,61),(32,2,62),(33,2,63),(34,2,64),(35,2,65),(36,2,66),(37,2,67),(38,2,68),(39,2,69),(40,2,70),(41,2,71),(42,2,72),(43,2,73),(44,2,74),(45,2,75),(46,2,76),(47,2,77),(48,2,78),(49,2,79),(50,2,80),(51,2,81),(52,2,82),(53,2,83),(54,2,84),(55,2,85),(56,2,86),(57,2,87),(58,2,88),(59,2,89),(60,2,90),(61,2,91),(62,2,92),(63,2,93),(64,2,94),(65,2,95),(66,2,96),(67,2,97),(68,2,98),(69,2,99),(73,2,103),(74,2,104),(75,2,105),(76,2,106),(77,2,107),(78,2,108),(79,2,109),(80,2,110),(81,2,111),(82,2,112),(83,2,113),(84,2,114),(85,2,115),(86,2,116),(87,2,117),(88,2,118),(89,2,119),(90,2,120),(91,2,121),(92,2,122),(93,2,123),(94,2,124),(95,2,125),(96,2,126);
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clients_anamnesis`
--

DROP TABLE IF EXISTS `clients_anamnesis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clients_anamnesis` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  `client_id` int(11) NOT NULL,
  `filled_when` date NOT NULL,
  `filled_where_id` int(11) NOT NULL,
  `author_id` int(11) NOT NULL,
  `nationality` smallint(5) unsigned NOT NULL,
  `ethnic_origin` smallint(5) unsigned NOT NULL,
  `living_condition` smallint(5) unsigned NOT NULL,
  `accomodation` smallint(5) unsigned NOT NULL,
  `lives_with_junkies` tinyint(1) DEFAULT NULL,
  `employment` smallint(5) unsigned NOT NULL,
  `education` smallint(5) unsigned NOT NULL,
  `been_cured_before` tinyint(1) NOT NULL,
  `been_cured_currently` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `client_id` (`client_id`),
  KEY `clients_anamnesis_7d456570` (`filled_where_id`),
  KEY `clients_anamnesis_337b96ff` (`author_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clients_anamnesis`
--

LOCK TABLES `clients_anamnesis` WRITE;
/*!40000 ALTER TABLE `clients_anamnesis` DISABLE KEYS */;
INSERT INTO `clients_anamnesis` VALUES (4,'2013-09-23 13:11:42','2013-09-25 13:37:17',874,'2013-08-15',32,3,1,3,2,1,0,5,1,1,0);
/*!40000 ALTER TABLE `clients_anamnesis` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clients_anonymous`
--

DROP TABLE IF EXISTS `clients_anonymous`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clients_anonymous` (
  `person_ptr_id` int(11) NOT NULL,
  `drug_user_type` smallint(5) unsigned NOT NULL,
  `sex` smallint(5) unsigned NOT NULL,
  PRIMARY KEY (`person_ptr_id`),
  UNIQUE KEY `sex` (`sex`,`drug_user_type`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clients_anonymous`
--

LOCK TABLES `clients_anonymous` WRITE;
/*!40000 ALTER TABLE `clients_anonymous` DISABLE KEYS */;
INSERT INTO `clients_anonymous` VALUES (1,1,1),(2,4,1),(3,2,1),(4,3,1),(5,1,2),(6,4,2),(7,2,2),(8,3,2);
/*!40000 ALTER TABLE `clients_anonymous` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clients_client`
--

DROP TABLE IF EXISTS `clients_client`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clients_client` (
  `person_ptr_id` int(11) NOT NULL,
  `code` varchar(63) NOT NULL,
  `sex` smallint(5) unsigned NOT NULL,
  `first_name` varchar(63) DEFAULT NULL,
  `last_name` varchar(63) DEFAULT NULL,
  `birthdate` date DEFAULT NULL,
  `birthdate_year_only` tinyint(1) NOT NULL,
  `town_id` int(11) NOT NULL,
  `primary_drug_id` int(11) DEFAULT NULL,
  `primary_drug_usage` smallint(5) unsigned DEFAULT NULL,
  `close_person` tinyint(1) NOT NULL DEFAULT '0',
  `sex_partner` tinyint(1) NOT NULL,
  PRIMARY KEY (`person_ptr_id`),
  UNIQUE KEY `code` (`code`),
  KEY `clients_client_1fb3d69c` (`town_id`),
  KEY `clients_client_6c32ab63` (`primary_drug_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clients_client`
--

LOCK TABLES `clients_client` WRITE;
/*!40000 ALTER TABLE `clients_client` DISABLE KEYS */;
INSERT INTO `clients_client` VALUES (885,'PPP01QQQ02',2,'','',NULL,0,46,3,1,0,0),(884,'MMM01NNN02',2,'','',NULL,0,31,3,1,0,0),(883,'JJJ01KKK02',2,'','',NULL,0,46,3,1,0,0),(882,'HHH01III02',2,'','',NULL,0,31,3,1,0,0),(880,'DDD01EEE02',1,'','',NULL,0,47,3,1,0,0),(881,'FFF01GGG02',2,'','',NULL,0,34,3,1,0,0),(879,'CCC01CCC02',1,'','',NULL,0,42,3,1,0,0),(876,'XXX01XXX02',2,'','',NULL,0,39,3,1,0,0),(877,'ZZZ01ZZZ02',1,'','',NULL,0,32,4,1,0,0),(878,'LLL01LLL02',2,'','',NULL,0,32,3,1,0,0),(875,'BBB01BBB02',2,'','',NULL,0,34,3,1,0,0),(874,'AAA01AAA02',1,'','','1993-01-01',1,38,11,1,0,0),(886,'1234567ABCD',2,'','','1990-01-01',1,46,3,3,0,0),(887,'123456789000AAA',1,'Lenka','??','1990-01-01',1,46,9,3,0,0);
/*!40000 ALTER TABLE `clients_client` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clients_clientnote`
--

DROP TABLE IF EXISTS `clients_clientnote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clients_clientnote` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `author_id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `datetime` datetime NOT NULL,
  `text` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `clients_clientnote_337b96ff` (`author_id`),
  KEY `clients_clientnote_4a4e8ffb` (`client_id`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clients_clientnote`
--

LOCK TABLES `clients_clientnote` WRITE;
/*!40000 ALTER TABLE `clients_clientnote` DISABLE KEYS */;
INSERT INTO `clients_clientnote` VALUES (8,3,887,'2013-10-14 13:31:00','Zatím toho nevíme moc.'),(7,3,886,'2013-10-14 13:25:00','Klient není příliš sdílný ohledně své rodiny.');
/*!40000 ALTER TABLE `clients_clientnote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clients_diseasetest`
--

DROP TABLE IF EXISTS `clients_diseasetest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clients_diseasetest` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `anamnesis_id` int(11) NOT NULL,
  `disease` smallint(5) unsigned NOT NULL,
  `result` smallint(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `disease` (`disease`,`anamnesis_id`),
  KEY `clients_diseasetest_38fae9c6` (`anamnesis_id`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clients_diseasetest`
--

LOCK TABLES `clients_diseasetest` WRITE;
/*!40000 ALTER TABLE `clients_diseasetest` DISABLE KEYS */;
INSERT INTO `clients_diseasetest` VALUES (8,4,2,0),(7,4,1,0),(9,4,3,3),(10,4,4,2);
/*!40000 ALTER TABLE `clients_diseasetest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clients_district`
--

DROP TABLE IF EXISTS `clients_district`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clients_district` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `region_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `clients_district_9574fce` (`region_id`)
) ENGINE=MyISAM AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clients_district`
--

LOCK TABLES `clients_district` WRITE;
/*!40000 ALTER TABLE `clients_district` DISABLE KEYS */;
INSERT INTO `clients_district` VALUES (17,'Mladá Boleslav',9),(16,'Mělník',9),(15,'Praha - východ',9),(21,'Nymburk',9);
/*!40000 ALTER TABLE `clients_district` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clients_drug`
--

DROP TABLE IF EXISTS `clients_drug`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clients_drug` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clients_drug`
--

LOCK TABLES `clients_drug` WRITE;
/*!40000 ALTER TABLE `clients_drug` DISABLE KEYS */;
INSERT INTO `clients_drug` VALUES (3,'Pervitin, jiné amfetaminy'),(4,'Subutex , Ravata, Buprenorphine alkaloid - legálně'),(5,'Tabák'),(14,'Subutex , Ravata, Buprenorphine alkaloid - ilegálně'),(8,'THC'),(9,'Extáze, LSD, lysohlávky'),(10,'Designer drugs'),(11,'Heroin'),(12,'Braun a jiné opiáty'),(13,'Surové opium'),(15,'Cigarety'),(16,'Alkohol'),(17,'Inhalační látky, ředidla'),(18,'Medikamenty'),(19,'Metadon'),(20,'Kokain, crack'),(21,'Suboxone');
/*!40000 ALTER TABLE `clients_drug` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clients_drugusage`
--

DROP TABLE IF EXISTS `clients_drugusage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clients_drugusage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `drug_id` int(11) NOT NULL,
  `anamnesis_id` int(11) NOT NULL,
  `application` smallint(5) unsigned NOT NULL,
  `frequency` smallint(5) unsigned NOT NULL,
  `first_try_age` smallint(5) unsigned NOT NULL,
  `first_try_iv_age` smallint(5) unsigned DEFAULT NULL,
  `first_try_application` smallint(5) unsigned NOT NULL,
  `was_first_illegal` tinyint(1) DEFAULT NULL,
  `is_primary` tinyint(1) NOT NULL,
  `note` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `drug_id` (`drug_id`,`anamnesis_id`),
  KEY `clients_drugusage_2f30f036` (`drug_id`),
  KEY `clients_drugusage_38fae9c6` (`anamnesis_id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clients_drugusage`
--

LOCK TABLES `clients_drugusage` WRITE;
/*!40000 ALTER TABLE `clients_drugusage` DISABLE KEYS */;
INSERT INTO `clients_drugusage` VALUES (6,3,4,1,5,15,16,4,0,1,''),(5,8,4,5,6,12,NULL,5,1,0,''),(7,11,4,1,11,17,17,1,0,0,'');
/*!40000 ALTER TABLE `clients_drugusage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clients_person`
--

DROP TABLE IF EXISTS `clients_person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clients_person` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  `title` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `clients_person_1bb8f392` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=888 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clients_person`
--

LOCK TABLES `clients_person` WRITE;
/*!40000 ALTER TABLE `clients_person` DISABLE KEYS */;
INSERT INTO `clients_person` VALUES (1,'2013-11-18 14:40:53','2013-11-18 14:40:53','žena - neuživatel',18),(2,'2013-11-18 14:40:53','2013-11-18 14:40:53','žena - rodič',18),(3,'2013-11-18 14:40:53','2013-11-18 14:40:53','žena - neIV uživatelka',18),(4,'2013-11-18 14:40:53','2013-11-18 14:40:53','žena - IV uživatelka',18),(5,'2013-11-18 14:40:53','2013-11-18 14:40:53','muž - neuživatel',18),(6,'2013-11-18 14:40:53','2013-11-18 14:40:53','muž - rodič',18),(7,'2013-11-18 14:40:53','2013-11-18 14:40:53','muž - neIV uživatel',18),(8,'2013-11-18 14:40:53','2013-11-18 14:40:53','muž - IV uživatel',18),(886,'2013-10-14 13:25:12','2013-10-14 13:25:37','1234567ABCD',19),(885,'2013-09-23 12:35:44','2013-09-23 12:35:44','PPP01QQQ02',19),(883,'2013-09-23 12:35:08','2013-09-23 12:35:08','JJJ01KKK02',19),(884,'2013-09-23 12:35:30','2013-09-23 12:35:30','MMM01NNN02',19),(882,'2013-09-23 12:34:50','2013-09-23 12:34:50','HHH01III02',19),(881,'2013-09-23 12:34:33','2013-09-23 12:34:33','FFF01GGG02',19),(880,'2013-09-23 12:34:12','2013-09-23 12:34:12','DDD01EEE02',19),(879,'2013-09-23 12:33:52','2013-09-23 12:33:52','CCC01CCC02',19),(876,'2013-09-23 12:33:02','2013-09-23 12:33:02','XXX01XXX02',19),(878,'2013-09-23 12:33:35','2013-09-23 12:33:35','LLL01LLL02',19),(874,'2013-09-23 12:30:08','2013-09-23 13:13:19','AAA01AAA02',19),(877,'2013-09-23 12:33:21','2013-09-23 12:33:21','ZZZ01ZZZ02',19),(875,'2013-09-23 12:32:47','2013-09-23 12:32:47','BBB01BBB02',19),(887,'2013-10-14 13:31:09','2013-10-14 13:31:27','123456789000AAA',19);
/*!40000 ALTER TABLE `clients_person` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clients_practitionercontact`
--

DROP TABLE IF EXISTS `clients_practitionercontact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clients_practitionercontact` (
  `note` longtext NOT NULL,
  `town_id` int(11) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_or_institution` varchar(255) NOT NULL,
  `date` date NOT NULL,
  UNIQUE KEY `clients_practitioner_id_6ddb43d9_uniq` (`id`),
  KEY `clients_practitioner_1fb3d69c` (`town_id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clients_practitionercontact`
--

LOCK TABLES `clients_practitionercontact` WRITE;
/*!40000 ALTER TABLE `clients_practitionercontact` DISABLE KEYS */;
INSERT INTO `clients_practitionercontact` VALUES ('MÚ',34,5,'Śárka Špírková','2012-02-01'),('mladá, sympatická',34,1,'lékárna náměstí 1','2012-08-20'),('mladá, sympatická',31,2,'lékárna náměstí 1','2012-06-06'),('mladá, sympatická',31,3,'lékárna náměstí 1','2012-05-27'),('mladá, sympatická',31,4,'lékárna náměstí 1','2012-02-17'),('MÚ',31,6,'Śárka Špírková','2012-01-11'),('Příjemný rozhovor.',31,7,'Zástupce semiramis OS','2013-08-02');
/*!40000 ALTER TABLE `clients_practitionercontact` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clients_practitionercontact_users`
--

DROP TABLE IF EXISTS `clients_practitionercontact_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clients_practitionercontact_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `practitionercontact_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `clients_practitioner_users_practitioner_id_b67713b_uniq` (`practitionercontact_id`,`user_id`),
  KEY `clients_practitioner_users_3ac71230` (`practitionercontact_id`),
  KEY `clients_practitioner_users_403f60f` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COLLATE=utf8_czech_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clients_practitionercontact_users`
--

LOCK TABLES `clients_practitionercontact_users` WRITE;
/*!40000 ALTER TABLE `clients_practitionercontact_users` DISABLE KEYS */;
INSERT INTO `clients_practitionercontact_users` VALUES (1,1,2),(2,2,3),(3,3,2),(4,4,2),(5,5,2),(6,6,2),(7,7,8);
/*!40000 ALTER TABLE `clients_practitionercontact_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clients_region`
--

DROP TABLE IF EXISTS `clients_region`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clients_region` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clients_region`
--

LOCK TABLES `clients_region` WRITE;
/*!40000 ALTER TABLE `clients_region` DISABLE KEYS */;
INSERT INTO `clients_region` VALUES (9,'Středočeský'),(10,'Pardubický'),(11,'Královéhradecký');
/*!40000 ALTER TABLE `clients_region` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clients_riskybehavior`
--

DROP TABLE IF EXISTS `clients_riskybehavior`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clients_riskybehavior` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clients_riskybehavior`
--

LOCK TABLES `clients_riskybehavior` WRITE;
/*!40000 ALTER TABLE `clients_riskybehavior` DISABLE KEYS */;
INSERT INTO `clients_riskybehavior` VALUES (1,'sdílení náčiní'),(2,'nechráněný sex'),(3,'sdílení jehel'),(4,'nitrožilní aplikace'),(5,'riziková aplikace'),(6,'předávkování'),(7,'zdravotní komplikace');
/*!40000 ALTER TABLE `clients_riskybehavior` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clients_riskymanners`
--

DROP TABLE IF EXISTS `clients_riskymanners`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clients_riskymanners` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `behavior_id` int(11) NOT NULL,
  `anamnesis_id` int(11) NOT NULL,
  `periodicity` smallint(5) unsigned DEFAULT NULL,
  `periodicity_in_past` int(10) unsigned,
  `periodicity_in_present` int(10) unsigned,
  PRIMARY KEY (`id`),
  UNIQUE KEY `behavior_id` (`behavior_id`,`anamnesis_id`),
  KEY `clients_riskymanners_1675d4f6` (`behavior_id`),
  KEY `clients_riskymanners_38fae9c6` (`anamnesis_id`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clients_riskymanners`
--

LOCK TABLES `clients_riskymanners` WRITE;
/*!40000 ALTER TABLE `clients_riskymanners` DISABLE KEYS */;
INSERT INTO `clients_riskymanners` VALUES (4,1,4,NULL,1,1),(5,2,4,NULL,2,5),(6,7,4,NULL,1,4),(7,4,4,NULL,3,5),(8,3,4,NULL,3,5),(9,6,4,NULL,2,5);
/*!40000 ALTER TABLE `clients_riskymanners` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clients_town`
--

DROP TABLE IF EXISTS `clients_town`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clients_town` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) CHARACTER SET utf8 NOT NULL,
  `district_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `clients_town_1f903cfa` (`district_id`)
) ENGINE=MyISAM AUTO_INCREMENT=51 DEFAULT CHARSET=utf8 COLLATE=utf8_czech_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clients_town`
--

LOCK TABLES `clients_town` WRITE;
/*!40000 ALTER TABLE `clients_town` DISABLE KEYS */;
INSERT INTO `clients_town` VALUES (34,'Neratovice',16),(33,'Mladá Boleslav',17),(32,'Mělník',16),(31,'Čelákovice',15),(46,'Brandýs nad Labem - Stará Boleslav',15),(38,'Bělá pod Bezdězem',17),(39,'Kralupy nad Vltavou',16),(42,'Bakov nad Jizerou',17),(47,'Mnichovo Hradiště',17),(48,'Benátky nad Jizerou',17);
/*!40000 ALTER TABLE `clients_town` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_403f60f` (`user_id`),
  KEY `django_admin_log_1bb8f392` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=607 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2012-01-04 11:32:09',1,4,'2','test',1,''),(2,'2012-01-04 11:33:07',1,4,'2','test',2,'Změněno: is_staff a user_permissions'),(3,'2012-01-04 13:12:51',2,13,'4','Středočeský',1,''),(4,'2012-01-04 13:12:53',2,14,'7','Mělník, Středočeský',1,''),(5,'2012-01-04 13:12:54',2,15,'15','Mělník (Mělník)',1,''),(6,'2012-01-04 13:13:04',2,25,'6001','muž - IV',1,''),(7,'2012-01-04 13:13:58',2,25,'6001','muž - IV',2,'Změněno: performed_on'),(8,'2012-01-04 13:16:45',2,19,'429','BLA01BLA02',1,''),(9,'2012-01-04 13:27:31',2,25,'6002','BLA01BLA02',1,''),(10,'2012-01-04 13:28:13',2,25,'6002','BLA01BLA02',2,'Změněno: performed_on'),(11,'2012-01-04 13:31:44',2,17,'430','MP1',1,''),(12,'2012-01-04 13:34:27',2,25,'6003','MP1',1,''),(13,'2012-01-04 18:17:40',2,19,'429','BLA01BLA02',2,'Pole \"performed_on\" pro položku \"BLA01BLA02\" typu Kontakt změněno/změněna.'),(14,'2012-01-04 18:20:52',2,25,'6004','BLA01BLA02',1,''),(15,'2012-01-04 19:20:49',2,25,'12005','muž - neuživatel',1,''),(16,'2012-01-04 19:44:25',2,25,'12006','muž - IV',1,''),(17,'2012-01-04 19:45:46',2,25,'12007','Client395',1,''),(18,'2012-01-04 19:54:48',2,42,'1','test - 2012-01-05 (12 Ks )',1,''),(19,'2012-01-04 19:55:10',2,42,'2','test - 2012-01-12 (30 Ks za mostem)',1,''),(20,'2012-01-04 19:57:37',2,42,'2','test - 2012-01-12 (30 Ks za mostem)',2,'Nebyla změněna žádná pole.'),(21,'2012-01-05 10:18:10',2,13,'8','Hlavní město Praha',1,''),(22,'2012-01-05 10:18:12',2,14,'14','Hlavní město Praha, Hlavní město Praha',1,''),(23,'2012-01-05 10:18:13',2,15,'30','Praha (Hlavní město Praha)',1,''),(24,'2012-01-11 11:55:38',2,19,'630','CODE200',3,''),(25,'2012-01-11 11:55:38',2,19,'629','CODE199',3,''),(26,'2012-01-11 11:55:38',2,19,'628','CODE198',3,''),(27,'2012-01-11 11:55:38',2,19,'627','CODE197',3,''),(28,'2012-01-11 11:55:38',2,19,'626','CODE196',3,''),(29,'2012-01-11 11:55:38',2,19,'625','CODE195',3,''),(30,'2012-01-11 11:55:38',2,19,'624','CODE194',3,''),(31,'2012-01-11 11:55:38',2,19,'623','CODE193',3,''),(32,'2012-01-11 11:55:38',2,19,'622','CODE192',3,''),(33,'2012-01-11 11:55:38',2,19,'621','CODE191',3,''),(34,'2012-01-11 11:55:38',2,19,'620','CODE190',3,''),(35,'2012-01-11 11:55:38',2,19,'619','CODE189',3,''),(36,'2012-01-11 11:55:38',2,19,'618','CODE188',3,''),(37,'2012-01-11 11:55:38',2,19,'617','CODE187',3,''),(38,'2012-01-11 11:55:38',2,19,'616','CODE186',3,''),(39,'2012-01-11 11:55:38',2,19,'615','CODE185',3,''),(40,'2012-01-11 11:55:38',2,19,'614','CODE184',3,''),(41,'2012-01-11 11:55:38',2,19,'613','CODE183',3,''),(42,'2012-01-11 11:55:38',2,19,'612','CODE182',3,''),(43,'2012-01-11 11:55:38',2,19,'611','CODE181',3,''),(44,'2012-01-11 11:55:38',2,19,'610','CODE180',3,''),(45,'2012-01-11 11:55:38',2,19,'609','CODE179',3,''),(46,'2012-01-11 11:55:38',2,19,'608','CODE178',3,''),(47,'2012-01-11 11:55:38',2,19,'607','CODE177',3,''),(48,'2012-01-11 11:55:38',2,19,'606','CODE176',3,''),(49,'2012-01-11 11:55:38',2,19,'605','CODE175',3,''),(50,'2012-01-11 11:55:38',2,19,'604','CODE174',3,''),(51,'2012-01-11 11:55:38',2,19,'603','CODE173',3,''),(52,'2012-01-11 11:55:38',2,19,'602','CODE172',3,''),(53,'2012-01-11 11:55:38',2,19,'601','CODE171',3,''),(54,'2012-01-11 11:55:38',2,19,'600','CODE170',3,''),(55,'2012-01-11 11:55:38',2,19,'599','CODE169',3,''),(56,'2012-01-11 11:55:38',2,19,'598','CODE168',3,''),(57,'2012-01-11 11:55:38',2,19,'597','CODE167',3,''),(58,'2012-01-11 11:55:38',2,19,'596','CODE166',3,''),(59,'2012-01-11 11:55:38',2,19,'595','CODE165',3,''),(60,'2012-01-11 11:55:38',2,19,'594','CODE164',3,''),(61,'2012-01-11 11:55:38',2,19,'593','CODE163',3,''),(62,'2012-01-11 11:55:38',2,19,'592','CODE162',3,''),(63,'2012-01-11 11:55:38',2,19,'591','CODE161',3,''),(64,'2012-01-11 11:55:38',2,19,'590','CODE160',3,''),(65,'2012-01-11 11:55:38',2,19,'589','CODE159',3,''),(66,'2012-01-11 11:55:38',2,19,'588','CODE158',3,''),(67,'2012-01-11 11:55:38',2,19,'587','CODE157',3,''),(68,'2012-01-11 11:55:38',2,19,'586','CODE156',3,''),(69,'2012-01-11 11:55:38',2,19,'585','CODE155',3,''),(70,'2012-01-11 11:55:38',2,19,'584','CODE154',3,''),(71,'2012-01-11 11:55:38',2,19,'583','CODE153',3,''),(72,'2012-01-11 11:55:38',2,19,'582','CODE152',3,''),(73,'2012-01-11 11:55:38',2,19,'581','CODE151',3,''),(74,'2012-01-11 11:55:38',2,19,'580','CODE150',3,''),(75,'2012-01-11 11:55:38',2,19,'579','CODE149',3,''),(76,'2012-01-11 11:55:38',2,19,'578','CODE148',3,''),(77,'2012-01-11 11:55:38',2,19,'577','CODE147',3,''),(78,'2012-01-11 11:55:38',2,19,'576','CODE146',3,''),(79,'2012-01-11 11:55:38',2,19,'575','CODE145',3,''),(80,'2012-01-11 11:55:38',2,19,'574','CODE144',3,''),(81,'2012-01-11 11:55:38',2,19,'573','CODE143',3,''),(82,'2012-01-11 11:55:38',2,19,'572','CODE142',3,''),(83,'2012-01-11 11:55:38',2,19,'571','CODE141',3,''),(84,'2012-01-11 11:55:38',2,19,'570','CODE140',3,''),(85,'2012-01-11 11:55:38',2,19,'569','CODE139',3,''),(86,'2012-01-11 11:55:38',2,19,'568','CODE138',3,''),(87,'2012-01-11 11:55:38',2,19,'567','CODE137',3,''),(88,'2012-01-11 11:55:38',2,19,'566','CODE136',3,''),(89,'2012-01-11 11:55:38',2,19,'565','CODE135',3,''),(90,'2012-01-11 11:55:38',2,19,'564','CODE134',3,''),(91,'2012-01-11 11:55:38',2,19,'563','CODE133',3,''),(92,'2012-01-11 11:55:38',2,19,'562','CODE132',3,''),(93,'2012-01-11 11:55:38',2,19,'561','CODE131',3,''),(94,'2012-01-11 11:55:38',2,19,'560','CODE130',3,''),(95,'2012-01-11 11:55:38',2,19,'559','CODE129',3,''),(96,'2012-01-11 11:55:38',2,19,'558','CODE128',3,''),(97,'2012-01-11 11:55:38',2,19,'557','CODE127',3,''),(98,'2012-01-11 11:55:38',2,19,'556','CODE126',3,''),(99,'2012-01-11 11:55:38',2,19,'555','CODE125',3,''),(100,'2012-01-11 11:55:38',2,19,'554','CODE124',3,''),(101,'2012-01-11 11:55:38',2,19,'553','CODE123',3,''),(102,'2012-01-11 11:55:38',2,19,'552','CODE122',3,''),(103,'2012-01-11 11:55:38',2,19,'551','CODE121',3,''),(104,'2012-01-11 11:55:38',2,19,'550','CODE120',3,''),(105,'2012-01-11 11:55:38',2,19,'549','CODE119',3,''),(106,'2012-01-11 11:55:38',2,19,'548','CODE118',3,''),(107,'2012-01-11 11:55:38',2,19,'547','CODE117',3,''),(108,'2012-01-11 11:55:38',2,19,'546','CODE116',3,''),(109,'2012-01-11 11:55:38',2,19,'545','CODE115',3,''),(110,'2012-01-11 11:55:38',2,19,'544','CODE114',3,''),(111,'2012-01-11 11:55:38',2,19,'543','CODE113',3,''),(112,'2012-01-11 11:55:38',2,19,'542','CODE112',3,''),(113,'2012-01-11 11:55:38',2,19,'541','CODE111',3,''),(114,'2012-01-11 11:55:38',2,19,'540','CODE110',3,''),(115,'2012-01-11 11:55:38',2,19,'539','CODE109',3,''),(116,'2012-01-11 11:55:38',2,19,'538','CODE108',3,''),(117,'2012-01-11 11:55:38',2,19,'537','CODE107',3,''),(118,'2012-01-11 11:55:38',2,19,'536','CODE106',3,''),(119,'2012-01-11 11:55:38',2,19,'535','CODE105',3,''),(120,'2012-01-11 11:55:38',2,19,'534','CODE104',3,''),(121,'2012-01-11 11:55:38',2,19,'533','CODE103',3,''),(122,'2012-01-11 11:55:38',2,19,'532','CODE102',3,''),(123,'2012-01-11 11:55:38',2,19,'531','CODE101',3,''),(124,'2012-01-11 12:24:04',2,13,'9','Středočeský',1,''),(125,'2012-01-11 12:24:05',2,14,'15','Praha - východ, Středočeský',1,''),(126,'2012-01-11 12:24:06',2,15,'31','Čelákovice (Praha - východ)',1,''),(127,'2012-01-11 12:25:59',2,11,'3','Pervitin, jiné amfetaminy',1,''),(128,'2012-01-11 12:26:15',2,19,'851','sve03pet13',1,''),(129,'2012-01-11 12:28:00',2,19,'851','sve03pet13',2,'Změněno: birthdate'),(130,'2012-01-11 12:30:00',2,25,'12008','sve03pet13',1,''),(131,'2012-01-11 12:30:53',2,25,'12008','sve03pet13',2,'Změněno: performed_on'),(132,'2012-01-11 12:31:58',2,19,'851','sve03pet13',2,'Změněno: birthdate a primary_drug_usage Pole \"performed_on\" pro položku \"sve03pet13\" typu Kontakt změněno/změněna.'),(133,'2012-01-11 12:32:30',2,25,'12009','sve03pet13',1,''),(134,'2012-01-11 12:32:45',2,25,'12009','sve03pet13',2,'Změněno: performed_on'),(135,'2012-01-11 12:33:16',2,19,'851','sve03pet13',2,'Změněno: birthdate Pole \"performed_on\" pro položku \"sve03pet13\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"sve03pet13\" typu Kontakt změněno/změněna.'),(136,'2012-01-11 12:35:05',2,14,'16','Mělník, Středočeský',1,''),(137,'2012-01-11 12:35:06',2,15,'32','Mělník (Mělník)',1,''),(138,'2012-01-11 12:35:33',2,11,'4','Subutex legálně',1,''),(139,'2012-01-11 12:35:37',2,19,'852','ann26rom12',1,''),(140,'2012-01-11 12:35:41',2,19,'852','ann26rom12',2,'Změněno: birthdate a primary_drug_usage'),(141,'2012-01-11 12:35:58',2,25,'12010','ann26rom12',1,''),(142,'2012-01-11 12:36:21',2,25,'12010','ann26rom12',2,'Změněno: performed_on'),(143,'2012-01-11 12:37:31',2,14,'17','Mladá Boleslav, Středočeský',1,''),(144,'2012-01-11 12:37:32',2,15,'33','Mladá Boleslav (Mladá Boleslav)',1,''),(145,'2012-01-11 12:37:57',2,19,'853','jit10mic01',1,''),(146,'2012-01-11 12:39:04',2,19,'853','jit10mic01',2,'Změněno: birthdate'),(147,'2012-01-11 12:39:22',2,25,'12011','jit10mic01',1,''),(148,'2012-01-11 12:40:09',2,25,'12011','jit10mic01',2,'Změněno: performed_on'),(149,'2012-01-11 12:48:16',2,17,'854','Špírková, Śárka',1,''),(150,'2012-01-11 12:48:35',2,25,'12012','Špírková, Śárka',1,''),(151,'2012-01-11 12:48:42',2,25,'12012','Špírková, Śárka',2,'Změněno: performed_on'),(152,'2012-01-11 12:52:12',2,25,'12011','jit10mic01',2,'Změněno: performed_on'),(153,'2012-01-11 12:52:32',2,25,'12011','jit10mic01',2,'Změněno: performed_on'),(154,'2012-01-11 12:53:04',2,25,'12011','jit10mic01',2,'Změněno: performed_on'),(155,'2012-01-11 12:53:40',2,25,'12013','jit10mic01',1,''),(156,'2012-01-11 12:53:45',2,25,'12013','jit10mic01',2,'Změněno: performed_on'),(157,'2012-01-11 13:05:58',2,15,'34','Neratovice (Mělník)',1,''),(158,'2012-01-11 13:06:51',2,19,'855','ren23dav08',1,''),(159,'2012-01-11 13:07:13',2,25,'12014','ren23dav08',1,''),(160,'2012-01-11 13:07:29',2,25,'12014','ren23dav08',2,'Změněno: performed_on'),(161,'2012-01-11 13:08:06',2,25,'12014','ren23dav08',2,'Změněno: performed_on'),(162,'2012-01-11 13:08:18',2,25,'12014','ren23dav08',2,'Změněno: performed_on'),(163,'2012-01-22 23:52:05',2,42,'3','admin - 2012-01-22 (10 Ks )',1,''),(164,'2012-01-22 23:52:42',2,25,'12015','ann26rom12',1,''),(165,'2012-01-22 23:52:55',2,25,'12015','ann26rom12',2,'Změněno: performed_on'),(166,'2012-01-25 22:08:39',3,25,'12016','ren23dav08',1,''),(167,'2012-02-01 18:21:08',2,25,'12017','muž - IV',1,''),(168,'2012-02-01 18:21:40',2,25,'12018','Špírková, Śárka',1,''),(169,'2012-02-22 14:02:31',2,42,'3','10ks v Neratovice (Mělník), 22. ledna 2012',2,'Změněno: location'),(170,'2012-02-27 10:06:27',2,19,'856','LUD10JIR07',1,''),(171,'2012-02-27 10:07:08',2,25,'12019','LUD10JIR07',1,''),(172,'2012-02-27 10:09:05',2,25,'12019','LUD10JIR07',2,'Změněno: performed_on'),(173,'2012-02-27 10:09:52',2,25,'12020','LUD10JIR07',1,''),(174,'2012-02-27 10:10:08',2,25,'12020','LUD10JIR07',2,'Změněno: performed_on'),(175,'2012-02-27 10:11:00',2,19,'857','LUD17DAV01',1,''),(176,'2012-02-27 10:11:25',2,25,'12021','LUD17DAV01',1,''),(177,'2012-02-27 10:12:34',2,25,'12022','LUD17DAV01',1,''),(178,'2012-02-27 10:13:47',2,25,'12023','LUD17DAV01',1,''),(179,'2012-02-27 10:15:49',2,25,'12024','muž - neuživatel',1,''),(180,'2012-02-27 10:17:14',2,25,'12024','muž - neuživatel',2,'Změněno: performed_on'),(181,'2012-02-27 10:17:26',2,25,'12024','muž - neuživatel',2,'Změněno: performed_on'),(182,'2012-02-27 10:17:51',2,25,'12024','muž - neuživatel',2,'Změněno: performed_on'),(183,'2012-02-27 10:18:41',2,25,'12025','muž - neuživatel',1,''),(184,'2012-02-27 10:19:50',2,42,'4','1ks v Neratovice (Mělník), 23. února 2012',1,''),(185,'2012-02-27 10:21:10',2,17,'858','lékárna náměstí 1',1,''),(186,'2012-02-27 10:21:35',2,25,'12026','lékárna náměstí 1',1,''),(187,'2012-02-27 10:29:27',2,25,'12027','jit10mic01',1,''),(188,'2012-02-27 12:10:23',2,42,'5','0ks v Neratovice (Mělník), 27. února 2012',1,''),(189,'2012-02-27 12:10:43',2,42,'5','100ks v Neratovice (Mělník), 27. února 2012',2,'Změněno: count'),(190,'2012-02-29 18:25:06',3,25,'12028','ren23dav08',1,''),(191,'2012-02-29 18:32:12',3,25,'12029','jit10mic01',1,''),(192,'2012-02-29 18:36:07',3,42,'6','55ks v Neratovice (Mělník), 29. února 2012',1,''),(193,'2012-03-01 21:38:39',2,25,'12030','LUD17DAV01',1,''),(194,'2012-03-02 11:02:40',3,4,'4','karel',1,''),(195,'2012-03-02 11:04:07',3,4,'4','Brunet',2,'Změněno: username, first_name, last_name a email'),(196,'2012-03-02 11:04:15',3,4,'4','Brunet',2,'Změněno: is_staff'),(197,'2012-03-02 11:06:20',3,4,'4','Brunet',2,'Změněno: is_superuser'),(198,'2012-03-02 11:08:32',4,4,'5','terenHK',1,''),(199,'2012-03-02 11:16:27',4,4,'5','terenHK',2,'Změněno: user_permissions'),(200,'2012-03-02 11:22:10',4,4,'5','terenHK',2,'Změněno: user_permissions'),(201,'2012-03-02 11:24:44',4,4,'5','terenHK',2,'Nebyla změněna žádná pole.'),(202,'2012-03-02 11:37:20',4,4,'5','terenHK',2,'Změněno: is_staff a user_permissions'),(203,'2012-03-02 11:42:25',4,4,'5','terenHK',2,'Změněno: user_permissions'),(204,'2012-03-08 09:32:09',3,42,'7','25ks v Čelákovice (Praha - východ), 4. března 2012',1,''),(205,'2012-03-08 09:38:14',3,4,'6','terenPCE',1,''),(206,'2012-03-08 09:39:02',3,4,'6','terenPCE',2,'Změněno: is_staff a user_permissions'),(452,'2012-11-01 09:54:55',10,25,'12089','NCC02NCC70',1,''),(451,'2012-11-01 09:54:22',10,25,'12088','NCC02NCC70',2,'Změněno: performed_on'),(450,'2012-11-01 09:54:17',10,25,'12088','NCC02NCC70',1,''),(449,'2012-11-01 09:53:59',10,19,'872','NCC02NCC70',2,'Pole \"performed_on\" pro položku \"NCC02NCC70\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"NCC02NCC70\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"NCC02NCC70\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"NCC02NCC70\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"NCC02NCC70\" typu Kontakt změněno/změněna.'),(448,'2012-11-01 09:53:34',10,25,'12086','NCC02NCC70',2,'Změněno: performed_on'),(447,'2012-11-01 09:53:15',10,25,'12087','NCC02NCC70',2,'Změněno: performed_on'),(446,'2012-11-01 09:53:05',10,25,'12087','NCC02NCC70',1,''),(224,'2012-03-19 11:54:31',3,19,'861','JAN07LUC07',1,''),(225,'2012-03-19 11:59:30',3,20,'2','Anamnéza: JAN07LUC07',1,''),(226,'2012-03-19 12:01:41',3,12,'1','sdílení náčiní',1,''),(227,'2012-03-19 12:01:51',3,20,'2','Anamnéza: JAN07LUC07',2,'Změněno: nationality, living_condition, accomodation, lives_with_junkies, employment a been_cured_before Položka \"4\" typu Vyšetření onemocnění byla přidána. Položka \"1\" typu Vyšetření onemocnění byla přidána. Položka \"Pervitin, jiné amfetaminy\" typu Užívaná droga byla přidána. Položka \"Subutex legálně\" typu Užívaná droga byla přidána. Položka \"JAN07LUC07: sdílení náčiní\" typu Rizikové chování byla přidána.'),(228,'2012-03-19 12:02:24',3,25,'12034','JAN07LUC07',1,''),(229,'2012-03-19 12:03:34',3,15,'38','Bělá pod Bezdězem (Mladá Boleslav)',1,''),(230,'2012-03-19 12:03:41',3,42,'8','51ks v Bělá pod Bezdězem (Mladá Boleslav), 7. března 2012',1,''),(231,'2012-03-19 12:05:02',3,12,'2','nechráněný sex',1,''),(232,'2012-03-19 12:05:32',3,15,'39','Kralupy nad Vltavou (Mělník)',1,''),(445,'2012-11-01 09:52:26',10,25,'12086','NCC02NCC70',2,'Změněno: performed_on'),(444,'2012-11-01 09:52:20',10,25,'12086','NCC02NCC70',1,''),(443,'2012-11-01 09:51:37',10,25,'12085','NCC02NCC70',2,'Změněno: performed_on'),(442,'2012-11-01 09:51:31',10,25,'12085','NCC02NCC70',1,''),(440,'2012-11-01 09:50:56',10,25,'12084','NCC02NCC70',1,''),(441,'2012-11-01 09:51:03',10,25,'12084','NCC02NCC70',2,'Změněno: performed_on'),(438,'2012-11-01 09:50:10',10,25,'12083','NCC02NCC70',1,''),(439,'2012-11-01 09:50:18',10,25,'12083','NCC02NCC70',2,'Změněno: performed_on'),(437,'2012-11-01 09:49:29',10,19,'872','NCC02NCC70',1,''),(436,'2012-11-01 09:48:43',10,42,'15','1ks v Mělník (Mělník), 4. října 2012',1,''),(435,'2012-10-11 09:37:48',8,25,'12082','MAR23TOM10',2,'Změněno: performed_on'),(434,'2012-10-11 09:29:58',8,25,'12082','MAR23TOM10',1,''),(433,'2012-10-11 09:29:15',8,19,'871','MAR23TOM10',1,''),(245,'2012-03-30 12:58:46',2,42,'10','15ks v Mladá Boleslav (Mladá Boleslav), 30. března 2012',1,''),(246,'2012-03-30 12:59:39',2,15,'41','Bradlec (Mladá Boleslav)',1,''),(247,'2012-03-30 13:00:32',2,42,'11','2ks v Bradlec (Mladá Boleslav), 9. března 2012',1,''),(248,'2012-03-30 13:00:41',2,42,'11','2ks v Bradlec (Mladá Boleslav), 9. března 2012',2,'Nebyla změněna žádná pole.'),(249,'2012-03-30 13:02:48',2,42,'10','15ks v Mladá Boleslav (Mladá Boleslav), 30. března 2012',2,'Nebyla změněna žádná pole.'),(250,'2012-03-30 13:02:49',2,42,'10','15ks v Mladá Boleslav (Mladá Boleslav), 30. března 2012',2,'Nebyla změněna žádná pole.'),(251,'2012-03-30 13:02:51',2,42,'10','15ks v Mladá Boleslav (Mladá Boleslav), 30. března 2012',2,'Nebyla změněna žádná pole.'),(252,'2012-03-30 13:02:52',2,42,'10','15ks v Mladá Boleslav (Mladá Boleslav), 30. března 2012',2,'Nebyla změněna žádná pole.'),(253,'2012-03-30 13:02:53',2,42,'10','15ks v Mladá Boleslav (Mladá Boleslav), 30. března 2012',2,'Nebyla změněna žádná pole.'),(254,'2012-03-30 13:04:19',2,20,'2','Anamnéza: JAN07LUC07',2,'Pole \"behavior\" pro položku \"JAN07LUC07: nechráněný sex\" typu Rizikové chování změněno/změněna.'),(255,'2012-03-30 13:08:47',2,25,'12037','jit10mic01',1,''),(256,'2012-03-30 13:09:21',2,25,'12037','jit10mic01',2,'Změněno: performed_on'),(257,'2012-03-30 13:09:27',2,25,'12037','jit10mic01',2,'Změněno: performed_on'),(258,'2012-03-30 13:09:55',2,25,'12037','jit10mic01',2,'Změněno: performed_on'),(259,'2012-03-30 13:16:30',2,11,'6','klepky',1,''),(260,'2012-03-30 13:17:42',2,25,'12038','sve03pet13',1,''),(261,'2012-03-30 13:18:21',2,25,'12038','sve03pet13',2,'Změněno: performed_on'),(262,'2012-03-30 13:18:43',2,25,'12038','sve03pet13',2,'Změněno: performed_on'),(263,'2012-03-30 13:20:01',2,11,'7','subutex',1,''),(264,'2012-03-30 13:21:39',2,19,'852','ann26rom12',2,'Změněno: birthdate a birthdate_year_only Pole \"performed_on\" pro položku \"ann26rom12\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"ann26rom12\" typu Kontakt změněno/změněna.'),(265,'2012-03-30 13:23:04',2,25,'12039','jit10mic01',1,''),(266,'2012-03-30 13:24:01',2,25,'12039','jit10mic01',2,'Změněno: performed_on'),(267,'2012-03-30 13:24:39',2,17,'863','špírková',1,''),(268,'2012-03-30 13:38:32',2,25,'12040','žena - neuživatel',1,''),(269,'2012-03-30 13:38:46',2,25,'12040','žena - neuživatel',2,'Změněno: performed_on'),(270,'2012-03-30 13:39:35',2,25,'12040','žena - neuživatel',2,'Změněno: performed_on'),(271,'2012-04-02 09:46:47',3,42,'12','21ks v Kralupy nad Vltavou (Mělník), 14. března 2012',1,''),(272,'2012-04-02 11:25:24',2,42,'13','1ks v Mladá Boleslav (Mladá Boleslav), 20. března 2012',1,''),(273,'2012-04-02 11:27:19',2,25,'12041','LUD10JIR07',1,''),(274,'2012-04-02 11:28:09',2,25,'12041','LUD10JIR07',2,'Změněno: performed_on'),(275,'2012-04-11 13:21:59',2,25,'12042','MAR30ANT12',1,''),(276,'2012-04-13 11:49:18',3,11,'6','Benzodiazepiny',2,'Změněno: title'),(277,'2012-04-13 11:49:25',3,11,'7','Subutex',2,'Změněno: title'),(278,'2012-04-13 11:49:32',3,11,'5','Tabák',2,'Změněno: title'),(279,'2012-04-13 11:49:38',3,11,'8','THC',1,''),(280,'2012-04-13 11:49:48',3,11,'9','LSD',1,''),(281,'2012-04-13 11:50:39',2,11,'10','Designer drugs',1,''),(282,'2012-04-13 11:53:30',2,25,'12042','MAR30ANT12',2,'Změněno: performed_on'),(283,'2012-04-13 11:54:06',2,25,'12043','LUD17DAV01',1,''),(284,'2012-04-13 11:55:07',2,25,'12043','LUD17DAV01',2,'Změněno: performed_on'),(285,'2012-04-26 09:40:40',2,25,'12044','MAR30ANT12',1,''),(286,'2012-05-16 10:23:50',2,19,'862','MAR30ANT12',2,'Změněno: birthdate a primary_drug Pole \"performed_on\" pro položku \"MAR30ANT12\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"MAR30ANT12\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"MAR30ANT12\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"MAR30ANT12\" typu Kontakt změněno/změněna.'),(287,'2012-05-16 10:29:21',2,19,'855','ren23dav08',2,'Změněno: birthdate Pole \"performed_on\" pro položku \"ren23dav08\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"ren23dav08\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"ren23dav08\" typu Kontakt změněno/změněna.'),(288,'2012-05-16 10:38:42',2,42,'14','645ks v Mělník (Mělník), 15. března 2012',1,''),(289,'2012-05-16 10:46:25',2,19,'864','NCC04NCC04',1,''),(290,'2012-05-16 10:46:36',2,19,'864','NCC04NCC04',2,'Nebyla změněna žádná pole.'),(291,'2012-05-16 10:48:57',2,19,'864','NCC04NCC01',2,'Změněno: code a primary_drug_usage'),(292,'2012-05-16 10:49:07',2,19,'864','NCC04NCC01',2,'Změněno: primary_drug_usage'),(293,'2012-05-16 10:49:32',2,19,'864','NCC04NCC01',2,'Změněno: birthdate, birthdate_year_only a primary_drug_usage'),(294,'2012-05-16 10:51:53',2,19,'864','NCC04NCC01',2,'Změněno: first_name a birthdate'),(295,'2012-05-16 10:52:00',2,19,'864','NCC04NCC01',2,'Změněno: last_name a birthdate'),(296,'2012-05-16 10:52:43',2,25,'12045','NCC04NCC01',1,''),(297,'2012-05-16 10:52:59',2,25,'12045','NCC04NCC01',2,'Změněno: performed_on'),(298,'2012-05-16 10:53:55',2,25,'12034','JAN07LUC07',2,'Změněno: performed_on'),(299,'2012-05-16 11:01:46',2,25,'12046','muž - neIV',1,''),(300,'2012-05-16 11:02:26',2,25,'12046','muž - neIV',2,'Změněno: performed_on'),(301,'2012-05-16 11:06:30',2,15,'42','Bakov nad Jizerou (Mladá Boleslav)',1,''),(302,'2012-05-16 11:06:42',2,19,'864','NCC04NCC01',2,'Změněno: town a birthdate Pole \"performed_on\" pro položku \"NCC04NCC01\" typu Kontakt změněno/změněna.'),(303,'2012-05-16 11:09:58',2,25,'12047','JAN24ROM12',1,''),(304,'2012-05-16 11:11:54',2,25,'12047','JAN24ROM12',2,'Změněno: performed_on'),(305,'2012-05-16 11:12:51',2,25,'12047','JAN24ROM12',2,'Změněno: performed_on'),(306,'2012-05-16 11:38:01',2,25,'12048','žena - neuživatel',1,''),(307,'2012-05-16 12:08:54',2,25,'12049','MAR30ANT12',1,''),(308,'2012-05-18 11:14:49',2,25,'12050','HAN02HAN02',1,''),(309,'2012-05-18 11:15:01',2,25,'12050','HAN02HAN02',2,'Změněno: performed_on'),(310,'2012-05-18 11:17:32',2,19,'865','ZOR28MIC02',1,''),(311,'2012-05-18 11:17:52',2,25,'12051','ZOR28MIC02',1,''),(312,'2012-05-18 11:38:47',2,25,'12052','LUD17DAV01',1,''),(313,'2012-05-25 16:26:02',2,19,'866','KAR12JAN10',1,''),(314,'2012-05-25 16:27:04',2,19,'866','KAR12JAN10',2,'Změněno: primary_drug'),(315,'2012-05-27 22:42:35',2,25,'12053','muž - neuživatel',1,''),(316,'2012-05-27 22:42:53',2,25,'12053','muž - neuživatel',2,'Změněno: performed_on'),(317,'2012-05-27 22:45:00',2,25,'12054','muž - IV',1,''),(318,'2012-05-27 22:47:41',2,25,'12054','muž - IV',2,'Změněno: performed_on'),(319,'2012-05-27 22:48:04',2,25,'12055','KAR12JAN10',1,''),(320,'2012-05-27 23:00:10',2,25,'12055','KAR12JAN10',2,'Změněno: performed_on'),(321,'2012-05-27 23:00:38',2,25,'12056','lékárna náměstí 1',1,''),(322,'2012-05-27 23:02:59',2,25,'12056','lékárna náměstí 1',2,'Změněno: performed_on'),(323,'2012-05-27 23:03:20',2,25,'12057','muž - neuživatel',1,''),(324,'2012-05-27 23:03:55',2,25,'12058','KAR12JAN10',1,''),(325,'2012-05-30 13:21:29',2,19,'866','KAR12JAN10',2,'Změněno: primary_drug a primary_drug_usage Pole \"performed_on\" pro položku \"KAR12JAN10\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"KAR12JAN10\" typu Kontakt změněno/změněna.'),(326,'2012-06-06 13:13:41',2,25,'12059','KAR12JAN10',1,''),(327,'2012-06-06 13:38:46',2,25,'12059','KAR12JAN10',2,'Změněno: performed_on'),(328,'2012-06-06 13:38:57',2,25,'12060','muž - IV',1,''),(329,'2012-06-06 13:40:04',2,25,'12060','muž - IV',2,'Změněno: performed_on'),(330,'2012-06-06 13:40:31',2,25,'12061','lékárna náměstí 1',1,''),(331,'2012-07-03 14:22:42',3,14,'20','Nymburský, Středočeský',1,''),(332,'2012-07-03 14:22:48',3,15,'43','Milovice (Nymburský)',1,''),(333,'2012-07-03 14:23:08',3,14,'21','Nymburk, Středočeský',1,''),(334,'2012-07-03 14:23:26',3,15,'43','Milovice (Nymburský)',3,''),(335,'2012-07-03 14:23:48',3,15,'44','Milovice (Nymburk)',1,''),(336,'2012-07-03 14:24:25',3,14,'20','Nymburský, Středočeský',3,''),(337,'2012-07-03 14:24:37',3,15,'41','Bradlec (Mladá Boleslav)',3,''),(338,'2012-07-03 14:25:06',3,15,'40','Choltice (Pardubice)',3,''),(339,'2012-07-03 14:25:06',3,15,'37','Kostelec nad Orlicí (Rychnov nad Kněžnou)',3,''),(340,'2012-07-03 14:25:06',3,15,'36','Dobruška (Rychnov nad Kněžnou)',3,''),(341,'2012-07-03 14:25:06',3,15,'35','Pardubice (Pardubice)',3,''),(342,'2012-07-03 14:25:53',3,15,'45','Lysá nad Labem (Nymburk)',1,''),(343,'2012-07-03 14:26:07',3,14,'19','Rychnov nad Kněžnou, Královéhradecký',3,''),(344,'2012-07-03 14:26:07',3,14,'18','Pardubice, Pardubický',3,''),(345,'2012-07-03 14:26:51',3,15,'46','Brandýs nad Labem - Stará Boleslav (Praha - východ)',1,''),(346,'2012-07-03 14:27:08',3,15,'47','Mnichovo Hradiště (Mladá Boleslav)',1,''),(347,'2012-07-03 14:27:27',3,15,'48','Benátky nad Jizerou (Mladá Boleslav)',1,''),(348,'2012-07-03 14:27:38',3,15,'49','Poděbrady (Nymburk)',1,''),(349,'2012-07-03 14:27:57',3,15,'50','Sadská (Nymburk)',1,''),(350,'2012-07-03 14:28:58',3,12,'3','sdílení stříkaček',1,''),(351,'2012-07-18 09:31:01',2,25,'12062','KAR12JAN10',1,''),(352,'2012-07-18 09:31:20',2,25,'12062','KAR12JAN10',2,'Změněno: performed_on'),(353,'2012-07-18 09:31:44',2,25,'12063','KAR12JAN10',1,''),(354,'2012-07-18 09:32:00',2,25,'12063','KAR12JAN10',2,'Změněno: performed_on'),(355,'2012-07-18 09:32:29',2,19,'852','ann26rom12',2,'Změněno: town, birthdate a primary_drug Pole \"performed_on\" pro položku \"ann26rom12\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"ann26rom12\" typu Kontakt změněno/změněna.'),(356,'2012-07-18 18:32:33',3,4,'7','test2',1,''),(357,'2012-07-18 18:32:43',3,4,'7','test2',2,'Změněno: groups'),(358,'2012-07-18 18:44:24',3,4,'7','test2',2,'Změněno: is_active'),(359,'2012-08-15 13:00:56',3,25,'12064','JAN07LUC07',1,''),(360,'2012-08-20 00:51:25',2,25,'12065','muž - IV uživatel',1,''),(361,'2012-08-20 00:51:40',2,25,'12065','muž - IV uživatel',2,'Změněno: performed_on'),(362,'2012-08-20 01:14:32',2,25,'12066','JAN07LUC07',1,''),(363,'2012-08-20 14:18:18',2,25,'12067','muž - neIV uživatel',1,''),(364,'2012-08-20 14:29:01',2,25,'12067','muž - neIV uživatel',2,'Změněno: performed_on'),(365,'2012-08-20 14:29:39',2,25,'12068','muž - neIV uživatel',1,''),(366,'2012-08-20 14:34:50',2,25,'12069','KAR12JAN10',1,''),(367,'2012-08-20 15:54:01',2,25,'12070','muž - IV uživatel',1,''),(368,'2012-08-20 15:54:33',2,25,'12070','muž - IV uživatel',2,'Změněno: performed_on'),(369,'2012-08-20 15:57:09',2,25,'12071','KAR12JAN10',1,''),(370,'2012-08-20 16:18:20',2,25,'12072','muž - IV uživatel',1,''),(371,'2012-08-20 16:23:01',2,25,'12072','muž - IV uživatel',2,'Změněno: performed_on'),(372,'2012-08-20 16:59:37',2,25,'12073','muž - rodič',1,''),(373,'2012-08-20 17:12:58',2,25,'12074','lékárna náměstí 1',1,''),(374,'2012-08-20 17:24:11',2,17,'867','komunitní pl.',1,''),(375,'2012-08-24 10:28:59',3,25,'12075','ZOR28MIC02',1,''),(376,'2012-08-30 10:37:03',2,20,'3','Anamnéza: KAR12JAN10',1,''),(377,'2012-08-30 10:39:15',2,20,'3','Anamnéza: KAR12JAN10',2,'Položka \"1\" typu Vyšetření onemocnění byla přidána. Položka \"4\" typu Vyšetření onemocnění byla přidána. Položka \"2\" typu Vyšetření onemocnění byla přidána. Položka \"3\" typu Vyšetření onemocnění byla přidána. Položka \"Pervitin, jiné amfetaminy\" typu Užívaná droga byla přidána. Položka \"THC\" typu Užívaná droga byla přidána. Položka \"KAR12JAN10: sdílení náčiní\" typu Rizikové chování byla přidána. Položka \"KAR12JAN10: nechráněný sex\" typu Rizikové chování byla přidána.'),(378,'2012-08-30 10:39:46',2,19,'866','KAR12JAN10',2,'Změněno: birthdate a birthdate_year_only Pole \"performed_on\" pro položku \"KAR12JAN10\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"KAR12JAN10\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"KAR12JAN10\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"KAR12JAN10\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"KAR12JAN10\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"KAR12JAN10\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"KAR12JAN10\" typu Kontakt změněno/změněna.'),(379,'2012-08-30 10:40:59',2,19,'868','ALE12NEE10',1,''),(380,'2012-08-30 10:41:13',2,25,'12076','ALE12NEE10',1,''),(381,'2012-08-30 10:41:20',2,25,'12076','ALE12NEE10',2,'Změněno: performed_on'),(382,'2012-08-30 10:41:47',2,25,'12077','ALE12NEE10',1,''),(383,'2012-08-30 10:43:36',2,25,'12077','ALE12NEE10',2,'Změněno: performed_on'),(384,'2012-08-30 10:43:54',2,25,'12077','ALE12NEE10',2,'Změněno: performed_on'),(385,'2012-08-30 10:46:17',2,25,'12078','NCC04NCC01',1,''),(386,'2012-08-30 10:46:48',2,25,'12079','NCC04NCC01',1,''),(387,'2012-08-30 10:50:06',2,25,'12077','ALE12NEE10',2,'Změněno: performed_on'),(388,'2012-08-30 12:28:55',2,25,'12080','jit10mic01',1,''),(389,'2012-09-20 12:28:49',3,4,'4','OndrejSulc',2,'Změněno: username'),(390,'2012-09-20 12:38:23',3,4,'8','LukasVerner',1,''),(391,'2012-09-20 12:39:12',3,4,'8','LukasVerner',2,'Změněno: first_name, last_name a groups'),(392,'2012-09-20 12:42:08',4,4,'9','TerezaMullerova',1,''),(393,'2012-09-20 12:42:33',4,4,'9','TerezaMullerova',2,'Změněno: first_name, last_name a groups'),(394,'2012-09-20 12:42:56',4,4,'10','MonikaZaveska',1,''),(395,'2012-09-20 12:42:59',4,4,'10','MonikaZaveska',2,'Nebyla změněna žádná pole.'),(396,'2012-09-20 12:43:56',9,25,'12081','muž - IV uživatel',1,''),(397,'2012-09-20 12:44:07',9,25,'12081','muž - IV uživatel',2,'Změněno: performed_on'),(398,'2012-09-20 12:46:14',4,4,'10','MonikaZaveska',2,'Změněno: groups'),(399,'2012-09-20 12:46:24',4,4,'10','MonikaZaveska',2,'Změněno: first_name a last_name'),(400,'2012-09-20 12:48:07',4,19,'868','ALE12NEE10',3,''),(401,'2012-09-20 12:49:19',4,19,'869','BLA01BLA02',1,''),(402,'2012-09-20 13:37:20',4,12,'4','nitrožilní aplikace',1,''),(403,'2012-09-20 13:37:32',4,12,'3','sdílení jehel',2,'Změněno: title'),(404,'2012-09-20 13:37:41',4,12,'5','riziková aplikace',1,''),(405,'2012-09-20 13:37:49',4,12,'6','předávkování',1,''),(406,'2012-09-20 13:39:46',4,12,'7','zdravotní komplikace',1,''),(407,'2012-09-20 13:40:36',4,15,'50','Sadská (Nymburk)',3,''),(408,'2012-09-20 13:40:36',4,15,'49','Poděbrady (Nymburk)',3,''),(409,'2012-09-20 13:40:36',4,15,'45','Lysá nad Labem (Nymburk)',3,''),(410,'2012-09-20 13:40:36',4,15,'44','Milovice (Nymburk)',3,''),(411,'2012-09-20 13:41:01',4,11,'11','Heroin',1,''),(412,'2012-09-20 13:44:23',4,11,'12','Braun a jiné opiáty',1,''),(413,'2012-09-20 13:44:35',4,11,'13','Surové opium',1,''),(414,'2012-09-20 13:45:36',4,11,'7','Subutex',3,''),(415,'2012-09-20 13:46:01',4,11,'14','Subutex ilegálně',1,''),(416,'2012-09-20 13:46:14',4,11,'15','Cigarety',1,''),(417,'2012-09-20 13:46:19',4,11,'16','Alkohol',1,''),(418,'2012-09-20 13:46:34',4,11,'17','Inhalační látky, ředidla',1,''),(419,'2012-09-20 13:46:46',4,11,'18','Medikamenty',1,''),(420,'2012-09-20 13:47:02',4,11,'9','Extáze, LSD, lysohlávky',2,'Změněno: title'),(421,'2012-09-20 13:47:12',4,11,'19','Metadon',1,''),(422,'2012-09-20 13:47:25',4,11,'20','Kokain, crack',1,''),(423,'2012-09-20 13:47:56',4,11,'6','Benzodiazepiny',3,''),(424,'2012-09-20 13:48:46',4,11,'14','Subutex , Ravata - ilegálně',2,'Změněno: title'),(425,'2012-09-20 13:48:59',4,11,'4','Subutex, Ravata - legálně',2,'Změněno: title'),(426,'2012-09-20 13:49:37',4,11,'14','Subutex , Ravata, jiné substituční preparáty - ilegálně',2,'Změněno: title'),(427,'2012-09-20 13:49:52',4,11,'4','Subutex, Ravata, jiné substituční preparáty - legálně',2,'Změněno: title'),(428,'2012-10-01 10:12:21',3,19,'869','BLA01BLA02',3,''),(429,'2012-10-01 10:13:04',3,19,'870','ANN02ANN02',1,''),(430,'2012-10-01 10:16:46',4,4,'7','test2',3,''),(431,'2012-10-01 10:17:02',4,4,'5','terenHK',3,''),(432,'2012-10-01 10:17:02',4,4,'6','terenPCE',3,''),(453,'2012-11-01 09:55:02',10,25,'12089','NCC02NCC70',2,'Změněno: performed_on'),(454,'2012-11-01 09:55:25',10,19,'872','NCC02NCC70',2,'Pole \"performed_on\" pro položku \"NCC02NCC70\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"NCC02NCC70\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"NCC02NCC70\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"NCC02NCC70\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"NCC02NCC70\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"NCC02NCC70\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"NCC02NCC70\" typu Kontakt změněno/změněna.'),(455,'2012-11-01 09:55:44',10,25,'12090','NCC02NCC70',1,''),(456,'2012-11-01 09:57:59',10,25,'12090','NCC02NCC70',2,'Změněno: performed_on'),(457,'2012-11-01 09:58:34',10,19,'872','NCC02NCC70',2,'Pole \"performed_on\" pro položku \"NCC02NCC70\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"NCC02NCC70\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"NCC02NCC70\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"NCC02NCC70\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"NCC02NCC70\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"NCC02NCC70\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"NCC02NCC70\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"NCC02NCC70\" typu Kontakt změněno/změněna.'),(458,'2012-11-01 09:59:13',10,19,'873','MAR06JAN09',1,''),(459,'2012-11-01 09:59:53',10,25,'12091','MAR06JAN09',1,''),(460,'2012-11-01 09:59:59',10,25,'12091','MAR06JAN09',2,'Změněno: performed_on'),(461,'2012-11-01 10:00:22',10,25,'12092','MAR06JAN09',1,''),(462,'2012-11-01 10:00:27',10,25,'12092','MAR06JAN09',2,'Změněno: performed_on'),(463,'2013-09-23 12:30:08',3,19,'874','AAA01AAA02',1,''),(464,'2013-09-23 12:30:26',3,19,'872','NCC02NCC70',2,'Změněno: first_name Pole \"performed_on\" pro položku \"NCC02NCC70\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"NCC02NCC70\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"NCC02NCC70\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"NCC02NCC70\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"NCC02NCC70\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"NCC02NCC70\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"NCC02NCC70\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"NCC02NCC70\" typu Kontakt změněno/změněna.'),(465,'2013-09-23 12:30:44',3,19,'871','MAR23TOM10',3,''),(466,'2013-09-23 12:30:44',3,19,'865','ZOR28MIC02',3,''),(467,'2013-09-23 12:30:57',3,19,'864','NCC04NCC01',2,'Změněno: first_name, last_name a birthdate Pole \"performed_on\" pro položku \"NCC04NCC01\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"NCC04NCC01\" typu Kontakt změněno/změněna.'),(468,'2013-09-23 12:31:24',3,19,'873','MAR06JAN09',3,''),(469,'2013-09-23 12:31:24',3,19,'870','ANN02ANN02',3,''),(470,'2013-09-23 12:31:24',3,19,'866','KAR12JAN10',3,''),(471,'2013-09-23 12:31:24',3,19,'861','JAN07LUC07',3,''),(472,'2013-09-23 12:31:24',3,19,'857','LUD17DAV01',3,''),(473,'2013-09-23 12:31:24',3,19,'856','LUD10JIR07',3,''),(474,'2013-09-23 12:31:24',3,19,'855','ren23dav08',3,''),(475,'2013-09-23 12:31:24',3,19,'853','jit10mic01',3,''),(476,'2013-09-23 12:31:24',3,19,'852','ann26rom12',3,''),(477,'2013-09-23 12:31:24',3,19,'851','sve03pet13',3,''),(478,'2013-09-23 12:31:33',3,19,'872','NCC02NCC70',3,''),(479,'2013-09-23 12:31:33',3,19,'864','NCC04NCC01',3,''),(480,'2013-09-23 12:32:47',3,19,'875','BBB01BBB02',1,''),(481,'2013-09-23 12:33:02',3,19,'876','XXX01XXX02',1,''),(482,'2013-09-23 12:33:21',3,19,'877','ZZZ01ZZZ02',1,''),(483,'2013-09-23 12:33:35',3,19,'878','LLL01LLL02',1,''),(484,'2013-09-23 12:33:52',3,19,'879','CCC01CCC02',1,''),(485,'2013-09-23 12:34:12',3,19,'880','DDD01EEE02',1,''),(486,'2013-09-23 12:34:33',3,19,'881','FFF01GGG02',1,''),(487,'2013-09-23 12:34:50',3,19,'882','HHH01III02',1,''),(488,'2013-09-23 12:35:08',3,19,'883','JJJ01KKK02',1,''),(489,'2013-09-23 12:35:30',3,19,'884','MMM01NNN02',1,''),(490,'2013-09-23 12:35:44',3,19,'885','PPP01QQQ02',1,''),(491,'2013-09-23 12:37:14',3,25,'12093','AAA01AAA02',1,''),(492,'2013-09-23 12:37:30',3,25,'12093','AAA01AAA02',2,'Změněno: performed_on'),(493,'2013-09-23 12:37:37',3,25,'12094','AAA01AAA02',1,''),(494,'2013-09-23 12:37:43',3,25,'12094','AAA01AAA02',2,'Změněno: performed_on'),(495,'2013-09-23 12:37:56',3,25,'12095','AAA01AAA02',1,''),(496,'2013-09-23 12:38:04',3,25,'12095','AAA01AAA02',2,'Změněno: performed_on'),(497,'2013-09-23 12:38:08',3,25,'12096','AAA01AAA02',1,''),(498,'2013-09-23 12:38:39',3,25,'12096','AAA01AAA02',2,'Změněno: performed_on'),(499,'2013-09-23 12:38:44',3,25,'12097','AAA01AAA02',1,''),(500,'2013-09-23 13:11:43',3,20,'4','Anamnéza: AAA01AAA02',1,''),(501,'2013-09-23 13:13:19',3,19,'874','AAA01AAA02',2,'Změněno: birthdate a birthdate_year_only Pole \"performed_on\" pro položku \"AAA01AAA02\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"AAA01AAA02\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"AAA01AAA02\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"AAA01AAA02\" typu Kontakt změněno/změněna. Pole \"performed_on\" pro položku \"AAA01AAA02\" typu Kontakt změněno/změněna.'),(502,'2013-09-23 13:15:02',3,20,'4','Anamnéza: AAA01AAA02',2,'Položka \"Pervitin, jiné amfetaminy\" typu Užívaná droga byla přidána.'),(503,'2013-09-23 13:16:48',3,20,'4','Anamnéza: AAA01AAA02',2,'Položka \"Heroin\" typu Užívaná droga byla přidána.'),(504,'2013-09-23 13:21:01',3,20,'4','Anamnéza: AAA01AAA02',2,'Položka \"AAA01AAA02: nitrožilní aplikace\" typu Rizikové chování byla přidána.'),(505,'2013-09-23 13:21:40',3,20,'4','Anamnéza: AAA01AAA02',2,'Položka \"AAA01AAA02: sdílení jehel\" typu Rizikové chování byla přidána.'),(506,'2013-09-25 13:37:17',3,20,'4','Anamnéza: AAA01AAA02',2,'Položka \"AAA01AAA02: předávkování\" typu Rizikové chování byla přidána.'),(507,'2013-10-14 10:12:12',3,25,'12098','PPP01QQQ02',1,''),(508,'2013-10-14 13:25:12',3,19,'886','1234567ABCD',1,''),(509,'2013-10-14 13:25:37',3,19,'886','1234567ABCD',2,'Změněno: birthdate'),(510,'2013-10-14 13:26:00',3,25,'12099','1234567ABCD',1,''),(511,'2013-10-14 13:31:09',3,19,'887','123456789000AAA',1,''),(512,'2013-10-14 13:31:27',3,19,'887','123456789000AAA',2,'Změněno: birthdate'),(513,'2013-10-14 13:31:38',3,25,'12100','123456789000AAA',1,''),(514,'2013-10-14 13:32:01',3,25,'12100','123456789000AAA',2,'Změněno: performed_on'),(515,'2013-10-14 13:52:40',3,17,'7','Zástupce semiramis OS v Čelákovice (Praha - východ), 2. srpna 2013',1,''),(516,'2013-10-14 13:53:11',3,42,'16','100ks v Čelákovice (Praha - východ), 7. října 2013',1,''),(517,'2013-10-14 14:05:53',3,25,'12101','PPP01QQQ02',1,''),(518,'2013-10-14 14:07:23',3,25,'12102','1234567ABCD',1,''),(519,'2013-10-14 14:07:57',3,25,'12102','1234567ABCD',2,'Změněno: performed_on'),(520,'2013-10-14 14:08:14',3,25,'12103','muž - rodič',1,''),(521,'2013-10-14 14:08:25',3,25,'12103','muž - rodič',2,'Změněno: performed_on'),(522,'2013-10-16 09:19:50',3,25,'12104','BBB01BBB02',1,''),(523,'2013-10-16 09:20:06',3,25,'12104','BBB01BBB02',2,'Změněno: performed_on'),(524,'2013-10-16 09:20:22',3,25,'12105','CCC01CCC02',1,''),(525,'2013-10-16 09:20:37',3,25,'12105','CCC01CCC02',2,'Změněno: performed_on'),(526,'2013-10-16 09:20:48',3,25,'12106','DDD01EEE02',1,''),(527,'2013-10-16 09:20:59',3,25,'12106','DDD01EEE02',2,'Změněno: performed_on'),(528,'2013-10-16 09:21:12',3,25,'12107','DDD01EEE02',1,''),(529,'2013-10-16 09:21:20',3,25,'12107','DDD01EEE02',2,'Změněno: performed_on'),(530,'2013-10-16 09:21:38',3,25,'12108','FFF01GGG02',1,''),(531,'2013-10-16 09:21:43',3,25,'12108','FFF01GGG02',2,'Změněno: performed_on'),(532,'2013-10-16 09:21:48',3,25,'12109','FFF01GGG02',1,''),(533,'2013-10-16 09:21:53',3,25,'12109','FFF01GGG02',2,'Změněno: performed_on'),(534,'2013-10-16 09:22:01',3,25,'12110','HHH01III02',1,''),(535,'2013-10-16 09:22:07',3,25,'12110','HHH01III02',2,'Změněno: performed_on'),(536,'2013-10-16 09:22:21',3,25,'12111','JJJ01KKK02',1,''),(537,'2013-10-16 09:22:29',3,25,'12111','JJJ01KKK02',2,'Změněno: performed_on'),(538,'2013-10-16 09:22:34',3,25,'12112','JJJ01KKK02',1,''),(539,'2013-10-16 09:23:05',3,25,'12112','JJJ01KKK02',2,'Změněno: performed_on'),(540,'2013-10-16 09:23:19',3,25,'12113','JJJ01KKK02',1,''),(541,'2013-10-16 09:23:28',3,25,'12113','JJJ01KKK02',2,'Změněno: performed_on'),(542,'2013-10-16 09:23:54',3,25,'12114','LLL01LLL02',1,''),(543,'2013-10-16 09:24:04',3,25,'12114','LLL01LLL02',2,'Změněno: performed_on'),(544,'2013-10-16 09:24:19',3,25,'12115','MMM01NNN02',1,''),(545,'2013-10-16 09:24:30',3,25,'12115','MMM01NNN02',2,'Změněno: performed_on'),(546,'2013-10-16 09:24:34',3,25,'12116','MMM01NNN02',1,''),(547,'2013-10-16 09:24:47',3,25,'12116','MMM01NNN02',2,'Změněno: performed_on'),(548,'2013-10-16 09:24:51',3,25,'12117','MMM01NNN02',1,''),(549,'2013-10-16 09:25:03',3,25,'12117','MMM01NNN02',2,'Změněno: performed_on'),(550,'2013-10-16 09:25:15',3,25,'12118','AAA01AAA02',1,''),(551,'2013-10-16 09:25:25',3,25,'12118','AAA01AAA02',2,'Změněno: performed_on'),(552,'2013-10-16 09:25:32',3,25,'12119','BBB01BBB02',1,''),(553,'2013-10-16 09:31:58',3,25,'12120','ZZZ01ZZZ02',1,''),(554,'2013-10-16 09:32:09',3,25,'12120','ZZZ01ZZZ02',2,'Změněno: performed_on'),(555,'2013-10-16 09:32:14',3,25,'12121','ZZZ01ZZZ02',1,''),(556,'2013-10-16 09:32:22',3,25,'12121','ZZZ01ZZZ02',2,'Změněno: performed_on'),(557,'2013-10-16 09:32:32',3,25,'12122','ZZZ01ZZZ02',1,''),(558,'2013-10-16 09:32:49',3,25,'12122','ZZZ01ZZZ02',2,'Změněno: performed_on'),(559,'2013-10-16 09:32:57',3,25,'12123','HHH01III02',1,''),(560,'2013-10-16 09:33:06',3,25,'12123','HHH01III02',2,'Změněno: performed_on'),(561,'2013-10-16 09:33:27',3,25,'12124','JJJ01KKK02',1,''),(562,'2013-10-16 09:33:37',3,25,'12124','JJJ01KKK02',2,'Změněno: performed_on'),(563,'2013-10-16 09:33:47',3,25,'12125','CCC01CCC02',1,''),(564,'2013-10-16 09:34:17',3,25,'12126','XXX01XXX02',1,''),(565,'2013-10-16 09:34:27',3,25,'12126','XXX01XXX02',2,'Změněno: performed_on'),(566,'2013-10-16 09:34:33',3,25,'12127','XXX01XXX02',1,''),(567,'2013-10-16 10:03:51',3,25,'12128','LLL01LLL02',1,''),(568,'2013-10-16 10:04:06',3,25,'12128','LLL01LLL02',2,'Změněno: performed_on'),(569,'2013-10-16 10:04:11',3,25,'12129','LLL01LLL02',1,''),(570,'2013-10-16 10:05:00',3,25,'12130','CCC01CCC02',1,''),(571,'2013-10-16 10:05:11',3,25,'12130','CCC01CCC02',2,'Změněno: performed_on'),(572,'2013-10-16 10:05:20',3,25,'12131','CCC01CCC02',1,''),(573,'2013-10-16 12:11:10',3,25,'12132','DDD01EEE02',1,''),(574,'2013-10-16 12:11:21',3,25,'12132','DDD01EEE02',2,'Změněno: performed_on'),(575,'2013-10-16 12:11:30',3,25,'12133','DDD01EEE02',1,''),(576,'2013-10-16 12:12:12',3,25,'12134','BBB01BBB02',1,''),(577,'2013-10-16 12:12:21',3,25,'12134','BBB01BBB02',2,'Změněno: performed_on'),(578,'2013-10-16 12:12:34',3,25,'12135','BBB01BBB02',1,''),(579,'2013-10-16 12:12:53',3,25,'12135','BBB01BBB02',2,'Změněno: performed_on'),(580,'2013-10-16 12:13:03',3,25,'12136','BBB01BBB02',1,''),(581,'2013-10-16 12:13:53',3,25,'12137','MMM01NNN02',1,''),(582,'2013-10-16 12:14:06',3,25,'12137','MMM01NNN02',2,'Změněno: performed_on'),(583,'2013-10-16 12:14:16',3,25,'12138','MMM01NNN02',1,''),(584,'2013-10-16 12:14:21',3,25,'12138','MMM01NNN02',2,'Změněno: performed_on'),(585,'2013-10-16 12:14:25',3,25,'12139','MMM01NNN02',1,''),(586,'2013-10-16 12:17:34',3,25,'12140','HHH01III02',1,''),(587,'2013-10-16 12:17:45',3,25,'12140','HHH01III02',2,'Změněno: performed_on'),(588,'2013-10-16 12:17:49',3,25,'12141','HHH01III02',1,''),(589,'2013-10-16 12:18:05',3,25,'12141','HHH01III02',2,'Změněno: performed_on'),(590,'2013-10-16 12:18:09',3,25,'12142','HHH01III02',1,''),(591,'2013-10-16 12:48:30',3,25,'12143','CCC01CCC02',1,''),(592,'2013-10-16 12:52:05',3,25,'12144','HHH01III02',1,''),(593,'2013-10-16 12:52:14',3,25,'12144','HHH01III02',2,'Změněno: performed_on'),(594,'2013-10-16 12:52:23',3,25,'12145','HHH01III02',1,''),(595,'2013-10-16 13:07:19',3,25,'12146','PPP01QQQ02',1,''),(596,'2013-10-16 13:09:02',3,25,'12147','CCC01CCC02',1,''),(597,'2013-10-16 13:09:12',3,25,'12147','CCC01CCC02',2,'Změněno: performed_on'),(598,'2013-10-16 13:09:15',3,25,'12148','CCC01CCC02',1,''),(599,'2013-10-16 13:09:39',3,25,'12148','CCC01CCC02',2,'Změněno: performed_on'),(600,'2013-10-16 13:09:43',3,25,'12149','CCC01CCC02',1,''),(601,'2013-10-16 13:10:15',3,25,'12150','CCC01CCC02',1,''),(602,'2013-10-16 13:10:18',3,25,'12150','CCC01CCC02',2,'Změněno: performed_on'),(603,'2013-10-16 13:10:24',3,25,'12151','CCC01CCC02',1,''),(604,'2013-10-16 13:23:10',3,25,'12152','MMM01NNN02',1,''),(605,'2013-10-29 10:03:07',3,25,'12153','FFF01GGG02',1,''),(606,'2013-11-14 14:35:09',3,3,'1','Terén',2,'Změněno: permissions');
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=47 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'log entry','admin','logentry'),(2,'permission','auth','permission'),(3,'group','auth','group'),(4,'user','auth','user'),(5,'message','auth','message'),(6,'content type','contenttypes','contenttype'),(7,'session','sessions','session'),(8,'site','sites','site'),(9,'redirect','redirects','redirect'),(10,'migration history','south','migrationhistory'),(11,'Droga','clients','drug'),(12,'Rizikové chování','clients','riskybehavior'),(13,'Kraj','clients','region'),(14,'Okres','clients','district'),(15,'Město','clients','town'),(16,'Osoba','clients','person'),(17,'Odborný kontakt','clients','practitionercontact'),(18,'Anonym','clients','anonymous'),(19,'Klient','clients','client'),(20,'Anamnéza','clients','anamnesis'),(21,'Poznámka','clients','clientnote'),(22,'Užívaná droga','clients','drugusage'),(23,'Rizikové chování','clients','riskymanners'),(24,'Vyšetření onemocnění','clients','diseasetest'),(25,'Kontakt','services','encounter'),(26,'service','services','service'),(27,'Harm Reduction','services','harmreduction'),(28,'Testování infekčních nemocí','services','diseasetest'),(29,'Asistenční služba','services','asistservice'),(30,'Informační servis','services','informationservice'),(31,'Krizová intervence','services','crisisintervention'),(32,'Sociální práce','services','socialwork'),(33,'Vstupní zhodnocení stavu klienta','services','incomeexamination'),(34,'Kontaktní práce','services','contactwork'),(46,'Použití telefonu klientem','services','phoneusage'),(36,'Další úkony','services','utilitywork'),(37,'Základní zdravotní ošetření','services','basicmedicaltreatment'),(38,'Individuální poradenství','services','individualcounseling'),(39,'Oslovení','services','address'),(40,'search encounter','reporting','searchencounter'),(41,'search service','reporting','searchservice'),(42,'syringe collection','syringes','syringecollection'),(43,'search syringe collection','reporting','searchsyringecollection'),(44,'Vyplnění IN-COME dotazníku','services','incomeformfillup'),(45,'Odborný kontakt','services','practitionerencounter');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_redirect`
--

DROP TABLE IF EXISTS `django_redirect`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_redirect` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `site_id` int(11) NOT NULL,
  `old_path` varchar(200) NOT NULL,
  `new_path` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `site_id` (`site_id`,`old_path`),
  KEY `django_redirect_6223029` (`site_id`),
  KEY `django_redirect_516c23f0` (`old_path`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_redirect`
--

LOCK TABLES `django_redirect` WRITE;
/*!40000 ALTER TABLE `django_redirect` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_redirect` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_3da3d3d8` (`expire_date`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('62f1126c3091014372d9d785404c9b52','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-01-18 18:16:39'),('7f04c73dc6e16b9f3307d0a768d1cb84','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-01-26 11:18:08'),('0c9372f81bffdc4283e2cc29fda87abb','NzQ4OWVkZjA1YmNkZWFlNjlmNzE4ZWQ3YzgwOWIzMjUzOTY0NjQ3ODqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==\n','2012-01-17 21:26:42'),('7ed7538b54b21932ca12f4efc99cab10','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-01-18 18:21:09'),('2151a271ec0703581c2da9b77f613faa','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-01-18 11:45:42'),('5adbf8b4dddc4d9a098c26baf2877f8f','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-01-18 11:45:59'),('b2f6cc3f1ed2c8cf3af2ab68c6ad6be2','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-01-19 10:10:15'),('7c4065d238a0ee7070f13e6b0493a66f','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-01-19 16:00:42'),('1ff00883a6a9f1417546cf41c379b792','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-01-25 11:59:40'),('231182a8a87848118a995e6277b7ae6e','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-01-25 13:40:46'),('58c6d943dbca5d7b491c09414e0c9972','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-02-05 19:36:45'),('e10590ede1fbcd4034a8848ec177ce34','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-01-30 10:58:33'),('ab6e46986955e1800cb172b9519f6ff9','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-02-09 23:05:02'),('01fcca3e53e1dc88a8218db2deecb715','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-02-05 19:27:21'),('ff3f006d8c6e9ffe434229291d1d8dbd','ZTFlZWM4NTA2MzA1NjA3ZGIwOGI1NDZjMjUwNmRiY2FmOTNiMzg3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2012-02-08 22:07:45'),('568b4686018ca8c06df5b3ebaab836f3','ZTFlZWM4NTA2MzA1NjA3ZGIwOGI1NDZjMjUwNmRiY2FmOTNiMzg3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2012-02-05 19:31:04'),('4933beef20516f2ae1618eb8c8bdac41','ZTFlZWM4NTA2MzA1NjA3ZGIwOGI1NDZjMjUwNmRiY2FmOTNiMzg3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2012-02-05 19:30:50'),('fc264fa2c29cefcd8f64a1058f882150','ZTFlZWM4NTA2MzA1NjA3ZGIwOGI1NDZjMjUwNmRiY2FmOTNiMzg3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2012-02-15 17:19:03'),('3a05421693f7cfff3b8525e95586f968','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-02-14 08:51:54'),('2f9b3b7af9e7b9860491ce0d611ca80a','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-02-15 09:53:06'),('c916db8ab348e43f612777eac4911ba0','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-02-25 17:55:56'),('3094be35512b5fba616a6df59b5114d4','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-02-15 13:31:08'),('5d7497496667cdc8f362a7d1bfceecec','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-02-28 13:05:37'),('bc8eabf241feabdc8ac2f7fe053f15f3','ZTFlZWM4NTA2MzA1NjA3ZGIwOGI1NDZjMjUwNmRiY2FmOTNiMzg3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2012-02-15 18:41:06'),('aeb172ef827e4080785c1f2c681f3eb1','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-02-15 18:25:03'),('4fb78489746876907c961cb96158420d','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-02-16 08:41:03'),('0cc912ba9fafcb25d9e7a8bed096ee05','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-02-19 09:43:13'),('2561f8855ad8e508f5107e60c21cc366','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-02-19 13:05:09'),('35692c70dd97c0993773685db8b4d2c4','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-02-19 10:41:32'),('72b9db9a71b58bddb151994e5ef5a2d0','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-02-19 21:29:36'),('32581193c6625b01f1f6631e72653319','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-03-06 17:10:28'),('ec4fdac190bbd7ad8ebeb9a77e46417c','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-03-04 16:21:54'),('bf9388f0d6b62556e54e32cbf0c68ae0','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-03-07 14:01:37'),('ec65abe0b4d6030efa63a787ca861d1d','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-03-07 14:04:55'),('08af55ab4a2adb0b55a5adfe09889a15','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-03-11 13:56:03'),('eb4f890bf5cf98f01334b66c3df673b8','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-03-09 12:16:40'),('aa0e06bf697bba48f47675b32cf84c6d','ZTFlZWM4NTA2MzA1NjA3ZGIwOGI1NDZjMjUwNmRiY2FmOTNiMzg3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2012-03-14 18:12:04'),('b3eeef4c94ccd890bc76459c80112e8f','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-03-12 12:08:20'),('1106dc01d1f6bb34870db785bbf59a4e','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-03-11 13:11:42'),('0905eb14939ebce1c5eb1f8da21733ce','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-03-12 10:49:55'),('bee95a078bf759fc91be37cdd1334066','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-03-12 11:35:40'),('e02906055749012bb4829c6575aae084','ZTFlZWM4NTA2MzA1NjA3ZGIwOGI1NDZjMjUwNmRiY2FmOTNiMzg3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2012-03-12 12:12:20'),('c9d69c399adbb9473d5b7f0cdd47412e','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-03-14 17:11:42'),('5d6b55413b1cd6affa0aa1d833cd041b','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-03-15 09:21:40'),('906e5d20378d6a39a35f73795f968c73','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-03-14 17:10:25'),('bf6236f9469df97e4ef9631585696c66','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-03-15 17:11:30'),('cf61d81064169d6315f8f73958e182cd','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-03-15 09:23:09'),('88b3d17b1a75150e5a2c0aab95c48a4b','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-03-15 21:41:08'),('b691be9ab33033892532aeba81b414f3','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-03-15 21:35:46'),('36faaf9e6a493e242dccbe6f3f490575','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-03-16 08:52:13'),('48de25ef90bcfdc827a14f6c6a0f3467','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-03-16 11:28:03'),('6c5be0bcb57f9df25c5068f048cf8a4d','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-03-16 16:18:55'),('f13f6a1c9f12df7254a740176be3469e','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-03-16 16:20:19'),('7740be8fbeeb9653de59762d5f5e9c1c','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-03-19 11:09:06'),('dcfdae7a4e006e8e63f023bc8d6d748e','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-03-19 11:13:11'),('51ebf1c713de38cc94062f0ccc5f3f65','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-03-19 11:22:58'),('61468af2245a0fd2021c11a1aa452e0b','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-03-16 12:13:57'),('64ec63acda6a1a80a2f695ff12f404d1','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-03-19 16:44:07'),('b5e4864a7a22879be39b6751701f0f8b','ZTFlZWM4NTA2MzA1NjA3ZGIwOGI1NDZjMjUwNmRiY2FmOTNiMzg3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2012-03-19 11:30:01'),('4fd266cd901b3526a26d05d4d1825814','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-03-19 16:25:45'),('3c008d1653d1c657e2ae9a16f2bb72c4','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-03-19 16:44:14'),('2cd73615e753de01906060f140361724','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-03-22 10:07:22'),('81e94300fc3695230c471335891efad1','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-03-21 13:02:35'),('e6842b7b19039cd81d906520ea9fb204','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-03-22 11:29:32'),('ab67e8c4ee32a7ffa2015f409a9ba2aa','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-03-21 14:42:06'),('5afcb24d5f40fe0afde9aabeafcf6d1e','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-03-22 09:41:22'),('8833d216b85c426dd719b5ed20001f08','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-03-22 21:39:18'),('58d7cb41fd6195bd827cfe5aaac14bb9','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-04-01 06:06:17'),('82e7733ed7b90a3d9ce0df8e24431908','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-03-23 10:46:52'),('36833569bb3b59c076f02c9c3af92dbe','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-03-23 13:48:55'),('432ba7f0c839a47a6c9bb89c61c61250','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-03-26 10:39:29'),('1e1a52fe3b6e8d1c99025fde507ff3d3','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-03-23 12:39:27'),('85f3a136586cc07bfaa30a49c53cc526','ZWE5M2QyYmFkYTA0MGQwOWY3MjFmNmMzZmI5ZmE2M2IyYjc0Nzc3ZTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQV1Lg==\n','2012-03-26 10:00:57'),('57531a0d39b3e7fcddd91557f3224ea1','ZWE5M2QyYmFkYTA0MGQwOWY3MjFmNmMzZmI5ZmE2M2IyYjc0Nzc3ZTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQV1Lg==\n','2012-03-27 08:58:35'),('07a61b52f7d91eba5285f0b0cb1623e3','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-04-07 10:37:40'),('91285dfb8aa3b9d7f97cb3878491a8a1','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-04-02 13:14:33'),('99b263af2bb592ff6616ebc5f7895075','YTQ4NDAwZWVlM2ZiZjM3MDZhY2QxOTNjMzk2MWE4ZThkYmI5NjEyNTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQZ1Lg==\n','2012-04-03 12:49:14'),('10cf03a12c7bb680b02a80d8f92496fc','ZTFlZWM4NTA2MzA1NjA3ZGIwOGI1NDZjMjUwNmRiY2FmOTNiMzg3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2012-04-23 16:48:47'),('f8d1e02ee5980cf4b31e7465a3b225f8','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-04-13 11:36:37'),('9bffeac5c908071d0f90c2fc0914dd8b','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-04-10 13:05:38'),('bdec07a970a99ed1a7119350cd006b96','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-04-13 13:02:34'),('ee622b6cb7cce411b4edacbf6e9170e6','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-04-13 11:37:06'),('55042f1f44ad605b03ba58519185349b','ZTFlZWM4NTA2MzA1NjA3ZGIwOGI1NDZjMjUwNmRiY2FmOTNiMzg3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2012-04-11 13:11:01'),('6e772bd1d411f7a2f60498cd31ba6200','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-04-13 13:39:35'),('866eaca66eec56fb6fcc9b8d5194d187','ZTFlZWM4NTA2MzA1NjA3ZGIwOGI1NDZjMjUwNmRiY2FmOTNiMzg3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2012-04-23 14:55:27'),('86541add664a429b7f018f71f147bb32','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-04-18 18:21:04'),('a70f07ac6519831a899b5080cab98e08','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-04-16 12:48:27'),('58fcfe96cf35bcf3425881a1cae684b0','ZTFlZWM4NTA2MzA1NjA3ZGIwOGI1NDZjMjUwNmRiY2FmOTNiMzg3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2012-04-18 18:11:02'),('4a63ef6384f3b1a32418dc4744caa048','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-06-01 12:52:22'),('ecd9248fe505c7b971cce54f3f75dad6','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-04-16 10:10:54'),('987248300f56c17c6d8a17fd5f5aee09','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-04-25 13:49:30'),('41c0163a29c5f5ae8e634790711c513b','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-04-26 19:22:58'),('ca31cba2672887032cc7063e7060e5f1','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-06-09 18:13:49'),('ebe830dbd7a90dba2ed23ec1ad7681a7','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-05-02 15:18:56'),('4eca3ee51c388c35ff1d29bb38b506e1','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-04-27 11:55:59'),('460bcb59d859b5e58866bac586fed169','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-05-01 05:10:02'),('63463bdd9476f86a1e456e63cae40fe7','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-05-10 09:49:52'),('945418fac43cb4b368c0b6e8b2dd97ae','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-05-28 16:54:27'),('90de531865b5352cf5dccfc4ba01f953','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-05-30 13:14:16'),('85cb2827a53654d86eeda6aa5ec1c4ff','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-06-08 16:27:42'),('47cfc678868b8cc22dfcd1ed3e4d0f78','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-06-10 23:43:57'),('1d2001fca0b874bc6e13d80830989501','ZTFlZWM4NTA2MzA1NjA3ZGIwOGI1NDZjMjUwNmRiY2FmOTNiMzg3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2012-06-24 19:14:22'),('00d8a03e980902539c3b5fd04a86abca','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-06-13 13:42:53'),('202b08da1dbcf96923317b7178e9fa75','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-06-14 09:33:29'),('fa8331c994b11f80cf67c42d4714a519','ZTFlZWM4NTA2MzA1NjA3ZGIwOGI1NDZjMjUwNmRiY2FmOTNiMzg3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2012-06-24 19:14:03'),('7fba3ca070f5f72320b36f09a4cc1906','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-06-20 13:40:31'),('2f57c3359d6d56310c56bec534f24d33','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-06-24 14:17:10'),('dcb6046e91599fbba2c908dbab587c82','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-06-27 08:31:13'),('ce15132369775e1214b38908a8d8bc97','ZTFlZWM4NTA2MzA1NjA3ZGIwOGI1NDZjMjUwNmRiY2FmOTNiMzg3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2012-06-25 13:00:18'),('b4329a7c06fe0e419c590d923b67bf5c','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-06-27 09:07:11'),('a8931216a03575da3a0d3313a384aa87','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-06-27 22:51:32'),('c3b2107dc5b7edf86d6a3d855a9bd10a','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-06-28 07:53:49'),('b149fed01b77a032c29a1141cffd0e2b','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-06-28 12:53:16'),('e9be0e029bcca0ed2337609af157fbc7','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-06-29 11:17:35'),('64b39a757cc27acfb601e82223c89452','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-06-29 10:46:04'),('721a36bda12dbe012038c91d6a22f97e','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-06-29 13:05:43'),('81eea062f722adec5e2881c6b6972dd6','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-06-29 16:45:32'),('11ef9c0827745b4cd1fd721f194f5f36','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-06-29 17:54:37'),('960df265bad0157d9e0622d1da15f93f','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-06-29 19:00:56'),('c132976d2031d4c66e9d37aad16db370','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-06-29 22:45:03'),('d7f078daa4c09e7231d664addaa3c5bc','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-06-30 08:50:48'),('1c93422c4b368d1a0e4baba9efc81374','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-07-01 11:07:37'),('cc7de9861c436dc6f3ee720902ef5e2c','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-07-01 12:13:12'),('f831abcc264749692a009e7247a97352','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-07-01 19:47:38'),('78bad350d3610fae0eccba483b18c2b2','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-07-02 21:28:02'),('9da0805884b16203c8120de6b374cae0','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-07-02 23:06:32'),('0a7fd77b99f9e50c9682d24d73c5544e','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-07-03 07:40:47'),('2e55012df96a573e44ea7e8515dbf080','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-07-03 13:05:34'),('80067f74a95a750be4709fd566c14e75','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-07-03 21:31:26'),('420c421a7e0c39b0c6caf4f9d3a79642','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-07-04 09:22:14'),('6af6034a0dfe9a5d2a2293e1473a9a3f','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-07-04 10:56:03'),('8538612e9cc05da115ce910b4977baab','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-07-04 23:52:08'),('ba073f8f55c183edac223ea8dd661a7a','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-07-06 00:04:34'),('507ef9be653fa71ad97b0315619413e4','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-07-08 17:15:57'),('2ca6474ab191fc1d579a225a5f679df3','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-07-08 18:26:35'),('8019666f9cdd1b8b86661820d3125a3a','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-07-08 20:39:50'),('54cf4fdbc7ce1764c2b4ebb22a865395','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-07-11 17:57:59'),('c8f9de0802656d3c4f5c7d60c85e3155','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-07-11 19:32:28'),('9fc56b2d97347c369c76bfd9f9523e42','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-07-16 12:48:17'),('1a6789aec701fbce1452d815ab5f725b','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-07-16 15:21:54'),('db5e9b38cda1f5c65cb69db145361047','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-08-08 14:38:58'),('9ce5caa40f0820604b1fbb123b8a5601','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-07-17 14:30:36'),('dc78298a73e690ded7de991bbe6d1bb7','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-08-01 09:44:55'),('d57160e6ff9744395e5aaf4b9dc27d63','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-08-01 09:32:29'),('ebfcaa6df199278c6e2b10cb80cbb176','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-08-01 18:53:55'),('cb2cced702a1b2b6af1d737361cb3fdf','ZTFlZWM4NTA2MzA1NjA3ZGIwOGI1NDZjMjUwNmRiY2FmOTNiMzg3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2012-08-08 12:52:35'),('eee4bb1c71adced9d8de4b996d130d30','ZTFlZWM4NTA2MzA1NjA3ZGIwOGI1NDZjMjUwNmRiY2FmOTNiMzg3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2012-08-01 09:39:26'),('afcc3b5e06dab2bac95e006261ba84b9','ZTFlZWM4NTA2MzA1NjA3ZGIwOGI1NDZjMjUwNmRiY2FmOTNiMzg3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2012-08-01 18:44:24'),('eaacaf6ed7c95a219366e5623f339d65','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-08-06 10:02:43'),('7a2758935262b08522b3caf635ef9d57','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-08-08 14:55:15'),('ff1b2f961e381dd701e9e9ff7c025483','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-08-08 14:54:54'),('93206f71befc6979b931f2180c33a14b','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-08-08 14:40:20'),('936b2dcf98caa39ffe25622a0287f947','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-08-08 14:42:57'),('f3d6db4f0b8152789168f4ea6680e356','ZTFlZWM4NTA2MzA1NjA3ZGIwOGI1NDZjMjUwNmRiY2FmOTNiMzg3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2012-08-08 14:41:00'),('aab145affd4335b26392edb15a49e396','ZTFlZWM4NTA2MzA1NjA3ZGIwOGI1NDZjMjUwNmRiY2FmOTNiMzg3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2012-08-08 14:43:07'),('d7fdc1c2a99cbd740c984c3bbed42115','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-09-20 12:54:58'),('548af124bc272adecf6c8cf5f2d8ce71','ZTFlZWM4NTA2MzA1NjA3ZGIwOGI1NDZjMjUwNmRiY2FmOTNiMzg3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2012-09-14 10:27:32'),('b1a080ee15a478e8bbf16a9ee2b22bfd','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-08-13 12:32:08'),('48123a3295369827ab1614ed71c1d286','ZTFlZWM4NTA2MzA1NjA3ZGIwOGI1NDZjMjUwNmRiY2FmOTNiMzg3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2012-08-20 11:54:46'),('79f3307236485894cb6c1f25584921f6','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-08-20 13:49:33'),('42ace7a7b334cde294437af0e02aea0f','ZTFlZWM4NTA2MzA1NjA3ZGIwOGI1NDZjMjUwNmRiY2FmOTNiMzg3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2012-08-28 12:32:02'),('d149d125730dab5cf12fbc4f7e992c4b','ZTFlZWM4NTA2MzA1NjA3ZGIwOGI1NDZjMjUwNmRiY2FmOTNiMzg3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2012-08-20 13:28:24'),('4876d9d474047877c08f808442c1e9bd','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-08-24 13:21:05'),('a233e0f55cead3edf78f93aad1be8a58','ZTFlZWM4NTA2MzA1NjA3ZGIwOGI1NDZjMjUwNmRiY2FmOTNiMzg3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2012-08-29 13:00:56'),('bbd0e8553009ae2f8e8b850cd7de6188','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-09-03 01:25:50'),('4fbb6c9d5e3627c32a090f28f18b6cb1','ZTFlZWM4NTA2MzA1NjA3ZGIwOGI1NDZjMjUwNmRiY2FmOTNiMzg3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2012-09-20 12:48:44'),('e934a0c4a14f2dff02b8848ba767d2ba','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2012-09-03 17:24:11'),('bc78595fcd99172b5e914d29ae3eea57','ZTFlZWM4NTA2MzA1NjA3ZGIwOGI1NDZjMjUwNmRiY2FmOTNiMzg3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2012-09-07 10:28:59'),('cd77427ef4bd082b5e2ea557a7e1ecf8','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-09-13 12:54:48'),('da3e46eae8d807dc4ab65afc7ce56b87','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-09-11 12:19:11'),('b4af918c01a0710fc3149065711cd907','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-09-20 12:54:45'),('b58b53f582d425c376d8c185f93ae17d','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-09-20 12:54:53'),('3ebfc0669090d5502c4ce40bc2ff7175','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-09-20 13:41:57'),('76180b5f300b8b06b5dca6aebebae8ef','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-09-20 13:42:06'),('307ded2168b6fb9192fda30832ad7a8a','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-09-20 13:42:15'),('1240d7e5f7d19367b6794a464155f3de','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-12-09 11:33:38'),('6ab94f842bb7be4ac6fee9a988cdf8b7','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-12-09 11:33:27'),('7cda9e138121e0aef6c0febb7f2be485','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-12-06 12:53:49'),('5b38981abc50c1cc086d0f41afa6cd89','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-12-03 17:40:10'),('ea5916f28022193720ab0c9881f4dbb6','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-12-04 12:04:24'),('81b3bfb34516243a5d6d7bb58757f3fd','ZWNlYWI3NmZmMWMyZDA5MzcyYTY0NDY5OTc2NTcxOTliOTYyMDE5YjqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQp1Lg==\n','2012-11-15 10:01:24'),('ff8f723cd41a4a40fbe209da1e526ab5','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-11-06 10:39:37'),('b5bcf8f323facf7ccd5826215d31b0a5','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-11-06 10:40:16'),('bba6ed4e574ba2150b4cba65a7a53b5f','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-10-04 12:49:27'),('3ef1937caa55501a897fb0e7baacaeaa','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-10-04 14:24:42'),('54108e78d5b4230d05d0008f74ddddc2','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-10-15 09:47:03'),('4c9398b746fc593f71a6010507bbf781','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-10-15 10:11:00'),('a1ca4bc99739b766570675ff5f6b9406','ZTFlZWM4NTA2MzA1NjA3ZGIwOGI1NDZjMjUwNmRiY2FmOTNiMzg3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2012-10-15 10:13:04'),('d081ba23e7fe2989033b0af6474a0563','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-11-23 10:45:11'),('5af6713b51769b7c5e730c1ab572d2cf','ZWE2ZjY1N2Y4Y2FlYTZiYzQzYTE2MDJiMTMzZjU4ZWY3NDVjNDNiYzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQh1Lg==\n','2012-10-25 09:37:48'),('7887b46df4f73d1a6cd1f3fceb0eaee3','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2012-10-15 10:24:56'),('5bef8378289e0bdd9a4e22bef34910a3','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-10-22 13:39:04'),('1d88fa32dbf5a1f734eb18ef3c90272b','ZTFlZWM4NTA2MzA1NjA3ZGIwOGI1NDZjMjUwNmRiY2FmOTNiMzg3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2012-10-15 10:59:41'),('52b20937265858a2b3de7e0c5cfda774','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2013-01-05 19:26:48'),('1e4b478794feb91fed989f8421795442','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2013-01-18 13:51:17'),('4233f1ac63ea405e844b86a3144b8db7','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2013-02-12 15:05:00'),('dff2199573df16dea292e22619a9a228','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2013-03-11 13:09:33'),('1510dc4cce59ae21913683d45a3a1427','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2013-03-11 13:09:33'),('40e0d1fa8bafde7b13acc6039b1ffea6','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2013-05-23 11:31:40'),('436ff117684f67d623754aa554b82776','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2013-06-10 21:50:58'),('7ba9a4dff3f5076d709b0046e0bcceaf','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2013-06-13 04:45:30'),('b31eea157b0bce21b7662bd6868177f1','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2013-06-26 22:55:04'),('de1eb3ac3772e15f9eff7b39d99606a6','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2013-07-25 11:08:47'),('88db2a7170ec9d4788fb2d8db1a88102','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2013-07-25 18:43:50'),('a08196b2605d29e5c8761a008464c358','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2013-08-01 07:21:21'),('cbc52df6704ba0a802af65189d72f0f3','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2013-08-02 12:56:31'),('320a2ebdab8e29f10083e9764a9f58af','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2013-08-03 22:11:43'),('a74a99c679c5cfcdf923f503527b7159','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2013-08-07 16:43:11'),('5d2a4b8d93f71150aae24c764fd571d0','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2013-08-08 10:35:14'),('88487b42945658fa5ef20ef2f03d33ea','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2013-08-14 12:11:17'),('fb61af4c33482c449bb9855d3b9c5845','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2013-08-16 04:16:10'),('eec0f290b8d7e3ecd347cf5706b74a32','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2013-08-16 09:21:16'),('7d3de51bff0fce561a208fd7c269a698','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2013-08-28 07:10:43'),('01afe4b8b160f48a4816cbebe29b2d63','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2013-08-31 19:10:45'),('2ccc1b8733180ad37c7e0309daa7fb81','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2013-09-12 15:17:31'),('730896dbd1a8e64d661428bf625cd9db','ODM0MzRjMTQ0ZmI2YjAwNzhmNjkxYWQzYmNhOGY2MDBjNGVlZTUwNDqAAn1xAShVDV9hdXRoX3Vz\nZXJfaWRxAooBA1USX2F1dGhfdXNlcl9iYWNrZW5kcQNVKWRqYW5nby5jb250cmliLmF1dGguYmFj\na2VuZHMuTW9kZWxCYWNrZW5kcQR1Lg==\n','2013-09-12 15:25:24'),('8471a6eb4e31d45991f2d2a0ce461c41','YTc1NzNkOTIyNDZmODVmY2Y0ZTNiZDRiOGMzOWUyMTcyZWNjOGE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2013-09-04 11:56:48'),('619250475074ee82e0673df25b950cb0','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2013-09-18 13:56:38'),('d413d17af3e974ce89401d491b4fd47e','MmIwNjUwYjhmZWIzZjUxOGRkNGNhMmViZTA0MjgyMDg1MmQ5Yzg3NDqAAn1xAShVDV9hdXRoX3Vz\nZXJfaWRxAooBBFUSX2F1dGhfdXNlcl9iYWNrZW5kcQNVKWRqYW5nby5jb250cmliLmF1dGguYmFj\na2VuZHMuTW9kZWxCYWNrZW5kcQR1Lg==\n','2013-09-18 11:27:36'),('94173937ed350a1164fab685286e64ea','ZTFlZWM4NTA2MzA1NjA3ZGIwOGI1NDZjMjUwNmRiY2FmOTNiMzg3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2013-09-25 13:31:17'),('0bd18b5f9db62a41eaa67995b312e49a','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2013-10-14 13:53:56'),('e454d459d26efca03ad768023ebc234d','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2013-09-23 14:07:21'),('703f95ef519f2c2675811a681634c990','ODM0MzRjMTQ0ZmI2YjAwNzhmNjkxYWQzYmNhOGY2MDBjNGVlZTUwNDqAAn1xAShVDV9hdXRoX3Vz\nZXJfaWRxAooBA1USX2F1dGhfdXNlcl9iYWNrZW5kcQNVKWRqYW5nby5jb250cmliLmF1dGguYmFj\na2VuZHMuTW9kZWxCYWNrZW5kcQR1Lg==\n','2013-10-14 10:48:39'),('f2ab7a1d0aa80d9df44383d1338f204c','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2013-09-25 14:25:23'),('51590183f50263be5e97a8801ccb3cc4','ZTFlZWM4NTA2MzA1NjA3ZGIwOGI1NDZjMjUwNmRiY2FmOTNiMzg3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2013-10-17 10:20:43'),('c1fac6930db38e534749d84a0deddd20','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2013-10-20 19:34:41'),('e02383ee2bfaf041c133684572a85164','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2013-10-17 00:53:19'),('4cba2192e5b01543df05cf8ee7e75edc','ZTFlZWM4NTA2MzA1NjA3ZGIwOGI1NDZjMjUwNmRiY2FmOTNiMzg3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2013-10-16 13:55:27'),('83c5104db856bab47a50218afe8a52b2','ODM0MzRjMTQ0ZmI2YjAwNzhmNjkxYWQzYmNhOGY2MDBjNGVlZTUwNDqAAn1xAShVDV9hdXRoX3Vz\nZXJfaWRxAooBA1USX2F1dGhfdXNlcl9iYWNrZW5kcQNVKWRqYW5nby5jb250cmliLmF1dGguYmFj\na2VuZHMuTW9kZWxCYWNrZW5kcQR1Lg==\n','2013-10-14 14:42:15'),('18c0fe841cdaa605b735b0241e8fd621','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2013-10-18 09:41:12'),('7ae1fbf65bb7d7b8d04a7b19fc4d2cfb','ZTFlZWM4NTA2MzA1NjA3ZGIwOGI1NDZjMjUwNmRiY2FmOTNiMzg3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2013-10-16 15:20:22'),('f4711660bcb154fc3ede5784885f6c17','ZTFlZWM4NTA2MzA1NjA3ZGIwOGI1NDZjMjUwNmRiY2FmOTNiMzg3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2013-10-16 10:35:32'),('4e63781d2b25ba8eb2924bb525e5a2b6','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2013-10-16 14:36:40'),('6f4aa0ac245a0f8165591c89b0e9b6c6','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2013-11-18 12:55:51'),('dd0a376894ad370f4bd4531077466ca3','MmIwNjUwYjhmZWIzZjUxOGRkNGNhMmViZTA0MjgyMDg1MmQ5Yzg3NDqAAn1xAShVDV9hdXRoX3Vz\nZXJfaWRxAooBBFUSX2F1dGhfdXNlcl9iYWNrZW5kcQNVKWRqYW5nby5jb250cmliLmF1dGguYmFj\na2VuZHMuTW9kZWxCYWNrZW5kcQR1Lg==\n','2013-10-22 12:54:41'),('2e18fa58749f4c67a8916f6e4c5336c8','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2013-10-23 12:43:40'),('c7bca79c07082acfba34abdb221b8cfa','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2013-10-25 09:26:10'),('a80c23177036d39281d798d0fd117883','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2013-10-29 10:38:20'),('887cc3b8361beb3842259fc82ac6b689','YjE4ZTUzODY0M2U5MTcwNTk1YWY2YTVhYjJmNDFhZTQwYmFkMmU1ODqAAn1xAS4=\n','2013-11-15 13:37:44'),('5d3c43952876188255db7f0971031ad2','ODM0MzRjMTQ0ZmI2YjAwNzhmNjkxYWQzYmNhOGY2MDBjNGVlZTUwNDqAAn1xAShVDV9hdXRoX3Vz\nZXJfaWRxAooBA1USX2F1dGhfdXNlcl9iYWNrZW5kcQNVKWRqYW5nby5jb250cmliLmF1dGguYmFj\na2VuZHMuTW9kZWxCYWNrZW5kcQR1Lg==\n','2013-11-15 15:52:42'),('74b4465b08ce079dbee218ad2115958e','ODM0MzRjMTQ0ZmI2YjAwNzhmNjkxYWQzYmNhOGY2MDBjNGVlZTUwNDqAAn1xAShVDV9hdXRoX3Vz\nZXJfaWRxAooBA1USX2F1dGhfdXNlcl9iYWNrZW5kcQNVKWRqYW5nby5jb250cmliLmF1dGguYmFj\na2VuZHMuTW9kZWxCYWNrZW5kcQR1Lg==\n','2013-11-14 15:23:39'),('4db209226df3c9079556c71d80784371','MDY5ZDJmMjczMDgyNWRjY2Q1MGZlNzg0ZWFjMTMzMDRiYzYwNTA0NTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2013-11-14 16:24:28'),('76a82bc4c6279c945822606ba72beb9e','ZTFlZWM4NTA2MzA1NjA3ZGIwOGI1NDZjMjUwNmRiY2FmOTNiMzg3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2013-11-15 14:05:19'),('8b69248058327c98636664a9a7d978da','ZTFlZWM4NTA2MzA1NjA3ZGIwOGI1NDZjMjUwNmRiY2FmOTNiMzg3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQN1Lg==\n','2013-11-18 10:43:59');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `reporting_searchencounter`
--

DROP TABLE IF EXISTS `reporting_searchencounter`;
/*!50001 DROP VIEW IF EXISTS `reporting_searchencounter`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `reporting_searchencounter` (
 `id` tinyint NOT NULL,
  `person_id` tinyint NOT NULL,
  `town_id` tinyint NOT NULL,
  `is_by_phone` tinyint NOT NULL,
  `year` tinyint NOT NULL,
  `month` tinyint NOT NULL,
  `is_client` tinyint NOT NULL,
  `client_sex` tinyint NOT NULL,
  `primary_drug_id` tinyint NOT NULL,
  `primary_drug_usage` tinyint NOT NULL,
  `is_close_person` tinyint NOT NULL,
  `is_sex_partner` tinyint NOT NULL,
  `is_anonymous` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `reporting_searchservice`
--

DROP TABLE IF EXISTS `reporting_searchservice`;
/*!50001 DROP VIEW IF EXISTS `reporting_searchservice`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `reporting_searchservice` (
 `id` tinyint NOT NULL,
  `service_id` tinyint NOT NULL,
  `encounter_id` tinyint NOT NULL,
  `content_type_model` tinyint NOT NULL,
  `town_id` tinyint NOT NULL,
  `person_id` tinyint NOT NULL,
  `year` tinyint NOT NULL,
  `month` tinyint NOT NULL,
  `is_client` tinyint NOT NULL,
  `is_anonymous` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `reporting_searchsyringecollection`
--

DROP TABLE IF EXISTS `reporting_searchsyringecollection`;
/*!50001 DROP VIEW IF EXISTS `reporting_searchsyringecollection`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `reporting_searchsyringecollection` (
 `id` tinyint NOT NULL,
  `count` tinyint NOT NULL,
  `town_id` tinyint NOT NULL,
  `month` tinyint NOT NULL,
  `year` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `services_asistservice`
--

DROP TABLE IF EXISTS `services_asistservice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `services_asistservice` (
  `service_ptr_id` int(11) NOT NULL,
  `where` varchar(10) NOT NULL,
  `note` longtext,
  PRIMARY KEY (`service_ptr_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services_asistservice`
--

LOCK TABLES `services_asistservice` WRITE;
/*!40000 ALTER TABLE `services_asistservice` DISABLE KEYS */;
INSERT INTO `services_asistservice` VALUES (16161,'s',''),(16170,'s',''),(16192,'m',''),(16203,'f',''),(16221,'s',''),(16235,'f','odvoz do TK Bílá Voda');
/*!40000 ALTER TABLE `services_asistservice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `services_diseasetest`
--

DROP TABLE IF EXISTS `services_diseasetest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `services_diseasetest` (
  `service_ptr_id` int(11) NOT NULL,
  `disease` smallint(5) unsigned,
  `sign` varchar(1),
  `pre_test_advice` tinyint(1) NOT NULL,
  `test_execution` tinyint(1) NOT NULL,
  `post_test_advice` tinyint(1) NOT NULL,
  PRIMARY KEY (`service_ptr_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services_diseasetest`
--

LOCK TABLES `services_diseasetest` WRITE;
/*!40000 ALTER TABLE `services_diseasetest` DISABLE KEYS */;
INSERT INTO `services_diseasetest` VALUES (16191,4,'n',1,1,1),(16173,1,'r',0,1,0);
/*!40000 ALTER TABLE `services_diseasetest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `services_encounter`
--

DROP TABLE IF EXISTS `services_encounter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `services_encounter` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `performed_on` date NOT NULL,
  `where_id` int(11) NOT NULL,
  `is_by_phone` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `services_encounter_21b911c5` (`person_id`),
  KEY `services_encounter_5c076264` (`where_id`)
) ENGINE=MyISAM AUTO_INCREMENT=12154 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services_encounter`
--

LOCK TABLES `services_encounter` WRITE;
/*!40000 ALTER TABLE `services_encounter` DISABLE KEYS */;
INSERT INTO `services_encounter` VALUES (12137,884,'2013-10-16',33,0),(12136,875,'2013-09-03',32,0),(12135,875,'2013-09-12',48,0),(12134,875,'2013-09-27',34,1),(12025,5,'2012-02-23',34,0),(12024,5,'2012-02-23',34,0),(12133,880,'2013-09-25',47,1),(12132,880,'2013-09-18',47,0),(12131,879,'2013-09-25',34,0),(12130,879,'2013-09-18',42,0),(12129,878,'2013-09-26',32,0),(12017,8,'2012-02-01',34,0),(12128,878,'2013-09-19',32,0),(12127,876,'2013-09-20',39,0),(12126,876,'2013-09-13',39,0),(12125,879,'2013-10-01',47,0),(12124,883,'2013-10-01',47,1),(12123,882,'2013-10-01',48,0),(12122,877,'2013-10-08',48,0),(12121,877,'2013-10-02',32,0),(12072,8,'2012-08-20',48,1),(12120,877,'2013-10-16',32,0),(12070,8,'2012-08-20',33,0),(12119,875,'2013-09-18',31,1),(12118,874,'2013-09-18',31,0),(12068,7,'2012-08-20',38,0),(12102,886,'2013-10-14',34,0),(12117,884,'2013-09-17',31,0),(12116,884,'2013-09-10',31,0),(12040,1,'2012-03-30',39,1),(12115,884,'2013-09-03',31,0),(12114,878,'2013-09-02',42,0),(12113,883,'2013-10-14',33,0),(12065,8,'2012-08-20',46,0),(12101,885,'2013-10-14',46,0),(12046,7,'2012-05-16',34,0),(12112,883,'2013-10-11',34,0),(12048,1,'2012-05-16',42,0),(12111,883,'2013-10-04',34,0),(12110,882,'2013-09-26',39,1),(12140,882,'2013-10-02',31,1),(12109,881,'2013-09-26',39,0),(12053,5,'2012-05-27',38,0),(12054,8,'2012-05-27',32,0),(12108,881,'2013-09-25',39,0),(12057,5,'2012-05-27',39,0),(12107,880,'2013-09-03',46,0),(12106,880,'2013-09-26',32,0),(12060,8,'2012-06-06',31,0),(12073,6,'2012-08-20',47,0),(12139,884,'2013-10-08',38,0),(12100,887,'2013-10-14',46,1),(12099,886,'2013-10-14',46,1),(12098,885,'2013-10-14',46,0),(12097,874,'2013-07-03',42,0),(12105,879,'2013-09-19',32,0),(12138,884,'2013-10-04',38,0),(12096,874,'2013-07-15',42,0),(12095,874,'2013-08-05',42,0),(12094,874,'2013-08-07',38,0),(12093,874,'2013-09-23',38,0),(12104,875,'2013-10-16',34,1),(12103,6,'2013-10-14',42,0),(12141,882,'2013-10-09',31,0),(12142,882,'2013-10-15',31,1),(12143,879,'2013-10-16',48,0),(12144,882,'2013-10-14',47,0),(12145,882,'2013-10-01',32,0),(12146,885,'2013-10-04',46,0),(12147,879,'2013-10-01',42,1),(12148,879,'2013-10-01',42,0),(12149,879,'2013-10-08',42,0),(12150,879,'2013-10-10',47,0),(12151,879,'2013-10-11',47,0),(12152,884,'2013-10-07',32,0),(12153,881,'2013-10-29',34,0);
/*!40000 ALTER TABLE `services_encounter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `services_encounter_performed_by`
--

DROP TABLE IF EXISTS `services_encounter_performed_by`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `services_encounter_performed_by` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `encounter_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `encounter_id` (`encounter_id`,`user_id`),
  KEY `services_encounter_performed_by_2a8382aa` (`encounter_id`),
  KEY `services_encounter_performed_by_403f60f` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=310 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services_encounter_performed_by`
--

LOCK TABLES `services_encounter_performed_by` WRITE;
/*!40000 ALTER TABLE `services_encounter_performed_by` DISABLE KEYS */;
INSERT INTO `services_encounter_performed_by` VALUES (299,12146,2),(298,12145,2),(297,12144,2),(295,12143,2),(308,12152,2),(294,12142,2),(293,12141,2),(291,12140,2),(289,12139,2),(32,12017,2),(309,12153,2),(288,12138,2),(286,12137,2),(284,12136,2),(283,12135,2),(281,12134,3),(44,12024,2),(45,12025,2),(279,12133,2),(278,12132,2),(276,12131,2),(275,12130,2),(304,12149,2),(160,12073,2),(159,12072,2),(273,12129,2),(272,12128,2),(270,12127,2),(156,12070,2),(269,12126,2),(267,12125,2),(266,12124,2),(77,12040,2),(301,12147,2),(264,12123,2),(262,12122,2),(153,12068,2),(231,12106,2),(260,12121,2),(258,12120,2),(229,12105,2),(227,12104,2),(100,12046,4),(99,12046,2),(256,12119,2),(148,12065,2),(107,12048,2),(108,12048,4),(255,12118,2),(253,12117,2),(251,12116,2),(249,12115,2),(307,12151,2),(306,12150,2),(247,12114,2),(303,12148,2),(122,12053,4),(121,12053,2),(124,12054,2),(245,12113,2),(129,12057,2),(243,12112,2),(241,12111,2),(239,12110,2),(138,12060,4),(137,12060,2),(225,12103,1),(223,12102,3),(221,12101,3),(220,12100,2),(218,12099,4),(217,12098,3),(237,12109,2),(216,12097,3),(215,12096,3),(213,12095,3),(211,12094,3),(209,12093,3),(235,12108,2),(233,12107,2);
/*!40000 ALTER TABLE `services_encounter_performed_by` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `services_harmreduction`
--

DROP TABLE IF EXISTS `services_harmreduction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `services_harmreduction` (
  `service_ptr_id` int(11) NOT NULL,
  `in_count` smallint(5) unsigned NOT NULL,
  `out_count` smallint(5) unsigned NOT NULL,
  `acid` tinyint(1) NOT NULL,
  `condoms` tinyint(1) NOT NULL,
  `stericup` tinyint(1) NOT NULL,
  `other` tinyint(1) NOT NULL,
  `pregnancy_test` tinyint(1) NOT NULL,
  `medical_supplies` tinyint(1) NOT NULL,
  `standard` tinyint(1) NOT NULL,
  `alternatives` tinyint(1) NOT NULL,
  `svip_person_count` smallint(5) unsigned NOT NULL,
  PRIMARY KEY (`service_ptr_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services_harmreduction`
--

LOCK TABLES `services_harmreduction` WRITE;
/*!40000 ALTER TABLE `services_harmreduction` DISABLE KEYS */;
INSERT INTO `services_harmreduction` VALUES (16220,500,500,1,0,1,1,0,0,1,1,2),(16217,45,45,0,0,0,0,0,0,1,1,1),(16216,120,120,1,0,0,0,0,0,0,1,3),(16213,54,82,0,0,0,0,0,0,1,1,2),(16208,14,10,0,0,0,0,1,1,1,0,0),(16201,10,10,0,0,0,0,0,0,1,1,2),(16199,12,12,0,0,0,0,0,0,0,1,0),(16196,500,250,0,1,0,0,0,1,1,1,8),(16195,154,154,0,0,0,0,0,1,1,1,5),(16181,15,15,0,0,0,0,0,0,0,0,0),(16169,4,10,0,0,1,0,0,0,1,0,1),(16167,5,10,0,0,0,0,0,0,0,1,2),(16164,20,10,0,0,0,0,0,0,0,0,0),(16229,146,150,1,0,0,0,1,1,1,0,5),(16156,15,15,0,0,0,0,0,0,1,1,6),(16224,120,120,0,0,0,0,0,1,1,0,3),(16231,9,10,1,0,0,0,0,0,1,0,0),(16234,250,200,1,1,1,0,0,0,0,0,6),(16240,52,50,1,0,1,1,1,1,1,0,5),(16243,12,12,0,0,0,0,0,0,0,0,0);
/*!40000 ALTER TABLE `services_harmreduction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `services_informationservice`
--

DROP TABLE IF EXISTS `services_informationservice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `services_informationservice` (
  `service_ptr_id` int(11) NOT NULL,
  `safe_usage` tinyint(1) NOT NULL,
  `safe_sex` tinyint(1) NOT NULL,
  `medical` tinyint(1) NOT NULL,
  `socio_legal` tinyint(1) NOT NULL,
  `cure_possibilities` tinyint(1) NOT NULL,
  `literature` tinyint(1) NOT NULL,
  `other` tinyint(1) NOT NULL,
  PRIMARY KEY (`service_ptr_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services_informationservice`
--

LOCK TABLES `services_informationservice` WRITE;
/*!40000 ALTER TABLE `services_informationservice` DISABLE KEYS */;
INSERT INTO `services_informationservice` VALUES (16207,0,0,0,0,1,0,0),(16202,0,0,1,1,0,0,0),(16180,0,0,0,1,1,0,0),(16179,0,0,0,1,1,0,0),(16174,0,0,1,1,0,0,0),(16158,0,0,1,1,0,0,0),(16215,0,1,1,0,0,0,0),(16222,0,1,1,0,0,0,0),(16232,0,1,1,0,0,0,0),(16239,0,1,1,1,0,0,0);
/*!40000 ALTER TABLE `services_informationservice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `services_service`
--

DROP TABLE IF EXISTS `services_service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `services_service` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  `encounter_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `services_service_2a8382aa` (`encounter_id`),
  KEY `services_service_1bb8f392` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=16247 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services_service`
--

LOCK TABLES `services_service` WRITE;
/*!40000 ALTER TABLE `services_service` DISABLE KEYS */;
INSERT INTO `services_service` VALUES (16217,'2013-10-16 12:11:18','2013-10-16 12:11:18',12132,'Výměnný a jiný harm reduction program (45 / 45)',27),(16216,'2013-10-16 10:05:29','2013-10-16 10:05:29',12131,'Výměnný a jiný harm reduction program (120 / 120)',27),(16214,'2013-10-16 10:04:16','2013-10-16 10:04:16',12129,'Krizová intervence',31),(16215,'2013-10-16 10:05:05','2013-10-16 10:05:05',12130,'Informační servis',30),(16030,'2012-02-27 10:17:24','2012-02-27 10:17:24',12024,'Oslovení',39),(16031,'2012-02-27 10:18:43','2012-02-27 10:18:43',12025,'Oslovení',39),(16213,'2013-10-16 10:04:05','2013-10-16 10:04:05',12128,'Výměnný a jiný harm reduction program (54 / 82)',27),(16212,'2013-10-16 09:34:37','2013-10-16 09:34:37',12127,'Krizová intervence',31),(16211,'2013-10-16 09:34:26','2013-10-16 09:34:26',12126,'Vyplnění IN-COME dotazníku',44),(16210,'2013-10-16 09:34:22','2013-10-16 09:34:22',12126,'Oslovení',39),(16209,'2013-10-16 09:34:20','2013-10-16 09:34:20',12126,'První kontakt',33),(16208,'2013-10-16 09:33:58','2013-10-16 09:33:58',12125,'Výměnný a jiný harm reduction program (14 / 10)',27),(16205,'2013-10-16 09:33:02','2013-10-16 09:33:02',12123,'Oslovení',39),(16206,'2013-10-16 09:33:05','2013-10-16 09:33:05',12123,'Krizová intervence',31),(16207,'2013-10-16 09:33:36','2013-10-16 09:33:36',12124,'Informační servis',30),(16204,'2013-10-16 09:33:00','2013-10-16 09:33:00',12123,'První kontakt',33),(16203,'2013-10-16 09:32:41','2013-10-16 09:32:41',12122,'Doprovod klienta: léčebné zařízení',29),(16202,'2013-10-16 09:32:19','2013-10-16 09:32:19',12121,'Informační servis',30),(16200,'2013-10-16 09:25:39','2013-10-16 09:25:39',12119,'Odkazy',36),(16201,'2013-10-16 09:32:07','2013-10-16 09:32:07',12120,'Výměnný a jiný harm reduction program (10 / 10)',27),(16199,'2013-10-16 09:25:22','2013-10-16 09:25:22',12118,'Výměnný a jiný harm reduction program (12 / 12)',27),(16197,'2013-10-16 09:24:55','2013-10-16 09:24:55',12117,'Odkazy',36),(16198,'2013-10-16 09:25:02','2013-10-16 09:25:02',12117,'Základní poradenství',38),(16196,'2013-10-16 09:24:46','2013-10-16 09:24:46',12116,'Výměnný a jiný harm reduction program (500 / 250)',27),(16166,'2013-10-14 13:26:06','2013-10-14 13:26:06',12099,'První kontakt',33),(16167,'2013-10-14 13:26:23','2013-10-14 13:26:23',12099,'Výměnný a jiný harm reduction program (5 / 10)',27),(16168,'2013-10-14 13:31:43','2013-10-14 13:31:43',12100,'První kontakt',33),(16169,'2013-10-14 13:31:58','2013-10-14 13:31:58',12100,'Výměnný a jiný harm reduction program (4 / 10)',27),(16170,'2013-10-14 14:06:00','2013-10-14 14:06:00',12101,'Doprovod klienta: sociální',29),(16171,'2013-10-14 14:06:07','2013-10-14 14:06:07',12101,'Případová práce',32),(16172,'2013-10-14 14:06:14','2013-10-14 14:06:14',12101,'Odkazy',36),(16173,'2013-10-14 14:07:40','2013-10-14 14:07:40',12102,'Testování infekčních nemocí: test',28),(16174,'2013-10-14 14:07:48','2013-10-14 14:07:48',12102,'Informační servis',30),(16175,'2013-10-14 14:07:51','2013-10-14 14:07:51',12102,'Základní zdravotní ošetření',37),(16176,'2013-10-14 14:07:54','2013-10-14 14:07:54',12102,'Vyplnění IN-COME dotazníku',44),(16177,'2013-10-14 14:08:16','2013-10-14 14:08:16',12103,'Oslovení',39),(16178,'2013-10-14 14:08:19','2013-10-14 14:08:19',12103,'První kontakt',33),(16179,'2013-10-14 14:08:24','2013-10-14 14:08:24',12103,'Informační servis',30),(16180,'2013-10-16 09:20:03','2013-10-16 09:20:03',12104,'Informační servis',30),(16181,'2013-10-16 09:20:30','2013-10-16 09:20:30',12105,'Výměnný a jiný harm reduction program (15 / 15)',27),(16164,'2013-10-14 10:12:26','2013-10-14 10:12:26',12098,'Výměnný a jiný harm reduction program (20 / 10)',27),(16165,'2013-10-14 13:26:03','2013-10-14 13:26:03',12099,'Oslovení',39),(16073,'2012-05-16 11:02:24','2012-05-16 11:02:24',12046,'Oslovení',39),(16195,'2013-10-16 09:24:29','2013-10-16 09:24:29',12115,'Výměnný a jiný harm reduction program (154 / 154)',27),(16194,'2013-10-16 09:24:03','2013-10-16 09:24:03',12114,'Základní zdravotní ošetření',37),(16193,'2013-10-16 09:24:01','2013-10-16 09:24:01',12114,'Vyplnění IN-COME dotazníku',44),(16102,'2012-08-20 00:51:36','2012-08-20 00:51:36',12065,'Oslovení',39),(16192,'2013-10-16 09:23:26','2013-10-16 09:23:26',12113,'Doprovod klienta: zdravotní',29),(16189,'2013-10-16 09:22:05','2013-10-16 09:22:05',12110,'Odkazy',36),(16190,'2013-10-16 09:22:27','2013-10-16 09:22:27',12111,'Případová práce',32),(16191,'2013-10-16 09:22:58','2013-10-16 09:22:58',12112,'Testování infekčních nemocí: poradenství, test',28),(16088,'2012-05-27 22:42:50','2012-05-27 22:42:50',12053,'Oslovení',39),(16089,'2012-05-27 22:47:39','2012-05-27 22:47:39',12054,'Oslovení',39),(16188,'2013-10-16 09:21:51','2013-10-16 09:21:51',12109,'Krizová intervence',31),(16187,'2013-10-16 09:21:41','2013-10-16 09:21:41',12108,'První kontakt',33),(16186,'2013-10-16 09:21:16','2013-10-16 09:21:16',12107,'Kontaktní práce',34),(16184,'2013-10-16 09:20:53','2013-10-16 09:20:53',12106,'Oslovení',39),(16185,'2013-10-16 09:20:57','2013-10-16 09:20:57',12106,'Základní zdravotní ošetření',37),(16183,'2013-10-16 09:20:51','2013-10-16 09:20:51',12106,'První kontakt',33),(16182,'2013-10-16 09:20:35','2013-10-16 09:20:35',12105,'Základní poradenství',38),(16163,'2013-09-23 12:38:49','2013-09-23 12:38:49',12097,'Základní zdravotní ošetření',37),(16162,'2013-09-23 12:38:32','2013-09-23 12:38:32',12096,'Základní poradenství',38),(16161,'2013-09-23 12:38:25','2013-09-23 12:38:26',12096,'Doprovod klienta: sociální',29),(16159,'2013-09-23 12:38:02','2013-09-23 12:38:02',12095,'Krizová intervence',31),(16160,'2013-09-23 12:38:19','2013-09-23 12:38:19',12096,'Odkazy',36),(16156,'2013-09-23 12:37:23','2013-09-23 12:37:23',12093,'Výměnný a jiný harm reduction program (15 / 15)',27),(16157,'2013-09-23 12:37:28','2013-09-23 12:37:28',12093,'První kontakt',33),(16158,'2013-09-23 12:37:42','2013-09-23 12:37:42',12094,'Informační servis',30),(16218,'2013-10-16 12:11:35','2013-10-16 12:11:35',12133,'Odkazy',36),(16219,'2013-10-16 12:12:19','2013-10-16 12:12:19',12134,'Odkazy',36),(16220,'2013-10-16 12:12:46','2013-10-16 12:12:46',12135,'Výměnný a jiný harm reduction program (500 / 500)',27),(16221,'2013-10-16 12:13:12','2013-10-16 12:13:12',12136,'Doprovod klienta: sociální',29),(16222,'2013-10-16 12:13:19','2013-10-16 12:13:19',12136,'Informační servis',30),(16223,'2013-10-16 12:13:21','2013-10-16 12:13:21',12136,'Krizová intervence',31),(16224,'2013-10-16 12:14:00','2013-10-16 12:14:00',12137,'Výměnný a jiný harm reduction program (120 / 120)',27),(16225,'2013-10-16 12:14:05','2013-10-16 12:14:05',12137,'Základní poradenství',38),(16226,'2013-10-16 12:14:20','2013-10-16 12:14:20',12138,'Kontaktní práce',34),(16227,'2013-10-16 12:14:28','2013-10-16 12:14:28',12139,'Vyplnění IN-COME dotazníku',44),(16228,'2013-10-16 12:17:40','2013-10-16 12:17:40',12140,'Odkazy',36),(16229,'2013-10-16 12:18:03','2013-10-16 12:18:03',12141,'Výměnný a jiný harm reduction program (146 / 150)',27),(16230,'2013-10-16 12:18:16','2013-10-16 12:18:16',12142,'Odkazy',36),(16231,'2013-10-16 12:48:39','2013-10-16 12:48:39',12143,'Výměnný a jiný harm reduction program (9 / 10)',27),(16232,'2013-10-16 12:52:11','2013-10-16 12:52:11',12144,'Informační servis',30),(16233,'2013-10-16 12:52:13','2013-10-16 12:52:13',12144,'Kontaktní práce',34),(16234,'2013-10-16 12:52:34','2013-10-16 12:52:34',12145,'Výměnný a jiný harm reduction program (250 / 200)',27),(16235,'2013-10-16 13:07:38','2013-10-16 13:07:38',12146,'Doprovod klienta: léčebné zařízení',29),(16236,'2013-10-16 13:09:06','2013-10-16 13:09:06',12147,'Odkazy',36),(16237,'2013-10-16 13:09:10','2013-10-16 13:09:10',12147,'Krizová intervence',31),(16238,'2013-10-16 13:09:32','2013-10-16 13:09:32',12148,'Případová práce',32),(16239,'2013-10-16 13:09:37','2013-10-16 13:09:37',12148,'Informační servis',30),(16240,'2013-10-16 13:09:55','2013-10-16 13:09:55',12149,'Výměnný a jiný harm reduction program (52 / 50)',27),(16241,'2013-10-16 13:10:17','2013-10-16 13:10:17',12150,'Kontaktní práce',34),(16242,'2013-10-16 13:10:30','2013-10-16 13:10:30',12151,'Případová práce',32),(16243,'2013-10-16 13:23:15','2013-10-16 13:23:15',12152,'Výměnný a jiný harm reduction program (12 / 12)',27),(16245,'2013-10-17 00:19:17','2013-10-17 00:19:17',12105,'Krizová intervence',31),(16246,'2013-10-17 09:50:13','2013-10-17 09:50:13',12120,'Základní poradenství',38);
/*!40000 ALTER TABLE `services_service` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `services_socialwork`
--

DROP TABLE IF EXISTS `services_socialwork`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `services_socialwork` (
  `service_ptr_id` int(11) NOT NULL,
  `socio_legal` tinyint(1) NOT NULL,
  `service_mediation` tinyint(1) NOT NULL,
  `other` tinyint(1) NOT NULL,
  `counselling` tinyint(1) NOT NULL,
  PRIMARY KEY (`service_ptr_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services_socialwork`
--

LOCK TABLES `services_socialwork` WRITE;
/*!40000 ALTER TABLE `services_socialwork` DISABLE KEYS */;
INSERT INTO `services_socialwork` VALUES (16238,1,0,0,0),(16190,0,0,0,1),(16171,1,0,0,0),(16242,0,0,0,1);
/*!40000 ALTER TABLE `services_socialwork` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `services_utilitywork`
--

DROP TABLE IF EXISTS `services_utilitywork`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `services_utilitywork` (
  `service_ptr_id` int(11) NOT NULL,
  `refs` varchar(40) COLLATE utf8_czech_ci NOT NULL,
  PRIMARY KEY (`service_ptr_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_czech_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services_utilitywork`
--

LOCK TABLES `services_utilitywork` WRITE;
/*!40000 ALTER TABLE `services_utilitywork` DISABLE KEYS */;
INSERT INTO `services_utilitywork` VALUES (16160,'t,no'),(16172,'mf,ep'),(16189,'cc'),(16197,'ep'),(16200,'crc'),(16218,'fp'),(16219,'cc'),(16228,'fp'),(16230,'crc,t'),(16236,'mf');
/*!40000 ALTER TABLE `services_utilitywork` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `south_migrationhistory`
--

DROP TABLE IF EXISTS `south_migrationhistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `south_migrationhistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_name` varchar(255) NOT NULL,
  `migration` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=30 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `south_migrationhistory`
--

LOCK TABLES `south_migrationhistory` WRITE;
/*!40000 ALTER TABLE `south_migrationhistory` DISABLE KEYS */;
INSERT INTO `south_migrationhistory` VALUES (1,'services','0001_initial','2012-07-18 07:38:55'),(2,'services','0002_change_tickboxes','2012-07-18 07:39:09'),(3,'clients','0001_initial','2012-09-06 10:44:28'),(8,'clients','0002_auto__add_field_practitioner_organization','2012-09-06 10:45:12'),(5,'services','0003_auto__del_field_harmreduction_svip__chg_field_asistservice_where','2012-09-06 10:44:35'),(6,'services','0004_auto__del_crisisintervention','2012-09-06 10:44:35'),(7,'services','0005_auto__add_utilitywork','2012-09-06 10:44:35'),(9,'clients','0003_auto__add_field_riskymanners_periodicity_in_past__add_field_riskymanne','2012-11-25 12:42:08'),(10,'clients','0004_migrate_peridodicity','2012-11-25 12:42:08'),(11,'services','0006_auto__add_field_harmreduction_svip_person_count','2012-11-25 12:42:08'),(12,'services','0007_create_incomeformfillup_content_type','2012-11-25 12:42:08'),(13,'clients','0005_auto__add_field_client_sex_partner','2013-07-23 14:51:18'),(14,'clients','0006_make_practitioner_special_part1','2013-07-23 14:51:18'),(15,'clients','0007_make_practitioner_special_part2','2013-07-23 14:51:19'),(16,'clients','0008_make_practitioner_special_part3','2013-07-23 14:51:19'),(17,'clients','0009_rename_practitioner_to_practitionercontact','2013-07-23 14:51:19'),(18,'clients','0010_rename_practitioner_contenttype','2013-07-23 14:51:19'),(19,'clients','0011_repair_permissions','2013-07-23 14:51:19'),(20,'services','0008_auto__add_field_diseasetest_pre_test_advice__add_field_diseasetest_tes','2013-07-23 14:51:19'),(21,'services','0009_add_practitionerencounter_permissions','2013-07-23 14:51:19'),(22,'services','0010_remove_practitionerencounter_permissions','2013-07-23 14:51:19'),(23,'services','0011_auto__add_field_encounter_is_by_phone','2013-08-01 10:45:15'),(24,'services','0012_move_phonecounseling','2013-08-01 10:45:15'),(25,'services','0013_create_phoneusage_contenttype','2013-11-14 13:32:22'),(26,'services','0014_update_group_permissions','2013-11-14 14:04:46'),(27,'clients','0012_auto__chg_field_diseasetest_result','2013-11-15 14:13:33'),(28,'clients','0013_update_disease_test_result_ids','2013-11-15 14:13:33'),(29,'services','0015_update_group_permissions','2013-11-18 13:40:53');
/*!40000 ALTER TABLE `south_migrationhistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `syringes_syringecollection`
--

DROP TABLE IF EXISTS `syringes_syringecollection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `syringes_syringecollection` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `count` int(10) unsigned NOT NULL,
  `town_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `location` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `other_syringecollection_1fb3d69c` (`town_id`)
) ENGINE=MyISAM AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `syringes_syringecollection`
--

LOCK TABLES `syringes_syringecollection` WRITE;
/*!40000 ALTER TABLE `syringes_syringecollection` DISABLE KEYS */;
INSERT INTO `syringes_syringecollection` VALUES (3,10,34,'2012-01-22',' na nádraží'),(4,1,34,'2012-02-23','ulice Bří Čapků'),(5,100,34,'2012-02-27','u cekarny, zabodnuto do psa'),(6,55,34,'2012-02-29',''),(7,25,31,'2012-03-04','doma'),(8,51,38,'2012-03-07','doma'),(15,1,32,'2012-10-04','Za budovou restaurace vedle ÚP'),(10,15,33,'2012-03-30','pískoviště na Výstavku'),(12,21,39,'2012-03-14','bla bla'),(13,1,33,'2012-03-20','gggggggggg'),(14,645,32,'2012-03-15','u hřbitova'),(16,100,31,'2013-10-07','u silnice');
/*!40000 ALTER TABLE `syringes_syringecollection` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `syringes_syringecollection_persons`
--

DROP TABLE IF EXISTS `syringes_syringecollection_persons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `syringes_syringecollection_persons` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `syringecollection_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `syringecollection_id` (`syringecollection_id`,`user_id`),
  KEY `other_syringecollection_persons_37bc4246` (`syringecollection_id`),
  KEY `other_syringecollection_persons_403f60f` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `syringes_syringecollection_persons`
--

LOCK TABLES `syringes_syringecollection_persons` WRITE;
/*!40000 ALTER TABLE `syringes_syringecollection_persons` DISABLE KEYS */;
INSERT INTO `syringes_syringecollection_persons` VALUES (6,4,2),(5,3,3),(8,5,2),(9,6,2),(10,6,3),(11,7,2),(12,7,4),(13,8,4),(23,10,2),(24,12,2),(25,12,3),(30,15,9),(27,14,4),(29,15,8),(31,16,9);
/*!40000 ALTER TABLE `syringes_syringecollection_persons` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `reporting_searchencounter`
--

/*!50001 DROP TABLE IF EXISTS `reporting_searchencounter`*/;
/*!50001 DROP VIEW IF EXISTS `reporting_searchencounter`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`boris`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `reporting_searchencounter` AS (select `services_encounter`.`id` AS `id`,`services_encounter`.`person_id` AS `person_id`,`services_encounter`.`where_id` AS `town_id`,`services_encounter`.`is_by_phone` AS `is_by_phone`,year(`services_encounter`.`performed_on`) AS `year`,month(`services_encounter`.`performed_on`) AS `month`,(`clients_client`.`person_ptr_id` is not null) AS `is_client`,`clients_client`.`sex` AS `client_sex`,`clients_client`.`primary_drug_id` AS `primary_drug_id`,`clients_client`.`primary_drug_usage` AS `primary_drug_usage`,`clients_client`.`close_person` AS `is_close_person`,`clients_client`.`sex_partner` AS `is_sex_partner`,(`clients_anonymous`.`person_ptr_id` is not null) AS `is_anonymous` from ((`services_encounter` left join `clients_client` on((`services_encounter`.`person_id` = `clients_client`.`person_ptr_id`))) left join `clients_anonymous` on((`services_encounter`.`person_id` = `clients_anonymous`.`person_ptr_id`)))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `reporting_searchservice`
--

/*!50001 DROP TABLE IF EXISTS `reporting_searchservice`*/;
/*!50001 DROP VIEW IF EXISTS `reporting_searchservice`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`boris`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `reporting_searchservice` AS (select `services_service`.`id` AS `id`,`services_service`.`id` AS `service_id`,`services_encounter`.`id` AS `encounter_id`,`django_content_type`.`model` AS `content_type_model`,`services_encounter`.`where_id` AS `town_id`,`services_encounter`.`person_id` AS `person_id`,year(`services_encounter`.`performed_on`) AS `year`,month(`services_encounter`.`performed_on`) AS `month`,(`clients_client`.`person_ptr_id` is not null) AS `is_client`,(`clients_anonymous`.`person_ptr_id` is not null) AS `is_anonymous` from ((((`services_service` join `services_encounter` on((`services_service`.`encounter_id` = `services_encounter`.`id`))) join `django_content_type` on((`services_service`.`content_type_id` = `django_content_type`.`id`))) left join `clients_client` on((`services_encounter`.`person_id` = `clients_client`.`person_ptr_id`))) left join `clients_anonymous` on((`services_encounter`.`person_id` = `clients_anonymous`.`person_ptr_id`)))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `reporting_searchsyringecollection`
--

/*!50001 DROP TABLE IF EXISTS `reporting_searchsyringecollection`*/;
/*!50001 DROP VIEW IF EXISTS `reporting_searchsyringecollection`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`boris`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `reporting_searchsyringecollection` AS (select `syringes_syringecollection`.`id` AS `id`,`syringes_syringecollection`.`count` AS `count`,`syringes_syringecollection`.`town_id` AS `town_id`,month(`syringes_syringecollection`.`date`) AS `month`,year(`syringes_syringecollection`.`date`) AS `year` from `syringes_syringecollection`) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-11-18 14:43:02
