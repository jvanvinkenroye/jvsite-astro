# Jan Vanvinkenroye

📧 [jan@vanvinkenroye.de](mailto:jan@vanvinkenroye.de) • 📞 [+49 171 185 4655](tel:+491711854655) • 🌐 [vanvinkenroye.de](https://vanvinkenroye.de)

Wissenschaftlicher Mitarbeiter an der Universität Stuttgart als Fachkraft für Digitalisierung. Engagiert in Lehre und Forschung mit Schwerpunkt in Themen der Bildung und Sozialer Arbeit.

Diplomierter Sozialarbeiter mit weiterem Diplom in Erwachsenenbildung. Weiterbildungen in Systemischer Beratung/Familientherapie, Systemischer Supervision und Systemischer Onlineberatung.

## 💼 Berufserfahrung

### `aktuell` Wissenschaftlicher Mitarbeiter
**Universität Stuttgart** - Universitäts-IT  
Systembetreuung, Support und Projektmanagement sowie Lehre

### `aktuell` Lehrkraft am Berufskolleg
Unterricht in Sozialpflege, Ethik und Pädagogik/Psychologie

### `laufend` Lehraufträge
Universitäten und Hochschulen - Medienpädagogik, Statistik und Forschungsmethoden, psychosoziale Beratung, Digitalisierung

### `laufend` Vorträge und Seminare
Erwachsenenbildung zu Themen der Medienerziehung und Digitalisierung

### `früher` Sozialarbeiter
Offene Jugendarbeit, Hilfen zur Erziehung und Hilfen zur Arbeit

## 👩‍🏫 Lehre

### Aktuelle Lehraufträge

#### `2024-2025` Hochschule München
„Gesellschaftliche Aspekte der Digitalisierung/Mediatisierung" - SoSe 2024, SoSe 2025  
*M.A. Forschungsmethoden und Digitalisierung in der Sozialen Arbeit*

#### `2024-2025` Hochschule Heilbronn
„Grundlagen empirischer Forschungsmethoden" - SoSe 2024, SoSe 2025  
*B.Sc. Angewandte Informatik*

#### `seit 2014` EH Ludwigsburg
„Einführung in die Medienpädagogik" - jedes Semester (3 SWS)  
*B.A. Soziale Arbeit, B.A. Religionspädagogik, B.A. Diakoniewissenschaft*

#### `2018-heute` Universität Stuttgart, TIK
„Studentisches Arbeiten mit Open Source Anwendungen und Betriebssystemen" (2 SWS)  
*Programm Studienübergreifende Schlüsselqualifikationen*

### Frühere Lehraufträge

#### `2022-2024` Macromedia Hochschule, Stuttgart
„Empirische Forschung und Statistik", „Orientierungsprojekt Forschung", „Medienpsychologie", „Einführung in die Psychologie", „Pädagogische Psychologie"

#### `2021-2024` IU – Internationale Hochschule
Standorte Stuttgart, Berlin, Essen, München, Leipzig  
„Methoden und Instrumente der sozialen Arbeit I", „Praxisreflexion I-V", „Offene Jugendarbeit", „Einführung in die Soziologie"

## 🎓 Qualifikation

### Diplom-Pädagoge
Erziehungswissenschaften, Schwerpunkt Erwachsenenbildung mit Nebenfach Psychologie und Wahlpflichtfächer Informatik und ev. Theologie

### Diplom-Sozialarbeiter (FH) / Diplom-Sozialpädagoge (FH)
Studium Sozialer Arbeit und Diakoniewissenschaft, kirchliches Examen

### Weiterbildungen
Systemische Beratung/Familientherapie, Systemische Supervision und Systemische Onlineberatung

## 📚 Veröffentlichungen

### `2021`
Bolten-Bühler, Ricarda, Dertinger, Andreas, Ellinger, Dorothea, Thielsch, Angelika, **Vanvinkenroye, Jan**, & Zender, Raphael. (2021). „Schöne neue (digitale) Welt?!" Tagungsband des Jungen Forums Medien und Hochschulentwicklung 2019. [DOI](https://doi.org/10.5281/zenodo.5736489)

### `2020`
Köhler, T., Bremer, C., Hafer, J., Himpsl-Gutermann, K., Thillosen, A., & **Vanvinkenroye, J.** (2020). Prolog: Was heißt ‚Medien in der Wissenschaft' im Kontext der Digitalisierung? Vom E-Learning zur Digitalisierung.

### `2018`
Hafer, J., Bremer, C., Himpsl-Gutermann, K., Köhler, T., Thillosen, A., & **Vanvinkenroye, J.** (2018). E-Learning. Ein Nachruf. Keine wissenschaftliche Analyse (pp. 26-35).

## 👥 Mitgliedschaften

- [Gesellschaft für Medien in der Wissenschaft e.V.](https://www.gmw-online.de) (Mitglied im Vorstand)
- [Deutsche Gesellschaft für Soziale Arbeit e.V.](https://www.dgsa.de/aktuelles-aus-der-dgsa/) - Fachgruppe Digitalisierung in der Sozialen Arbeit
- [Deutsche Gesellschaft für Erziehungswissenschaft e.V.](https://www.dgfe.de/sektionen-kommissionen-ag/sektion-12-medienpaedagogik) - Sektion Medienpädagogik (Assoziiertes Mitglied)
- [Systemische Gesellschaft e.V.](https://systemische-gesellschaft.de)
- Chaos Computer Club e.V.

## 🔗 Links

[GitHub](https://github.com/jvanvinkenroye) • [LinkedIn](https://www.linkedin.com/in/jvanvinkenroye/) • [Mastodon](https://higher-edu.social/@jvanvinkenroye) • [WhatsApp](http://wa.me/+491711854655)

## 🚀 Development & Deployment

This website is built with [Pelican](https://getpelican.com/) static site generator.

### Building the Site

```bash
# Build the site
./build.sh

# Or use make
make html
```

### Local Development Server

```bash
# Start development server with auto-reload at http://localhost:8000
./serve.sh

# Or use make
make devserver
```

### Deployment

1. Copy the environment configuration example:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and fill in your server details:
   ```bash
   export DEPLOY_USER="your_ssh_username"
   export DEPLOY_HOST="your.server.com"
   export DEPLOY_PATH="/var/www/html"
   export DEPLOY_PORT="22"
   ```

3. Deploy to your server:
   ```bash
   # Test first with dry-run
   ./deploy.sh --dry-run

   # Deploy to server
   ./deploy.sh

   # Verbose output
   ./deploy.sh --verbose
   ```

**Note:** Make sure you have SSH key authentication set up for passwordless deployment.

---
© 2024 Jan Vanvinkenroye