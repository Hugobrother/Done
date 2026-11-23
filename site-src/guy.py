# Personnage v3 : hoodie capuche relevée, baggy délavé, plis, ombres, texture, lumières de contour
COOL, SUN = "#9DB7FF", "#FFB070"
HOOD = dict(g="gHood", fold="#5E574C", hi="#F6F0E2", deep="#3F3A33")
HOODF = dict(g="gHoodF", fold="#35312B", hi="#A69E8E", deep="#24211D")
JEAN = dict(g="gJean", fold="#2B3857", hi="#DCE7F7", deep="#1F2942")
JEANF = dict(g="gJeanF", fold="#161D30", hi="#8094B8", deep="#10151F")

def tube(L, a, b, cap=10):
    return (f"M{-a},{-cap*.4:.1f} C{-a-3},{L*.3:.1f} {-b-2},{L*.7:.1f} {-b},{L:.1f} Q0,{L+cap:.1f} {b},{L:.1f} "
            f"C{b+2},{L*.7:.1f} {a+3},{L*.3:.1f} {a},{-cap*.4:.1f} Q0,{-cap*1.7:.1f} {-a},{-cap*.4:.1f} Z")

def fold(d, c, w=2.4, o=.5):
    """un pli = un creux sombre + un rebord clair juste dessous"""
    return (f'<path d="{d}" fill="none" stroke="{c["fold"]}" stroke-width="{w}" stroke-linecap="round" opacity="{o}"/>'
            f'<path d="{d}" transform="translate(0,2.6)" fill="none" stroke="{c["hi"]}" stroke-width="{w*.5:.1f}" stroke-linecap="round" opacity="{o*.55:.2f}"/>')

def rim(d, cls="rim", col=COOL, w=6, o=1):
    """lumière de contour : halo large + liseré fin"""
    return (f'<g class="{cls}" stroke="{col}" fill="none" stroke-linecap="round" opacity="{o}">'
            f'<path d="{d}" stroke-width="{w}" opacity=".2"/><path d="{d}" stroke-width="{w*.36:.1f}" opacity=".7"/></g>')

def thigh(c, far=False):
    d = tube(130, 23, 22)
    s = f'<path d="{d}" fill="url(#{c["g"]})"/><path d="{d}" fill="url(#pDenim)"/>'
    if not far:
        s += '<ellipse cx="7" cy="64" rx="9" ry="42" fill="#fff" opacity=".09"/>'
        s += f'<path d="M-3,2 C-5,44 -4,90 -3,126" fill="none" stroke="{c["fold"]}" stroke-width="1.5" opacity=".6"/>'
        s += f'<path d="M-.4,4 C-2.4,44 -1.4,90 -.4,124" fill="none" stroke="{c["hi"]}" stroke-width=".9" stroke-dasharray="3 3" opacity=".55"/>'
        s += f'<path d="M-19,16 L-5,11 L-3,35 L-11,42 L-20,36 Z" fill="{c["deep"]}" fill-opacity=".14" stroke="{c["fold"]}" stroke-width="1.3" opacity=".7"/>'
        s += f'<path d="M-17,18 L-7,14.5" stroke="{c["hi"]}" stroke-width=".9" stroke-dasharray="2.5 2.5" opacity=".5"/>'
    s += fold("M21,9 Q11,18 1,15", c, 2.4, .5) + fold("M22,25 Q13,35 5,33", c, 2, .4)
    s += fold("M12,34 C17,62 6,92 13,118", c, 2, .3)
    s += fold("M-22,109 Q-12,103 -1,108", c, 2.4, .5) + fold("M-20,121 Q-9,116 2,121", c, 2, .4)
    s += f'<path d="M-23,0 C-27,40 -25,92 -22,128 Q-12,134 -4,134 C-8,92 -8,40 -6,-6 Z" fill="{c["deep"]}" opacity=".22"/>'
    if not far:
        s += rim("M21,6 C24,40 24,90 21,122", "rimS", SUN, 5, .9) + rim("M20,8 C23,40 23,90 20,120")
    return s

