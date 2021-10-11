-- upgrade --
ALTER TABLE `count_channels` ADD `count_name` VARCHAR(255) NOT NULL;
-- downgrade --
ALTER TABLE `count_channels` DROP COLUMN `count_name`;
