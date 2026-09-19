#!/usr/bin/env python3
"""Render the static portfolio. No third-party build dependencies.
Edit PROJECTS/EXPERIENCES/CAPABILITIES and CONTACT, then run this file.
Original company CAD/test images have not been supplied. Illustrations are labeled.
"""
from pathlib import Path
from html import escape as esc
import json, shutil

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT/'content/portfolio.json').read_text())
CONTACT = DATA['contact']
PROJECTS = DATA['projects']
EXPERIENCES = DATA['experiences']
CAPABILITIES = DATA['capabilities']

def svg_base(title,content):
 return f'<svg viewBox="0 0 800 440" role="img" aria-label="{esc(title)}" xmlns="http://www.w3.org/2000/svg"><defs><pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#223141" stroke-width=".5"/></pattern><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="none" stroke="#98bfdc"/></marker></defs><rect width="800" height="440" fill="#0d151e"/><rect x="25" y="25" width="750" height="390" fill="url(#grid)"/><g font-family="monospace" font-size="15" fill="#b5c9d9" stroke-width="1.5">{content}</g></svg>'

def diagram(kind):
 if kind=='mesh':
  c='<text x="45" y="55" font-size="13">MESH STUDY / C3D10M</text>'
  for n,(step,label) in enumerate([(30,'4 mm'),(20,'2 mm'),(15,'1.5 mm'),(10,'1 mm')]):
   x=45+n*190;c+=f'<rect x="{x}" y="100" width="140" height="140" fill="none" stroke="'+('#a8d6f2' if n==1 else '#435365')+'"/>'
   for i in range(step,140,step):
    c+=f'<path d="M{x+i} 100V240 M{x} {100+i}H{x+140}" fill="none" stroke="#55728a" stroke-width=".65"/>'
   c+=f'<text x="{x}" y="275" font-size="23">{label}</text>'
   if n==1:c+=f'<text x="{x}" y="304" fill="#a8d6f2" font-size="12">SELECTED</text>'
  c+='<path d="M45 333H755" stroke="#384b5b"/><text x="45" y="373" font-size="19">1.11% response difference</text><text x="470" y="373" font-size="19">~4× faster runtime</text>'
  return svg_base('Schematic of four mesh sizes. Selected 2 millimeter mesh was within 1.11 percent of converged response with about four times faster runtime.',c)
 if kind in ('loop','automation'):
  labels=['ATTITUDE','PID','PWM / MOTOR','BODY'] if kind=='loop' else ['SENSOR','PLC LOGIC','ACTUATOR','PROCESS']
  c='<text x="45" y="65" font-size="13">'+('CLOSED-LOOP CONTROL / CONCEPTUAL SIGNAL FLOW' if kind=='loop' else 'AUTOMATION / CONCEPTUAL SIGNAL FLOW')+'</text>'
  for i,t in enumerate(labels):
   x=45+i*190;c+=f'<rect x="{x}" y="155" width="145" height="80" fill="#131f2b" stroke="#6588a3"/><text x="{x+72}" y="201" text-anchor="middle" font-size="14">{t}</text>'
   if i<3:c+=f'<path d="M{x+146} 195H{x+180}" stroke="#98bfdc" marker-end="url(#arrow)"/>'
  c+='<path d="M687 237V327H117V247" fill="none" stroke="#98bfdc" marker-end="url(#arrow)"/><text x="290" y="363" font-size="14">MEASURE / COMPARE / UPDATE</text>'
  return svg_base('Conceptual feedback loop connecting sensing, control, actuation and system behavior',c)
 if kind=='loadpath':
  c='<text x="45" y="60" font-size="13">DESIGN TRADE / LOAD PATH</text><text x="45" y="120" font-size="20">01  COMPLIANT CONCEPT</text><rect x="45" y="153" width="240" height="68" fill="#121e29" stroke="#6588a3"/><text x="165" y="192" text-anchor="middle">Assembly displacement</text><path d="M286 187H425" stroke="#98bfdc" marker-end="url(#arrow)"/><rect x="445" y="153" width="305" height="68" fill="#121e29" stroke="#6588a3"/><text x="596" y="192" text-anchor="middle">Interface reactions / moments</text><text x="45" y="280" font-size="20">02  REVISED CONCEPT</text><path d="M45 325H230 M245 325H490 M505 325H750" stroke="#b6d1e6" stroke-width="6"/><path d="M237 309V341 M498 309V341" stroke="#7f98ad"/><text x="45" y="385">Three-piece torque bar / controlled load transfer</text>'
  return svg_base('Conceptual load path comparison between flexure accommodation and revised three-piece torque bar',c)
 if kind=='balance':
  c='<text x="45" y="60" font-size="13">ONE-AXIS BALANCE / PROPOSED MODEL</text><path d="M200 350H640" stroke="#688094"/><path d="M400 340L325 353H475Z" fill="#253748"/><path d="M400 330L315 125" stroke="#adc8dc" stroke-width="4"/><path d="M400 330V105" stroke="#466579" stroke-dasharray="5 7"/><circle cx="315" cy="125" r="13" fill="#a8d6f2"/><path d="M315 145V245" stroke="#98bfdc" marker-end="url(#arrow)"/><text x="335" y="203">mg</text><text x="210" y="118">Center of mass</text><path d="M400 265Q380 265 375 275" fill="none" stroke="#a8d6f2"/><text x="369" y="250">θ</text><text x="465" y="157" font-size="23">τg = mgl sin θ</text><text x="465" y="196" font-size="14">Actuation to be selected</text><text x="465" y="222" font-size="14">Sensing  /  control  /  response</text><text x="45" y="394" font-size="12">SIMPLIFIED MODEL · NO MEASURED BALANCE RESULT YET</text>'
  return svg_base('Simplified proposed balancing model showing the center of mass, gravity force, angle and gravitational torque',c)
 if kind=='reel':
  c='<text x="45" y="60" font-size="13">REEL REDESIGN / COMPONENT RELATIONSHIPS</text>'
  labels=[('FLANGE','Stacking / handling'),('HUB','Location / interface'),('CLIP','Assembly / retention')]
  for i,(a,b) in enumerate(labels):
   x=55+i*245;c+=f'<rect x="{x}" y="135" width="200" height="160" fill="#121e29" stroke="#5e7f98"/><text x="{x+20}" y="176" font-size="12">0{i+1}</text><text x="{x+20}" y="215" font-size="23">{a}</text><text x="{x+20}" y="266" font-size="12">{b}</text>'
   if i<2:c+=f'<path d="M{x+201} 215H{x+233}" stroke="#98bfdc" marker-end="url(#arrow)"/>'
  c+='<text x="55" y="358" font-size="15">REVERSE ENGINEER  /  PROTOTYPE  /  DRAWING PACKAGE</text><text x="55" y="392" font-size="12">FUNCTIONAL DIAGRAM · NOT A MANUFACTURING DRAWING</text>'
  return svg_base('Functional component diagram of a manufacturing reel with flange, hub and clip',c)
 return ''

