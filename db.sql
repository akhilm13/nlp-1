-- phpMyAdmin SQL Dump
-- version 4.6.4
-- https://www.phpmyadmin.net/
--
-- Client :  127.0.0.1
-- Généré le :  Mar 24 Avril 2018 à 20:32
-- Version du serveur :  5.7.14
-- Version de PHP :  5.6.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `dbadb`
--

DELIMITER $$
--
-- Procédures
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `link_article_tag` (IN `id_article` INT, IN `id_tag` INT)  SQL SECURITY INVOKER
BEGIN
	insert into tags_linker values (NULL, id_article, id_tag);
END$$

--
-- Fonctions
--
CREATE DEFINER=`root`@`localhost` FUNCTION `add_tag` (`tag` VARCHAR(45)) RETURNS INT(11) BEGIN
declare id int;
	if not exists (Select id from tags t where t.content = tag) 
    then
		insert into tags values (NULL, tag);
        set id = (Select t.id from tags t where t.content = tag);
        return id;
	else   
		set id = (Select t.id from tags t where t.content = tag);
		return id;
    end if;
    
    
END$$

CREATE DEFINER=`root`@`localhost` FUNCTION `new_article` (`title` MEDIUMTEXT, `link` MEDIUMTEXT, `content` LONGTEXT) RETURNS INT(11) BEGIN
	declare ID int;
    if not exists(SELECT a.id from articles a where strcmp(a.title,title) and strcmp(a.link,link) and strcmp(a.content,content)) then
	insert into articles values (NULL, title, link, content);
	set ID = (SELECT a.id from articles a where strcmp(a.title,title) and strcmp(a.link,link) and strcmp(a.content,content)); 
    return ID;
    else
    set ID = (SELECT a.id from articles a where strcmp(a.title,title) and strcmp(a.link,link) and strcmp(a.content,content)); 
    return ID;
    end if;
    
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Structure de la table `articles`
--

CREATE TABLE `articles` (
  `id` int(11) NOT NULL,
  `content` longtext NOT NULL,
  `title` mediumtext NOT NULL,
  `link` mediumtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `articles`
--

INSERT INTO `articles` (`id`, `content`, `title`, `link`) VALUES
(5, 'testtitle', 'http://lol', 'jvojobvourzvg');

-- --------------------------------------------------------

--
-- Doublure de structure pour la vue `linked_view`
-- (Voir ci-dessous la vue réelle)
--
CREATE TABLE `linked_view` (
`title` mediumtext
,`content` longtext
,`link` mediumtext
,`tag` varchar(45)
);

-- --------------------------------------------------------

--
-- Structure de la table `tags`
--

CREATE TABLE `tags` (
  `id` int(11) NOT NULL,
  `content` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `tags`
--

INSERT INTO `tags` (`id`, `content`) VALUES
(1, 'hello'),
(2, 'bonjour');

-- --------------------------------------------------------

--
-- Structure de la table `tags_linker`
--

CREATE TABLE `tags_linker` (
  `id` int(11) NOT NULL,
  `articles_id` int(11) NOT NULL,
  `tags_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `tags_linker`
--

INSERT INTO `tags_linker` (`id`, `articles_id`, `tags_id`) VALUES
(1, 5, 1);

-- --------------------------------------------------------

--
-- Structure de la vue `linked_view`
--
DROP TABLE IF EXISTS `linked_view`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `linked_view`  AS  select `a`.`title` AS `title`,`a`.`content` AS `content`,`a`.`link` AS `link`,`t`.`content` AS `tag` from ((`articles` `a` join `tags` `t`) join `tags_linker` `l`) where ((`l`.`articles_id` = `a`.`id`) and (`t`.`id` = `l`.`tags_id`)) ;

--
-- Index pour les tables exportées
--

--
-- Index pour la table `articles`
--
ALTER TABLE `articles`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `tags`
--
ALTER TABLE `tags`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `tags_linker`
--
ALTER TABLE `tags_linker`
  ADD PRIMARY KEY (`id`,`articles_id`,`tags_id`),
  ADD KEY `fk_tags_linker_Article_link_idx` (`articles_id`),
  ADD KEY `fk_tags_linker_tags1_idx` (`tags_id`);

--
-- AUTO_INCREMENT pour les tables exportées
--

--
-- AUTO_INCREMENT pour la table `articles`
--
ALTER TABLE `articles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT pour la table `tags`
--
ALTER TABLE `tags`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT pour la table `tags_linker`
--
ALTER TABLE `tags_linker`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- Contraintes pour les tables exportées
--

--
-- Contraintes pour la table `tags_linker`
--
ALTER TABLE `tags_linker`
  ADD CONSTRAINT `fk_tags_linker_Article_link` FOREIGN KEY (`articles_id`) REFERENCES `articles` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_tags_linker_tags1` FOREIGN KEY (`tags_id`) REFERENCES `tags` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
