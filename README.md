# HudIsThinking LLC — Web Archive & Software Repository

A minimalist, high-performance web platform built with Python & Django. Designed as a personal archive for philosophical arguments, manuscripts, and downloadable game/software builds.

---

## Aesthetic & Design Principles
- **Monochromatic Scheme**: Pure black (`#000000`), deep surface layers (`#0a0a0a`), and stark white/silver typography (`#ffffff` / `#a3a3a3`).
- **Typography**: **Special Elite** font (Google Fonts) for a weathered, authentic dossier / typewriter aesthetic.
- **No Client-side Slop**: 100% native Django Server-Side Rendering (SSR). Zero React, zero heavy frontend frameworks, instant loading, accessible and clean HTML5.
- **Built-in SEO & Schema**: Automatic OpenGraph cards and Google JSON-LD structured data (`Article`, `SoftwareApplication`, `WebSite`).

---

## Quickstart (Local Development)

### 1. Activate Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

### 2. Run the Development Server
```powershell
python manage.py runserver
```
Visit `http://127.0.0.1:8000` in your browser.

---

## Content Management (Zero-Code Admin)

You don't need to write code to post essays or upload files. Everything is managed through the Django Admin dashboard:

1. Navigate to: `http://127.0.0.1:8000/admin/`
2. Administrator login:
   - **Username**: `hud`
   - **Password**: *(your configured master password)*
3. From the dashboard:
   - **Philosophy Archive**: Add philosophical arguments, essays, blog posts, or fragments. Supports full Markdown formatting (headings, code blocks, quotes, lists).
   - **Projects & Downloads**: Add software works, games, and prototypes. Upload your `.exe` or `.zip` files directly (<100MB), specify system requirements, version numbers, and platform tags.
   - **About Page**: Edit your bio and LLC information anytime.

---

## Project Structure

```
HudNewSite/
├── config/                  # Django project root settings & URLs
│   ├── settings.py          # Decouple configuration, Whitenoise, Media storage
│   ├── urls.py              # Global URL routes
│   └── wsgi.py              # Production WSGI application
├── core/                    # Core branding, Home page, About page, Markdown filters
├── philosophy/              # Philosophical arguments, essays, reading time, JSON-LD
├── projects/                # Downloadable games, binaries, specs, JSON-LD
├── static/
│   ├── css/gothic-theme.css # Monochromatic styling & Special Elite typography
│   └── images/logo.png      # HudIsThinking logo
├── templates/               # Semantic HTML5 server-rendered templates
├── Dockerfile               # Google Cloud Run container specification
├── cloudbuild.yaml          # Google Cloud Build deployment pipeline
├── requirements.txt         # Pinned Python dependencies
└── manage.py                # Django CLI
```

---

## Deploying to Google Cloud (Cloud Run & Cloud Build)

The repository includes a ready-to-use `Dockerfile` and `cloudbuild.yaml`:

### Automatic Deployment with GitHub & Cloud Build:
1. Initialize a git repository and commit:
   ```powershell
   git init
   git add .
   git commit -m "Initial commit of HudIsThinking website"
   ```
2. Push to your GitHub repository.
3. Connect your GitHub repository to **Google Cloud Build** triggers.
4. Cloud Build will automatically build the container image and deploy it directly to **Google Cloud Run**.

### Manual Cloud Run Deploy:
```bash
gcloud run deploy hudisthinking-repo --source . --region us-east1 --allow-unauthenticated
```
