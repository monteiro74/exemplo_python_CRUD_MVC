#
# Structure for table "pets"
#

CREATE TABLE `pets` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `apelido` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `raca` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `data_nascimento` date DEFAULT NULL,
  `foto` longblob,
  `cpf` int DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
