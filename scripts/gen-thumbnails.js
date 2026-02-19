import sharp from 'sharp';
import { readFileSync, existsSync, mkdirSync } from 'fs';
import { join, basename, extname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = fileURLToPath(new URL('.', import.meta.url));
const root = join(__dirname, '..');
const manifest = JSON.parse(readFileSync(join(root, 'src/data/pics-manifest.json'), 'utf-8'));
const thumbDir = join(root, 'public/pics/thumbs');

mkdirSync(thumbDir, { recursive: true });

const images = new Set();
for (const post of manifest) {
  for (const img of post.images) {
    if (!img.endsWith('.mp4')) images.add(img);
  }
}

let generated = 0, skipped = 0;
for (const img of images) {
  const base = basename(img, extname(img));
  const thumbPath = join(thumbDir, `${base}.webp`);
  if (existsSync(thumbPath)) { skipped++; continue; }
  await sharp(join(root, 'public/pics', img))
    .resize({ width: 400 })
    .webp({ quality: 82 })
    .toFile(thumbPath);
  generated++;
}

console.log(`Thumbnails: ${generated} generated, ${skipped} skipped.`);
