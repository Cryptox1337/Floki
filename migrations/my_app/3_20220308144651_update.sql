-- upgrade --
ALTER TABLE `ticket_config` ADD `embed` BIGINT;
-- downgrade --
ALTER TABLE `ticket_config` DROP COLUMN `embed`;
