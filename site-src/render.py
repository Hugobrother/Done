# Rendu image par image du film (déterministe) → dossier d'images pour ffmpeg
import sys, os, time
from playwright.sync_api import sync_playwright
S=os.path.dirname(os.path.abspath(__file__))+"/"
gd=S+"node_modules/gsap/dist/"; fd=S+"node_modules/@fontsource/space-grotesk/files/"
kind,W,H=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]); FPS=60
DSF=int(sys.argv[4]) if len(sys.argv)>4 else 1
first=int(sys.argv[5]) if len(sys.argv)>5 else 0; last=int(sys.argv[6]) if len(sys.argv)>6 else None
out=S+f".cap/{kind}/"; os.makedirs(out,exist_ok=True)
FONTCSS="".join(f"@font-face{{font-family:'Space Grotesk';font-style:normal;font-weight:{w};font-display:block;src:url(https://fonts.gstatic.com/l/{w}.woff2) format('woff2')}}" for w in (400,500,700))
HIDE="header,#cursor,.fvig,.fgrain,.fbarT,.fbarB,.fcap,#ftime,.fbar,#fstate,#progress,#wipe{display:none!important}#film{--bt:0px!important;--bb:0px!important}"
STEP="""(t)=>{const f=window.__doneFilm, D=f.dur;
  if(!f._init){f._init=1; f.tl.pause(); f.amb.forEach(a=>a.pause()); document.getAnimations().forEach(a=>a.pause());}
  if(t<D-0.001){f.tl.time(t,false);} else { if(!f._dive){f._dive=1; f.tl.time(D-0.001,false); f.dive.invalidate(); f.dive.pause();} f.dive.time(t-D); }
  f.amb.forEach(a=>a.totalTime(t+20)); document.getAnimations().forEach(a=>{a.currentTime=t*1000});
  f.cam(); return f.tl.time();}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    c=b.new_context(viewport={"width":W,"height":H},device_scale_factor=DSF)
    pg=c.new_page(); errs=[]
    pg.on("pageerror",lambda e: errs.append(str(e)))
    pg.route("**/gsap.min.js", lambda r: r.fulfill(path=gd+"gsap.min.js", content_type="text/javascript"))
    pg.route("**/ScrollTrigger.min.js", lambda r: r.fulfill(path=gd+"ScrollTrigger.min.js", content_type="text/javascript"))
    pg.route("**/fonts.googleapis.com/**", lambda r: r.fulfill(body=FONTCSS, content_type="text/css", headers={"Access-Control-Allow-Origin":"*"}))
    pg.route("**/fonts.gstatic.com/l/*", lambda r: r.fulfill(path=fd+"space-grotesk-latin-"+r.request.url.split("/")[-1].split(".")[0]+"-normal.woff2", content_type="font/woff2", headers={"Access-Control-Allow-Origin":"*"}))
    pg.route("**/film-*.*", lambda r: r.abort())
    pg.add_init_script("(()=>{const go=()=>{if(!document.documentElement)return setTimeout(go,0);const s=document.createElement('style');s.textContent=%r;document.documentElement.appendChild(s);};go();})()" % HIDE)
    pg.goto("file://"+os.path.abspath(S+"../public/index.html")); pg.wait_for_timeout(2600)
    pg.evaluate("document.fonts.ready.then(()=>1)")
    print("font ok:",pg.evaluate("document.fonts.check(\"700 20px 'Space Grotesk'\")"),"viewBox",pg.evaluate("document.querySelector('#film-svg').getAttribute('viewBox')"),flush=True)
    pg.evaluate("window.scrollTo(0, document.querySelector('#film').offsetTop)")
    pg.wait_for_function("document.documentElement.classList.contains('locked')",timeout=5000); pg.wait_for_timeout(1500)
    D=pg.evaluate("__doneFilm.dur"); n=int(round((D+0.7)*FPS)); print("mode",pg.evaluate("__doneFilm.mode()"),"dur",D,"frames",n,flush=True)
    last=n if last is None else min(last,n); t0=time.time()
    for i in range(0,last):
        t=i/FPS
        pg.evaluate(STEP,t)          # on avance toujours image par image (les déclencheurs dépendent de l'ordre)
        if i>=first: pg.screenshot(path=out+f"f_{i:04d}.jpg",type="jpeg",quality=97)
        if i%100==0: print(i,"%.0fs"%(time.time()-t0),flush=True)
    print("done",last-first,"frames in %.0fs"%(time.time()-t0),"errors",errs[:3],flush=True)
    b.close()
