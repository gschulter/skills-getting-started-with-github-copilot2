# Documentatie - Mergington High School API

## 📋 Inhoudsopgave

1. [Overzicht](#overzicht)
2. [Installatie](#installatie)
3. [De Applicatie Starten](#de-applicatie-starten)
4. [API Eindpunten](#api-eindpunten)
5. [Voorbeelden](#voorbeelden)
6. [Testen](#testen)
7. [Projectstructuur](#projectstructuur)

---

## 🎯 Overzicht

Dit project is een eenvoudige FastAPI-applicatie voor het Mergington High School systeem. De API stelt studenten in staat om:

- **Activiteiten** te bekijken
- **Zich in te schrijven** voor extracurriculaire activiteiten
- **Zich af te melden** van activiteiten
- **Steden per land** op te vragen

De applicatie maakt gebruik van een in-memory database met activiteiten en landen/steden gegevens.

### Technologieën

- **Framework**: FastAPI
- **Taal**: Python 3
- **Frontend**: HTML, CSS, JavaScript
- **Testing**: pytest

---

## 💻 Installatie

### Vereisten

- Python 3.8+
- pip (Python package manager)

### Stappen

1. **Clone de repository** (als je dit nog niet hebt gedaan):
   ```bash
   git clone <repository-url>
   cd skills-getting-started-with-github-copilot2
   ```

2. **Installeer de afhankelijkheden**:
   ```bash
   pip install -r requirements.txt
   ```

   Dit zal alle benodigde pakketten installeren, inclusief:
   - fastapi
   - uvicorn
   - pytest

---

## 🚀 De Applicatie Starten

### Stap 1: Ga naar de src directory
```bash
cd src
```

### Stap 2: Start de server
```bash
python -m uvicorn app:app --reload
```

De applicatie zal starten op: **http://localhost:8000**

### Stap 3: Open de API documentatie
Ga naar: **http://localhost:8000/docs**

Hier zie je de interactieve Swagger UI documentatie waar je alle eindpunten kunt testen.

---

## 📡 API Eindpunten

### 1. **Startpagina Omleiden**
```
GET /
```
**Beschrijving**: Stuurt je door naar de statische index pagina.

**Response**: Redirect naar `/static/index.html`

---

### 2. **Alle Activiteiten Ophalen**
```
GET /activities
```
**Beschrijving**: Haalt alle beschikbare activiteiten op.

**Response** (200 OK):
```json
{
  "Chess Club": {
    "description": "Leer strategieën en doe mee aan schaaktoernooien",
    "schedule": "Vrijdagen, 15:30 - 17:00 uur",
    "max_participants": 12,
    "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
  },
  ...
}
```

---

### 3. **Inschrijven voor Activiteit**
```
POST /activities/{activity_name}/signup?email={email}
```

**Beschrijving**: Schrijft een student in voor een activiteit.

**Parameters**:
- `activity_name` (path): Naam van de activiteit
- `email` (query): E-mailadres van de student

**Response** (200 OK):
```json
{
  "message": "Signed up student@mergington.edu for Chess Club"
}
```

**Foutmeldingen**:
- `404 Not Found`: Activiteit bestaat niet
- `400 Bad Request`: Student is al ingeschreven

---

### 4. **Afmelden voor Activiteit**
```
DELETE /activities/{activity_name}/unregister?email={email}
```

**Beschrijving**: Meldt een student af voor een activiteit.

**Parameters**:
- `activity_name` (path): Naam van de activiteit
- `email` (query): E-mailadres van de student

**Response** (200 OK):
```json
{
  "message": "Unregistered student@mergington.edu from Chess Club"
}
```

**Foutmeldingen**:
- `404 Not Found`: Activiteit bestaat niet
- `400 Bad Request`: Student is niet ingeschreven

---

### 5. **Steden per Land Ophalen** ⭐ (NIEUW)
```
GET /countries/{country_name}/cities
```

**Beschrijving**: Haalt alle steden voor een specifiek land op.

**Parameters**:
- `country_name` (path): Naam van het land

**Response** (200 OK):
```json
{
  "country": "United States",
  "cities": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
}
```

**Beschikbare Landen**:
- United States
- United Kingdom
- France
- Germany
- Japan
- Canada
- Australia

**Foutmeldingen**:
- `404 Not Found`: Land bestaat niet

---

## 📚 Voorbeelden

### Voorbeeld 1: Activiteiten Bekijken
```bash
curl http://localhost:8000/activities
```

### Voorbeeld 2: Inschrijven voor Activiteit
```bash
curl -X POST "http://localhost:8000/activities/Chess%20Club/signup?email=john@mergington.edu"
```

### Voorbeeld 3: Steden in Japan Ophalen
```bash
curl http://localhost:8000/countries/Japan/cities
```

**Response**:
```json
{
  "country": "Japan",
  "cities": ["Tokyo", "Osaka", "Yokohama", "Kyoto", "Sapporo"]
}
```

### Voorbeeld 4: Steden in het Verenigd Koninkrijk
```bash
curl "http://localhost:8000/countries/United%20Kingdom/cities"
```

**Response**:
```json
{
  "country": "United Kingdom",
  "cities": ["London", "Manchester", "Birmingham", "Leeds", "Glasgow"]
}
```

### Voorbeeld 5: Afmelden voor Activiteit
```bash
curl -X DELETE "http://localhost:8000/activities/Chess%20Club/unregister?email=john@mergington.edu"
```

---

## 🧪 Testen

### Alle Tests Uitvoeren
```bash
pytest
```

### Specifieke Test Uitvoeren
```bash
pytest tests/test_app.py::test_get_cities_by_country -v
```

### Met Uitgebreide Output
```bash
pytest -v
```

### Coverage Rapport
```bash
pytest --cov=src tests/
```

### Beschikbare Tests

#### Activiteit Tests
- `test_get_activities()` - Haalt alle activiteiten op
- `test_signup_for_activity()` - Schrijft in voor activiteit
- `test_signup_duplicate()` - Test dubbele inschrijving
- `test_signup_nonexistent_activity()` - Test niet-bestaande activiteit
- `test_unregister_from_activity()` - Meldt af voor activiteit
- `test_unregister_not_signed_up()` - Test afmelden zonder inschrijving
- `test_unregister_nonexistent_activity()` - Test afmelden niet-bestaande activiteit

#### Land/Steden Tests (NIEUW)
- `test_get_cities_by_country()` - Haalt steden per land op
- `test_get_cities_multiple_countries()` - Test meerdere landen
- `test_get_cities_nonexistent_country()` - Test niet-bestaand land

---

## 📁 Projectstructuur

```
skills-getting-started-with-github-copilot2/
├── src/
│   ├── app.py                    # Hoofd API applicatie
│   ├── static/
│   │   ├── index.html           # Startpagina
│   │   ├── app.js              # Frontend JavaScript
│   │   └── styles.css          # Stijlen
│   └── README.md
├── tests/
│   ├── conftest.py             # Pytest configuratie
│   └── test_app.py             # Tests voor API
├── requirements.txt             # Python dependencies
├── pytest.ini                   # Pytest configuratie
├── DOCUMENTATIE.md              # Deze file (Nederlands)
├── README.md                    # Originele README (Engels)
└── LICENSE                      # Licentie
```

---

## 🔧 Configuratie

### Environment Variabelen

Op dit moment gebruikt de applicatie geen speciale environment variabelen. Alle configuratie is hardcoded in `app.py`.

### FastAPI Instellingen

De FastAPI applicatie is geconfigureerd met:
- **Titel**: "Mergington High School API"
- **Beschrijving**: "API for viewing and signing up for extracurricular activities"
- **Docs URL**: `/docs` (Swagger UI)
- **ReDoc URL**: `/redoc` (ReDoc)

---

## 📖 Aanvullende Informatie

### Static Files

De applicatie serviert statische bestanden (HTML, CSS, JS) vanuit de `/static` map:
- URL: `http://localhost:8000/static/`
- Directory: `src/static/`

### In-Memory Database

De applicatie gebruikt in-memory storage. Dit betekent dat:
- Alle gegevens verdwijnen wanneer je de server stopt
- Wijzigingen worden niet opgeslagen in een bestand
- Dit is geschikt voor development/testing, niet voor productie

---

## 🐛 Troubleshooting

### Poort 8000 is al in gebruik
```bash
# Gebruik een andere poort
python -m uvicorn app:app --port 8001
```

### ModuleNotFoundError
```bash
# Zorg dat je in de juiste directory bent
cd src
# Of voeg src toe aan PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/pad/naar/project"
```

### Tests falen
```bash
# Zorg dat je in de root directory bent (niet in src/)
cd ..
pytest
```

---

## 📞 Contact & Ondersteuning

Voor vragen of problemen, open een issue in de repository.

---

**Versie**: 1.0  
**Laatste Update**: Januari 2026  
**Taal**: Nederlands
