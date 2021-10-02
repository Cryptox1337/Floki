-- upgrade --
CREATE TABLE IF NOT EXISTS `kicks` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `guild_id` BIGINT NOT NULL,
    `user_id` BIGINT NOT NULL,
    `author` BIGINT NOT NULL,
    `reason` VARCHAR(255) NOT NULL,
    `date` DATETIME(6) NOT NULL
) CHARACTER SET utf8mb4;;
ALTER TABLE `mutes` ALTER COLUMN `status` SET DEFAULT 'muted';
-- downgrade --
ALTER TABLE `mutes` ALTER COLUMN `status` SET DEFAULT 'mute';
DROP TABLE IF EXISTS `kicks`;