def shoe(far=False):
    up, sole = ("#8C877D", "#A8A297") if far else ("url(#gShoe)", "#F4EFE6")
    s = f'<path d="M-18,110 L8,108 Q24,110 34,123 L54,133 Q62,137 62,145 L62,148 L-18,148 Z" fill="{up}"/>'
    s += f'<path d="M-21,145 H61 Q66,145 66,150 Q66,155 60,155 H-18 Q-23,155 -23,150 Q-23,145 -21,145 Z" fill="{sole}"/>'
    s += '<path d="M-21,154 H62" stroke="#24221F" stroke-width="2.4" stroke-linecap="round"/>'
    if not far:
        s += '<path d="M41,127 Q47,137 45,145" fill="none" stroke="#B5AE9F" stroke-width="1.6"/>'
        s += '<path d="M-4,131 L26,141" stroke="#D97757" stroke-width="3.4" stroke-linecap="round"/><path d="M-8,138 L18,146" stroke="#D97757" stroke-width="2" stroke-linecap="round" opacity=".6"/>'
        s += '<path d="M12,113 L20,119 M18,112 L26,119 M24,113 L31,121" stroke="#8E897E" stroke-width="1.5" stroke-linecap="round"/>'
        s += '<path d="M-18,110 L-18,146 L-2,146 C-8,134 -10,122 -8,109 Z" fill="#000" opacity=".16"/>'
    return s

def shin(c, far=False):
    d = tube(110, 21, 26)
    sid = "fHemF" if far else "fHem"
    s = shoe(far)
    s += f'<path d="{d}" fill="url(#{c["g"]})"/><path d="{d}" fill="url(#pDenim)"/>'
    if not far:
        s += f'<path d="M-3,0 C-5,40 -5,80 -4,108" fill="none" stroke="{c["fold"]}" stroke-width="1.5" opacity=".6"/>'
        s += f'<path d="M-.4,2 C-2.4,40 -2.4,80 -1.4,106" fill="none" stroke="{c["hi"]}" stroke-width=".9" stroke-dasharray="3 3" opacity=".55"/>'
    s += fold("M-19,10 Q-9,4 2,9", c, 2.2, .42) + fold("M-9,14 C-14,42 -3,62 -12,92", c, 2, .3)
    s += fold("M-25,80 Q-9,71 8,79", c, 2.6, .5) + fold("M27,90 Q10,83 -7,92", c, 2.6, .5) + fold("M-26,98 Q-12,93 2,98", c, 2.2, .45)
    s += f'<path d="M-21,-4 C-25,30 -27,76 -26,108 Q-14,114 -6,114 C-9,76 -9,30 -6,-8 Z" fill="{c["deep"]}" opacity=".22"/>'
    # revers retourné, un peu plus clair, qui bouge avec un temps de retard
    cuff = "#4A6096" if far else "#A9C0EA"
    s += (f'<g transform="translate(0,104)"><g id="{sid}"><path d="M-27,-3 Q0,7 28,-3 L29,13 Q0,24 -28,13 Z" fill="{cuff}"/>'
          f'<path d="M-27,-3 Q0,7 28,-3" fill="none" stroke="{c["deep"]}" stroke-width="2.4" opacity=".45"/>'
          f'<path d="M-27,8 Q0,19 28,8" fill="none" stroke="{c["fold"]}" stroke-width=".9" stroke-dasharray="3 3" opacity=".6"/>'
          f'<path d="M-28,-3 L-28,13 Q-18,18 -10,19 L-10,3 Z" fill="{c["deep"]}" opacity=".25"/></g></g>')
    if not far:
        s += rim("M22,2 C26,34 28,74 27,100", "rimS", SUN, 5, .9) + rim("M21,4 C25,34 27,74 26,98")
    return s

