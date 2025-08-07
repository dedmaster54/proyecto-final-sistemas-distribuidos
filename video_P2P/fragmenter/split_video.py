import os
import subprocess
import json

VIDEO_FILE = "video.mp4"
OUTPUT_DIR = "output"
NUM_PARTS = 10

def get_video_duration():
    """Obtiene la duración del video en segundos usando ffprobe."""
    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        VIDEO_FILE
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        output = json.loads(result.stdout)
        return float(output["format"]["duration"])
    except Exception as e:
        print("Error al obtener duración del video:", e)
        print("Salida de ffprobe:", result.stdout)
        exit(1)

def split_video():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    duration = get_video_duration()
    part_duration = duration / NUM_PARTS

    print(f"Duración total: {duration:.2f}s, cada fragmento: {part_duration:.2f}s")

    for i in range(NUM_PARTS):
        start_time = part_duration * i
        output_file = os.path.join(OUTPUT_DIR, f"fragment_{i+1}.mp4")
        cmd = [
            "ffmpeg",
            "-ss", str(start_time),
            "-i", VIDEO_FILE,
            "-t", str(part_duration),
            "-c", "copy",
            output_file
        ]
        print(f"Generando fragmento {i+1}...")
        subprocess.run(cmd)

    print("División completada.")

if __name__ == "__main__":
    split_video()


        

