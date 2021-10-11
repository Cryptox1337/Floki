-- upgrade --
CREATE TABLE IF NOT EXISTS `embeds` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `guild_id` BIGINT NOT NULL,
    `title` VARCHAR(255),
    `title_url` VARCHAR(255),
    `description` LONGTEXT,
    `color` VARCHAR(255),
    `author` VARCHAR(255),
    `author_icon` BOOL,
    `thumbnail` VARCHAR(255),
    `image` VARCHAR(255),
    `footer` LONGTEXT,
    `footer_icon` VARCHAR(255),
    `status` VARCHAR(255)   DEFAULT 'disabled'
) CHARACTER SET utf8mb4;
-- downgrade --
DROP TABLE IF EXISTS `embeds`;
