#!/usr/bin/env python3
"""Check portable corpus integrity; optionally verify local screenshot hashes/samples."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import statistics


def audit(skill, source_dir=None):
    data = json.loads((skill / 'references/corpus.json').read_text(encoding='utf-8'))
    files = data['files']
    names = {f['filename'] for f in files}
    assert len(names) == len(files) == data['image_count'], 'Duplicate/missing source records'
    index = {f['filename']: f for f in files}
    palettes = data['palettes']
    assert len({p['id'] for p in palettes}) == len(palettes), 'Duplicate palette IDs'
    seen = set()
    color_count = 0
    for p in palettes:
        assert p['source'] in index, f"Unrecognized source: {p['id']}"
        seen.add(p['source'])
        assert p['colors'], f"Empty palette: {p['id']}"
        record = index[p['source']]
        assert p['id'] in record['palette_ids'], 'Palette/source index mismatch'
        for c in p['colors']:
            color_count += 1
            for key in ('hex', 'printed_hex', 'sampled_hex'):
                value = c[key]
                assert value is None or re.fullmatch(r'#[0-9A-F]{6}', value), f'Invalid color: {value}'
            assert c['hex'] is not None, 'Missing usable color'
            origin = c['origin']
            assert origin in ('printed_hex', 'sampled_swatch', 'adapted_anchor'), 'Unknown provenance'
            if origin == 'printed_hex':
                assert c['hex'] == c['printed_hex'], 'Printed color was silently changed'
            elif origin == 'sampled_swatch':
                assert c['hex'] == c['sampled_hex'] and c['note'], 'Sampled correction missing evidence'
            else:
                assert c['printed_hex'] is None and c['note'], 'Adaptation confused with source label'
            xy = c['sample_xy']
            if c['sampled_hex']:
                assert xy is not None, 'Sample lacks location'
                assert 6 <= xy[0] < record['width_px']-6 and 6 <= xy[1] < record['height_px']-6, 'Sample outside image'
    assert seen == names, 'Some images have no extracted palette'
    for f in files:
        assert re.fullmatch(r'[0-9a-f]{64}', f['sha256']), 'Invalid hash'
        expected = {p['id'] for p in palettes if p['source'] == f['filename']}
        assert set(f['palette_ids']) == expected, 'Stale source index'
    verified = 0
    if source_dir:
        from PIL import Image
        images = {}
        for f in files:
            path = source_dir / f['filename']
            assert path.is_file(), f"Missing local image: {f['filename']}"
            assert hashlib.sha256(path.read_bytes()).hexdigest() == f['sha256'], f"Source changed: {path.name}"
            im = Image.open(path).convert('RGB')
            assert im.size == (f['width_px'], f['height_px']), 'Image size mismatch'
            images[path.name] = im
            verified += 1
        for p in palettes:
            for c in p['colors']:
                if not c['sampled_hex']:
                    continue
                x, y = c['sample_xy']
                crop = images[p['source']].crop((x-6, y-6, x+7, y+7))
                rgb = [int(statistics.median(crop.getchannel(i).tobytes())) for i in range(3)]
                recorded = bytes.fromhex(c['sampled_hex'][1:])
                assert max(abs(a-b) for a, b in zip(rgb, recorded)) <= 2, f"Sample changed: {p['id']} {x,y}"
    return {'images':len(files), 'palettes':len(palettes), 'color_positions':color_count,
            'source_hashes_verified':verified}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir', type=Path, help='Optional private original image folder; needs Pillow')
    args = parser.parse_args()
    result = audit(Path(__file__).resolve().parents[1], args.source_dir)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
