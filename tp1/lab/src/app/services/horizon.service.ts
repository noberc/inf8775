import { Injectable } from "@angular/core";


export interface Vec2 {
  x: number;
  y: number;
}

export interface Vec3 {
  x1: number;
  x2: number;
  h: number;
}

@Injectable({
  providedIn: 'root'
})
export class HorizonService {
  public ctx: CanvasRenderingContext2D;
  public ctxFront: CanvasRenderingContext2D;
  private origin: Vec2 = null;
  private unitWidth: number = null;
  private unitHeight: number = null;
  private axes: Vec2[] = [];
  private pointSize: number = 5;
  listBuildings: Vec3[] = [];
  public nbBuildings = 5;
  public listCriticPoints: Vec2[] = [];
  public criticPoints = false;

  constructor() { }

  setCanvas(canvas: CanvasRenderingContext2D) {
    this.ctx = canvas;
    this.unitWidth = this.ctx.canvas.width / 100;
    this.unitHeight = this.ctx.canvas.height / 100;
    this.initGraph();
  }

  initGraph() {
    this.origin = { x: this.unitWidth, y: this.ctx.canvas.height - this.unitHeight };
    const ord: Vec2 = { x: this.unitWidth, y: this.unitHeight };
    const abs: Vec2 = { x: this.ctx.canvas.width - this.unitWidth, y: this.ctx.canvas.height - this.unitHeight };
    this.axes.push(this.origin);
    this.axes.push(ord);
    this.axes.push(abs);
    this.drawAxe();
    this.generateBuildings(this.nbBuildings);
    console.log(this.listCriticPoints);
    this.sortCriticPoints();
    this.naifAlgorithm();
  }

  drawAxe() {
    this.ctx.strokeStyle = "black";
    this.ctx.fillStyle = "black";
    this.drawArrow(this.axes[0], this.axes[1], "black", 3);
    this.drawArrow(this.axes[0], this.axes[2], "black", 3);
    this.drawPoint(this.axes[0], "black", 1, "black");
  }

  drawLine(p1: Vec2, p2: Vec2, color: string, thickness: number) {
    this.ctx.beginPath();
    this.ctx.moveTo(p1.x, p1.y);
    this.ctx.lineTo(p2.x, p2.y);
    this.ctx.lineWidth = thickness;
    this.ctx.strokeStyle = color;
    this.ctx.stroke();
    this.ctx.lineWidth = 1;
  }

  drawArrow(p1: Vec2, p2: Vec2, color: string, thickness: number) {
    const headlen = 10; // length of head in pixels
    const dx = p2.x - p1.x;
    const dy = p2.y - p1.y;
    const angle = Math.atan2(dy, dx);
    this.ctx.moveTo(p1.x, p1.y);
    this.ctx.lineTo(p2.x, p2.y);
    this.ctx.stroke();
    this.ctx.lineTo(p2.x - headlen * Math.cos(angle - Math.PI / 6), p2.y - headlen * Math.sin(angle - Math.PI / 6));
    this.ctx.moveTo(p2.x, p2.y);
    this.ctx.stroke();
    this.ctx.lineTo(p2.x - headlen * Math.cos(angle + Math.PI / 6), p2.y - headlen * Math.sin(angle + Math.PI / 6));
    this.ctx.stroke();
  }

  drawPoint(coord: Vec2, color: string, thickness: number, borderCorlor: string) {
    this.ctx.beginPath();
    this.ctx.lineWidth = thickness;
    this.ctx.strokeStyle = borderCorlor;
    this.ctx.arc(coord.x, coord.y, this.pointSize, 0, 2 * Math.PI);
    this.ctx.stroke();
    this.ctx.fillStyle = color;
    this.ctx.fill();
  }

  generateBuildings(nbBuildings: number) {
    for (let i = 0; i < nbBuildings; i++) {
      const building: Vec3 = this.generateBuilding();
      this.drawBuilding(building);
      this.listBuildings.push(building);
    }
  }

