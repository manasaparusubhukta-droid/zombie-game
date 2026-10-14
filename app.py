import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="LAST STAND | Zombie Survival", page_icon="🧟", layout="wide")

st.markdown("""
<style>
    .stApp { background: #090d10; color: #e8eeee; }
    header, footer {visibility: hidden;}
    .block-container { padding-top: 1rem; padding-bottom: 0.5rem; max-width: 1250px; }
    h1 { color: #d9e7df; letter-spacing: 3px; text-align: center; }
    .subtitle { text-align:center; color:#9eaaa6; margin-top:-8px; margin-bottom:14px; }
    .help { text-align:center; color:#b9c4c0; font-size:14px; }
</style>
""", unsafe_allow_html=True)

st.markdown("# LAST STAND")
st.markdown('<div class="subtitle">2D ZOMBIE SURVIVAL • Stay alive. Collect supplies. Survive the waves.</div>', unsafe_allow_html=True)

components.html(r"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
*{box-sizing:border-box}
body{margin:0;background:#090d10;color:#eaf0ec;font-family:Arial,sans-serif}
.wrap{max-width:1120px;margin:auto}
canvas{display:block;width:100%;height:auto;border:1px solid #35413d;border-radius:10px;background:#101a19;box-shadow:0 10px 35px #0009;cursor:crosshair}
.hint{color:#b5c1bc;text-align:center;font-size:13px;line-height:1.6;margin:9px 0 2px}
kbd{background:#25312d;border:1px solid #52625a;border-radius:4px;padding:2px 6px;color:#fff}
</style>
</head>
<body>
<div class="wrap">
<canvas id="game" width="1100" height="650" aria-label="Last Stand zombie survival game"></canvas>
<div class="hint">
Move <kbd>WASD</kbd>/<kbd>↑↓←→</kbd> · Aim with mouse · Shoot <kbd>Left Click</kbd>/<kbd>Space</kbd> ·
Collect nearby supplies <kbd>E</kbd> · Pause <kbd>Esc</kbd> · Restart <kbd>R</kbd> · Sound <kbd>M</kbd>
</div>
</div>
<script>
(() => {
const canvas=document.getElementById('game'), ctx=canvas.getContext('2d');
const W=canvas.width,H=canvas.height;
const keys={}, mouse={x:W/2,y:H/2,down:false};
let player,zombies,bullets,crates,particles,score,wave,gameOver,paused,started,ammo,health,stamina,spawnTimer,lastTime=0,muted=false,audioCtx=null;
const rand=(a,b)=>Math.random()*(b-a)+a;
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
function sound(freq=220,dur=.07,type='square',vol=.035,slide=0){
 if(muted)return;
 try{
  audioCtx=audioCtx||new (window.AudioContext||window.webkitAudioContext)();
  if(audioCtx.state==='suspended')audioCtx.resume();
  const o=audioCtx.createOscillator(),g=audioCtx.createGain();
  o.type=type;o.frequency.setValueAtTime(freq,audioCtx.currentTime);
  if(slide)o.frequency.exponentialRampToValueAtTime(Math.max(30,freq+slide),audioCtx.currentTime+dur);
  g.gain.setValueAtTime(vol,audioCtx.currentTime);g.gain.exponentialRampToValueAtTime(.001,audioCtx.currentTime+dur);
  o.connect(g);g.connect(audioCtx.destination);o.start();o.stop(audioCtx.currentTime+dur);
 }catch(e){}
}
function reset(){
 player={x:W/2,y:H/2,r:15,speed:230,angle:0,invuln:0};
 zombies=[];bullets=[];crates=[];particles=[];score=0;wave=1;gameOver=false;paused=false;started=false;ammo=40;health=100;stamina=100;spawnTimer=0;
 for(let i=0;i<5;i++)spawnZombie();
 for(let i=0;i<4;i++)spawnCrate();
}
function spawnZombie(){
 let side=Math.floor(rand(0,4)),x,y;
 if(side===0){x=rand(0,W);y=-20}else if(side===1){x=W+20;y=rand(0,H)}else if(side===2){x=rand(0,W);y=H+20}else{x=-20;y=rand(0,H)}
 zombies.push({x,y,r:rand(13,18),speed:rand(38,57)+wave*3,hp:1+(wave>2?1:0),attack:0,wob:rand(0,7)});
}
function spawnCrate(){crates.push({x:rand(60,W-60),y:rand(70,H-60),r:12,bob:rand(0,6)});}
function burst(x,y,color,n=8){for(let i=0;i<n;i++){let a=rand(0,Math.PI*2),s=rand(35,180);particles.push({x,y,vx:Math.cos(a)*s,vy:Math.sin(a)*s,life:rand(.18,.5),max:.5,color});}}
function shoot(){
 if(!started||paused||gameOver)return;
 if(ammo<=0){sound(100,.04,'triangle',.02);return}
 ammo--;sound(175,.09,'sawtooth',.045,-100);
 const a=Math.atan2(mouse.y-player.y,mouse.x-player.x);
 bullets.push({x:player.x+Math.cos(a)*20,y:player.y+Math.sin(a)*20,vx:Math.cos(a)*600,vy:Math.sin(a)*600,life:.85});
 burst(player.x+Math.cos(a)*22,player.y+Math.sin(a)*22,'#ffc66d',3);
}
function startGame(){if(!started){started=true;sound(440,.12,'triangle',.035);}}
function pointer(e){const r=canvas.getBoundingClientRect();mouse.x=(e.clientX-r.left)*W/r.width;mouse.y=(e.clientY-r.top)*H/r.height;}
canvas.addEventListener('mousemove',pointer);
canvas.addEventListener('mousedown',e=>{pointer(e);mouse.down=true;startGame();shoot();});
window.addEventListener('mouseup',()=>mouse.down=false);
canvas.addEventListener('contextmenu',e=>e.preventDefault());
window.addEventListener('keydown',e=>{
 const k=e.key.toLowerCase();keys[k]=true;
 if([' ','arrowup','arrowdown','arrowleft','arrowright'].includes(k))e.preventDefault();
 if(k===' '){startGame();shoot()}
 if(k==='escape'&&started&&!gameOver){paused=!paused;sound(paused?150:350,.08,'triangle',.025)}
 if(k==='r'){reset()}
 if(k==='e'&&started&&!gameOver&&!paused)collect();
 if(k==='m'){muted=!muted;if(!muted)sound(520,.08,'sine',.025)}
 if(k==='enter'&&(!started||gameOver)){if(gameOver)reset();started=true}
});
window.addEventListener('keyup',e=>keys[e.key.toLowerCase()]=false);
function collect(){
 let nearest=-1,dist=48;
 crates.forEach((c,i)=>{let d=Math.hypot(c.x-player.x,c.y-player.y);if(d<dist){dist=d;nearest=i}});
 if(nearest>=0){const c=crates.splice(nearest,1)[0];ammo+=18;health=Math.min(100,health+20);stamina=Math.min(100,stamina+25);score+=25;burst(c.x,c.y,'#76e5a4',16);sound(600,.16,'sine',.04,250);spawnCrate();}
}
function update(dt){
 if(!started||paused||gameOver)return;
 let dx=0,dy=0;
 if(keys.w||keys.arrowup)dy--;if(keys.s||keys.arrowdown)dy++;
 if(keys.a||keys.arrowleft)dx--;if(keys.d||keys.arrowright)dx++;
 if(dx||dy){let l=Math.hypot(dx,dy);dx/=l;dy/=l;player.x+=dx*player.speed*dt;player.y+=dy*player.speed*dt;stamina=Math.max(0,stamina-7*dt)}
 else stamina=Math.min(100,stamina+12*dt);
 if(keys.shift&&stamina>0&&(dx||dy)){player.x+=dx*100*dt;player.y+=dy*100*dt;stamina=Math.max(0,stamina-18*dt)}
 player.x=clamp(player.x,player.r+8,W-player.r-8);player.y=clamp(player.y,player.r+8,H-player.r-8);
 player.angle=Math.atan2(mouse.y-player.y,mouse.x-player.x);player.invuln=Math.max(0,player.invuln-dt);
 if(mouse.down&&Math.random()<dt*8)shoot();
 bullets=bullets.filter(b=>{b.x+=b.vx*dt;b.y+=b.vy*dt;b.life-=dt;return b.life>0&&b.x>-10&&b.x<W+10&&b.y>-10&&b.y<H+10});
 spawnTimer-=dt;
 if(spawnTimer<=0){spawnZombie();spawnTimer=Math.max(.35,1.4-wave*.07)}
 for(let z of zombies){
  const a=Math.atan2(player.y-z.y,player.x-z.x),d=Math.hypot(player.x-z.x,player.y-z.y);
  // Zombies actively chase the player and steer around one another slightly.
  z.x+=Math.cos(a)*z.speed*dt;z.y+=Math.sin(a)*z.speed*dt;z.wob+=dt*5;
  if(d<z.r+player.r+2&&z.attack<=0&&player.invuln<=0){health-=10;player.invuln=.55;z.attack=.65;sound(85,.12,'sawtooth',.04,-35);burst(player.x,player.y,'#d9534f',5)}
  z.attack=Math.max(0,z.attack-dt);
 }
 for(let b of bullets){for(let z of zombies){if(z.hp>0&&Math.hypot(b.x-z.x,b.y-z.y)<z.r+4){z.hp=0;b.life=0;score+=10;burst(z.x,z.y,'#8ab56e',8);sound(270,.035,'triangle',.018);break}}}
 zombies=zombies.filter(z=>z.hp>0);
 particles=particles.filter(p=>{p.x+=p.vx*dt;p.y+=p.vy*dt;p.vx*=.96;p.vy*=.96;p.life-=dt;return p.life>0});
 if(health<=0){health=0;gameOver=true;sound(70,.5,'sawtooth',.05,-45)}
 if(score>=wave*120){wave++;health=Math.min(100,health+8);ammo+=10;sound(520,.2,'triangle',.04,250);for(let i=0;i<2;i++)spawnCrate()}
}
function background(){
 ctx.fillStyle='#111b19';ctx.fillRect(0,0,W,H);
 // cracked, overgrown asphalt
 for(let x=0;x<W;x+=54)for(let y=0;y<H;y+=54){
  ctx.strokeStyle=((x+y)/54)%2?'#1b2924':'#192520';ctx.lineWidth=1;ctx.strokeRect(x,y,54,54);
 }
 for(let i=0;i<16;i++){
  let x=(i*173+47)%W,y=(i*97+29)%H;
  ctx.fillStyle='#202b24';ctx.fillRect(x,y,rand(18,44),rand(9,24));
  ctx.strokeStyle='#354138';ctx.beginPath();ctx.moveTo(x+3,y+4);ctx.lineTo(x+rand(6,35),y+rand(6,20));ctx.stroke();
 }
 // ruined perimeter silhouettes
 ctx.fillStyle='#0a100f';
 for(let x=0;x<W;x+=90){let h=rand(18,43);ctx.fillRect(x,0,rand(28,55),h);ctx.fillRect(x,H-h,rand(30,60),h)}
 const g=ctx.createRadialGradient(W/2,H/2,80,W/2,H/2,610);g.addColorStop(0,'#0000');g.addColorStop(1,'#000b');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
}
function drawPlayer(){
 ctx.save();ctx.translate(player.x,player.y);ctx.rotate(player.angle);
 ctx.fillStyle='#b7c8be';ctx.beginPath();ctx.arc(0,0,player.r,0,Math.PI*2);ctx.fill();
 ctx.fillStyle='#283a32';ctx.fillRect(0,-6,24,12);
 ctx.fillStyle='#e3b36b';ctx.fillRect(11,-3,15,6);
 ctx.restore();
 if(player.invuln>0&&Math.floor(player.invuln*20)%2===0){ctx.strokeStyle='#ff6868';ctx.lineWidth=3;ctx.beginPath();ctx.arc(player.x,player.y,22,0,Math.PI*2);ctx.stroke()}
}
function drawZombie(z){
 ctx.save();ctx.translate(z.x,z.y);ctx.rotate(Math.sin(z.wob)*.08);
 ctx.fillStyle='#536c4c';ctx.beginPath();ctx.arc(0,0,z.r,0,Math.PI*2);ctx.fill();
 ctx.fillStyle='#28352a';ctx.fillRect(-z.r*.65,-z.r*.2,z.r*1.3,z.r*.65);
 ctx.fillStyle='#f3d58b';ctx.fillRect(-z.r*.45,-z.r*.35,4,4);ctx.fillRect(z.r*.1,-z.r*.35,4,4);
 ctx.strokeStyle='#a9bb9b';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(-z.r*.5,z.r*.5);ctx.lineTo(-z.r*1.1,z.r*.95);ctx.moveTo(z.r*.5,z.r*.5);ctx.lineTo(z.r*1.1,z.r*.85);ctx.stroke();
 ctx.restore();
}
function draw(){
 background();
 // supplies
 crates.forEach(c=>{c.bob+=.04;ctx.save();ctx.translate(c.x,c.y+Math.sin(c.bob)*2);ctx.fillStyle='#8e6337';ctx.fillRect(-12,-10,24,20);ctx.strokeStyle='#edc27c';ctx.lineWidth=2;ctx.strokeRect(-12,-10,24,20);ctx.fillStyle='#d9f0b1';ctx.fillRect(-3,-7,6,14);ctx.fillRect(-7,-3,14,6);ctx.restore()});
 bullets.forEach(b=>{ctx.fillStyle='#ffd27a';ctx.beginPath();ctx.arc(b.x,b.y,3,0,Math.PI*2);ctx.fill()});
 zombies.forEach(drawZombie);drawPlayer();
 particles.forEach(p=>{ctx.globalAlpha=Math.max(0,p.life/p.max);ctx.fillStyle=p.color;ctx.fillRect(p.x,p.y,3,3)});ctx.globalAlpha=1;
 // HUD
 ctx.fillStyle='#070b0acc';ctx.fillRect(14,14,300,94);ctx.strokeStyle='#405249';ctx.strokeRect(14,14,300,94);
 ctx.fillStyle='#e7eee9';ctx.font='bold 17px Arial';ctx.fillText('LAST STAND',27,38);
 ctx.font='13px Arial';ctx.fillStyle='#b8c5be';ctx.fillText('SCORE  '+score+'     WAVE  '+wave+'     ZOMBIES  '+zombies.length,27,59);
 ctx.fillText('HEALTH',27,80);ctx.fillStyle='#432b2b';ctx.fillRect(88,69,105,12);ctx.fillStyle=health>35?'#70c77e':'#e05c56';ctx.fillRect(88,69,105*health/100,12);
 ctx.fillStyle='#b8c5be';ctx.fillText('AMMO  '+ammo,210,80);ctx.fillText('STAMINA',27,99);ctx.fillStyle='#273c36';ctx.fillRect(88,89,105,8);ctx.fillStyle='#72bde3';ctx.fillRect(88,89,105*stamina/100,8);
 ctx.textAlign='right';ctx.fillStyle=muted?'#e6a5a5':'#9de0b0';ctx.fillText(muted?'SOUND OFF (M)':'SOUND ON (M)',W-18,25);ctx.textAlign='left';
 if(!started||gameOver||paused){
  ctx.fillStyle='#030706c9';ctx.fillRect(0,0,W,H);
  ctx.textAlign='center';
  if(!started){ctx.fillStyle='#e5eee8';ctx.font='bold 46px Arial';ctx.fillText('LAST STAND',W/2,H/2-70);ctx.fillStyle='#a5b7ad';ctx.font='19px Arial';ctx.fillText('THE CITY HAS FALLEN. YOU HAVE NOT.',W/2,H/2-34);ctx.fillStyle='#f1c67b';ctx.font='bold 20px Arial';ctx.fillText('CLICK OR PRESS ENTER TO START',W/2,H/2+28);ctx.fillStyle='#bac6bf';ctx.font='15px Arial';ctx.fillText('Move • Aim • Shoot • Collect supplies • Survive the waves',W/2,H/2+62)}
  else if(gameOver){ctx.fillStyle='#f07870';ctx.font='bold 44px Arial';ctx.fillText('YOU WERE OVERRUN',W/2,H/2-40);ctx.fillStyle='#e8eee9';ctx.font='22px Arial';ctx.fillText('Final score: '+score+'  |  Wave: '+wave,W/2,H/2+2);ctx.fillStyle='#f1c67b';ctx.font='bold 19px Arial';ctx.fillText('PRESS R OR ENTER TO TRY AGAIN',W/2,H/2+49)}
  else{ctx.fillStyle='#e5eee8';ctx.font='bold 44px Arial';ctx.fillText('PAUSED',W/2,H/2-10);ctx.fillStyle='#f1c67b';ctx.font='19px Arial';ctx.fillText('PRESS ESC TO RESUME',W/2,H/2+32)}
  ctx.textAlign='left';
 }
}
function loop(t){let dt=Math.min(.033,(t-lastTime)/1000||0);lastTime=t;update(dt);draw();requestAnimationFrame(loop)}
reset();requestAnimationFrame(loop);
})();
</script>
</body>
</html>
""", height=720, scrolling=False)

st.markdown('<div class="help">Tip: walk close to a supply crate and press <b>E</b> to restore health and ammo. Zombies follow your position, so keep moving!</div>', unsafe_allow_html=True)
