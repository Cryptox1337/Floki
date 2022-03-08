-- upgrade --
ALTER TABLE `ticket_config` ADD `title` VARCHAR(255);
-- downgrade --
ALTER TABLE `ticket_config` DROP COLUMN `title`;
