# 하루 연기 팁 — 빈칸 대사 퀴즈 릴스 템플릿 (2026-11-28 대표 승인 형식). LINES, HOOK, 팁 장면 문구만 바꿔서 매주 사용. 출력 경로(out)는 실행 환경에 맞게 수정.
from PIL import Image, ImageDraw, ImageFont
import subprocess, math
B='/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'; BD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'; R='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
_fc={}
def F(p,s):
    if (p,s) not in _fc: _fc[(p,s)]=ImageFont.truetype(p,s,index=1)
    return _fc[(p,s)]
BG=(245,245,240); FG=(10,10,10); AC=(22,130,70); SUB=(86,89,98); BOX=(255,255,255); LINE=(225,222,218); BLANK=(214,236,222)
W,H=1080,1920; L=90; FPS=30
def ease(x): x=max(0,min(1,x)); return 1-(1-x)**3
def back(x):
    x=max(0,min(1,x)); c=1.70158; return 1+(c+1)*(x-1)**3+c*(x-1)**2
def tag(d,text='화이트 챌린지'):
    f=F(BD,34); tw=d.textlength(text,font=f)
    d.rounded_rectangle((L,250,L+tw+40,310),radius=30,outline=AC,width=3); d.text((L+20,258),text,font=f,fill=AC)
def pop(im,text,font,xy,t,color,delay=0,dur=0.5):
    p=(t-delay)/dur
    if p<=0: return 0
    s=0.7+0.3*back(p); a=int(255*ease(p*1.5))
    d0=ImageDraw.Draw(im); w=int(d0.textlength(text,font=font))+10; h=int(font.size*1.45)
    lay=Image.new('RGBA',(w,h),(0,0,0,0)); ImageDraw.Draw(lay).text((0,0),text,font=font,fill=color+(a,))
    lay=lay.resize((max(1,int(w*s)),max(1,int(h*s))),Image.LANCZOS)
    im.paste(lay,(int(xy[0]),int(xy[1]+(h-lay.height)/2)),lay); return w
def rich(im,parts,x,y,size,t,delay):
    for txt,acc in parts:
        f=F(B,size); pop(im,txt,f,(x,y),t,AC if acc else FG,delay); x+=ImageDraw.Draw(im).textlength(txt,font=f)
# 직접 쓴 예시 대사 (실제 작품 아님)
LINES=[('민호','나 오늘 오디션 ','붙었어','.'),('지수','진짜? 무슨 ','역할','인데?'),('민호','대사 세 줄. 그래도 ','이름','은 있어.')]
def ring(d,cx,cy,r,frac,num):
    d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=LINE,width=14)
    if frac>0: d.arc((cx-r,cy-r,cx+r,cy+r),-90,-90+360*frac,fill=AC,width=14)
    f=F(B,int(r*1.1)); tw=d.textlength(num,font=f); d.text((cx-tw/2,cy-r*0.78),num,font=f,fill=FG)
def script(d,y,mode,t=0):
    """mode: show / blank / reveal(t)"""
    d.rounded_rectangle((L,y,W-L,y+470),radius=28,fill=BOX,outline=LINE,width=3)
    f=F(BD,50)
    for i,(n,a,k,b) in enumerate(LINES):
        ly=y+60+i*130; x=L+40
        d.text((x,ly),n,font=F(BD,44),fill=SUB); x=L+170
        d.text((x,ly),a,font=f,fill=FG); x+=d.textlength(a,font=f)
        kw=d.textlength(k,font=f)
        if mode=='show':
            d.text((x,ly),k,font=f,fill=FG)
        else:
            shown = mode=='reveal' and t>0.4+i*0.9
            if shown:
                p=ease((t-0.4-i*0.9)/0.3)
                d.rounded_rectangle((x-8,ly+2,x+kw+8,ly+70),radius=10,fill=BLANK)
                d.text((x,ly),k,font=f,fill=AC)
                cx=W-L-60; d.ellipse((cx-26,ly+10,cx+26,ly+62),fill=AC)
                if p>0.3: d.line([(cx-12,ly+36),(cx-3,ly+46),(cx+14,ly+24)],fill=(255,255,255),width=6)
            else:
                d.rounded_rectangle((x-4,ly+8,x+kw+4,ly+66),radius=10,fill=LINE)
                d.text((x+kw/2-14,ly+2),'?',font=f,fill=SUB)
        x+=kw; d.text((x,ly),b,font=f,fill=FG)
# ---- 장면 ----
HOOK=[('하루 연기 팁',[('대사 외우는 데',False)],[('하루',True),(' 넘게 걸려?',False)],'3초 테스트부터 해 봐')]
def s1(t):  # 훅: 첫 프레임부터 대상이 바로 보이게(튀어나오기 없이 고정)
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
    who,l1,l2,act=HOOK[0]
    f=F(B,52); tw=d.textlength(who,font=f)
    d.rounded_rectangle((L,430,L+tw+60,530),radius=50,fill=AC); d.text((L+30,440),who,font=f,fill=(255,255,255))
    y=600
    for parts in (l1,l2):
        x=L
        for txt,acc in parts:
            ff=F(B,118); d.text((x,y),txt,font=ff,fill=AC if acc else FG); x+=d.textlength(txt,font=ff)
        y+=158
    pop(im,act,F(BD,56),(L,y+40),t,FG,delay=0.6)
    if t>1.2: d.text((L,y+140),'퀴즈 1개 + 외우는 법 4개',font=F(BD,44),fill=SUB)
    ring(d,W-L-110,1330,90,(t%1),'3')
    return im
