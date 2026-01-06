# Connexion
## Connexion locale
```bash
mysql -u root -p
```

## Connexion à un serveur distant
```bash
mysql -h <host> -u <username> -p
```

# 2. Commandes de base MySQL
## Créer et supprimer une base
CREATE DATABASE nom_de_la_base;
DROP DATABASE nom_de_la_base;

## Utiliser une base
USE nom_de_la_base;

## Créer une table
CREATE TABLE clients (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    date_inscription DATE
);

## Modifier une table
ALTER TABLE clients ADD COLUMN age INT;
ALTER TABLE clients DROP COLUMN age;
ALTER TABLE clients MODIFY COLUMN email VARCHAR(150);

## Supprimer une table
DROP TABLE clients;

# Commandes de manipulation de données
## Insérer des données
INSERT INTO clients (nom, email, date_inscription)
VALUES ('Alice Dupont', 'alice@mail.com', '2025-01-15');

## Lire des données
SELECT * FROM clients;
SELECT nom, email FROM clients;
SELECT * FROM clients WHERE id = 1;
SELECT * FROM clients WHERE nom LIKE 'A%';

## Mettre à jour
UPDATE clients
SET email = 'alice.dupont@mail.com'
WHERE id = 1;

## Supprimer
DELETE FROM clients WHERE id = 1;

# Commandes de lecture avancée
## Filtres et conditions
SELECT * FROM commandes
WHERE montant > 100
  AND statut = 'validée';

## Tri
SELECT * FROM produits ORDER BY prix DESC;

## Limiter les résultats
SELECT * FROM clients LIMIT 10;

## Alias
SELECT nom AS "Nom du client", email AS "Courriel" FROM clients;

## Fonctions d’agrégation
SELECT COUNT(*) FROM clients;
SELECT AVG(prix) FROM produits;
SELECT SUM(montant) FROM commandes;
SELECT MIN(prix), MAX(prix) FROM produits;

## Regroupement
SELECT categorie, COUNT(*) AS nb_produits
FROM produits
GROUP BY categorie
HAVING COUNT(*) > 5;

# Jointures
## INNER JOIN
→ Renvoie seulement les lignes qui correspondent dans les deux tables.

SELECT c.nom, cmd.montant
FROM clients AS c
INNER JOIN commandes AS cmd
ON c.id = cmd.client_id;

## LEFT JOIN
→ Renvoie tous les clients, même ceux sans commande.

SELECT c.nom, cmd.montant
FROM clients AS c
LEFT JOIN commandes AS cmd
ON c.id = cmd.client_id;

## RIGHT JOIN
→ L’inverse du LEFT JOIN.

SELECT c.nom, cmd.montant
FROM clients AS c
RIGHT JOIN commandes AS cmd
ON c.id = cmd.client_id;

## FULL OUTER JOIN
SELECT *
FROM table1
FULL OUTER JOIN table2
ON table1.id = table2.id;

# Commandes d’administration (DCL / TCL)
## Gestion des utilisateurs
CREATE USER 'bob'@'localhost' IDENTIFIED BY 'motdepasse';
GRANT ALL PRIVILEGES ON ma_base.* TO 'bob'@'localhost';
FLUSH PRIVILEGES;

## Transactions
START TRANSACTION;

UPDATE comptes SET solde = solde - 100 WHERE id = 1;
UPDATE comptes SET solde = solde + 100 WHERE id = 2;

COMMIT;   -- Valide la transaction
-- ou
ROLLBACK; -- Annule tout

# Requêtes utiles pour la data
## Nombre total de clients
SELECT COUNT(*) FROM clients;

## Montant total des commandes par client
SELECT client_id, SUM(montant)
FROM commandes
GROUP BY client_id;

## Top 5 des produits les plus chers
SELECT nom, prix
FROM produits
ORDER BY prix DESC
LIMIT 5;