def uarm(c, far=False):
    d = tube(85, 16, 15, 9)
    s = f'<path d="{d}" fill="url(#{c["g"]})"/><path d="{d}" fill="url(#pFleece)"/>'
    s += fold("M5,8 C9,30 1,46 7,62", c, 2, .3) + fold("M-15,64 Q-5,57 6,63", c, 2.4, .5) + fold("M16,73 Q6,67 -4,73", c, 2.2, .42)
    s += f'<path d="M-16,-3 C-19,26 -18,60 -15,85 Q-8,91 -3,92 C-6,60 -6,26 -4,-8 Z" fill="{c["deep"]}" opacity=".2"/>'
    if not far:
        s += rim("M16,2 C19,30 18,60 16,82", "rimS", SUN, 5, .9) + rim("M15,4 C18,30 17,60 15,80")
    return s

def larm(c, far=False, phone=""):
    d = tube(54, 15, 13, 8)
    skin, cuff = ("#9A6B50", "#6E675B") if far else ("url(#gSkin)", "#BDB3A0")
    s = f'<path d="{d}" fill="url(#{c["g"]})"/><path d="{d}" fill="url(#pFleece)"/>'
    s += fold("M-14,9 Q-3,15 8,9", c, 2.2, .45) + fold("M14,43 Q4,37 -6,44", c, 2.2, .42)
    s += f'<path d="M-15,-2 C-17,16 -16,38 -13,54 Q-8,58 -3,58 C-5,38 -5,16 -4,-6 Z" fill="{c["deep"]}" opacity=".2"/>'
    s += f'<rect x="-12" y="51" width="24" height="14" rx="4.5" fill="{cuff}"/>'
    s += "".join(f'<path d="M{x},53 V63" stroke="{c["fold"]}" stroke-width="1" opacity=".55"/>' for x in (-8, -4, 0, 4, 8))
    s += phone
    s += f'<ellipse cx="0" cy="76" rx="10.5" ry="11.5" fill="{skin}"/>'
    if not far:
        s += '<path d="M-8,80 Q-2,86 6,82" fill="none" stroke="#8F5E44" stroke-width="1.4" stroke-linecap="round" opacity=".7"/><path d="M-9,75 Q-2,80 7,76" fill="none" stroke="#8F5E44" stroke-width="1.2" stroke-linecap="round" opacity=".5"/>'
        s += rim("M15,2 C17,18 16,38 13,52", "rimS", SUN, 5, .9) + rim("M14,4 C16,18 15,38 12,50")
    return s

PHONE = '''<g id="fHandPhone" transform="translate(-9,86)" opacity="0">
                <g id="fHpBody"><rect x="-6" y="-34" width="34" height="62" rx="8" fill="#09090B" stroke="#55505C" stroke-width="2"/>
                  <g clip-path="url(#cHp)"><g id="fHpFeed"><rect x="-2" y="-29" width="26" height="24" fill="#FF6A3D"/><rect x="-2" y="-5" width="26" height="24" fill="#7B2CBF"/><rect x="-2" y="19" width="26" height="24" fill="#00C2A8"/><rect x="-2" y="43" width="26" height="24" fill="#FFC93C"/><rect x="-2" y="67" width="26" height="24" fill="#FF6A3D"/><rect x="-2" y="91" width="26" height="24" fill="#7B2CBF"/></g></g></g>
              </g>'''

