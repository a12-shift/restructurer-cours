# restructurer-cours

Skill Claude qui réécrit et réorganise intégralement une partie de cours dans Word (complément Claude installé) : sous-titres, puces, **gras** et *italique*, langue corrigée, sans supprimer aucune idée ni modifier les titres existants.

## Fonctionnement

Le skill cible soit la sélection de l'utilisateur, soit une grande partie désignée par son titre (un titre de style Titre / Titre 1 et tout son contenu jusqu'au titre suivant de même niveau). Il procède en cinq étapes :

1. **Lecture** de la cible et du jeu de styles du document (puces, titres, encadrés, police du corps de texte).
2. **Nouveau plan** : regroupement des idées par thème, sous-titres descriptifs, correction de la langue, énumérations en puces.
3. **Insertion** du nouveau contenu après le titre d'ancrage, puis suppression de l'ancien seulement après vérification.
4. **Vérification** du rendu (styles, numérotation, puces, encadrés, absence de doublons).
5. **Compte rendu** court dans le chat : sous-parties créées, regroupements, listes ajoutées, corrections incertaines, erreurs repérées dans les titres.

## Règles principales

- aucune idée n'est supprimée et le texte n'est pas raccourci ;
- le texte des titres existants n'est jamais modifié (les erreurs y sont signalées dans le chat) ;
- aucun fait absent des notes n'est ajouté au document ;
- les encadrés ne deviennent jamais des éléments de liste.

## Environnement

Le skill est conçu pour le complément Claude dans Word et s'appuie sur ses outils Office.js : `read_surface_context`, `execute_office_js`, `search_doc_text` et `verify_doc_visual`.

## Installation

Le fichier [`SKILL.md`](SKILL.md) contient l'intégralité des instructions.

- **Claude (application)** : compresser ce dossier en `.zip` et l'importer dans les paramètres des skills.
- **Claude Code** : cloner le dépôt dans le dossier des skills :

```bash
git clone https://github.com/a12-shift/restructurer-cours.git ~/.claude/skills/restructurer-cours
```
