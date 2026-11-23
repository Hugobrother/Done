# Génère film.html v3 : scène + étalonnage + sources de lumière + gros plan téléphone
import random, sys, os
HERE=os.path.dirname(os.path.abspath(__file__))+"/"
sys.path.insert(0, HERE)
import guy as G
random.seed(7)
KW,FN,ST,VA,CO,GR="#C792EA","#82AAFF","#F0A983","#D6D9E8","#5C6078","#9BD5A6"
FONT="font-family=\"'Space Grotesk',system-ui,sans-serif\""

def code_lines():
    out=[]
    spec=[(0,[(KW,14),(FN,22),(VA,6)]),(1,[(KW,10),(VA,18),(ST,24)]),(1,[(VA,12),(FN,20),(VA,10)]),
     (2,[(KW,8),(VA,22)]),(1,[(CO,44)]),(1,[(KW,12),(FN,16),(ST,18),(VA,6)]),(0,[(VA,5)]),
     (0,[(KW,14),(FN,28),(VA,6)]),(1,[(KW,10),(VA,14),(FN,22)]),(1,[(KW,6),(VA,20),(ST,26)]),
     (2,[(FN,18),(VA,12),(ST,20)]),(2,[(KW,12),(VA,26)]),(1,[(VA,10),(FN,24)]),(1,[(KW,12),(ST,30)]),(0,[(VA,5)])]
    for i,(ind,toks) in enumerate(spec):
        y=262+i*8.6; x=858+ind*7; new=i>=7
        g=[f'<rect x="851" y="{y:.1f}" width="3" height="3" rx="1" fill="#2A2C3A"/>']
        if new: g.append(f'<rect x="847.5" y="{y-1.5:.1f}" width="1.6" height="6" fill="{GR}"/>')
        for c,w in toks:
            g.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="3.2" rx="1.6" fill="{c}"/>'); x+=w+3
        out.append(f'<g class="{"fNew" if new else "fOld"}">'+"".join(g)+'</g>')
    return "\n        ".join(out)

def sidebar():
    ws=[20,24,18,22,16,24,19,21,17,23,15]
    r=['<rect x="814" y="275.5" width="30" height="8" rx="2" fill="#232532"/>']
    for i,w in enumerate(ws):
        r.append(f'<rect x="{817+(4 if i%3 else 0)}" y="{262+i*8:.0f}" width="{w}" height="3" rx="1.5" fill="{"#8A8FAD" if i==2 else "#3A3D52"}"/>')
    return "".join(r)

def motes():
    r=[]
    for i in range(14):
        x=random.uniform(250,980); y=random.uniform(170,640); rad=random.uniform(1.2,2.4)
        r.append(f'<circle class="fMote" cx="{x:.0f}" cy="{y:.0f}" r="{rad:.1f}" fill="#FFE2C4" opacity="{random.uniform(.15,.45):.2f}"/>')
    return "".join(r)

