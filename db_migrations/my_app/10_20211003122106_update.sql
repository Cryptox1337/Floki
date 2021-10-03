-- upgrade --
CREATE TABLE IF NOT EXISTS `temporary_voice_channels` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `guild_id` BIGINT NOT NULL,
    `owner_id` BIGINT NOT NULL,
    `channel_id` BIGINT NOT NULL,
    `config_id` BIGINT NOT NULL
) CHARACTER SET utf8mb4;
-- downgrade --
DROP TABLE IF EXISTS `temporary_voice_channels`;
