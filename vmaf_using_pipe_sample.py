import subprocess
import cv2 as cv
import time
import os

sr_pipe = '/data/home/mckim/tmp/sr_pipe'
hr_pipe = '/data/home/mckim/tmp/hr_pipe'

os.mkfifo(sr_pipe)
os.mkfifo(hr_pipe)

sr_image_path = '/data/home/mckim/Eagle/VMAF-Tester/Eagle_result/test_sphere_view_SR_(3).png'
hr_image_path = '/data/home/mckim/Eagle/VMAF-Tester/Eagle_result/test_sphere_view_(315,45).png'

sr_image = cv.imread(sr_image_path)
sr_image  = cv.cvtColor(sr_image, cv.COLOR_BGR2RGB)

hr_image = cv.imread(hr_image_path)
hr_image = cv.cvtColor(hr_image, cv.COLOR_BGR2RGB)

# ffmpeg 명령 구성
cmd = [
    'ffmpeg', '-hide_banner', '-loglevel', 'error',
    '-f', 'rawvideo', '-pixel_format', 'rgb24', '-video_size', '1280x1280', '-i', sr_pipe,
    '-f', 'rawvideo', '-pixel_format', 'rgb24', '-video_size', '1280x1280', '-i', hr_pipe,
    '-filter_complex', f'[0:v][1:v]libvmaf=feature=name=psnr|name=float_ssim:model=path=/data/home/mckim/Eagle/VMAF-Tester/vmaf/model/vmaf_v0.6.1.json\\\\:enable_transform=true:log_fmt=json:log_path=/dev/stdout:n_threads=6',
    '-f', 'null', '-'
]

# subprocess.Popen을 사용하여 ffmpeg 프로세스 시작
proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


startTime = time.time()
with open(sr_pipe, 'wb') as f:
    f.write(sr_image)

with open(hr_pipe, 'wb') as f:
    f.write(hr_image)
print("time: ", time.time() - startTime)

# 프로세스 종료 및 출력 결과 읽기
stdout, stderr = proc.communicate()
print(stdout.decode())
print(stderr.decode())

os.remove(sr_pipe)
os.remove(hr_pipe)