def s2(t):  # 3초 외우기
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im); tag(d)
    d.text((L,420),'지금 외워!',font=F(B,84),fill=FG)
    script(d,600,'show')
    left=max(0,3-t); num=str(math.ceil(left)) if left>0 else '0'
    ring(d,W//2,1330,120,min(1,t/3),num)
    return im
def s3(t):  # 빈칸
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im); tag(d)
    d.text((L,420),'빈칸에 뭐였지?',font=F(B,84),fill=FG)
    script(d,600,'blank')
    d.text((L,1140),'속으로 말해 보고 넘어가',font=F(BD,44),fill=SUB)
    left=max(0,3-t); ring(d,W//2,1380,100,min(1,t/3),str(math.ceil(left)) if left>0 else '0')
    return im
def s4(t):  # 정답
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im); tag(d)
    d.text((L,420),'정답',font=F(B,84),fill=AC)
    script(d,600,'reveal',t)
    if t>3.2:
        p=ease((t-3.2)/0.4); d.text((L,1140+int((1-p)*20)),'핵심 단어만 빠져도 대사가 막혀.',font=F(BD,46),fill=FG)
    if t>3.8:
        d.text((L,1220),'빠진 건 전부 정보를 가진 단어야.',font=F(BD,42),fill=SUB)
        d.text((L,1285),'무슨 일? 붙었어 · 뭐? 역할 · 뭐가 있어? 이름',font=F(BD,40),fill=AC)
    return im
def s5(t):  # 결과
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im); tag(d)
    rich(im,[('몇 개',True),(' 맞혔어?',False)],L,470,110,t,0)
    if t>0.5:
        for i,txt in enumerate(['3개: 오디션 준비 끝','2개: 거의 다 왔어','0~1개: 같이 연습하자']):
            if t<0.5+i*0.35: break
            y=700+i*120; d.rounded_rectangle((L,y,W-L,y+100),radius=20,fill=BOX,outline=LINE,width=3)
            d.text((L+40,y+20),txt,font=F(BD,46),fill=FG)
    if t>1.8:
        p=ease((t-1.8)/0.4); d.text((L,1120+int((1-p)*20)),'막힌 데가 있었다면,',font=F(B,58),fill=FG)
        d.text((L,1200+int((1-p)*20)),'이렇게 외워 봐 ↓',font=F(B,58),fill=AC)
    return im
def tipbase(n,title,sub,t):
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im); tag(d,'외우는 법')
    d.text((L,380),f'TIP {n}/4',font=F(B,44),fill=AC)
    rich(im,[(title,False)],L,440,80,t,0)
    if t>0.4: d.text((L,560),sub,font=F(BD,40),fill=SUB)
    return im,d
def card(d,y,h): d.rounded_rectangle((L,y,W-L,y+h),radius=28,fill=BOX,outline=LINE,width=3)
def step(d,y,t,at,label,text,color=FG):
    if t<at: return
    p=ease((t-at)/0.4); x=L+int((1-p)*40)
    d.text((x,y),label,font=F(B,40),fill=AC); d.text((x+90,y),text,font=F(BD,44),fill=color)
def tip1(t):
    im,d=tipbase(1,'첫 글자만 남기기','다 가리지 말고, 힌트를 한 단계씩 줄여.',t)
    card(d,660,470); f=F(BD,52)
    rows=[('원래','나 오늘 오디션 붙었어.',0.6),('1단계','나 오.. 오.. 붙..',1.8),('2단계','나 .. .. ..',3.2),('0단계','(아무것도 안 보고)',4.4)]
    for i,(lab,txt,at) in enumerate(rows):
        if t<at: break
        y=690+i*108; d.text((L+40,y+8),lab,font=F(BD,34),fill=SUB)
        d.text((L+190,y),txt,font=f,fill=AC if i else FG)
    if t>5.4: d.text((L,1170),'0단계까지 가면 진짜 외운 거야.',font=F(B,48),fill=FG)
    return im
def tip2(t):
    im,d=tipbase(2,'핵심 단어부터','방금 퀴즈 빈칸 같은 단어가 기둥이야.',t)
    card(d,660,400); f=F(BD,48)
    for i,(n,a,k,b) in enumerate(LINES):
        ly=700+i*115; x=L+40; d.text((x,ly),a,font=f,fill=FG); x+=d.textlength(a,font=f)
        kw=d.textlength(k,font=f); on=t>0.6+i*0.4
        if on: d.rounded_rectangle((x-6,ly+4,x+kw+6,ly+68),radius=10,fill=BLANK)
        d.text((x,ly),k,font=f,fill=AC if on else FG); x+=kw; d.text((x,ly),b,font=f,fill=FG)
    step(d,1110,t,2.4,'①','기둥만 소리 내기: 붙었어-역할-이름')
    step(d,1190,t,3.8,'②','사이를 채워서 문장으로')
    step(d,1270,t,5.0,'③','기둥 순서 = 장면이 흘러가는 순서')
    return im
