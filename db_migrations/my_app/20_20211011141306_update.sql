-- upgrade --
ALTER TABLE `roles` ADD `auto_role` BOOL   DEFAULT 0;
-- downgrade --
ALTER TABLE `roles` DROP COLUMN `auto_role`;
