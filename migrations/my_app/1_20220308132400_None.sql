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
CREATE TABLE IF NOT EXISTS `channels` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `guild_id` BIGINT NOT NULL,
    `channel_id` BIGINT NOT NULL,
    `xp_channel` BOOL   DEFAULT 1
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `count_channels` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `guild_id` BIGINT NOT NULL,
    `count_name` VARCHAR(255) NOT NULL,
    `count_type` VARCHAR(255) NOT NULL,
    `channel_id` BIGINT NOT NULL,
    `status` VARCHAR(255) NOT NULL  DEFAULT 'disabled'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `embeds` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `guild_id` BIGINT NOT NULL,
    `title` VARCHAR(255),
    `title_url` VARCHAR(255),
    `description` LONGTEXT,
    `color` BIGINT,
    `author` BIGINT,
    `author_icon` BOOL,
    `thumbnail` VARCHAR(255),
    `image` VARCHAR(255),
    `footer` LONGTEXT,
    `footer_icon` VARCHAR(255),
    `status` VARCHAR(255)   DEFAULT 'disabled'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `guilds` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `guild_id` BIGINT NOT NULL UNIQUE,
    `lang` VARCHAR(255) NOT NULL  DEFAULT 'english',
    `timezone` VARCHAR(255) NOT NULL  DEFAULT 'UTC',
    `created` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `mute_role` BIGINT NOT NULL  DEFAULT 0,
    `xp_rate` DOUBLE NOT NULL  DEFAULT 1
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `kicks` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `guild_id` BIGINT NOT NULL,
    `user_id` BIGINT NOT NULL,
    `author` BIGINT NOT NULL,
    `reason` VARCHAR(255) NOT NULL,
    `date` DATETIME(6) NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `mutes` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `guild_id` BIGINT NOT NULL,
    `user_id` BIGINT NOT NULL,
    `author` BIGINT NOT NULL,
    `reason` VARCHAR(255) NOT NULL,
    `date` DATETIME(6) NOT NULL,
    `end_date` DATETIME(6) NOT NULL,
    `status` VARCHAR(255) NOT NULL  DEFAULT 'muted'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `response_channels` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `guild_id` BIGINT NOT NULL,
    `response_type` VARCHAR(255) NOT NULL,
    `channel_id` BIGINT NOT NULL  DEFAULT 0,
    `status` VARCHAR(255) NOT NULL  DEFAULT 'disabled'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `roles` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `guild_id` BIGINT NOT NULL,
    `role_id` BIGINT NOT NULL,
    `auto_role` BOOL   DEFAULT 0,
    `xp_role` BOOL   DEFAULT 1
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `temporary_voice_channels` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `guild_id` BIGINT NOT NULL,
    `owner_id` BIGINT NOT NULL,
    `channel_id` BIGINT NOT NULL,
    `config_id` BIGINT NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `temporary_voice_config` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `guild_id` BIGINT NOT NULL,
    `channel_id` BIGINT NOT NULL,
    `category_id` BIGINT NOT NULL,
    `limit` BIGINT NOT NULL  DEFAULT 0,
    `bitrate` BIGINT NOT NULL  DEFAULT 64,
    `status` VARCHAR(255) NOT NULL  DEFAULT 'disabled'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `ticket_config` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `guild_id` BIGINT NOT NULL,
    `channel_id` BIGINT NOT NULL,
    `category_id` BIGINT NOT NULL,
    `message_id` BIGINT NOT NULL  DEFAULT 0,
    `status` VARCHAR(255) NOT NULL  DEFAULT 'disabled'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `tickets` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `guild_id` BIGINT NOT NULL,
    `user_id` BIGINT NOT NULL,
    `config_id` BIGINT NOT NULL,
    `ticket_channel` BIGINT NOT NULL,
    `message_id` BIGINT NOT NULL,
    `status` VARCHAR(255) NOT NULL  DEFAULT 'Open'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `users` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `guild_id` BIGINT NOT NULL,
    `user_id` BIGINT NOT NULL,
    `level` INT NOT NULL  DEFAULT 0,
    `xp` DOUBLE NOT NULL  DEFAULT 0,
    `warns` INT NOT NULL  DEFAULT 0
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `warns` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `guild_id` BIGINT NOT NULL,
    `user_id` BIGINT NOT NULL,
    `author` BIGINT NOT NULL,
    `reason` VARCHAR(255) NOT NULL,
    `date` DATETIME(6) NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `xp_table` (
    `level` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `xp` DOUBLE NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(20) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;
