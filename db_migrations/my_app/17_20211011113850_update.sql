-- upgrade --
CREATE TABLE IF NOT EXISTS `count_channels` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `guild_id` BIGINT NOT NULL,
    `count_type` VARCHAR(255) NOT NULL,
    `channel_id` BIGINT NOT NULL,
    `status` VARCHAR(255) NOT NULL  DEFAULT 'disabled'
) CHARACTER SET utf8mb4;;
ALTER TABLE `guilds` ADD `count_category` BIGINT NOT NULL;
-- downgrade --
ALTER TABLE `guilds` DROP COLUMN `count_category`;
DROP TABLE IF EXISTS `count_channels`;
