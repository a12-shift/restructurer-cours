---
name: restructurer-cours
description: "Réécrit et réorganise intégralement une partie de cours dans Word (la sélection, ou une grande partie désignée par son titre) : sous-titres, puces, gras et italique, langue corrigée, sans supprimer aucune idée ni modifier les titres existants. À utiliser quand on demande de restructurer, réorganiser, réécrire ou mettre en page une partie, une séance ou un chapitre de cours."
license: MIT
metadata:
  version: "1.1.1"
---

## When to use
Quand l'utilisateur demande de restructurer, réorganiser, réécrire ou mettre en page une partie de cours : « restructure la partie sélectionnée », « fais de même pour la séance suivante », « réorganise cette partie », « refais la partie sélectionnée », ou quand il désigne une grande partie par son titre (ex. « la séance sur Foucault »).

## Environment
Ce skill s'appuie sur les outils du complément Claude pour Word : `read_surface_context`, `execute_office_js`, `search_doc_text` et `verify_doc_visual`. S'ils ne sont pas disponibles (par exemple dans le chat de claude.ai), le dire à l'utilisateur et proposer de rendre la partie restructurée dans le chat, en Markdown, selon les mêmes règles.

## Inputs
- `cible` : la sélection de l'utilisateur. Sans sélection, la grande partie qu'il nomme (un titre de style Titre / Titre 1 et tout son contenu jusqu'au titre suivant de même niveau). Sans sélection ni partie nommée, demander quelle partie restructurer avant toute modification.

## Goal
La partie ciblée est réécrite et réorganisée dans le document :
- **aucune idée n'est supprimée** et le texte n'est pas raccourci ;
- les titres existants restent tels quels ;
- des sous-titres structurent la partie ;
- les énumérations sont en puces, les définitions et concepts clés en **gras**, les noms propres, dates et titres d'œuvres en *italique* ;
- la langue est corrigée dans un registre académique, sans emoji ;
- les corrections incertaines sont signalées dans le chat.

## Steps

### 1. Lire la cible et le jeu de styles
- Appeler `read_surface_context` pour connaître la sélection et les styles du document.
- Dans `execute_office_js`, lire `context.document.getSelection().paragraphs` : `text`, `style`, `isListItem`.
- Relever les styles utilisés : le style de puces maison (ex. « Liste à puces »), les styles de titres (Titre 1/2/3), les styles d'encadré (ex. « Accentuation intense »), ainsi que la police, la taille et la couleur du corps de texte (ex. Aptos 10, #000000).
**Done when:** on connaît le premier et le dernier paragraphe de la cible, leur nombre et les styles à réutiliser.
**Produces:** l'index du titre d'ancrage et la liste exacte des anciens paragraphes à remplacer.

### 2. Construire le nouveau plan
- Regrouper les idées par thème et déplacer les phrases dispersées qui portent sur le même sujet.
- Ajouter des sous-titres descriptifs. Chaque idée de l'original doit se retrouver dans le nouveau texte.
- Corriger l'orthographe, la grammaire et la ponctuation françaises (espaces avant « : ; ? ! », guillemets « »).
- Découper les énumérations en puces : minuscule en début de puce, « ; » entre les puces, « . » à la dernière.
- **Rule :** ne jamais modifier le texte des titres existants. Signaler plutôt les erreurs qu'on y repère (ex. « LTI (1847) » au lieu de 1947).
- **Rule :** ne pas ajouter de faits absents des notes. On peut suggérer l'auteur probable dans le chat, mais pas dans le document.
**Done when:** le plan couvre chaque paragraphe d'origine.

### 3. Insérer le nouveau contenu, puis supprimer l'ancien
- Dans un seul `execute_office_js`, insérer les paragraphes avec `insertParagraph("", "After")` à la suite du titre d'ancrage, en chaînant chaque paragraphe après le précédent.
- Appliquer les styles :
  - corps de texte : `styleBuiltIn = "Normal"` ;
  - puces : le style de puces maison ;
  - sous-titres : le style de titre du document au niveau adapté ;
  - encadrés : le style d'origine, repris avec `style` depuis le paragraphe original.
- Pour le gras et l'italique, découper le texte en segments `**gras**` / `*italique*` et insérer chaque segment avec `insertText(t, "End")`. Fixer explicitement bold, italic, police, taille et couleur du corps sur chaque segment.
- Supprimer les anciens paragraphes seulement après l'insertion et un `sync`.
- **Rule :** repérer le titre d'ancrage par son style et une sous-chaîne (le texte peut contenir des espaces doubles). Vérifier que le nombre d'anciens paragraphes correspond à la sélection avant toute suppression.
- **Rule :** numérotation des sous-titres : suivre le jeu de styles de l'utilisateur, c'est-à-dire appliquer le style de titre tel qu'il est défini dans le document. Si la numérotation obtenue prolonge à tort la séance précédente (ex. 1.1.6 sous une nouvelle séance), le signaler et demander avant de la retirer.
- **Rule :** les encadrés (« Accentuation intense », etc.) ne doivent jamais devenir des éléments de liste. Si la lecture montre `isListItem = true`, appeler `detachFromList()` et rétablir le style d'origine.
**Done when:** les nouveaux paragraphes existent, les anciens ont disparu, il ne reste aucun `*` littéral (vérifier avec `search_doc_text`), et chaque puce a `isListItem = true`.

### 4. Vérifier
- Relire le résultat : styles des sous-titres, numérotation, puces, encadrés. Si besoin, appeler `verify_doc_visual` en indiquant la section avec `page_hint`.
- Si un appel est interrompu ou si l'utilisateur signale une erreur, relire l'état réel du document avant de refaire quoi que ce soit : ne jamais relancer un script d'insertion sans vérifier qu'il n'a pas déjà été appliqué. Si l'utilisateur a annulé, refaire à partir de l'état actuel.
- Ne pas toucher au texte que l'utilisateur est en train de saisir hors de la cible.
**Done when:** le rendu est propre et sans doublon.

### 5. Compte rendu dans le chat
Rédiger un message court, en français, sous forme de puces à libellé gras :
- les sous-parties créées ;
- les regroupements et déplacements ;
- les listes ajoutées ;
- les corrections incertaines, citées (ex. « des schtuk » → *Stück*) ;
- les éventuelles erreurs dans les titres, non modifiées.
Pas de tableau.