  generateBuilding(): Vec3 {
    const x1 = this.getRandomInt(this.origin.x, this.axes[2].x);
    let x2 = this.getRandomInt(this.origin.x, this.axes[2].x);
    while (x2 < x1) {
      x2 = this.getRandomInt(this.origin.x, this.axes[2].x);
    }
    const h = this.getRandomInt(this.origin.y, this.axes[1].y);

    this.listCriticPoints.push({ x: this.origin.x + x1, y: this.origin.y - h });
    this.listCriticPoints.push({ x: this.origin.x + x1 + Math.abs(x2 - x1), y: this.origin.y })
    return { x1: x1, x2: x2, h: h };
  }

  drawBuilding(building: Vec3) {
    this.ctx.fillStyle = this.randomColor();
    this.ctx.beginPath();
    this.ctx.fillRect(this.origin.x + building.x1, this.origin.y, Math.abs(building.x2 - building.x1), -building.h);
    this.ctx.rect(this.origin.x + building.x1, this.origin.y, Math.abs(building.x2 - building.x1), -building.h);
    this.ctx.strokeStyle = 'black';
    this.ctx.stroke();
    this.drawPoint({ x: this.origin.x + building.x1, y: this.origin.y }, "black", 1, "black");
    this.drawPoint({ x: this.origin.x + building.x1 + Math.abs(building.x2 - building.x1), y: this.origin.y }, "black", 1, "black");
    this.drawPoint({ x: this.origin.x + building.x1, y: this.origin.y - building.h }, "black", 1, "black");
    this.drawPoint({ x: this.origin.x + building.x1 + Math.abs(building.x2 - building.x1), y: this.origin.y - building.h }, "black", 1, "black");
  }

  randomColor() {
    let r = this.getRandomInt(0, 255).toString();
    let v = this.getRandomInt(0, 255).toString();
    let b = this.getRandomInt(0, 255).toString();
    return "rgba(" + r + "," + v + ',' + b + ', 0.5)'
  }

  getRandomInt(min, max): number {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min)) + min;
  }

  reset() {
    this.ctx.clearRect(0, 0, this.ctx.canvas.width, this.ctx.canvas.height);
    this.origin = null;
    this.listBuildings = [];
    this.axes = [];
    this.listCriticPoints = [];
    this.ctx.clearRect(0, 0, this.ctx.canvas.width, this.ctx.canvas.height);
    this.drawLine({ x: 0, y: 0 }, { x: 0, y: 0 }, "white", 1);
    this.initGraph();
  }

  changeNbBuildings(value: number) {
    this.nbBuildings = value;
  }


  showCriticsPoints() {
    this.criticPoints = !this.criticPoints;
    if (!this.criticPoints) {
      for (let point of this.listCriticPoints) {
        this.drawPoint(point, "black", 1, "black");
      }
    } else {
      for (let point of this.listCriticPoints) {
        this.drawPoint(point, "red", 1, "red");
      }
    }
  }

  sortCriticPoints() {
    this.listCriticPoints.sort(function (a, b) {
      return a.x - b.x;
    });
  }

  naifAlgorithm() {
    let solution: Vec2[] = [];
    solution.push(this.origin);
    for (let point of this.listCriticPoints) {
      for (let building of this.listBuildings) {
        if (this.isPointInBuilding(point, building)) {
          if (point.y > this.origin.y - building.h) {
            point.y = this.origin.y - building.h;
          }
        }
      }
      if (point.y != solution[solution.length - 1].y) {
        solution.push(point);
      }
    }
    this.listCriticPoints = solution;
    console.log('solution', solution);
    this.drawHorizon(solution);
  }

  isPointInBuilding(point: Vec2, building: Vec3): boolean {
    if (point.x > this.origin.x + building.x1 &&
      point.x < this.origin.x + building.x1 + Math.abs(building.x2 - building.x1) &&
      point.y <= this.origin.y &&
      point.y >= this.origin.y - building.h) {
      return true;
    }
    else {
      return false;
    }
  }

  drawHorizon(solution: Vec2[]) {
    for (let i = 0; i < solution.length - 1; i++) {
      this.drawLine(solution[i], { x: solution[i + 1].x, y: solution[i].y }, "red", 5);
      this.drawLine({ x: solution[i + 1].x, y: solution[i].y }, solution[i + 1], "red", 5);
    }
  }


}