SVG=f'''<div id="flive"><svg id="film-svg" viewBox="0 0 1200 760" aria-hidden="true">
  <defs>
    <linearGradient id="gSkyDay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4A5CA0"/><stop offset=".55" stop-color="#D98474"/><stop offset="1" stop-color="#FFB56A"/></linearGradient>
    <linearGradient id="gSkyNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0B1030"/><stop offset="1" stop-color="#2A3266"/></linearGradient>
    <linearGradient id="gRay" gradientUnits="userSpaceOnUse" x1="200" y1="100" x2="820" y2="700"><stop offset="0" stop-color="#FF9E55" stop-opacity=".42"/><stop offset=".65" stop-color="#FF9E55" stop-opacity=".12"/><stop offset="1" stop-color="#FF9E55" stop-opacity="0"/></linearGradient>
    <linearGradient id="gCone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFC98A" stop-opacity=".42"/><stop offset=".55" stop-color="#FFC98A" stop-opacity=".1"/><stop offset="1" stop-color="#FFC98A" stop-opacity="0"/></linearGradient>
    <linearGradient id="gSpill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7C9CFF" stop-opacity=".4"/><stop offset="1" stop-color="#7C9CFF" stop-opacity="0"/></linearGradient>
    <linearGradient id="gSpillW" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FF9E6E" stop-opacity=".42"/><stop offset="1" stop-color="#FF9E6E" stop-opacity="0"/></linearGradient>
    <linearGradient id="gCar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFEBC2" stop-opacity="0"/><stop offset=".3" stop-color="#FFEBC2" stop-opacity=".13"/><stop offset="1" stop-color="#FFEBC2" stop-opacity="0"/></linearGradient>
    <linearGradient id="gWall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4E4A50"/><stop offset="1" stop-color="#5A5350"/></linearGradient>
    <linearGradient id="gFloor" gradientUnits="userSpaceOnUse" x1="0" y1="690" x2="0" y2="1300"><stop offset="0" stop-color="#3A3230"/><stop offset="1" stop-color="#1D1918"/></linearGradient>
    <linearGradient id="gDeskTop" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8A6248"/><stop offset="1" stop-color="#6B4A36"/></linearGradient>
    <linearGradient id="gGloss" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".07"/><stop offset=".45" stop-color="#fff" stop-opacity="0"/></linearGradient>
    <radialGradient id="gCool"><stop offset="0" stop-color="#7C9CFF" stop-opacity=".34"/><stop offset=".45" stop-color="#7C9CFF" stop-opacity=".11"/><stop offset="1" stop-color="#7C9CFF" stop-opacity="0"/></radialGradient>
    <radialGradient id="gWarm"><stop offset="0" stop-color="#FFA873" stop-opacity=".36"/><stop offset=".45" stop-color="#FFA873" stop-opacity=".11"/><stop offset="1" stop-color="#FFA873" stop-opacity="0"/></radialGradient>
    <radialGradient id="gLampA"><stop offset="0" stop-color="#FFC58A" stop-opacity=".2"/><stop offset=".5" stop-color="#FFC58A" stop-opacity=".06"/><stop offset="1" stop-color="#FFC58A" stop-opacity="0"/></radialGradient>
    <radialGradient id="gLampP"><stop offset="0" stop-color="#FFD9A8" stop-opacity=".55"/><stop offset="1" stop-color="#FFD9A8" stop-opacity="0"/></radialGradient>
    <radialGradient id="gLed"><stop offset="0" stop-color="#FF6A3A" stop-opacity=".5"/><stop offset="1" stop-color="#FF6A3A" stop-opacity="0"/></radialGradient>
    <radialGradient id="gPhone"><stop offset="0" stop-color="#DCE6FF" stop-opacity=".6"/><stop offset=".4" stop-color="#DCE6FF" stop-opacity=".18"/><stop offset="1" stop-color="#DCE6FF" stop-opacity="0"/></radialGradient>
    <radialGradient id="gFlash"><stop offset="0" stop-color="#FFE7D3" stop-opacity=".95"/><stop offset=".25" stop-color="#FF9B66" stop-opacity=".6"/><stop offset="1" stop-color="#FF9B66" stop-opacity="0"/></radialGradient>
    <radialGradient id="gShadow"><stop offset="0" stop-color="#000" stop-opacity=".6"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
    <radialGradient id="gSunPool"><stop offset="0" stop-color="#FF9E55" stop-opacity=".34"/><stop offset="1" stop-color="#FF9E55" stop-opacity="0"/></radialGradient>
    {G.DEFS}
    <clipPath id="cWin"><rect x="110" y="96" width="250" height="210" rx="6"/></clipPath>
    <clipPath id="cHp"><rect x="-2" y="-29" width="26" height="52" rx="5"/></clipPath>
    <clipPath id="cMon"><rect x="812" y="244" width="246" height="156" rx="4"/></clipPath>
    <clipPath id="cT1"><rect id="fT1" x="986" y="0" width="70" height="800"/></clipPath>
    <clipPath id="cT2"><rect id="fT2" x="986" y="0" width="70" height="800"/></clipPath>
  </defs>

  <g id="fCam">
    <!-- ================= arrière-plan (parallaxe lointaine) ================= -->
    <g id="fBg">
      <rect x="-4000" y="-4000" width="9200" height="4690" fill="url(#gWall)"/>
      <rect x="-4000" y="690" width="9200" height="4000" fill="url(#gFloor)"/>
      <rect x="-4000" y="678" width="9200" height="13" fill="#6A625C"/><rect x="-4000" y="678" width="9200" height="2" fill="#8A8178"/>
      <!-- fenêtre -->
      <rect x="110" y="96" width="250" height="210" rx="6" fill="url(#gSkyDay)"/>
      <g clip-path="url(#cWin)">
        <circle id="fSun" cx="292" cy="250" r="30" fill="#FFF0C0"/>
        <rect id="fNightSky" x="110" y="96" width="250" height="210" fill="url(#gSkyNight)" opacity="0"/>
        <g id="fStars" fill="#F3EEE6" opacity="0"><circle cx="150" cy="118" r="1.6"/><circle cx="238" cy="130" r="1.3"/><circle cx="318" cy="112" r="1.8"/><circle cx="276" cy="162" r="1.2"/><circle cx="182" cy="176" r="1.1"/><circle cx="336" cy="188" r="1.4"/><circle cx="130" cy="210" r="1.2"/></g>
        <circle id="fMoon" cx="196" cy="150" r="13" fill="#F2F4FF" opacity="0"/>
        <g id="fClouds" fill="#FFE9D6" opacity=".28"><ellipse cx="170" cy="150" rx="46" ry="11"/><ellipse cx="200" cy="143" rx="30" ry="11"/><ellipse cx="320" cy="196" rx="52" ry="10"/><ellipse cx="60" cy="210" rx="40" ry="9"/></g>
        <path d="M110,306 V268 h26 v-22 h22 v30 h30 v-46 h24 v38 h34 v-20 h26 v34 h30 v-28 h28 v42 Z" fill="#17141C"/>
        <g id="fCity" fill="#FFD9A0" opacity="0"><rect x="142" y="254" width="4" height="5"/><rect x="150" y="262" width="4" height="5"/><rect x="196" y="236" width="4" height="5"/><rect x="204" y="250" width="4" height="5"/><rect x="262" y="262" width="4" height="5"/><rect x="330" y="284" width="4" height="5"/><rect x="296" y="278" width="4" height="5"/></g>
      </g>
      <rect x="110" y="96" width="250" height="210" rx="6" fill="none" stroke="#2B2729" stroke-width="10"/>
      <path d="M235,96 V306 M110,201 H360" stroke="#2B2729" stroke-width="6"/>
      <rect x="96" y="304" width="278" height="12" rx="3" fill="#2B2729"/>
      <path d="M100,304 H370" stroke="#FFB678" stroke-width="2" opacity=".7" id="fSill"/>
      <!-- horloge -->
      <g transform="translate(1085,150)">
        <ellipse cx="5" cy="7" rx="46" ry="46" fill="#000" opacity=".25"/>
        <circle r="46" fill="#2B2729"/><circle r="39" fill="#EFE9DC"/>
        <g stroke="#A9A294" stroke-width="3" stroke-linecap="round"><path d="M0,-33 V-28"/><path d="M33,0 H28"/><path d="M0,33 V28"/><path d="M-33,0 H-28"/></g>
        <g id="fHour"><path d="M0,3 V-19" stroke="#2B2729" stroke-width="5" stroke-linecap="round"/></g>
        <g id="fMin"><path d="M0,4 V-30" stroke="#D97757" stroke-width="3.5" stroke-linecap="round"/></g>
        <circle r="4" fill="#2B2729"/>
      </g>
      <!-- cadres au mur -->
      <rect x="1196" y="116" width="120" height="150" rx="4" fill="#000" opacity=".22"/>
      <rect x="1190" y="110" width="120" height="150" rx="4" fill="#33303A" stroke="#77706A" stroke-width="5"/><circle cx="1250" cy="170" r="26" fill="#D97757"/><rect x="1212" y="214" width="76" height="8" rx="4" fill="#77706A"/>
      <rect x="-150" y="150" width="150" height="110" rx="4" fill="#33303A" stroke="#77706A" stroke-width="5"/><path d="M-130,240 l40,-50 l30,30 l24,-22 l26,42 Z" fill="#77706A"/>
    </g>

    <!-- ================= plan principal ================= -->
    <g id="fMid">
      <path d="M806,-4000 V92" stroke="#1B191E" stroke-width="4"/>
      <path d="M758,138 Q806,56 854,138 Z" fill="#2E2B33"/><path d="M764,134 Q806,66 848,134" fill="none" stroke="#6A6570" stroke-width="2.5"/>
      <!-- ombre du bureau sur le mur et au sol -->
      <ellipse cx="850" cy="700" rx="330" ry="22" fill="url(#gShadow)"/>
      <rect x="596" y="496" width="360" height="190" fill="#000" opacity=".22"/>
      <!-- bureau -->
      <g id="fDesk">
        <rect x="584" y="494" width="13" height="196" fill="#3B2B22"/>
        <rect x="952" y="494" width="166" height="196" rx="3" fill="#553D2E"/>
        <rect x="952" y="494" width="166" height="26" fill="#000" opacity=".22"/>
        <path d="M966,556 H1104 M966,622 H1104" stroke="#35251C" stroke-width="4"/>
        <rect x="1020" y="520" width="30" height="6" rx="3" fill="#A07A5C"/><rect x="1020" y="584" width="30" height="6" rx="3" fill="#A07A5C"/><rect x="1020" y="650" width="30" height="6" rx="3" fill="#A07A5C"/>
        <rect x="560" y="480" width="574" height="16" rx="4" fill="url(#gDeskTop)"/>
        <rect x="560" y="480" width="574" height="4" rx="2" fill="#B58A68" id="fDeskEdge"/>
        <!-- écran : pied, coque -->
        <ellipse cx="935" cy="482" rx="70" ry="4" fill="#000" opacity=".35"/>
        <rect x="924" y="412" width="22" height="62" fill="#2A272E"/><rect x="924" y="412" width="6" height="62" fill="#3C3842"/>
        <rect x="882" y="470" width="106" height="10" rx="5" fill="#34303A"/>
        <rect x="802" y="234" width="266" height="178" rx="9" fill="#141318" stroke="#4A4650" stroke-width="2.5"/>
        <!-- clavier, souris, tasse -->
        <rect x="640" y="470" width="124" height="10" rx="4" fill="#34303A"/><rect x="646" y="467" width="112" height="4" rx="2" fill="#565160"/><path d="M648,468 H756" stroke="#B9CBFF" stroke-width="1.2" opacity=".7"/>
        <ellipse cx="792" cy="475" rx="14" ry="6" fill="#34303A"/>
        <g id="fMug"><ellipse cx="1097" cy="481" rx="20" ry="3" fill="#000" opacity=".3"/><rect x="1080" y="448" width="30" height="32" rx="5" fill="#E4DED2"/><rect x="1080" y="448" width="9" height="32" rx="4" fill="#B4AEA2"/><path d="M1110,456 q14,2 14,10 q0,9 -14,10" fill="none" stroke="#E4DED2" stroke-width="5"/>
          <g id="fSteam" stroke="#F3EEE6" stroke-width="3" stroke-linecap="round" fill="none" opacity=".3"><path d="M1089,440 q-6,-10 0,-18 q6,-8 0,-18"/><path d="M1101,440 q6,-10 0,-18 q-6,-8 0,-18"/></g></g>
        <g id="fDeskPhone"><rect x="590" y="471" width="44" height="9" rx="4" fill="#141318" stroke="#6A6570" stroke-width="1.5"/></g>
      </g>
      <!-- plante -->
      <g transform="translate(1160,690)">
        <ellipse cx="0" cy="4" rx="46" ry="8" fill="#000" opacity=".35"/>
        <g stroke="#2F5A40" stroke-width="9" stroke-linecap="round" fill="none"><path d="M0,-52 Q-34,-110 -50,-150"/><path d="M0,-52 Q4,-120 16,-176"/><path d="M0,-52 Q34,-100 60,-128"/></g>
        <g fill="#3F7A56"><ellipse cx="-52" cy="-154" rx="14" ry="26" transform="rotate(-24 -52 -154)"/><ellipse cx="17" cy="-182" rx="14" ry="28" transform="rotate(8 17 -182)"/><ellipse cx="63" cy="-132" rx="13" ry="24" transform="rotate(46 63 -132)"/></g>
        <path d="M-30,-56 H30 L22,0 H-22 Z" fill="#6A6570"/><path d="M-30,-56 H-10 L-12,0 H-22 Z" fill="#000" opacity=".2"/>
      </g>
      {G.chair()}
      {G.guy()}
    </g>

    <!-- ================= étalonnage : assombrit et teinte TOUTE la scène (soir → nuit) ================= -->
    <rect id="fGrade" x="-4000" y="-4000" width="9200" height="8700" fill="#EDB08A" opacity=".42" style="mix-blend-mode:multiply"/>

    <!-- ================= lumière : s'additionne à l'image comme une vraie source ================= -->
    <g id="fLights">
      <g id="fRays"><path d="M118,104 L232,104 L770,700 L500,700 Z" fill="url(#gRay)"/><path d="M240,104 L352,104 L980,700 L730,700 Z" fill="url(#gRay)"/>
        <ellipse cx="740" cy="704" rx="300" ry="26" fill="url(#gSunPool)"/><ellipse cx="235" cy="200" rx="230" ry="190" fill="url(#gSunPool)" opacity=".6"/></g>
      <g id="fCar" opacity="0" fill="url(#gCar)"><path d="M0,60 h150 l130,640 h-200 Z"/><path d="M178,60 h150 l160,640 h-200 Z"/></g>
      <g id="fLampOn" opacity="0">
        <path d="M762,138 L850,138 L1060,690 L560,690 Z" fill="url(#gCone)"/>
        <ellipse cx="880" cy="482" rx="170" ry="8" fill="url(#gLampP)" opacity=".7"/>
        <ellipse cx="806" cy="300" rx="300" ry="250" fill="url(#gLampA)"/>
        <ellipse cx="806" cy="696" rx="250" ry="18" fill="url(#gLampP)" opacity=".5"/>
      </g>
      <ellipse id="fMonCool" cx="935" cy="322" rx="360" ry="270" fill="url(#gCool)"/>
      <ellipse id="fMonWarm" cx="935" cy="322" rx="360" ry="270" fill="url(#gWarm)" opacity="0"/>
      <path id="fSpill" d="M812,414 L1058,414 L1126,480 L700,480 Z" fill="url(#gSpill)"/>
      <path id="fSpillW" d="M812,414 L1058,414 L1126,480 L700,480 Z" fill="url(#gSpillW)" opacity="0"/>
      <ellipse id="fLed" cx="770" cy="590" rx="230" ry="110" fill="url(#gLed)" opacity=".5"/>
      <ellipse id="fLedFloor" cx="770" cy="700" rx="240" ry="14" fill="#FF7A4A" opacity=".25"/>
    </g>
    <!-- ================= ce qui émet de la lumière (jamais assombri) ================= -->
    <g id="fEmis">
      <rect x="812" y="244" width="246" height="156" rx="4" fill="#12131A"/>
      <g clip-path="url(#cMon)" id="fIde">
        <rect x="812" y="244" width="246" height="12" fill="#1A1B24"/>
        <circle cx="819" cy="250" r="1.9" fill="#FF6B5E"/><circle cx="825.5" cy="250" r="1.9" fill="#F5BF4F"/><circle cx="832" cy="250" r="1.9" fill="#61C454"/>
        <rect x="842" y="246.5" width="36" height="7" rx="2" fill="#262838"/><rect x="846" y="249" width="20" height="2.4" rx="1.2" fill="#8A8FAD"/>
        <rect x="881" y="246.5" width="32" height="7" rx="2" fill="#171821"/><rect x="885" y="249" width="18" height="2.4" rx="1.2" fill="#4A4E66"/>
        <rect x="812" y="256" width="35" height="144" fill="#151620"/>
        {sidebar()}
        <rect x="976" y="256" width="82" height="144" fill="#171821"/><path d="M976.3,256 V400" stroke="#262838" stroke-width=".8"/>
        {code_lines()}
        <rect id="fCaretCode" x="868" y="312" width="1.2" height="6" fill="#D6D9E8"/>
        <rect x="982" y="261" width="7" height="7" rx="2" fill="#D97757"/>
        <text x="992" y="267.2" {FONT} font-weight="700" font-size="5.6" fill="#D6D9E8">Claude</text>
        <rect x="981" y="366" width="73" height="28" rx="6" fill="#12131A" stroke="#2E3144" stroke-width=".8"/>
        <rect x="1042" y="382" width="8" height="8" rx="2.5" fill="#D97757" id="fSend"/>
        <g id="fPrompt">
          <rect id="fPromptBg" x="983" y="274" width="70" height="22" rx="5" fill="#262838"/>
          <text clip-path="url(#cT1)" x="987" y="283" {FONT} font-size="5" fill="#E6E8F2">Refactor the auth</text>
          <text clip-path="url(#cT2)" x="987" y="290.6" {FONT} font-size="5" fill="#E6E8F2">module + add tests</text>
          <rect id="fCaret" x="987" y="278.4" width=".9" height="5.6" fill="#D97757" opacity="0"/>
        </g>
        <g id="fThink" opacity="0"><circle cx="986" cy="308" r="1.8" fill="#8A8FAD"/><circle cx="992" cy="308" r="1.8" fill="#8A8FAD"/><circle cx="998" cy="308" r="1.8" fill="#8A8FAD"/>
          <rect x="983" y="316" width="58" height="3.4" rx="1.7" fill="#2A2C3A"/><rect x="983" y="323" width="42" height="3.4" rx="1.7" fill="#2A2C3A"/>
          <text x="1004" y="310" {FONT} font-size="4.6" fill="#7C8099">Thinking…</text></g>
        <g id="fTodo" {FONT} font-size="4.7" fill="#D6D9E8">
          <g class="fTick"><circle cx="986.5" cy="307" r="3" fill="{GR}"/><path d="M985,307 l1.2,1.3 l2,-2.4" fill="none" stroke="#12131A" stroke-width="1"/><text x="993" y="308.7">auth.ts refactored</text></g>
          <g class="fTick"><circle cx="986.5" cy="317" r="3" fill="{GR}"/><path d="M985,317 l1.2,1.3 l2,-2.4" fill="none" stroke="#12131A" stroke-width="1"/><text x="993" y="318.7">auth.test.ts added</text></g>
          <g class="fTick"><circle cx="986.5" cy="327" r="3" fill="{GR}"/><path d="M985,327 l1.2,1.3 l2,-2.4" fill="none" stroke="#12131A" stroke-width="1"/><text x="993" y="328.7">12 tests passed</text></g>
        </g>
        <rect x="812" y="244" width="246" height="156" fill="url(#gGloss)"/>
      </g>
      <g id="fCheck" transform="translate(806,238)"><circle r="20" fill="#D97757"/><path d="M-9,0 L-3,7 L10,-7" fill="none" stroke="#141413" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/></g>
      <path d="M724,497.500 H948" stroke="#FF7A4A" stroke-width="3" stroke-linecap="round" id="fLedStrip"/>
      <ellipse id="fBulb" cx="806" cy="139" rx="46" ry="6.5" fill="#57504A"/>
    </g>

    <g id="fLights2">
      <circle id="fPhoneLight" r="120" fill="url(#gPhone)" opacity="0"/>
      <g id="fMotes">{motes()}</g>
      <circle id="fFlash" r="90" fill="url(#gFlash)" opacity="0"/>
      <g id="fRings" fill="none" stroke="#FFB48A" stroke-width="3" opacity="0"><circle class="fRing" r="30"/><circle class="fRing" r="30"/><circle class="fRing" r="30"/></g>
    </g>
    <circle id="fIris" cx="806" cy="238" r="20" fill="#D97757" opacity="0"/>
  </g>
</svg>
<!-- premier plan hors-focus (parallaxe forte) -->
<div id="ffg" aria-hidden="true"><svg viewBox="0 0 1200 760" preserveAspectRatio="none">
  <defs><radialGradient id="gSoft"><stop offset="0" stop-color="#050706"/><stop offset=".62" stop-color="#050706"/><stop offset="1" stop-color="#050706" stop-opacity="0"/></radialGradient>
  <linearGradient id="gSoftL" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#040405" stop-opacity="0"/><stop offset=".3" stop-color="#040405"/></linearGradient></defs>
  <g fill="url(#gSoft)"><ellipse cx="60" cy="640" rx="62" ry="176" transform="rotate(24 60 640)"/><ellipse cx="176" cy="706" rx="54" ry="168" transform="rotate(52 176 706)"/><ellipse cx="-24" cy="552" rx="56" ry="156" transform="rotate(-8 -24 552)"/><ellipse cx="110" cy="776" rx="80" ry="150" transform="rotate(70 110 776)"/></g>
  <rect x="1236" y="-400" width="560" height="1600" fill="url(#gSoftL)"/>
</svg></div>
__POV__
<div id="fflashHtml" aria-hidden="true"></div></div>
<video id="fvid" muted playsinline preload="auto" disablepictureinpicture disableremoteplayback tabindex="-1" aria-hidden="true"></video>
<div class="fvig" aria-hidden="true"></div>
<div class="fgrain" aria-hidden="true"></div>
<div class="fbarT" id="fbarT" aria-hidden="true"></div>
<div class="fbarB" id="fbarB" aria-hidden="true"></div>
'''
pov = open(HERE+"pov.html").read()
open(HERE+"film.html","w").write(SVG.replace("__POV__", pov))
print("film.html", len(SVG))
