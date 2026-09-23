// PROTOTYPE: original interaction implementation using the user's own artwork.
const works=galleryWorks.filter(work=>!work.newCandidate);
const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
let mode='film';
const clamp=(n,min,max)=>Math.max(min,Math.min(max,n));
const pad=n=>String(n).padStart(2,'0');
const selectedIds=selectedGalleryIds();
const filmWorks=(selectedIds.length?selectedIds:suggestedGalleryIds).map(id=>galleryWorks.find(work=>work.id===id));
const filmController=createFilmstrip(filmWorks,{reduced});
const selectionLink=document.getElementById('selection-link');
selectionLink.href=`prototype-selection.html?works=${filmWorks.map(work=>work.id).join(',')}`;
works.forEach((work,i)=>{
  const accessible=document.createElement('button');accessible.type='button';accessible.textContent=work.title;accessible.addEventListener('click',()=>openWork(i));document.getElementById('accessible-works').append(accessible);
});

// Native modal, with a thumbnail-to-image transition and keyboard navigation.
const viewer=document.getElementById('viewer'),viewerImage=document.getElementById('viewer-image');let viewerIndex=0,viewerOrigin=null,openingAnimation=null;
function viewerBounds(work){const iw=work.image?.naturalWidth||1,ih=work.image?.naturalHeight||1;const maxW=innerWidth*(innerWidth<700?.87:.72),maxH=innerHeight*.62;const scale=Math.min(maxW/iw,maxH/ih);return{width:iw*scale,height:ih*scale,left:(innerWidth-iw*scale)/2,top:(innerHeight*.76-ih*scale)/2};}
function updateViewer(index,origin){viewerIndex=index;const work=works[index];viewerImage.src=work.src;viewerImage.alt=work.title;const r=viewerBounds(work);Object.assign(viewerImage.style,{left:r.left+'px',top:r.top+'px',width:r.width+'px',height:r.height+'px'});document.getElementById('viewer-index').textContent=`${pad(index+1)} / ${works.length}`;document.getElementById('viewer-title').textContent=work.title;if(openingAnimation)openingAnimation.cancel();if(origin&&!reduced){openingAnimation=viewerImage.animate([{transformOrigin:'0 0',transform:`translate(${origin.left-r.left}px,${origin.top-r.top}px) scale(${origin.width/r.width},${origin.height/r.height})`,filter:'brightness(.45)'},{transformOrigin:'0 0',transform:'translate(0,0) scale(1,1)',filter:'brightness(1)'}],{duration:780,easing:'cubic-bezier(.2,.8,.2,1)',fill:'both'});}else if(!reduced){openingAnimation=viewerImage.animate([{opacity:0,transform:'translateY(15px)'},{opacity:1,transform:'translateY(0)'}],{duration:400,easing:'ease-out',fill:'both'});}viewer.classList.add('viewer-ready');}
function openWork(index,origin=null){if(!works[index].image?.complete)return;viewerOrigin=origin;viewer.showModal();updateViewer(index,origin);}
function closeViewer(){if(!viewer.open)return;viewer.classList.remove('viewer-ready');if(reduced||!viewerOrigin){viewer.close();return;}if(openingAnimation)openingAnimation.cancel();const r=viewerImage.getBoundingClientRect();const origin=viewerOrigin;viewerImage.animate([{transform:'none',transformOrigin:'0 0',opacity:1},{transform:`translate(${origin.left-r.left}px,${origin.top-r.top}px) scale(${origin.width/r.width},${origin.height/r.height})`,transformOrigin:'0 0',opacity:.35}],{duration:420,easing:'cubic-bezier(.45,0,.3,1)'}).finished.then(()=>viewer.close()).catch(()=>viewer.close());}
viewer.querySelector('.viewer-close').addEventListener('click',closeViewer);viewer.addEventListener('cancel',e=>{e.preventDefault();closeViewer();});viewer.addEventListener('click',e=>{if(e.target===viewer)closeViewer();});
function advanceViewer(direction){viewerOrigin=null;updateViewer((viewerIndex+direction+works.length)%works.length);}
viewer.querySelector('.viewer-next').addEventListener('click',()=>advanceViewer(1));viewer.querySelector('.viewer-prev').addEventListener('click',()=>advanceViewer(-1));
document.addEventListener('keydown',e=>{if(e.target.closest('input,textarea,[contenteditable]'))return;if(e.key!=='ArrowLeft'&&e.key!=='ArrowRight')return;if(viewer.open){e.preventDefault();advanceViewer(e.key==='ArrowRight'?1:-1);}});

