-- upgrade --
CREATE TABLE IF NOT EXISTS `ticket_config` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `guild_id` BIGINT NOT NULL,
    `channel_id` BIGINT NOT NULL,
    `category_id` BIGINT NOT NULL,
    `message_id` BIGINT NOT NULL  DEFAULT 0,
    `status` VARCHAR(255) NOT NULL  DEFAULT 'disabled'
) CHARACTER SET utf8mb4;
-- downgrade --
DROP TABLE IF EXISTS `ticket_config`;