def tip3(t):
    im,d=tipbase(3,'상대 대사를 신호로','내 대사만 외우면 장면에서 끊겨.',t)
    card(d,660,340); f=F(BD,48)
    d.text((L+40,700),'지수',font=F(BD,38),fill=SUB); d.text((L+160,700),'진짜? 무슨 ',font=f,fill=FG)
    x=L+160+d.textlength('진짜? 무슨 ',font=f)
    d.text((x,700),'역할인데?',font=f,fill=AC if t>0.9 else FG)
    if t>0.9:
        p=ease((t-0.9)/0.5); xx=L+90; d.line((xx,775,xx,775+int(110*p)),fill=AC,width=8)
        if p>0.95: d.polygon([(xx-18,880),(xx+18,880),(xx,905)],fill=AC)
    if t>1.5: d.text((L+40,920),'민호',font=F(BD,38),fill=SUB); d.text((L+160,920),'대사 세 줄. 그래도…',font=f,fill=AC)
    step(d,1060,t,2.6,'①','상대 대사 끝 단어에 밑줄')
    step(d,1140,t,3.8,'②','상대 대사만 녹음해 두기')
    step(d,1220,t,5.0,'③','내 차례는 비워 두고 맞춰 말하기')
    return im
def tip4(t):
    im,d=tipbase(4,'나눠서, 자고 나서','몰아서 한 번보다 나눠서 세 번.',t)
    card(d,660,400)
    pts=[('밤','소리 내서 3번',0.6),('아침','안 보고 1번 → 막힌 곳 표시',1.8),('이동 중','막힌 곳만 첫 글자 힌트로',3.0)]
    for i,(when,what,at) in enumerate(pts):
        if t<at: break
        y=700+i*115; d.ellipse((L+40,y+16,L+78,y+54),fill=AC)
        d.text((L+105,y),when,font=F(B,46),fill=FG); d.text((L+300,y+4),what,font=F(BD,42),fill=SUB)
    if t>4.4: d.text((L,1110),'나는 자고 일어나서 확인할 때',font=F(BD,46),fill=FG)
    if t>5.0: d.text((L,1180),'제일 오래 남더라.',font=F(B,52),fill=AC)
    return im
def s_end(t):
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im); tag(d,'오늘 5분 처방')
    rich(im,[('저장',True),('해 두고',False)],L,520,110,t,0)
    rich(im,[('다음 대본 때',False)],L,680,110,t,0.3)
    rich(im,[('써 봐',False)],L,840,110,t,0.6)
    if t>1.4:
        d.line((L,1060,W-L,1060),fill=LINE,width=3)
        d.text((L,1090),'1 첫 글자  2 핵심 단어  3 상대 신호  4 밤·아침',font=F(BD,40),fill=FG)
        d.text((L,1160),'종이로 해도 되고, 앱으로 해도 돼.',font=F(BD,40),fill=SUB)
    if t>2.4: d.text((L,1280),'오디션 앞둔 친구한테 보내 봐 →',font=F(B,50),fill=AC)
    return im
def slow(fn,k=1.5): return lambda t: fn(t/k)
SC=[(slow(s1),4.0),(s2,3.4),(s3,3.6),(slow(s4),6.6),(slow(s5),6.0),(tip1,7.0),(tip2,7.0),(tip3,7.0),(tip4,7.0),(slow(s_end),7.0)]
TOTAL=sum(x for _,x in SC); TR=0.5
def render(T):
    acc=0
    for i,(fn,dur) in enumerate(SC):
        if T<acc+dur or i==len(SC)-1:
            t=T-acc; cur=fn(t)
            if i>0 and t<TR:
                prev=SC[i-1][0](SC[i-1][1]); p=ease(t/TR); off=int(W*p)
                fr=Image.new('RGB',(W,H),BG); fr.paste(prev,(-off,0)); fr.paste(cur,(W-off,0)); cur=fr
            break
        acc+=dur
    d=ImageDraw.Draw(cur); d.rectangle((0,0,int(W*T/TOTAL),10),fill=AC)
    d.text((L,1500),'@actmate_official',font=F(R,34),fill=SUB)
    return cur
out='/home/claude/reels2/quiz6.mp4'
p=subprocess.Popen(['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',out],stdin=subprocess.PIPE)
keys={0}
for k in range(int(TOTAL*FPS)):
    fr=render(k/FPS); p.stdin.write(fr.tobytes())
    if k in keys: fr.save(f'/home/claude/reels2/g{k:04d}.png')
p.stdin.close(); p.wait(); print('done',TOTAL)
