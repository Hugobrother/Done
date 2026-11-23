#!/bin/sh
# Encode les images rendues par render.py en vidéos (H.264 + WebM) dans ../public
set -e
cd "$(dirname "$0")"
enc() { k=$1; sz=$2
  VF="scale=$sz:flags=lanczos:in_color_matrix=bt601:in_range=full:out_color_matrix=bt709:out_range=tv,format=yuv420p"
  CM="-colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv"
  ffmpeg -y -loglevel error -framerate 60 -i .cap/$k/f_%04d.jpg -vf "$VF" -c:v libx264 -preset slow -crf 21 -profile:v high -level 4.2 -g 60 -bf 2 $CM -movflags +faststart -an ../public/film-$k.mp4
  ffmpeg -y -loglevel error -framerate 60 -i .cap/$k/f_%04d.jpg -vf "$VF" -c:v libvpx-vp9 -crf 33 -b:v 0 -g 60 -row-mt 1 -cpu-used 3 -deadline good $CM -an ../public/film-$k.webm
}
enc wide 1920:800
enc tall 1080:1460