def torso(c):
    d = "M-38,8 C-52,-36 -50,-104 -34,-140 Q-22,-162 0,-162 Q24,-162 33,-146 C46,-114 48,-52 40,8 Q0,24 -38,8 Z"
    s = f'<path d="M-32,-132 Q-50,-152 -32,-168 Q-10,-178 10,-162 Q-12,-152 -32,-132 Z" fill="#8F8677"/>'
    s += f'<path d="{d}" fill="url(#{c["g"]})"/><path d="{d}" fill="url(#pFleece)"/>'
    s += f'<path d="M-38,8 C-52,-36 -50,-104 -34,-140 Q-28,-152 -18,-158 C-28,-110 -26,-44 -14,16 Q-28,14 -38,8 Z" fill="{c["deep"]}" opacity=".2"/>'
    s += '<ellipse cx="6" cy="-96" rx="15" ry="36" fill="#3F3A33" opacity=".2"/>'
    s += fold("M40,-22 Q22,-10 4,-15", c, 2.6, .5) + fold("M41,-44 Q27,-36 12,-41", c, 2.2, .4) + fold("M-40,-30 Q-26,-22 -12,-27", c, 2.4, .45)
    s += fold("M16,-122 C24,-92 12,-62 22,-34", c, 2, .28) + fold("M-22,-112 C-30,-82 -20,-52 -28,-22", c, 2, .3)
    s += f'<path d="M-8,-152 Q12,-142 26,-118" fill="none" stroke="{c["fold"]}" stroke-width="1.3" opacity=".5"/>'
    # poche kangourou
    s += f'<path d="M10,-58 L38,-64 L42,-16 L8,-9 Z" fill="{c["deep"]}" fill-opacity=".1" stroke="{c["fold"]}" stroke-width="1.4" stroke-linejoin="round" opacity=".75"/>'
    s += f'<path d="M36,-60 L41,-20" stroke="{c["deep"]}" stroke-width="3.2" stroke-linecap="round" opacity=".5"/>'
    # bord-côte du bas
    s += f'<g id="fHoodHem"><path d="M-39,1 Q0,16 41,1 L40,17 Q0,32 -38,17 Z" fill="#B0A693"/>'
    s += "".join(f'<path d="M{x},{4+ (1-(x/40)**2)*11:.1f} v13" stroke="{c["fold"]}" stroke-width="1" opacity=".5"/>' for x in range(-34, 40, 6))
    s += f'<path d="M-39,1 Q0,16 41,1" fill="none" stroke="{c["deep"]}" stroke-width="2.2" opacity=".4"/></g>'
    s += rim("M-36,-136 C-51,-104 -53,-40 -40,2", "rimS", SUN, 7, 1) + rim("M34,-142 C47,-112 49,-54 42,0", w=7)
    # cordons : ils pendent toujours vers le bas et se balancent
    for i, (x, y, L) in enumerate(((17, -138, 36), (25, -132, 30))):
        s += (f'<g transform="translate({x},{y})"><g class="fStr"><path d="M0,0 Q2.5,{L*.5} 0,{L}" fill="none" stroke="#F2ECDD" stroke-width="2.2" stroke-linecap="round"/>'
              f'<rect x="-1.8" y="{L-1}" width="3.6" height="7" rx="1.3" fill="#8E897E"/></g></g>')
    return s

