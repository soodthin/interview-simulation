import os
import sys
import subprocess
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FFMPEG = r"D:\Project\MakingMoneyWithVideo\.venv\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
AUDIO = os.path.join(BASE_DIR, "interview_audio.mp3")
DATA_FILE = os.path.join(BASE_DIR, "interview_data.json")
OUTPUT_MP4 = os.path.join(BASE_DIR, "Esco_AV_Interview_Master.mp4")

def generate_ass_subtitles(data, ass_path):
    header = """[Script Info]
Title: Esco AV Interview Simulation - Thai Do Thinh
ScriptType: v4.00+
WrapStyle: 2
PlayResX: 1920
PlayResY: 1080
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Speaker_Interviewer,Arial,34,&H00FFF2A0,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,3.5,1.5,2,60,60,40,1
Style: Speaker_Thinh,Arial,34,&H007DFEA0,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,3.5,1.5,2,60,60,40,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    def sec_to_ass(s):
        h = int(s // 3600)
        m = int((s % 3600) // 60)
        sec = s % 60
        return f"{h}:{m:02d}:{sec:05.2f}"

    for d in data.get("dialogues", []):
        st = sec_to_ass(d["start"])
        et = sec_to_ass(d["end"])
        style = "Speaker_Interviewer" if d["speaker"] == "interviewer" else "Speaker_Thinh"
        speaker_tag = "{\\b1\\c&H0038BDF8&}[Interviewer]: {\\c&H00FFFFFF&}" if d["speaker"] == "interviewer" else "{\\b1\\c&H0034D399&}[Thái Đỗ Thịnh]: {\\c&H00FFFFFF&}"
        text_en = d["text_en"].replace("'", "\\'")
        text_vi = d["text_vi"].replace("'", "\\'")
        line = f"Dialogue: 0,{st},{et},{style},,0,0,0,,{speaker_tag}{text_en}\\N{{\\fs24\\c&H00E2E8F0&\\i1}}({text_vi}){{\\i0}}"
        events.append(line)

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events))
    print(f"✅ Generated ASS subtitle file: {ass_path}")

def render_sample(duration=30):
    """Render a fast sample video for verification"""
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    ass_path = os.path.join(BASE_DIR, "interview_subtitles.ass")
    generate_ass_subtitles(data, ass_path)

    # Escape path for FFmpeg filter on Windows
    ass_filter_path = ass_path.replace("\\", "/").replace(":", "\\:")
    output_sample = os.path.join(BASE_DIR, f"Esco_AV_Interview_Preview_{duration}s.mp4")

    print(f"🎬 Rendering {duration}s preview video...")
    # Generate background with dynamic audio visualizer and burned subtitles
    cmd = [
        FFMPEG, "-y",
        "-ss", "0.0", "-t", str(duration),
        "-i", AUDIO,
        "-f", "lavfi", "-i", f"color=c=#0b1329:s=1920x1080:r=30:d={duration}",
        "-filter_complex",
        f"[0:a]showwaves=s=1280x160:mode=line:colors=0x38bdf8[wave];"
        f"[1:v][wave]overlay=(W-w)/2:H-260[bg_wave];"
        f"[bg_wave]drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='ESCO AV VIETNAM // SMART MEETING ROOM 302':x=(w-text_w)/2:y=60:fontsize=32:fontcolor=0x38bdf8,"
        f"drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='IT SUPPORT & AV SYSTEMS INTERVIEW SIMULATION - THAI DO THINH':x=(w-text_w)/2:y=105:fontsize=22:fontcolor=0x94a3b8,"
        f"subtitles='{ass_filter_path}'[v]",
        "-map", "[v]",
        "-map", "0:a",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-profile:v", "high",
        "-level", "4.1",
        "-c:a", "aac",
        "-b:a", "192k",
        "-movflags", "+faststart",
        output_sample
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("❌ Error rendering preview:")
        print(res.stderr[-1000:])
    else:
        print(f"🎉 Success! Preview video generated at: {output_sample}")

if __name__ == "__main__":
    dur = 20
    if len(sys.argv) > 1:
        try:
            dur = int(sys.argv[1])
        except ValueError:
            pass
    render_sample(dur)
