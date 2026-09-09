# Xianzhe Wang — Personal Website

Static personal website with research, talks, an English blog archive, and a downloadable CV.

## Publish on GitHub Pages

1. Create a GitHub repository and upload this project folder.
2. In the repository, open **Settings → Pages** and select **GitHub Actions** as the source.
3. Push to the `main` branch. The workflow in `.github/workflows/static.yml` publishes the site automatically.

The deployment workflow publishes only the public site:

- `index.html`, `assets/`, and `images/`
- English blog pages and their locally stored images
- `docs/CV_Inter.pdf`

Local source materials, Chinese article drafts, and build intermediates remain in the project for future editing but are excluded from the deployed website.

## Preview locally

Run:

```bash
python3 -m http.server 8000
```

Then open `http://127.0.0.1:8000/`.

## Main folders

- `blog/en/` — published English articles
- `blog/assets/` — images used by articles
- `blog-translated-all/` — editable English article source files
- `images/talks/` — Talk cover images
- `docs/CV_Inter.pdf` — published CV
- `scripts/` — optional article-processing utilities

## Credits

Based on the Strata template by HTML5 UP, under the CCA 3.0 license.
