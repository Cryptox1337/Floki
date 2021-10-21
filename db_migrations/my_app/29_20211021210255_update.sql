-- upgrade --
ALTER TABLE `roles` ADD `xp_role` BOOL   DEFAULT 1;
-- downgrade --
ALTER TABLE `roles` DROP COLUMN `xp_role`;
