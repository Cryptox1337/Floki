-- upgrade --
CREATE TABLE IF NOT EXISTS `xp_table` (
    `level` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `xp` DOUBLE NOT NULL
) CHARACTER SET utf8mb4;
-- downgrade --
DROP TABLE IF EXISTS `xp_table`;