def head():
    shell = "M-34,0 C-54,-34 -50,-92 -8,-104 C24,-112 47,-94 49,-71 C41,-77 31,-75 23,-65 C13,-51 11,-27 17,-4 Q-10,10 -34,0 Z"
    s = '<path d="M-34,0 C-54,-34 -50,-92 -8,-104 C24,-112 47,-94 49,-71 L42,-30 L22,-2 Q-8,10 -34,0 Z" fill="#2A2621"/>'      # intérieur de la capuche
    s += '<rect x="-6" y="-22" width="24" height="26" rx="8" fill="#A9795C"/>'
    s += '<path d="M10,-78 C30,-80 39,-68 39,-57 L45,-45 Q46,-40 40,-39 L40,-33 Q41,-21 29,-17 C18,-13 6,-17 2,-26 Z" fill="url(#gSkin)"/>'
    s += '<path d="M12,-78 C27,-82 38,-72 39,-60 C31,-67 22,-69 12,-66 Z" fill="#1B1512"/>'
    s += '<path id="fBrow" d="M25,-58 L36,-56" stroke="#1B1512" stroke-width="3.2" stroke-linecap="round"/>'
    s += '<g transform="translate(31,-49)"><g id="fEye"><ellipse rx="2.7" ry="3.7" fill="#17110E"/></g></g>'
    s += '<path d="M39,-42 Q43,-41 41,-38" fill="none" stroke="#8F5E44" stroke-width="1.3" stroke-linecap="round" opacity=".7"/>'
    s += '<path id="fMouth" d="M30,-30 Q35,-28 39,-31" stroke="#7A4334" stroke-width="2.6" fill="none" stroke-linecap="round"/>'
    s += '<ellipse id="fMouthO" cx="36" cy="-28" rx="3.6" ry="5" fill="#5A2A20" opacity="0"/>'
    # ombre portée de la capuche sur le haut du visage
    s += '<path d="M10,-78 C30,-80 39,-68 39,-57 L38,-51 Q24,-54 9,-44 Z" fill="#120E0B" opacity=".42"/>'
    s += '<path d="M2,-26 C6,-17 18,-13 29,-17 L27,-24 Q14,-20 8,-34 Z" fill="#120E0B" opacity=".25"/>'
    s += '<circle id="fFaceGlow" cx="34" cy="-40" r="44" fill="url(#gPhone)" opacity="0"/>'
    s += f'<path d="{shell}" fill="url(#gHood)"/><path d="{shell}" fill="url(#pFleece)"/>'
    s += '<path d="M-34,0 C-54,-34 -50,-92 -8,-104 C-30,-84 -34,-36 -22,6 Z" fill="#3F3A33" opacity=".22"/>'
    s += fold("M-34,-32 Q-18,-64 12,-90", HOOD, 2.4, .38) + fold("M-22,-8 Q-6,-20 10,-18", HOOD, 2.2, .4)
    # ourlet épais de l'ouverture
    s += '<path d="M49,-71 C41,-77 31,-75 23,-65 C13,-51 11,-27 17,-4" fill="none" stroke="#3F3A33" stroke-width="7" stroke-linecap="round" opacity=".35" transform="translate(-3,1)"/>'
    s += '<path d="M49,-71 C41,-77 31,-75 23,-65 C13,-51 11,-27 17,-4" fill="none" stroke="#E9E2D2" stroke-width="4.6" stroke-linecap="round"/>'
    s += rim("M-45,-28 C-51,-64 -35,-96 -8,-104", "rimS", SUN, 7, 1) + rim("M-2,-105 C24,-112 45,-96 49,-73", w=6)
    s += rim("M49,-71 C41,-77 31,-75 23,-65 C13,-51 11,-27 17,-4", w=4, o=.7)
    return s

def chair():
    return '''<g id="fChair" transform="translate(540,520)">
        <path id="fLongSh" d="M-70,166 L60,166 L420,182 L190,190 Z" fill="#000" opacity=".3"/>
        <ellipse cx="0" cy="172" rx="120" ry="15" fill="url(#gShadow)"/>
        <path d="M0,36 V150" stroke="#2B2830" stroke-width="12"/><path d="M4,40 V148" stroke="#4A4650" stroke-width="2" opacity=".6"/>
        <path d="M-54,158 Q0,136 54,158" stroke="#2B2830" stroke-width="10" fill="none" stroke-linecap="round"/>
        <g class="fWheel" transform="translate(-54,161)"><circle r="9" fill="#2B2830"/><path d="M-5,0 H5" stroke="#0C0B0E" stroke-width="2.5"/></g>
        <g class="fWheel" transform="translate(0,162)"><circle r="9" fill="#2B2830"/><path d="M-5,0 H5" stroke="#0C0B0E" stroke-width="2.5"/></g>
        <g class="fWheel" transform="translate(54,161)"><circle r="9" fill="#2B2830"/><path d="M-5,0 H5" stroke="#0C0B0E" stroke-width="2.5"/></g>
        <g transform="translate(-54,24)"><g id="fBack"><path d="M0,4 C-12,-60 -10,-130 4,-184" fill="none" stroke="#2B2830" stroke-width="26" stroke-linecap="round"/>
          <path d="M-6,-10 C-16,-64 -14,-126 -2,-176" fill="none" stroke="#17151A" stroke-width="8" stroke-linecap="round" opacity=".6"/>
          <g class="rimS" stroke="#FFB070" fill="none" stroke-linecap="round"><path d="M-11,-6 C-22,-62 -20,-128 -8,-180" stroke-width="3" opacity=".55"/></g>
          <g class="rim" stroke="#9DB7FF" fill="none" stroke-linecap="round"><path d="M10,-6 C-1,-62 1,-128 14,-178" stroke-width="3" opacity=".35"/></g></g></g>
        <rect x="-66" y="16" width="136" height="24" rx="12" fill="#2B2830"/><rect x="-66" y="30" width="136" height="10" rx="5" fill="#17151A" opacity=".6"/>
        <g class="rim" stroke="#9DB7FF" fill="none" stroke-linecap="round"><path d="M-52,18.5 H58" stroke-width="3" opacity=".3"/></g>
      </g>'''

