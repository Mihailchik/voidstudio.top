// PROTOTYPE: local presentation state only. No publication, analytics or persistence.
const variants=['A','B','C'];
const names={A:'01 / Воздух',B:'02 / Линза',C:'03 / Живое письмо'};
const url=new URL(location.href);
let selected=variants.includes(url.searchParams.get('variant'))?url.searchParams.get('variant'):'A';
const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
function renderVariant(){
  document.body.dataset.variant=selected;
  document.querySelectorAll('[data-concept]').forEach(el=>el.hidden=el.dataset.concept!==selected);
  document.getElementById('variant-label').textContent=names[selected];
  document.querySelectorAll('.portfolio-link').forEach(el=>el.href='prototype-portfolio.html?variant='+selected);
  url.searchParams.set('variant',selected);history.replaceState(null,'',url);
}
function changeVariant(direction){selected=variants[(variants.indexOf(selected)+direction+3)%3];renderVariant();window.scrollTo({top:0,behavior:'instant'});if(selected==='B')requestAnimationFrame(centerLens);}
document.getElementById('previous').addEventListener('click',()=>changeVariant(-1));
document.getElementById('next').addEventListener('click',()=>changeVariant(1));
document.addEventListener('keydown',e=>{if(e.target.closest('input,textarea,[contenteditable=true]')||document.querySelector('dialog[open]'))return;if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();changeVariant(e.key==='ArrowLeft'?-1:1);}});
if(['localhost','127.0.0.1',''].includes(location.hostname))document.querySelector('.prototype-switcher').style.display='flex';
renderVariant();
const stage=document.getElementById('orbit-stage');
const photos=[...stage.querySelectorAll('[data-depth]')];
let targetX=0,targetY=0,x=0,y=0,frame=0;
function animatePhotos(){x+=(targetX-x)*.065;y+=(targetY-y)*.065;photos.forEach(photo=>{const depth=Number(photo.dataset.depth);photo.style.setProperty('--dx',`${x*depth}px`);photo.style.setProperty('--dy',`${y*depth}px`);});if(Math.abs(targetX-x)+Math.abs(targetY-y)>.1)frame=requestAnimationFrame(animatePhotos);else frame=0;}
stage.addEventListener('pointermove',e=>{if(reduced||e.pointerType==='touch')return;const r=stage.getBoundingClientRect();targetX=((e.clientX-r.left)/r.width-.5)*35;targetY=((e.clientY-r.top)/r.height-.5)*27;if(!frame)frame=requestAnimationFrame(animatePhotos);});
stage.addEventListener('pointerleave',()=>{targetX=targetY=0;if(!reduced&&!frame)frame=requestAnimationFrame(animatePhotos);});
const lensStage=document.getElementById('lens-stage'),lens=document.getElementById('glass-lens'),picture=lens.querySelector('.lens-picture');
let lensOn=true;
function positionLens(cx,cy){const r=lensStage.getBoundingClientRect();const px=Math.max(0,Math.min(r.width,cx-r.left)),py=Math.max(0,Math.min(r.height,cy-r.top));lens.style.left=`${px}px`;lens.style.top=`${py}px`;const img=lensStage.querySelector('.panorama');const scale=Math.max(r.width/(img.naturalWidth||1136),r.height/(img.naturalHeight||928));const w=(img.naturalWidth||1136)*scale,h=(img.naturalHeight||928)*scale;const magnify=1.35;picture.style.backgroundSize=`${w*magnify}px ${h*magnify}px`;picture.style.backgroundPosition=`${lens.offsetWidth/2+20-(px+(w-r.width)/2)*magnify}px ${lens.offsetHeight/2+20-(py+(h-r.height)*.48)*magnify}px`;}
function centerLens(){if(selected!=='B')return;const r=lensStage.getBoundingClientRect();positionLens(r.left+r.width*.58,r.top+r.height*.47);}
new ResizeObserver(centerLens).observe(lensStage);
centerLens();
lensStage.addEventListener('pointermove',e=>{if(lensOn&&!reduced)positionLens(e.clientX,e.clientY);});
lensStage.addEventListener('pointerdown',e=>{if(lensOn)positionLens(e.clientX,e.clientY);});
document.querySelector('.lens-toggle').addEventListener('click',e=>{lensOn=!lensOn;lens.hidden=!lensOn;const button=e.currentTarget;button.setAttribute('aria-pressed',String(lensOn));button.innerHTML=`Линза ${lensOn?'включена':'выключена'} <span>↗</span>`;});
const dialog=document.getElementById('art-dialog');
document.querySelectorAll('[data-image]').forEach(button=>button.addEventListener('click',()=>{dialog.querySelector('img').src=button.dataset.image;dialog.showModal();}));
dialog.querySelector('button').addEventListener('click',()=>dialog.close());
dialog.addEventListener('click',e=>{if(e.target===dialog)dialog.close();});
