/**
 * Artworks Registry
 * 
 * Add new artworks by:
 * 1. Creating a new file in this folder (e.g., my-artwork.js)
 * 2. Importing it below
 * 3. Adding it to the artworks array
 * 
 * Each artwork should export a default function with signature:
 *   function(canvas: HTMLCanvasElement) => cleanupFunction
 * 
 * The cleanup function is called when the artwork is removed.
 */

import gentleWaves from './gentle-waves.js';
import scrollingVerticalBars from './scrolling-vertical-bars.js';
import tetheredFlow from './tethered-flow.js';

// Register all artworks here
export const artworks = [
  gentleWaves,
  scrollingVerticalBars,
  tetheredFlow,
];

// Get a random artwork
export function getRandomArtwork() {
  const index = Math.floor(Math.random() * artworks.length);
  return artworks[index];
}
