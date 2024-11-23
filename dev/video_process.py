import os
import subprocess
from pathlib import Path
import argparse

def compress_video(input_path, output_path):
  """Compress video using ffmpeg with specified parameters."""
  try:
    # Ensure the output file has an .mp4 extension
    if not str(output_path).endswith('.mp4'):
      output_path = str(output_path) + '.mp4'
    cmd = [
      'ffmpeg',
      '-i', str(input_path),
      '-vf', 'scale=min(1280\\,iw):-2',
      '-c:v', 'libx264',
      '-crf', '28',
      '-c:a', 'aac',
      '-b:a', '128k',
      str(output_path)
    ]
    subprocess.run(cmd, check=True)
    return True
  except subprocess.CalledProcessError as e:
    print(f"Error processing {input_path}: {e}")
    return False

def extract_thumbnail(input_path, output_path, time='00:00:01', size='320x240'):
    """Extract thumbnail from video at specified timestamp."""
    try:
        cmd = [
            'ffmpeg',
            '-i', str(input_path),
            '-ss', time,
            '-vframes', '1',
            '-vf', f'scale={size}',
            str(output_path)
        ]
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error extracting thumbnail for {input_path}: {e}")
        return False

def process_folder(folder_path):
  """Process all video files in the specified folder."""
  folder = Path(folder_path)
  video_extensions = ['.mp4', '.avi', '.mov', '.mkv']  # Add more if needed
  
  for file_path in folder.glob('*'):
    if file_path.suffix.lower() in video_extensions:
      # Setup paths
      base_name = file_path.name.replace(' ', '_')
      if args.output:
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / 'videos').mkdir(exist_ok=True)
        (output_dir / 'thumbs').mkdir(exist_ok=True)
        video_path = output_dir / f"videos/compressed_{base_name}"
        thumb_path = output_dir / f"thumbs/thumb_{base_name}.jpg"
      else:
        output_dir = file_path.parent
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / 'videos').mkdir(exist_ok=True)
        (output_dir / 'thumbs').mkdir(exist_ok=True)
        video_path = output_dir / f"compressed_{base_name}"
        thumb_path = output_dir / f"thumb_{base_name}.jpg"
      
      print(f"Processing: {file_path}")
      if compress_video(file_path, video_path):
        extract_thumbnail(file_path, thumb_path, 
                          time=args.thumb_time,
                          size=args.thumb_size)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Convert and compress video files')
  parser.add_argument('--input', required=True, help='Path to the folder containing video files')
  parser.add_argument('--output', required=False, help='Path to the output folder')
  parser.add_argument('--thumb-time', default='00:00:01', help='Timestamp for thumbnail extraction (HH:MM:SS)')
  parser.add_argument('--thumb-size', default='1280x720', help='Thumbnail dimensions (WxH)')
  args = parser.parse_args()
  process_folder(args.input)