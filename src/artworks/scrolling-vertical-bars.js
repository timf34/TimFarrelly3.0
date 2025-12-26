/**
 * Scrolling Vertical Bars
 * Themes: inexhaustible source, smoothing complexity, effortless flow
 * Vertical patterns that endlessly transform, showing how complexity resolves into fluid motion
 */
export default function scrollingVerticalBars(canvas) {
  const ctx = canvas.getContext('2d');
  if (!ctx) return () => {};

  let scrollPosition = 0;
  let animId;

  const numLines = 60;

  const createPattern = (offset) => {
    const pattern = [];
    for (let i = 0; i < numLines; i++) {
      const bars = [];
      const numBars = 10 + Math.sin(i * 0.3 + offset) * 5;

      for (let j = 0; j < numBars; j++) {
        bars.push({
          yRatio: j / numBars + Math.sin(i * 0.5 + j * 0.3 + offset) * 0.05,
          heightRatio: 0.01 + Math.sin(i * 0.2 + j * 0.4) * 0.005,
          widthRatio: 0.004 + Math.cos(i * 0.3) * 0.004
        });
      }
      pattern.push(bars);
    }
    return pattern;
  };

  const pattern1 = createPattern(0);
  const pattern2 = createPattern(Math.PI);

  const render = () => {
    const { width, height } = canvas;
    const lineSpacing = width / numLines;

    scrollPosition += 0.0025;
    const scrollFactor = (Math.sin(scrollPosition) + 1) / 2;

    ctx.fillStyle = '#efeee7';
    ctx.fillRect(0, 0, width, height);

    for (let i = 0; i < numLines; i++) {
      const x = i * lineSpacing + lineSpacing / 2;

      ctx.beginPath();
      ctx.strokeStyle = '#666';
      ctx.lineWidth = 1;
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height);
      ctx.stroke();

      const bars1 = pattern1[i];
      const bars2 = pattern2[i];
      const maxBars = Math.max(bars1.length, bars2.length);

      for (let j = 0; j < maxBars; j++) {
        const bar1 = bars1[j] || bars2[j];
        const bar2 = bars2[j] || bars1[j];

        const y = (bar1.yRatio + (bar2.yRatio - bar1.yRatio) * scrollFactor) * height;
        const h = (bar1.heightRatio + (bar2.heightRatio - bar1.heightRatio) * scrollFactor) * height;
        const w = (bar1.widthRatio + (bar2.widthRatio - bar1.widthRatio) * scrollFactor) * width;

        ctx.fillStyle = '#222';
        ctx.fillRect(x - w / 2, y - h / 2, w, h);
      }
    }

    animId = requestAnimationFrame(render);
  };

  render();

  // Return cleanup function
  return () => {
    if (animId) cancelAnimationFrame(animId);
  };
}
