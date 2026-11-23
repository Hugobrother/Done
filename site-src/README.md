# Sources de la landing page

`public/index.html` est généré : ne pas l'éditer à la main.

| Fichier | Rôle |
|---|---|
| `style.css`, `body.html`, `main.js` | la page (styles, structure, animations GSAP) |
| `genfilm.py`, `guy.py`, `pov.html` | la scène du film (pièce, personnage, gros plan téléphone) → `film.html` |
| `build.py` | assemble le tout dans `public/index.html` |
| `render.py`, `encode.sh` | calculent le film en vidéo (`public/film-wide.*`, `public/film-tall.*`) |

## Reconstruire la page

```
python3 genfilm.py && python3 build.py
```

## Recalculer les vidéos (à refaire dès que le film change)

Le film est joué en vidéo pré-calculée pour rester fluide sur n'importe quelle machine ;
la scène animée en direct ne sert que de secours. Si on modifie le film sans refaire
les vidéos, les visiteurs verront l'ancienne version.

```
npm i gsap@3.12.5 @fontsource/space-grotesk      # une fois
pip install playwright pillow                    # une fois
python3 render.py wide 1920 800 2                # ~7 min
python3 render.py tall 540 730 4                 # ~7 min
sh encode.sh                                     # nécessite ffmpeg
```
