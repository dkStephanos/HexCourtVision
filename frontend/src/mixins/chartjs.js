import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  BarController
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  BarController
);

class RoundedBarElement extends BarElement {
  draw(ctx) {
    const { x, y, base, width } = this.getProps(['x', 'y', 'base', 'width']);
    const radius = 5; // Customize the corner radius here

    ctx.beginPath();
    ctx.moveTo(x + radius, y);
    ctx.lineTo(x + width - radius, y);
    ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
    ctx.lineTo(x + width, base - radius);
    ctx.quadraticCurveTo(x + width, base, x + width - radius, base);
    ctx.lineTo(x + radius, base);
    ctx.quadraticCurveTo(x, base, x, base - radius);
    ctx.lineTo(x, y + radius);
    ctx.quadraticCurveTo(x, y, x + radius, y);
    ctx.closePath();

    ctx.fill();
    if (this.options.borderWidth) {
      ctx.stroke();
    }
  }
}

RoundedBarElement.id = 'roundedBar';
RoundedBarElement.defaults = BarElement.defaults;

ChartJS.register(RoundedBarElement);