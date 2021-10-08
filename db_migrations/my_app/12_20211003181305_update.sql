-- upgrade --
CREATE TABLE IF NOT EXISTS `tickets` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `guild_id` BIGINT NOT NULL,
    `user_id` BIGINT NOT NULL,
    `config_id` BIGINT NOT NULL,
    `ticket_channel` BIGINT NOT NULL,
    `message_id` BIGINT NOT NULL,
    `status` VARCHAR(255) NOT NULL  DEFAULT 'Open'
) CHARACTER SET utf8mb4;
-- downgrade --
DROP TABLE IF EXISTS `tickets`;