def tags(items):return '<div class="tags">'+''.join(f'<span class="tag">{esc(t)}</span>' for t in items)+'</div>'
def paras(items):return ''.join(f'<p>{esc(p)}</p>' for p in items)
def external(url,label,cls=''):return f'<a class="{cls}" href="{esc(url,quote=True)}" target="_blank" rel="noopener noreferrer">{label}<span aria-hidden="true"> </span></a>'
def nav(home=False):
 prefix='' if home else '/'
 return f'''<a class="skip" href="#main">Skip to content</a><header class="nav"><div class="wrap nav-inner"><a class="brand" href="/" aria-label="Rafael Ponce De Leon home">RP <span>//</span> ME</a><button class="menu-toggle" aria-expanded="false" aria-controls="nav-links">Menu</button><nav class="nav-links" id="nav-links" aria-label="Main navigation"><a href="{prefix}#work">Work</a><a href="/experience/">Experience</a><a href="{prefix}#about">About</a>{external(CONTACT['resume'],'Resume','resume-nav')}<a class="contact-nav" href="{prefix}#contact">Contact <span aria-hidden="true"></span></a></nav></div></header>'''
def footer():
 email=f'<a href="mailto:{esc(CONTACT["email"])}">Email </a>' if CONTACT['email'] else '<span class="unavailable">Email<small>Details to be added</small></span>'
 linkedin=external(CONTACT['linkedin'],'LinkedIn') if CONTACT['linkedin'] else '<span class="unavailable">LinkedIn<small>Profile link to be added</small></span>'
 return f'''<section class="contact" id="contact"><div class="wrap"><div class="eyebrow">THE NEXT CHALLENGE</div><h2>LET’S BUILD<br><span>SOMETHING.</span></h2><div class="contact-bottom"><p class="contact-sub">Interested in product development, precision hardware, and the engineering that makes a design work.</p><div class="contact-links">{email}{linkedin}{external(CONTACT['github'],'GitHub')}{external(CONTACT['resume'],'Resume')}</div></div><footer class="footer"><span>© 2026 RAFAEL PONCE DE LEON</span><span>DESIGN · SIMULATE · BUILD · TEST</span><a href="#main">BACK TO TOP </a></footer></div></section>'''
