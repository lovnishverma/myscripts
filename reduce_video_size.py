import subprocess
import os
import sys


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_FILE = "video.mp4"
OUTPUT_FILE = "video_100mb.mp4"

# Hard target
TARGET_SIZE_MB = 100

# Keep some safety margin
# 95 MB target gives room for MP4 overhead
ENCODE_TARGET_MB = 95

# Audio
AUDIO_KBPS = 64

# Output height
OUTPUT_HEIGHT = 1080

# NVIDIA HEVC
VIDEO_CODEC = "hevc_nvenc"

# NVENC preset
NVENC_PRESET = "p5"


# ============================================================
# RUN COMMAND
# ============================================================

def run_command(command):

    print("\nRunning:")
    print(" ".join(command))
    print()

    subprocess.run(command, check=True)


# ============================================================
# GET DURATION
# ============================================================

def get_duration(filename):

    command = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        filename
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=True
    )

    return float(result.stdout.strip())


# ============================================================
# MAIN
# ============================================================

def main():

    if not os.path.isfile(INPUT_FILE):
        print(f"ERROR: {INPUT_FILE} not found.")
        sys.exit(1)

    # --------------------------------------------------------
    # Check NVENC
    # --------------------------------------------------------

    print("Checking NVIDIA NVENC...")

    check = subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-encoders"
        ],
        capture_output=True,
        text=True
    )

    if "hevc_nvenc" not in check.stdout:

        print("\nERROR: hevc_nvenc is not available.")
        sys.exit(1)

    print("NVIDIA HEVC NVENC available.")

    # --------------------------------------------------------
    # Duration
    # --------------------------------------------------------

    duration = get_duration(INPUT_FILE)

    print("\n" + "=" * 65)
    print("NVIDIA GPU VIDEO COMPRESSION")
    print("=" * 65)

    print(f"Input       : {INPUT_FILE}")
    print(f"Duration    : {duration / 60:.2f} minutes")
    print(f"Hard limit  : {TARGET_SIZE_MB} MB")
    print(f"Encode size : {ENCODE_TARGET_MB} MB")
    print(f"Resolution  : 1080p")
    print(f"Codec       : HEVC NVENC")
    print(f"Preset      : {NVENC_PRESET}")

    # --------------------------------------------------------
    # BITRATE CALCULATION
    # --------------------------------------------------------

    target_bits = ENCODE_TARGET_MB * 1024 * 1024 * 8

    audio_bits = AUDIO_KBPS * 1000 * duration

    available_video_bits = target_bits - audio_bits

    video_bitrate_kbps = int(
        available_video_bits / duration / 1000
    )

    print(f"\nVideo bitrate: {video_bitrate_kbps} kbps")
    print(f"Audio bitrate: {AUDIO_KBPS} kbps")

    # --------------------------------------------------------
    # REMOVE OLD OUTPUT
    # --------------------------------------------------------

    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    # --------------------------------------------------------
    # PASS 1
    # --------------------------------------------------------

    print("\n" + "=" * 65)
    print("PASS 1")
    print("=" * 65)

    pass1 = [
        "ffmpeg",
        "-y",

        "-i", INPUT_FILE,

        # 4K -> 1080p
        "-vf", "scale=-2:1080",

        # NVIDIA HEVC
        "-c:v", VIDEO_CODEC,

        # STRICT bitrate
        "-rc", "cbr",
        "-b:v", f"{video_bitrate_kbps}k",
        "-maxrate", f"{video_bitrate_kbps}k",
        "-bufsize", f"{video_bitrate_kbps * 2}k",

        "-preset", NVENC_PRESET,

        # First pass
        "-pass", "1",

        # No audio
        "-an",

        # Windows null output
        "-f", "null",
        "NUL"
    ]

    run_command(pass1)

    # --------------------------------------------------------
    # PASS 2
    # --------------------------------------------------------

    print("\n" + "=" * 65)
    print("PASS 2")
    print("=" * 65)

    pass2 = [
        "ffmpeg",
        "-y",

        "-i", INPUT_FILE,

        # 4K -> 1080p
        "-vf", "scale=-2:1080",

        # NVIDIA HEVC
        "-c:v", VIDEO_CODEC,

        # STRICT bitrate
        "-rc", "cbr",
        "-b:v", f"{video_bitrate_kbps}k",
        "-maxrate", f"{video_bitrate_kbps}k",
        "-bufsize", f"{video_bitrate_kbps * 2}k",

        "-preset", NVENC_PRESET,

        # Second pass
        "-pass", "2",

        # Audio
        "-c:a", "aac",
        "-b:a", f"{AUDIO_KBPS}k",

        # MP4 optimization
        "-movflags", "+faststart",

        OUTPUT_FILE
    ]

    run_command(pass2)

    # --------------------------------------------------------
    # CLEANUP
    # --------------------------------------------------------

    for filename in [
        "ffmpeg2pass-0.log",
        "ffmpeg2pass-0.log.mbtree"
    ]:

        if os.path.exists(filename):
            os.remove(filename)

    # --------------------------------------------------------
    # FINAL SIZE
    # --------------------------------------------------------

    final_size_mb = (
        os.path.getsize(OUTPUT_FILE)
        / (1024 * 1024)
    )

    print("\n" + "=" * 65)
    print("COMPRESSION COMPLETE")
    print("=" * 65)

    print(f"Output file : {OUTPUT_FILE}")
    print(f"Final size  : {final_size_mb:.2f} MB")

    if final_size_mb <= TARGET_SIZE_MB:

        print("\nSUCCESS!")
        print(f"Video is below {TARGET_SIZE_MB} MB.")

    else:

        print("\nWARNING!")
        print("Output is still above the target.")


if __name__ == "__main__":
    main()