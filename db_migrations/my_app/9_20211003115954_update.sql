-- upgrade --
CREATE TABLE IF NOT EXISTS `temporary_voice_config` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `guild_id` BIGINT NOT NULL,
    `channel_id` BIGINT NOT NULL,
    `category_id` BIGINT NOT NULL,
    `limit` BIGINT NOT NULL  DEFAULT 0,
    `bitrate` BIGINT NOT NULL  DEFAULT 64,
    `status` VARCHAR(255) NOT NULL  DEFAULT 'disabled'
) CHARACTER SET utf8mb4;
-- downgrade --
DROP TABLE IF EXISTS `temporary_voice_config`;
