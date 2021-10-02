-- upgrade --
ALTER TABLE `users` ADD `warns` INT NOT NULL  DEFAULT 0;
-- downgrade --
ALTER TABLE `users` DROP COLUMN `warns`;
