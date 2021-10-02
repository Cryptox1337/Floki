-- upgrade --
CREATE TABLE IF NOT EXISTS `bans` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `guild_id` BIGINT NOT NULL,
    `user_id` BIGINT NOT NULL,
    `author` BIGINT NOT NULL,
    `reason` VARCHAR(255) NOT NULL,
    `date` DATETIME(6) NOT NULL,
    `end_date` DATETIME(6) NOT NULL,
    `status` VARCHAR(255) NOT NULL  DEFAULT 'banned'
) CHARACTER SET utf8mb4;
-- downgrade --
DROP TABLE IF EXISTS `bans`;
