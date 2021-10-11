-- upgrade --
ALTER TABLE `embeds` MODIFY COLUMN `color` BIGINT;
ALTER TABLE `embeds` MODIFY COLUMN `author` BIGINT;
-- downgrade --
ALTER TABLE `embeds` MODIFY COLUMN `color` VARCHAR(255);
ALTER TABLE `embeds` MODIFY COLUMN `author` VARCHAR(255);