def page(title,description,content,home=False):
 import re
 counter=iter(range(100))
 def unique_svg(match):
  n=next(counter);return match.group(0).replace('id="grid"',f'id="grid-{n}"').replace('url(#grid)',f'url(#grid-{n})').replace('id="arrow"',f'id="arrow-{n}"').replace('url(#arrow)',f'url(#arrow-{n})')
 content=re.sub(r'<svg\b.*?</svg>',unique_svg,content,flags=re.S)
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#090b0e"><title>{esc(title)}</title><meta name="description" content="{esc(description,quote=True)}"><meta property="og:title" content="{esc(title,quote=True)}"><meta property="og:description" content="{esc(description,quote=True)}"><meta property="og:type" content="website"><link rel="icon" type="image/svg+xml" href="/assets/portfolio/favicon.svg"><link rel="stylesheet" href="/assets/portfolio/style.css"><script src="/assets/portfolio/site.js" defer></script></head><body>{nav(home)}{content}{footer()}<div class="cursor-cross" aria-hidden="true"></div></body></html>'''
def visual(p,case=False):
 if p['image']:
  return f'<img src="/assets/portfolio/{p["image"]}.{p.get("image_ext","webp")}" alt="{esc(p["image_alt"])}" width="{p.get("image_width",1536)}" height="{p.get("image_height",1024)}" loading="{"eager" if case else "lazy"}" decoding="async">'
 return '<div class="diagram-card">'+diagram(p['diagram'])+'</div>'

def project_card(p,featured=False):
 specs=f'<dl class="hover-spec"><dt>MATERIAL</dt><dd>{esc(p["material"])}</dd><dt>ANALYSIS</dt><dd>{esc(p["analysis"])}</dd><dt>TOOLS</dt><dd>{esc(p["tools"][0])}</dd><dt>TESTING</dt><dd>{esc(p["testing"])}</dd><dt>STATUS</dt><dd>{esc(p["status"])}</dd></dl>'
 image_label='COMPANY LOGO' if p.get('company_logo') else 'PROJECT PHOTOGRAPH' if p.get('photo') else 'PROJECT CAD' if p.get('actual_image') else 'AI CONCEPT ILLUSTRATION' if p['image'] else 'TECHNICAL OVERVIEW'
 result=f'<div class="project-result"><strong>{esc(p["metric"])}</strong><span>{esc(p["metric_label"])}</span></div>' if featured else ''
 mini='' if featured else f'<span class="mini-result">{esc(p["metric"])} {esc(p["metric_label"])}</span>'
 media_class=('company-media company-'+p['company_logo']) if p.get('company_logo') else 'actual-media' if p.get('actual_image') else 'photo-media' if p.get('photo') else ''
 return f'''<article class="project-card {'featured' if featured else ''} reveal" data-project="{p['slug']}" data-sort-date="{p.get('sort_date') or ''}"><div class="project-image {media_class}">{visual(p)}<div class="image-top mono"><span>PROJECT / {p['number']}</span><span>{p['date'].upper()}</span></div><div class="image-bottom">{image_label}</div>{specs}</div><div class="project-body"><div class="project-type">{esc(p['project_type'])}</div><div class="project-kicker">{esc(p['company'])} / {esc(p['category'])}</div><h3>{esc(p['title'])}</h3><p>{esc(p['challenge'])}</p>{tags(p['tools'])}{result}<div class="project-footer"><a class="text-link" href="/projects/{p['slug']}/">View Case Study</a>{mini}</div></div></article>'''

