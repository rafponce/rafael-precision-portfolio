(() => {
  'use strict';
  document.documentElement.classList.add('js');
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  const nav = document.querySelector('.nav');
  const menu = document.querySelector('.menu-toggle');
  const links = document.querySelector('.nav-links');
  function closeMenu(){ links?.classList.remove('open'); menu?.setAttribute('aria-expanded','false'); }
  menu?.addEventListener('click',()=>{const open=links.classList.toggle('open');menu.setAttribute('aria-expanded',String(open));});
  links?.querySelectorAll('a').forEach(a=>a.addEventListener('click',closeMenu));
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&links?.classList.contains('open')){closeMenu();menu.focus();}});
  document.addEventListener('click',e=>{if(!nav?.contains(e.target))closeMenu();});
  const scroll=()=>nav?.classList.toggle('scrolled',window.scrollY>15);
  scroll();window.addEventListener('scroll',scroll,{passive:true});
  if('IntersectionObserver' in window){
    const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('visible');observer.unobserve(entry.target);}}),{threshold:.08});
    document.querySelectorAll('.reveal').forEach(el=>observer.observe(el));
    const counts=new IntersectionObserver(entries=>entries.forEach(entry=>{if(!entry.isIntersecting)return;counts.unobserve(entry.target);if(reduce.matches)return;const el=entry.target;const target=Number(el.dataset.count);const suffix=el.dataset.suffix||'';const start=performance.now();function tick(now){const t=Math.min((now-start)/1000,1);el.textContent=Math.round(target*(1-Math.pow(1-t,3)))+suffix;if(t<1)requestAnimationFrame(tick);}requestAnimationFrame(tick);}),{threshold:.8});
    document.querySelectorAll('[data-count]').forEach(el=>counts.observe(el));
  }else{document.querySelectorAll('.reveal').forEach(el=>el.classList.add('visible'));}
  const cursor=document.querySelector('.cursor-cross');
  if(cursor&&matchMedia('(pointer:fine)').matches&&!reduce.matches){document.addEventListener('pointermove',e=>{cursor.style.transform=`translate(${e.clientX}px,${e.clientY}px) translate(-50%,-50%)`;cursor.style.opacity='1';},{passive:true});document.addEventListener('pointerleave',()=>cursor.style.opacity='0');}
  if(!reduce.matches&&matchMedia('(pointer:fine)').matches){let pending=false;const pictures=[...document.querySelectorAll('.project-image:not(.actual-media) img')];window.addEventListener('scroll',()=>{if(pending)return;pending=true;requestAnimationFrame(()=>{pictures.forEach(img=>{const box=img.getBoundingClientRect();if(box.bottom>0&&box.top<innerHeight)img.style.setProperty('--parallax',`${Math.max(-7,Math.min(7,(box.top-innerHeight/2)*.012))}px`);});pending=false;});},{passive:true});}
  const canvas=document.getElementById('mesh');if(!canvas)return;
  const ctx=canvas.getContext('2d');if(!ctx)return;
  const toggle=document.getElementById('motion-toggle');
  let w=1,h=1,angle=.45,tilt=.64,paused=reduce.matches,inView=true,raf=0,last=0,targetTilt=.64;
  function resize(){const box=canvas.getBoundingClientRect();w=box.width;h=box.height;const dpr=Math.min(devicePixelRatio||1,2);canvas.width=Math.round(w*dpr);canvas.height=Math.round(h*dpr);ctx.setTransform(dpr,0,0,dpr,0,0);draw();}
  function point(u,v){const major=1.58,minor=.39;const x=(major+minor*Math.cos(v))*Math.cos(u),y=(major+minor*Math.cos(v))*Math.sin(u),z=minor*Math.sin(v);const a=x*Math.cos(angle)-y*Math.sin(angle),b=x*Math.sin(angle)+y*Math.cos(angle);const yy=b*Math.cos(tilt)-z*Math.sin(tilt),zz=b*Math.sin(tilt)+z*Math.cos(tilt);const scale=Math.min(w,h)*.22;const perspective=5/(5+zz);return [w*.5+a*scale*perspective,h*.5+yy*scale*perspective,zz];}
  function line(points,alpha){ctx.beginPath();points.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));ctx.strokeStyle=`rgba(155,192,218,${alpha})`;ctx.lineWidth=.7;ctx.stroke();}
  function draw(){ctx.clearRect(0,0,w,h);for(let j=0;j<18;j++){const points=[];for(let i=0;i<=72;i++)points.push(point(i/72*Math.PI*2,j/18*Math.PI*2));line(points,.22+j/90);}for(let i=0;i<56;i++){const points=[];for(let j=0;j<=36;j++)points.push(point(i/56*Math.PI*2,j/36*Math.PI*2));line(points,.3);}const center=[w*.5,h*.5];ctx.strokeStyle='#65819777';ctx.setLineDash([4,7]);ctx.beginPath();ctx.moveTo(center[0]-w*.36,center[1]);ctx.lineTo(center[0]+w*.36,center[1]);ctx.moveTo(center[0],center[1]-h*.3);ctx.lineTo(center[0],center[1]+h*.3);ctx.stroke();ctx.setLineDash([]);ctx.font='12px monospace';ctx.fillStyle='#8ca3b5';ctx.fillText('X',center[0]+w*.36+8,center[1]+4);ctx.fillText('Y',center[0]+8,center[1]-h*.3);ctx.fillStyle='#b2d4ed';ctx.fillRect(center[0]-2,center[1]-2,4,4);}
  function frame(now){raf=0;if(paused||!inView||document.hidden)return;if(now-last>=32){angle+=.0017;tilt+=(targetTilt-tilt)*.035;draw();last=now;}raf=requestAnimationFrame(frame);}
  function sync(){if(raf)cancelAnimationFrame(raf);raf=0;toggle.textContent=paused?'Play motion':'Pause motion';toggle.setAttribute('aria-pressed',String(!paused));if(!paused&&inView&&!document.hidden)raf=requestAnimationFrame(frame);else draw();}
  toggle.addEventListener('click',()=>{paused=!paused;sync();});
  canvas.addEventListener('pointermove',e=>{if(paused||reduce.matches)return;const r=canvas.getBoundingClientRect();targetTilt=.4+((e.clientY-r.top)/h)*.55;},{passive:true});
  canvas.addEventListener('pointerleave',()=>targetTilt=.64);
  if('IntersectionObserver' in window)new IntersectionObserver(entries=>{inView=entries[0].isIntersecting;sync();}).observe(canvas);
  document.addEventListener('visibilitychange',sync);reduce.addEventListener('change',()=>{paused=reduce.matches;sync();});
  new ResizeObserver(resize).observe(canvas);resize();sync();
})();
