# Installer le plugin LibreAgent

Serveur LibreAgent : https://libreagent.92.222.229.134.sslip.io

Ce guide s’adresse à l’assistant de code qui l’a ouvert (Codex ou Claude Code). Exécute les étapes dans l’ordre sur l’ordinateur de la personne, puis explique-lui l’étape de connexion, qu’elle seule peut faire. Les commandes sont prévues pour macOS et Linux.

Prérequis : la personne doit avoir un compte LibreAgent sur ce serveur. Si elle n’en a pas, elle doit demander un lien d’invitation à un administrateur de son organisation LibreAgent avant de continuer.

## Installer dans Codex (application ou CLI)

```bash
codex plugin marketplace add ncleton/libreagent-plugin
codex plugin add libreagent-agent-builder@libreagent
codex mcp login libreagent
```

La dernière commande ouvre la page de connexion LibreAgent dans le navigateur. La personne s’y connecte avec son compte LibreAgent ; la commande se termine quand la connexion est acceptée. Redémarrez ensuite Codex, ou ouvrez une nouvelle conversation, pour charger le plugin.

## Installer dans Claude Code

```bash
claude plugin marketplace add ncleton/libreagent-plugin
claude plugin install libreagent-agent-builder@libreagent
```

La personne redémarre ensuite Claude Code, tape /mcp, choisit le serveur libreagent, puis Authenticate, et se connecte avec son compte LibreAgent.

## Vérifier

Dans une nouvelle conversation, demandez : « Liste mes agents LibreAgent. » Le plugin doit répondre avec les agents de l’organisation. Si la réponse indique authentication_required, refaites l’étape de connexion.

## Mettre à jour

```bash
codex plugin marketplace upgrade libreagent
codex plugin add libreagent-agent-builder@libreagent
claude plugin marketplace update libreagent
claude plugin update libreagent-agent-builder@libreagent
```

N’exécutez que les lignes du client installé.
