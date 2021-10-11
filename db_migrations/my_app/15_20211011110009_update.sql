-- upgrade --
CREATE TABLE IF NOT EXISTS `channels` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `guild_id` BIGINT NOT NULL,
    `channel_id` BIGINT NOT NULL
) CHARACTER SET utf8mb4;
-- downgrade --
DROP TABLE IF EXISTS `channels`;
