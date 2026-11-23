import os
d=os.path.dirname(os.path.abspath(__file__))+"/"
css=open(d+"style.css").read(); body=open(d+"body.html").read().replace("__FILM__",open(d+"film.html").read().rstrip()); js=open(d+"main.js").read()
html=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>done. — work, wander, come back on time</title>
<meta name="description" content="done. pings your phone the second Claude finishes or needs your approval. Mac, Windows, Linux. Free beta.">
<meta name="theme-color" content="#141413">
<link rel="manifest" href="/manifest.json">
<link rel="icon" href="/icon-192.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&display=swap">
<style>
{css}</style>
</head>
<body>
{body}
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script>
{js}</script>
</body>
</html>
'''
open(d+"../public/index.html","w").write(html)
print("built", len(html))
