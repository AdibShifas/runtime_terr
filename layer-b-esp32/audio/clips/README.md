# Audio Clips Folder

Drop your audio clips here!

## Naming Convention

Name your files to match entries in `clip_manifest.json`:

```
boot_low.mp3
boot_mid.mp3
boot_high.mp3
collision_low_1.mp3
collision_low_2.mp3
collision_mid_1.mp3
...
```

## Alternative Naming

You can also use this format (auto-detected):
```
BOOT_0.mp3        # BOOT, tier 0
COLLISION_2_1.mp3 # COLLISION, tier 2, variant 1
STUCK_1.mp3       # STUCK, tier 1
```

## Supported Formats

- `.mp3` (recommended)
- `.wav`
- `.ogg`

## Testing

After adding clips, run from the `layer-b-esp32` folder:

```bash
python3 -c "from audio_cache import AudioCache; c = AudioCache(); print(c.list_clips())"
```
