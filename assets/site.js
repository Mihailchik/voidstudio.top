// Public-facing preview interactions only.
const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
if(!reduced){const hero=document.querySelector('.hero-images');const images=[...hero.querySelectorAll('figure')];let x=0,y=0,tx=0,ty=0,frame=0;function move(){x+=(tx-x)*.07;y+=(ty-y)*.07;images.forEach((el,i)=>{const d=[.42,-.75,.9][i];el.style.transform=`translate3d(${x*d}px,${y*d}px,0)`});frame=Math.abs(tx-x)+Math.abs(ty-y)>.1?requestAnimationFrame(move):0}hero.addEventListener('pointermove',e=>{const r=hero.getBoundingClientRect();tx=((e.clientX-r.left)/r.width-.5)*28;ty=((e.clientY-r.top)/r.height-.5)*22;if(!frame)frame=requestAnimationFrame(move)});hero.addEventListener('pointerleave',()=>{tx=ty=0;if(!frame)frame=requestAnimationFrame(move)})}