def project_collection():
 dated=[p for p in PROJECTS if p.get('sort_date')]
 personal=[p for p in PROJECTS if not p.get('sort_date')]
 out='<div class="project-grid">'+''.join(project_card(p,i in (0,len(dated)-1)) for i,p in enumerate(dated))+'</div>'
 if personal:
  out+='<div class="section-head softgoods-heading"><div><div class="eyebrow">PERSONAL / SOFTGOODS</div><h2>Reworking what exists.</h2></div><p>Completed in 2024–2025. Exact months were not recorded. Original garments, new silhouettes, and useful details kept in circulation.</p></div><div class="project-grid">'+''.join(project_card(p,i==0) for i,p in enumerate(personal))+'</div>'
 return out

def home_page():
 cards=project_collection()
 experiences=''
 for company,style,date,role,sub,desc,skills,slug in EXPERIENCES:
  experiences+=f'''<article class="experience-item reveal"><div class="experience-company"><span class="wordmark {style}">{company}</span><p>{date}</p></div><div><h3>{role}</h3><p class="role">{sub}</p><p>{desc}</p>{tags(skills)}</div><a class="text-link exp-link" href="/projects/{slug}/">Explore work <span aria-hidden="true"></span></a></article>'''
 capabilities=''.join(f'<section class="capability"><header><h3>{esc(name.upper())}</h3><span>0{i+1}</span></header><ul>'+''.join(f'<li>{esc(skill)}</li>' for skill in skills)+'</ul></section>' for i,(name,skills) in enumerate(CAPABILITIES))
 about_visual=(f'<img src="{esc(CONTACT["portrait"])}" alt="Rafael Ponce De Leon" class="portrait" width="1024" height="1536" loading="lazy">' if CONTACT['portrait'] else '<div class="about-plate"><div class="plate-top"><span>RP / ME</span><span>33.98° N · 117.37° W</span></div><span class="monogram" aria-hidden="true">RP.</span><div class="plate-bottom"><span>CURIOUS BY NATURE.<br>ENGINEER BY PRACTICE.</span><span>UCR<br>2026</span></div></div>')
 content=f'''<main id="main"><section class="hero"><div class="hero-grid" aria-hidden="true"></div><div class="hero-visual"><canvas id="mesh" role="img" aria-label="Slowly rotating parametric ring mesh, an illustrative engineering visualization"></canvas></div><div class="wrap"><div class="eyebrow">MECHANICAL ENGINEERING / PORTFOLIO 2026</div><h1><span>RAFAEL</span><span class="last">PONCE DE LEON</span></h1><p class="hero-role">Mechanical Engineer</p><p class="disciplines">Product Design • Simulation • Opto-Mechanical • Manufacturing</p><p class="hero-intro">I design, simulate, build, and test mechanical systems across product development, aerospace, and manufacturing.</p><div class="actions"><a href="#work" class="btn primary">View Projects <span class="arrow" aria-hidden="true"></span></a>{external(CONTACT['resume'],'Resume','btn')}</div></div><div class="model-label mono" aria-hidden="true"><span>FIG. 001 / PARAMETRIC MESH</span><span>U × V / SURFACE STUDY</span></div><div class="model-controls"><span>MOVE TO EXPLORE</span><button id="motion-toggle" aria-pressed="true" aria-label="Toggle mesh animation">Pause motion</button></div><div class="wrap hero-bottom"><a href="#work" class="scroll-cue mono"><i aria-hidden="true"></i> SCROLL TO EXPLORE</a><span class="mono">FROM FIRST PRINCIPLES TO PHYSICAL HARDWARE</span></div></section><div class="trusted"><div class="wrap"><span class="trusted-label mono">ENGINEERING<br>INTERNSHIPS</span><span class="wordmark nike">NIKE</span><span class="wordmark jpl">NASA JPL</span><span class="wordmark tesla">TESLA</span><span class="wordmark sorenson">SORENSON<br>ENGINEERING</span></div></div><section id="work" class="section wrap"><div class="section-head reveal"><div><div class="eyebrow">01 / SELECTED WORK</div><h2>Built on curiosity.<br>Backed by engineering.</h2></div><p>Dated projects run newest to oldest. Personal softgoods work from 2024–2025 follows as a separate collection.</p></div>{cards}<div class="stats-bar reveal"><div class="stat"><b data-count="70" data-suffix="+">70+</b><p>NONLINEAR SIMULATIONS / NIKE</p></div><div class="stat"><b data-count="22">22</b><p>MECHANICAL TEST CURVES / NIKE</p></div><div class="stat"><b data-count="11">11</b><p>FOAM MATERIALS / NIKE</p></div><div class="stat"><b>~4×</b><p>FASTER SIMULATION RUNTIME / NIKE</p></div></div></section><section id="experience" class="section experience"><div class="wrap"><div class="section-head reveal"><div><div class="eyebrow">02 / INTERNSHIP EXPERIENCE</div><h2>Different industries.<br>Same engineering instinct.</h2></div><a class="text-link" href="/experience/">View internship timeline</a></div><p class="internship-note">All professional roles shown here were internships.</p><div class="experience-list">{experiences}</div></div></section><section class="section wrap" id="capabilities"><div class="section-head reveal"><div><div class="eyebrow">03 / TECHNICAL CAPABILITIES</div><h2>A connected toolkit.</h2></div><p>From mechanical definition to simulation, manufacturing, and a measured result.</p></div><div class="capabilities reveal">{capabilities}</div></section><section id="about" class="section wrap about"><div class="reveal">{about_visual}</div><div class="about-copy reveal"><div class="eyebrow">04 / BEYOND THE DRAWING</div><h2>I like figuring out<br>how things work.<br>Then making them.</h2><p>I’m Rafael, a mechanical engineer drawn to problems I can model, build, and put to the test. My internship experience spans footwear, precision space hardware, and manufacturing equipment.</p><p>I enjoy moving between the screen and the physical world: working through a design in CAD, questioning a simulation, and learning something new from a prototype.</p><p>Outside engineering, you’ll find me strength training, sewing and altering clothes, or trying a new skill, a new food, or a new experience. I like being a beginner at something.</p><p class="mono">UNIVERSITY OF CALIFORNIA, RIVERSIDE<br>B.S. MECHANICAL ENGINEERING · EXPECTED DEC 2026</p><div class="interests"><span class="interest">Strength training</span><span class="interest">Sewing & fashion</span><span class="interest">Building things</span><span class="interest">New experiences</span></div></div></section></main>'''
 return page('Rafael Ponce De Leon — Mechanical Engineer','Mechanical engineering portfolio spanning product design, nonlinear simulation, precision opto-mechanics, manufacturing, and physical testing.',content,True)

