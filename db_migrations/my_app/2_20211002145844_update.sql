-- upgrade --
ALTER TABLE `guilds` ADD `mute_role` BIGINT NOT NULL  DEFAULT 0;
-- downgrade --
ALTER TABLE `guilds` DROP COLUMN `mute_role`;
