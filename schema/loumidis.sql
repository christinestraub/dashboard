/*
Navicat MySQL Data Transfer

Source Server         : local_mysql
Source Server Version : 50505
Source Host           : localhost:3306
Source Database       : loumidis

Target Server Type    : MYSQL
Target Server Version : 50505
File Encoding         : 65001

Date: 2019-05-20 01:17:44
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for tbl_data
-- ----------------------------
DROP TABLE IF EXISTS `tbl_data`;
CREATE TABLE `tbl_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `mcgs_time` datetime DEFAULT NULL,
  `mcgs_timems` smallint(6) DEFAULT NULL,
  `weight` double DEFAULT NULL,
  `product_name` varchar(50) DEFAULT NULL,
  `product_type` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30027 DEFAULT CHARSET=utf8;
