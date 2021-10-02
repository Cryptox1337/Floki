-- upgrade --
CREATE TABLE IF NOT EXISTS `warns` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `guild_id` BIGINT NOT NULL,
    `user_id` BIGINT NOT NULL,
    `author` BIGINT NOT NULL,
    `reason` VARCHAR(255) NOT NULL,
    `date` DATETIME(6) NOT NULL
) CHARACTER SET utf8mb4;
-- downgrade --
DROP TABLE IF EXISTS `warns`;
