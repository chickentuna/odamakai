import os
import datetime
import sys

format = '%H:%M:%S.%f'

#TODO: final video is too long

movie = sys.argv[1] if len(sys.argv) > 1 else 'Movie.mkv'
output = sys.argv[2] if len(sys.argv) > 2 else 'Mux.mp4'

if not os.path.exists('out'):
  os.mkdir('out')

if ' ' in movie:
  print('no spaces please')
  exit(1)

if not os.path.exists(movie):
  print(f'Cannot find file {movie}')
  exit(1)

def minus(start, end):
  startDateTime = datetime.datetime.strptime(start, format)
  endDateTime = datetime.datetime.strptime(end, format)
  diff = endDateTime - startDateTime
  return diff

if not os.path.exists(f'{movie}_subs.srt'):
  os.system(f'ffmpeg -i {movie} -map 0:s:0 {movie}_subs.srt')

file = open(f'{movie}_subs.srt')
lines = file.readlines()
timestamps = []

current = '00:00:00.000'

for raw in filter(lambda t: '-->' in t, lines):
  fromT, toT = raw.replace(',', '.').strip().split(' --> ')
  timestamps.append([current, fromT])
  current = toT

os.system(f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 -sexagesimal {movie} > length.txt')
endT = open('length.txt').readline().strip()
timestamps.append([current, endT])


idx = 0
for t in timestamps:
  duration = minus(t[0], t[1])
  
  if duration != '00:00:00.000':
    if not os.path.exists(f'out/{movie}{idx}.mp4'):
      os.system(f'ffmpeg -ss {t[0]} -i {movie} -t {duration} -c:v libx264 -c:a aac -strict experimental -b:a 128k out/{movie}{idx}.mp4')
  idx += 1

file = open('inputs.txt', 'w')
for i in range(1, idx):
  print(f'file out/{movie}{i}.mp4', file=file)

if not os.path.exists(f'{output}'):
  os.system(f'ffmpeg -f concat -i inputs.txt -vcodec copy -acodec copy {output}')






# ffmpeg -i Movie.mkv -ss 00:00:03 -t 00:00:01 -async 1 cut.mkv