def evidence(image,alt,caption,width,height,cls=''):
 return f'<figure class="case-visual evidence {cls}"><a href="/assets/portfolio/{image}.webp" target="_blank" rel="noopener" aria-label="Open full-size image: {esc(alt)}"><img src="/assets/portfolio/{image}.webp" alt="{esc(alt)}" width="{width}" height="{height}" loading="lazy"></a><figcaption>{esc(caption)}</figcaption></figure>'

def photo_gallery(p):
 captions={1:'Planning donor material and panel placement.',2:'Cardboard template laid over donor denim.',3:'Outseam panels assembled into the jeans.',4:'Completed outseam flare shown in wear.',5:'The base garment before the inseam modification.',6:'Inseams opened and insert material positioned.',7:'Completed inseam flare, laid flat.',8:'Completed tote, first side and handles.',9:'Completed tote, opposite side and retained pockets.'}
 crops={1:(296,944),2:(502,532),3:(138,1260),4:(138,1260),5:(296,944),6:(296,944),7:(296,944),8:(138,1260),9:(138,1260)}
 out='<div class="photo-gallery">'
 for i in p['gallery']:
  top,h=crops[i]
  if i==5:
   out+=f'<figure><a class="photo-window" href="/assets/portfolio/softgoods-5-cropped.svg" target="_blank" rel="noopener" style="aspect-ratio:709/{h}" aria-label="Open full-size photo: {captions[i]}"><img src="/assets/portfolio/softgoods-5-cropped.svg" alt="{captions[i]}" width="709" height="884" loading="lazy" style="height:100%;object-fit:contain"></a><figcaption>{captions[i]}</figcaption></figure>'
   continue
  out+=f'<figure><a class="photo-window" href="/assets/portfolio/softgoods-{i}.webp" target="_blank" rel="noopener" style="aspect-ratio:709/{h}" aria-label="Open full-size photo: {captions[i]}"><img src="/assets/portfolio/softgoods-{i}.webp" alt="{captions[i]}" width="709" height="1536" loading="lazy" style="transform:translateY(-{100*top/1536:.4f}%)"></a><figcaption>{captions[i]}</figcaption></figure>'
 return out+'</div>'

