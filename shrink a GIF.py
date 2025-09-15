from PIL import Image, ImageSequence

def compress_gif(input_path, output_path,
                 resize_scale=0.5,
                 max_colors=64,
                 frame_skip=2,
                 loop=0):
    """
    Compress a GIF file to reduce size.

    Args:
        input_path (str): Path to input GIF
        output_path (str): Path to save compressed GIF
        resize_scale (float): Scale down size (e.g., 0.5 = half resolution)
        max_colors (int): Max number of colors (reduce palette)
        frame_skip (int): Keep every nth frame (drop others)
        loop (int): 0 for infinite loop, 1+ for specific loops
    """
    gif = Image.open(input_path)
    frames = []
    frame_durations = []

    for i, frame in enumerate(ImageSequence.Iterator(gif)):
        if i % frame_skip != 0:
            continue  # skip frames

        # Resize
        w, h = frame.size
        frame = frame.resize(
            (int(w * resize_scale), int(h * resize_scale)),
            Image.Resampling.LANCZOS
        )

        # Reduce colors (adaptive palette)
        frame = frame.convert("P", palette=Image.ADAPTIVE, colors=max_colors)

        frames.append(frame)
        frame_durations.append(frame.info.get('duration', 100))

    # Save compressed GIF
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=frame_durations,
        loop=loop,
        optimize=True,
        disposal=2
    )

    print(f"✅ Compressed GIF saved at {output_path}")


# Example usage:
compress_gif(
    "input.gif",
    "compressed.gif",
    resize_scale=0.3,   # shrink resolution
    max_colors=32,      # reduce palette
    frame_skip=3        # drop frames
)
