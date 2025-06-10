#
# Structure for table "alunos"
#

CREATE TABLE `alunos` (
  `matricula` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `nome` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `cpf` varchar(11) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `curso` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `sexo` varchar(1) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `idade` int DEFAULT NULL,
  `foto` longblob,
  `observacao` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`matricula`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