def case_page(p,next_p):
 specs='<table class="spec-table"><thead><tr><th scope="col">Requirement</th><th scope="col">Engineering definition</th></tr></thead><tbody>'+''.join(f'<tr><td>{esc(a)}</td><td>{esc(b)}</td></tr>' for a,b in p['requirements'])+'</tbody></table>'
 concepts='<div class="iteration-grid">'+''.join(f'<article class="iteration"><span class="mono">ITERATION / 0{i+1}</span><h3>{esc(a)}</h3><p>{esc(b)}</p></article>' for i,(a,b) in enumerate(p['concepts']))+'</div>'
 analysis=paras(p['analysis_text'])
 if p['slug']=='collimator-study':
  analysis+='<div class="comparison-grid">'+evidence('collimator-aligned','Aligned Zemax spot diagram','Aligned configuration. Original Zemax output.',734,622)+evidence('collimator-tilted','Zemax spot diagram after a one-degree coordinate-break tilt','1° tilt configuration. Original Zemax output.',751,628)+'</div>'
  analysis+=evidence('collimator-setup','Zemax lens data with the one-degree coordinate break','Zemax configuration used for the tilt comparison.',1871,412)
  analysis+='<div class="stress-evidence">'+evidence('collimator-stress','Original SolidWorks von Mises stress result','Separate 10 N asymmetric structural load case.',599,602)+evidence('collimator-legend','Stress legend and yield strength from the SolidWorks result','Original stress scale, N/m².',262,608)+'</div>'
 elif p['analysis_diagram']!='softgoods':
  chart=diagram(p['analysis_diagram'])
  caption={'mesh':'Schematic mesh-size comparison, not an exported Abaqus stress plot.','loadpath':'Conceptual load-path diagram, not an original JPL drawing.','loop':'Simplified control architecture, not a measured response plot.','balance':'Proposed one-axis model, with hardware selection and validation still in development.','reel':'Functional component relationships, not a manufacturing drawing.','automation':'Conceptual sensing and control flow.'}[p['analysis_diagram']]
  analysis+=f'<figure class="analysis-figure">{chart}<figcaption>{caption}</figcaption></figure>'
 design=paras(p['design'])
 if p['slug']=='reaction-wheel':design+=evidence('tumbler-wiring','Project Tumbler wiring schematic showing controller, IMU and four motors','Senior-design wiring schematic, Final Design Report, Figure 2.',866,654)
 elif p['slug']=='collimator-study':design+=evidence('collimator-cad',p['image_alt'],'Original SolidWorks mount CAD for the 25 mm lens.',946,730)
 elif p['image'] and not p.get('photo') and not p.get('company_logo'):design+=f'<figure class="case-visual">{visual(p)}<figcaption>AI-generated concept illustration, not original company CAD or simulation output.</figcaption></figure>'
 results=f'<p>{esc(p["result_text"])}</p><div class="result-grid">'+''.join(f'<div class="result-block"><b>{esc(a)}</b><span>{esc(b)}</span></div>' for a,b in p['results'])+'</div>'
 build_content=paras(p['build'])
 if p['slug']=='reaction-wheel':build_content+=evidence('tumbler-yaw','Measured wrapped-yaw response to disturbances','Senior-design test response. Final Design Report, Figure 8. The yaw trace wraps at 360°.',751,457)
 if p.get('gallery'):build_content+=photo_gallery(p)
 sections=[('problem','Problem',paras(p['problem'])),('requirements','Requirements',specs),('concepts','Concepts',concepts),('analysis','Pattern Geometry' if p.get('softgoods_kind') in ('outseam','inseam') else 'Engineering Analysis',analysis),('design','Design',design),('build-test','Build / Test',build_content),('results','Results',results),('reflection','What I Learned',f'<p>{esc(p["learning"])}</p>')]
 navlinks=''.join(f'<a href="#{slug}">{i+1:02d} {name}</a>' for i,(slug,name,_) in enumerate(sections))
 body=''.join(f'<section class="case-section reveal" id="{slug}"><header><div class="eyebrow">{i+1:02d}</div><h2>{name}</h2></header><div class="case-content">{content}</div></section>' for i,(slug,name,content) in enumerate(sections))
 media_note=p.get('media_caption') or ('AI-generated concept illustration, not original company CAD or measured analysis.' if p['image'] else 'Engineering concept diagram. Project status and test evidence are described below.')
 date=esc(p['date'])+('<br><small>'+esc(p['date_note'])+'</small>' if p.get('date_note') else '')
 content=f'''<main id="main"><header class="case-hero wrap"><a class="back-link" href="/#work">BACK TO SELECTED WORK</a><div class="eyebrow">{esc(p['company'])} / CASE STUDY {p['number']}</div><h1>{esc(p['title'])}</h1><p class="case-intro">{esc(p['challenge'])}</p><dl class="case-meta"><div><dt>Project type</dt><dd>{esc(p['project_type'])}</dd></div><div><dt>Role</dt><dd>{esc(p['role'])}</dd></div><div><dt>Timeline</dt><dd>{date}</dd></div><div><dt>Disciplines</dt><dd>{esc(p['disciplines'])}</dd></div><div><dt>Status</dt><dd>{esc(p['status'])}</dd></div></dl></header><div class="wrap"><figure class="case-visual {('company-hero company-'+p['company_logo']) if p.get('company_logo') else 'photo-hero' if p.get('photo') else ''}">{visual(p,True)}<figcaption>{media_note}</figcaption></figure><nav class="case-nav" aria-label="Case study sections">{navlinks}</nav>{body}<a class="next-project" href="/projects/{next_p['slug']}/"><div><span class="mono blue">NEXT CASE STUDY / {next_p['number']}</span><h2>{esc(next_p['title'])}</h2></div></a></div></main>'''
 return page(p['title']+' — Rafael Ponce De Leon',p['challenge'],content)

