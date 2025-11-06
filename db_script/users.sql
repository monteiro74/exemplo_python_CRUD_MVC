#
# Structure for table "users"
#

CREATE TABLE `users` (
  `login` varchar(190) NOT NULL,
  `pswd` varchar(255) NOT NULL,
  PRIMARY KEY (`login`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
