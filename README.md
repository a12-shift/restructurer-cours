# restructurer-cours

Skill Claude pour **Word** : il réécrit et réorganise une partie de cours (sous-titres, puces, **gras** et *italique*, langue corrigée) **sans supprimer aucune idée** ni modifier les titres existants.

**[Télécharger restructurer-cours.zip](https://github.com/a12-shift/restructurer-cours/releases/latest/download/restructurer-cours.zip)**, puis suivez les trois étapes ci-dessous.

## Installation dans Word

### Avant de commencer

- Un abonnement Claude **Pro, Max, Team ou Enterprise**.
- Le complément **Claude** installé dans Word : ouvrez la fiche [Claude for Microsoft 365 sur Microsoft AppSource](https://marketplace.microsoft.com/en-us/product/office/WA200010725?tab=Overview), cliquez sur **Get it now**, puis connectez-vous à votre compte Claude dans Word.
- Word Microsoft 365 sur Windows ou Mac, ou Word sur le web. Word 2016 ou 2019, Word sur iPad et Word sur Android ne sont pas pris en charge.
- Dans les paramètres de claude.ai, l'option **Code execution and file creation** (ou **Create and edit files**) doit être activée : les skills en ont besoin.
- Avec un compte Team ou Enterprise (université, entreprise), l'administrateur de l'organisation doit avoir autorisé les skills. Si l'option d'import n'apparaît pas, demandez-lui.

### 1. Télécharger le skill

Cliquez sur **[restructurer-cours.zip](https://github.com/a12-shift/restructurer-cours/releases/latest/download/restructurer-cours.zip)**. Gardez le fichier tel quel : **ne le décompressez pas**.

> N'utilisez pas le bouton vert **Code › Download ZIP** de GitHub. L'archive obtenue contient un dossier `restructurer-cours-main` dont le nom ne correspond pas à celui du skill, et Claude peut la refuser.

> Sur Mac, Safari peut décompresser le fichier automatiquement. Dans ce cas, téléchargez-le avec Chrome ou Firefox, ou décochez **Ouvrir les fichiers fiables après téléchargement** (Safari › Réglages › Général), puis téléchargez-le à nouveau. Ne recompressez pas vous-même le dossier.

### 2. Importer le skill dans Claude

1. Ouvrez [claude.ai/customize/skills](https://claude.ai/customize/skills) (menu **Customize › Skills**).
2. Cliquez sur **+**, puis sur **Create skill › Upload a skill**.
3. Choisissez le fichier `restructurer-cours.zip`.
4. Vérifiez que l'interrupteur à côté de **restructurer-cours** est activé.

Le skill est enregistré sur votre compte Claude : il est disponible dans Word sur tous vos ordinateurs.

### 3. L'utiliser dans Word

1. Ouvrez votre cours dans Word, puis le volet Claude (onglet **Accueil**, bouton **Claude** ou **Compléments**).
2. Sélectionnez la partie à restructurer, ou ne sélectionnez rien et nommez-la dans votre demande.
3. Écrivez par exemple :
   - « Restructure la partie sélectionnée » ;
   - « Réorganise la séance sur Foucault » ;
   - « Fais de même pour la séance suivante ».

Vous pouvez aussi taper `/` dans le volet et choisir **restructurer-cours**.

Claude réécrit la partie directement dans le document, puis résume dans le chat ce qu'il a fait : sous-parties créées, regroupements, listes ajoutées, corrections incertaines et erreurs repérées dans les titres.

> Pour une partie longue, enregistrez une copie du document avant de lancer le skill. Ctrl+Z (Cmd+Z sur Mac) annule les modifications, parfois en plusieurs fois.

### Autre méthode : importer le skill depuis le complément

Dans le volet Claude de Word, cliquez sur le bouton **+** sous la zone de saisie, ouvrez **Skills** et importez `restructurer-cours.zip`.

Un skill importé de cette façon n'est enregistré **que sur cet ordinateur**, et il peut disparaître après certaines mises à jour de Microsoft 365 sous Windows. Pour le conserver, survolez-le dans le menu **Skills** et cliquez sur l'icône en forme de nuage (**Save to claude.ai**). La méthode de l'étape 2 reste préférable.

## Mettre à jour le skill

1. Téléchargez la dernière version : [restructurer-cours.zip](https://github.com/a12-shift/restructurer-cours/releases/latest/download/restructurer-cours.zip). La liste des versions se trouve dans les [Releases](https://github.com/a12-shift/restructurer-cours/releases).
2. Dans [Customize › Skills](https://claude.ai/customize/skills), supprimez l'ancienne version (menu **…** › **Delete**).
3. Importez le nouveau fichier comme à l'étape 2.

## En cas de problème

- **Le fichier est refusé à l'import** : importez le `restructurer-cours.zip` téléchargé depuis le lien ci-dessus, sans l'avoir décompressé ni recompressé.
- **Le skill n'apparaît pas dans Word** : vérifiez que son interrupteur est activé dans [Customize › Skills](https://claude.ai/customize/skills) et que l'option **Code execution and file creation** est active, puis fermez et rouvrez le volet Claude.
- **Claude ne lance pas le skill de lui-même** : tapez `/` dans le volet et choisissez **restructurer-cours**, ou commencez votre demande par « Restructure ».
- **Le skill a disparu après une mise à jour de Windows** : cela concerne les skills importés depuis le complément. Réimportez-le depuis claude.ai (étape 2). Voir la [note d'Anthropic](https://claude.com/docs/office-agents/data-storage#chat-history-and-skills-missing-after-a-microsoft-365-update-on-windows).
- **Claude indique que les outils Word ne sont pas disponibles** : la demande a été faite dans claude.ai et non dans Word. Ouvrez le document dans Word avec le complément, ou laissez Claude rendre le texte restructuré dans le chat.

## Ce que fait le skill

Le skill cible soit la sélection, soit une grande partie désignée par son titre : un titre de style Titre ou Titre 1, avec tout son contenu jusqu'au titre suivant de même niveau. Il procède en cinq étapes :

1. **Lecture** de la partie et du jeu de styles du document : puces, titres, encadrés, police du corps de texte.
2. **Nouveau plan** : regroupement des idées par thème, sous-titres descriptifs, correction de la langue, énumérations en puces.
3. **Insertion** du nouveau contenu après le titre d'ancrage, puis suppression de l'ancien, seulement après vérification.
4. **Vérification** du rendu : styles, numérotation, puces, encadrés, absence de doublons.
5. **Compte rendu** court dans le chat.

Règles principales :

- aucune idée n'est supprimée et le texte n'est pas raccourci ;
- le texte des titres existants n'est jamais modifié (les erreurs repérées sont signalées dans le chat) ;
- aucun fait absent des notes n'est ajouté au document ;
- les encadrés ne deviennent jamais des éléments de liste.

Le skill utilise les outils Office.js du complément Claude pour Word : `read_surface_context`, `execute_office_js`, `search_doc_text` et `verify_doc_visual`. Toutes les instructions se trouvent dans [`SKILL.md`](SKILL.md).

## Pour les développeurs

### Installer dans Claude Code

```bash
git clone https://github.com/a12-shift/restructurer-cours.git ~/.claude/skills/restructurer-cours
```

### Publier une nouvelle version

1. Modifiez `SKILL.md` et augmentez `metadata.version` dans l'en-tête (par exemple `1.1.0` → `1.2.0`).
2. Poussez sur `main`. Le workflow [`skill.yml`](.github/workflows/skill.yml) valide le skill avec [`skills-ref`](https://github.com/agentskills/agentskills/tree/main/skills-ref), construit `restructurer-cours.zip` et publie la release `v1.2.0`. Le lien de téléchargement pointe alors automatiquement vers cette version.

Pour construire l'archive en local : `python tools/build_zip.py` produit `dist/restructurer-cours.zip`.

## Licence

[MIT](LICENSE) : vous pouvez utiliser, modifier et partager ce skill librement, à condition de conserver la mention de copyright et le texte de la licence.
