-- upgrade --
ALTER TABLE `users` ADD `level` INT NOT NULL  DEFAULT 0;
ALTER TABLE `users` ADD `xp` DOUBLE NOT NULL  DEFAULT 0;
-- downgrade --
ALTER TABLE `users` DROP COLUMN `level`;
ALTER TABLE `users` DROP COLUMN `xp`;
