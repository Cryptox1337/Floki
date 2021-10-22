-- upgrade --
ALTER TABLE `channels` ADD `xp_channel` BOOL   DEFAULT 1;
-- downgrade --
ALTER TABLE `channels` DROP COLUMN `xp_channel`;
