-- MySQL dump 10.13  Distrib 5.1.73, for redhat-linux-gnu (x86_64)
--
-- Host: localhost    Database: ems
-- ------------------------------------------------------
-- Server version	5.1.73

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
-- Table structure for table `t_ems_equipment`
--

DROP TABLE IF EXISTS `t_ems_equipment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_ems_equipment` (
  `sn` varchar(16) NOT NULL,
  `status` tinyint(1) NOT NULL DEFAULT 1,
  `eq_type` tinyint(1) NOT NULL,
  `sold` tinyint(1) NOT NULL DEFAULT 0,
  `desc` varchar(300),
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`sn`),
  KEY `idx_ems_sold` (`sold`),
  KEY `idx_ems_eq_type` (`eq_type`),
  KEY `idx_ems_update_time` (`update_time`),
  KEY `idx_ems_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `t_ems_import_record`
--

DROP TABLE IF EXISTS `t_ems_import_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_ems_import_record` (
  `file_name` varchar(128) NOT NULL,
  `op_user` varchar(64) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `op_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`file_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;


DROP TABLE IF EXISTS `t_operation_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_operation_log` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(32) COLLATE utf8_bin NOT NULL,
  `operation` varchar(2) COLLATE utf8_bin NOT NULL,
  `operation_ip` varchar(32) COLLATE utf8_bin NOT NULL,
  `operation_service` varchar(512) COLLATE utf8_bin NOT NULL,
  `request_body` text COLLATE utf8_bin,
  `request_args` varchar(512) COLLATE utf8_bin DEFAULT NULL,
  `operation_result` varchar(1) COLLATE utf8_bin NOT NULL,
  `operation_message` varchar(512) COLLATE utf8_bin DEFAULT NULL,
  `execute_time` int(32) NOT NULL,
  `operation_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_usr_name` (`user_name`),
  KEY `idx_operation_time` (`operation_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;
-- Dump completed on 2018-02-03 15:58:14



DROP TABLE IF EXISTS `t_failing_sn`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_failing_sn` (
  `sn` varchar(100) NOT NULL,
  `eq_type` tinyint(1) NOT NULL,
  `op_user` varchar(64) NOT NULL,
  `filename` varchar(100),
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`sn`),
  KEY `idx_ems_update_time` (`update_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;