def timeline_page():
 rows=''
 for company,style,date,role,sub,desc,skills,slug in reversed(EXPERIENCES):
  rows+=f'<li class="timeline-entry reveal"><div class="timeline-date mono">{date}</div><article><div class="project-type">INTERNSHIP</div><span class="wordmark {style}">{company}</span><h2>{role}</h2><p class="timeline-location">{sub}</p><p>{desc}</p>{tags(skills)}<a class="text-link" href="/projects/{slug}/">View internship project</a></article></li>'
 content=f'<main id="main" class="wrap"><header class="case-hero"><a class="back-link" href="/">BACK TO PORTFOLIO</a><div class="eyebrow">ENGINEERING EXPERIENCE / 2023–2026</div><h1>My internship timeline.</h1><p class="case-intro">Five internships across manufacturing equipment, mechanical design, precision optics, controls, and product simulation. Every professional role below was an internship.</p><p class="timeline-order mono">EARLIEST TO MOST RECENT</p></header><ol class="internship-timeline">{rows}</ol></main>'
 return page('Engineering Internship Timeline — Rafael Ponce De Leon','Five separate engineering internships from Tesla Sparks in 2023 through Nike in 2026.',content)

def build():
 (ROOT/'index.html').write_text(home_page())
 for i,p in enumerate(PROJECTS):
  folder=ROOT/'projects'/p['slug'];folder.mkdir(parents=True,exist_ok=True)
  (folder/'index.html').write_text(case_page(p,PROJECTS[(i+1)%len(PROJECTS)]))
 icon='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="5" fill="#090b0e"/><path d="M8 24V8h8a5 5 0 010 10H8m7 0 8 6" fill="none" stroke="#a8d6f2" stroke-width="2.5"/><path d="M25 4v5m-2.5-2.5h5" stroke="#a8d6f2"/></svg>'
 (ROOT/'assets/portfolio/favicon.svg').write_text(icon)
 notfound='<main id="main" class="wrap not-found"><div class="eyebrow">404 / PAGE NOT FOUND</div><h1>Off the drawing.</h1><p>This page is no longer here. Return to the portfolio to explore the latest work.</p><div class="actions"><a class="btn primary" href="/">Back to portfolio </a></div></main>'
 (ROOT/'404.html').write_text(page('Page not found — Rafael Ponce De Leon','Return to the mechanical engineering portfolio.',notfound))
 # Keep the legacy /projects.html entrypoint useful without relying on JavaScript.
 (ROOT/'projects.html').write_text(page('Selected projects — Rafael Ponce De Leon','Engineering case studies.', '<main id="main" class="wrap section" style="padding-top:145px"><div class="section-head"><h1>Selected work.</h1></div>'+project_collection()+'</main>'))
 (ROOT/'experience').mkdir(exist_ok=True)
 (ROOT/'experience/index.html').write_text(timeline_page())
 legacy=ROOT/'projects/manufacturing-automation/index.html'
 legacy.parent.mkdir(parents=True,exist_ok=True)
 legacy.write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=/projects/tesla-equipment/"><title>Equipment engineering project</title></head><body><main><h1>Equipment engineering project</h1><a href="/projects/tesla-equipment/">Continue to the Tesla Sparks internship project</a></main></body></html>')
 dist=ROOT/'dist';dist.mkdir(exist_ok=True)
 for filename in ('index.html','projects.html','404.html'):shutil.copy2(ROOT/filename,dist/filename)
 shutil.copytree(ROOT/'projects',dist/'projects',dirs_exist_ok=True)
 shutil.copytree(ROOT/'experience',dist/'experience',dirs_exist_ok=True)
 shutil.copytree(ROOT/'assets/portfolio',dist/'assets/portfolio',dirs_exist_ok=True)
 print(f'Rendered home, project index, 404, and {len(PROJECTS)} case studies into dist/.')

if __name__=='__main__':build()
