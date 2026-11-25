import sys,os,subprocess,re,glob
d=sys.argv[1]; name=os.path.basename(d)[2:]
out=f'/tmp/edit/out_y/{name}.mp4'
if os.path.exists(out): sys.exit(0)
os.makedirs('/tmp/edit/out_y',exist_ok=True)
ass=open(d+'/cap.ass',encoding='utf-8').read().replace('&H1409E5&','&H00D7FF&')
open(d+'/cap_y.ass','w',encoding='utf-8').write(ass)
dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',d+'/cat.mp4'],capture_output=True,text=True).stdout)
TOTAL=dur
fc=[f"[0:v]tpad=stop_mode=clone:stop_duration=0.5,ass={d}/cap_y.ass:fontsdir=/usr/share/fonts/truetype/dejavu[vo]",
 "[0:a]highpass=f=90,acompressor=threshold=0.1:ratio=3:attack=5:release=80:makeup=2,loudnorm=I=-16:TP=-2:LRA=7,apad=pad_dur=0.5[voice]",
 f"[1:a]atrim=0:{TOTAL+0.5:.2f},asetpts=PTS-STARTPTS,volume=-8.5dB,afade=t=in:d=2.5,afade=t=out:st={max(TOTAL-2.6,0):.2f}:d=2.6[mus]",
 "[voice][mus]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.89[ao]"]
tmp=out+'.tmp.mp4'
subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-i',d+'/cat.mp4','-i','/tmp/edit/music.wav','-filter_complex',';'.join(fc),'-map','[vo]','-map','[ao]','-c:v','libx264','-preset','slow','-crf','17','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-c:a','aac','-b:a','192k','-movflags','+faststart',tmp],check=True)
os.rename(tmp,out); print('OK',name,flush=True)