def guy():
    return f'''<g id="fGuy" transform="translate(540,520)"><g id="fSquash">
        <g id="fThighF" transform="rotate(-78)">{thigh(JEANF, True)}
          <g transform="translate(0,130)"><g id="fShinF" transform="rotate(80)">{shin(JEANF, True)}</g></g></g>
        <g class="fTorso" transform="rotate(8)">
          <g transform="translate(-4,-132)"><g id="fUArmF" transform="rotate(-40)">{uarm(HOODF, True)}
            <g transform="translate(0,85)"><g id="fLArmF" transform="rotate(-48)">{larm(HOODF, True)}</g></g></g></g>
          {torso(HOOD)}
          <g transform="translate(2,-152)"><g id="fHead" transform="rotate(-3)">{head()}</g></g>
        </g>
        <g id="fThigh" transform="rotate(-82)">{thigh(JEAN)}
          <g transform="translate(0,130)"><g id="fShin" transform="rotate(82)">{shin(JEAN)}</g></g></g>
        <g class="fTorso" transform="rotate(8)">
          <g transform="translate(2,-134)"><g id="fUArm" transform="rotate(-47)">{uarm(HOOD)}
            <g transform="translate(0,85)"><g id="fLArm" transform="rotate(-37)">{larm(HOOD, False, PHONE)}</g></g></g></g>
        </g>
      </g></g>'''

DEFS = '''<linearGradient id="gHood" x1="0" x2="1"><stop offset="0" stop-color="#7A7265"/><stop offset=".5" stop-color="#B5AB98"/><stop offset="1" stop-color="#DAD1BF"/></linearGradient>
    <linearGradient id="gHoodF" x1="0" x2="1"><stop offset="0" stop-color="#4A453D"/><stop offset="1" stop-color="#857D6F"/></linearGradient>
    <linearGradient id="gJean" x1="0" x2="1"><stop offset="0" stop-color="#2B4274"/><stop offset=".5" stop-color="#4E72B6"/><stop offset="1" stop-color="#8BABE2"/></linearGradient>
    <linearGradient id="gJeanF" x1="0" x2="1"><stop offset="0" stop-color="#1A2746"/><stop offset="1" stop-color="#3A558C"/></linearGradient>
    <linearGradient id="gSkin" x1="0" x2="1"><stop offset="0" stop-color="#A9795C"/><stop offset="1" stop-color="#DBA886"/></linearGradient>
    <linearGradient id="gShoe" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#EFE9DC"/><stop offset="1" stop-color="#CFC8B8"/></linearGradient>
    <pattern id="pDenim" width="3.2" height="3.2" patternUnits="userSpaceOnUse" patternTransform="rotate(38)"><path d="M0,.8 H3.2" stroke="#fff" stroke-opacity=".10" stroke-width=".8"/><path d="M0,2.4 H3.2" stroke="#0B1020" stroke-opacity=".10" stroke-width=".8"/></pattern>
    <pattern id="pFleece" width="2.6" height="2.6" patternUnits="userSpaceOnUse" patternTransform="rotate(24)"><circle cx=".7" cy=".7" r=".45" fill="#fff" fill-opacity=".09"/><circle cx="2" cy="2" r=".45" fill="#2A2520" fill-opacity=".09"/></pattern>'''
