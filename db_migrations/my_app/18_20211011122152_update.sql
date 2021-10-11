-- upgrade --
ALTER TABLE `guilds` DROP COLUMN `count_category`;
-- downgrade --
ALTER TABLE `guilds` ADD `count_category` BIGINT NOT NULL;
