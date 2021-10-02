-- upgrade --
CREATE TABLE IF NOT EXISTS `response_channels` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `guild_id` BIGINT NOT NULL,
    `response_type` VARCHAR(255) NOT NULL,
    `channel_id` BIGINT NOT NULL  DEFAULT 0,
    `status` VARCHAR(255) NOT NULL  DEFAULT 'disabled'
) CHARACTER SET utf8mb4;
-- downgrade --
DROP TABLE IF EXISTS `response_channels`;
