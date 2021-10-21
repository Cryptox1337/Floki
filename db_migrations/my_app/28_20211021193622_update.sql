-- upgrade --
ALTER TABLE `guilds` ADD `xp_rate` DOUBLE NOT NULL  DEFAULT 1;
-- downgrade --
ALTER TABLE `guilds` DROP COLUMN `xp_rate`;