// The lens samples a higher-resolution mosaic at the exact same world position.
const mosaicStage=document.getElementById('mosaic-stage'),mosaic=document.getElementById('mosaic'),ctx=mosaic.getContext('2d'),source=document.createElement('canvas'),sourceCtx=source.getContext('2d'),magnifier=document.getElementById('magnifier'),lensCanvas=document.getElementById('magnified'),lensCtx=lensCanvas.getContext('2d');
let loaded=false,mosaicW=0,mosaicH=0,tiles=[],lensX=.53,lensY=.49,zoom=3,pinned=false,lensWork=0,touchStart=null,mosaicFrame=0,pointerInside=false;
const sourceScale=3;
function cropImage(context,image,x,y,w,h,seed){const ratio=Math.max(w/image.naturalWidth,h/image.naturalHeight)*(seed%5===0?1.2:1);const sw=w/ratio,sh=h/ratio;const ox=(image.naturalWidth-sw)*(.3+(seed%4)*.13),oy=(image.naturalHeight-sh)*(.28+(seed%3)*.18);context.drawImage(image,ox,oy,sw,sh,x,y,w,h);}
function drawMosaic(){if(!loaded||mode!=='collage')return;mosaicW=mosaicStage.clientWidth;mosaicH=mosaicStage.clientHeight;if(!mosaicW||!mosaicH)return;const columns=mosaicW<600?6:12,rows=mosaicW<600?10:7,cw=mosaicW/columns,ch=mosaicH/rows,occupied=new Set();tiles=[];source.width=mosaicW*sourceScale;source.height=mosaicH*sourceScale;sourceCtx.setTransform(sourceScale,0,0,sourceScale,0,0);sourceCtx.fillStyle='#e7e9df';sourceCtx.fillRect(0,0,mosaicW,mosaicH);let n=0;
  for(let row=0;row<rows;row++){for(let col=0;col<columns;col++){if(occupied.has(`${col},${row}`))continue;let spanX=n%6===0?2:1,spanY=n%6===0?2:1;if(col+spanX>columns||row+spanY>rows||occupied.has(`${col+1},${row}`)||occupied.has(`${col},${row+1}`)){spanX=spanY=1;}for(let a=0;a<spanX;a++)for(let b=0;b<spanY;b++)occupied.add(`${col+a},${row+b}`);const index=(n*5+Math.floor(n/works.length))%works.length;const tile={x:col*cw+2,y:row*ch+2,w:spanX*cw-4,h:spanY*ch-4,index};tiles.push(tile);cropImage(sourceCtx,works[index].image,tile.x,tile.y,tile.w,tile.h,n);n++;}}
  const dpr=Math.min(devicePixelRatio||1,2);mosaic.width=mosaicW*dpr;mosaic.height=mosaicH*dpr;ctx.setTransform(dpr,0,0,dpr,0,0);ctx.drawImage(source,0,0,mosaicW,mosaicH);drawLens();
}
function drawLens(){mosaicFrame=0;if(!loaded||mode!=='collage'||!mosaicW)return;const diameter=magnifier.clientWidth,dpr=Math.min(devicePixelRatio||1,2),x=lensX*mosaicW,y=lensY*mosaicH;if(lensCanvas.width!==Math.round(diameter*dpr)){lensCanvas.width=diameter*dpr;lensCanvas.height=diameter*dpr;}lensCtx.setTransform(dpr,0,0,dpr,0,0);lensCtx.fillStyle='#e7e9df';lensCtx.fillRect(0,0,diameter,diameter);const sampled=diameter/zoom; lensCtx.drawImage(source,(x-sampled/2)*sourceScale,(y-sampled/2)*sourceScale,sampled*sourceScale,sampled*sourceScale,0,0,diameter,diameter);magnifier.style.left=`${x}px`;magnifier.style.top=`${y}px`;const tile=tiles.find(t=>x>=t.x&&x<=t.x+t.w&&y>=t.y&&y<=t.y+t.h);if(tile){lensWork=tile.index;document.getElementById('mosaic-title').textContent=`${works[lensWork].title} / ${zoom}×`;}}
function showLens(visible){magnifier.classList.toggle('lens-visible',visible);mosaicStage.classList.toggle('lens-following',visible&&!pinned);}
function moveLens(e){if(pinned||!mosaicW)return;if(e.target.closest('button')){showLens(false);return;}const r=mosaicStage.getBoundingClientRect();lensX=clamp((e.clientX-r.left)/r.width,0,1);lensY=clamp((e.clientY-r.top)/r.height,0,1);pointerInside=true;showLens(true);if(!mosaicFrame)mosaicFrame=requestAnimationFrame(drawLens);}
mosaicStage.addEventListener('pointerenter',e=>{pointerInside=true;if(e.pointerType!=='touch')moveLens(e);});
mosaicStage.addEventListener('pointerleave',()=>{pointerInside=false;if(!pinned)showLens(false);});
mosaicStage.addEventListener('pointercancel',()=>{pointerInside=false;if(!pinned)showLens(false);});
window.addEventListener('blur',()=>{pointerInside=false;showLens(false);});
window.addEventListener('scroll',()=>{pointerInside=false;if(!pinned)showLens(false);},{passive:true});
function openLensWork(){const x=lensX*mosaicW,y=lensY*mosaicH;const tile=tiles.find(t=>x>=t.x&&x<=t.x+t.w&&y>=t.y&&y<=t.y+t.h);const r=mosaicStage.getBoundingClientRect();openWork(lensWork,tile?{left:r.left+tile.x,top:r.top+tile.y,width:tile.w,height:tile.h}:null);}
mosaicStage.addEventListener('pointermove',e=>{if(e.pointerType!=='touch'||e.buttons)moveLens(e);});
mosaicStage.addEventListener('pointerdown',e=>{if(e.target.closest('button'))return;moveLens(e);touchStart={x:e.clientX,y:e.clientY,type:e.pointerType};});
mosaicStage.addEventListener('pointerup',e=>{if(e.target.closest('button'))return;if(touchStart&&touchStart.type!=='touch'&&Math.hypot(e.clientX-touchStart.x,e.clientY-touchStart.y)<5)openLensWork();touchStart=null;});
mosaicStage.querySelector('.mosaic-open').addEventListener('click',openLensWork);
mosaicStage.addEventListener('keydown',e=>{if(e.key==='Enter'&&e.target===mosaicStage){e.preventDefault();openLensWork();}});
document.getElementById('zoom').addEventListener('input',e=>{zoom=Number(e.target.value);document.getElementById('zoom-label').textContent=zoom+'×';document.querySelector('.lens-zoom').textContent=zoom+'×';drawLens();});
document.getElementById('pin-lens').addEventListener('click',e=>{pinned=!pinned;e.currentTarget.setAttribute('aria-pressed',String(pinned));e.currentTarget.textContent=pinned?'Освободить линзу':'Закрепить линзу';showLens(pinned||pointerInside);drawLens();});
new ResizeObserver(()=>{if(mode==='collage')drawMosaic();}).observe(mosaicStage);

function setMode(next){mode=next;document.body.dataset.mode=mode;document.getElementById('film').hidden=mode!=='film';document.getElementById('collage').hidden=mode!=='collage';document.querySelectorAll('.mode-switch button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.mode===mode)));const url=new URL(location.href);url.searchParams.set('mode',mode);history.replaceState(null,'',url);filmController.setActive(mode==='film');if(mode==='collage')requestAnimationFrame(drawMosaic);}
document.querySelectorAll('.mode-switch button').forEach(b=>b.addEventListener('click',()=>setMode(b.dataset.mode)));
setMode(new URL(location.href).searchParams.get('mode')==='collage'?'collage':'film');
Promise.all(works.map(work=>new Promise(resolve=>{const image=new Image();work.image=image;image.onload=resolve;image.onerror=resolve;image.src=work.src;}))).then(()=>{loaded=works.every(w=>w.image.naturalWidth>0);if(loaded)drawMosaic();else document.getElementById('mosaic-title').textContent='Часть изображений не загрузилась. Перезагрузите страницу.';});
window.addEventListener('resize',()=>{if(viewer.open)updateViewer(viewerIndex);});
