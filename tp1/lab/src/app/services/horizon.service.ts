import { Injectable } from "@angular/core";
import Chart from 'chart.js/auto';


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
  public ctxChart: CanvasRenderingContext2D;
  private origin: Vec2 = null;
  private unitWidth: number = null;
  private unitHeight: number = null;
  private axes: Vec2[] = [];
  private pointSize: number = 5;
  listBuildings: Vec3[] = [];
  public nbBuildings = 15;
  public listCriticPoints: Vec2[] = [];
  public criticPoints = false;
  myChart;

  constructor() { }

  generatePlot(): Chart {
    let listNaif: number[] = [];
    let listDivid: number[] = [];
    let abs: number[] = [];
    for (let i = 0; i < 350; i += 50) {
      this.nbBuildings = i;
      this.reset();
      let sol = this.calculSolution(1);
      if (i % 200 === 0) {
        abs.push(i)
        listDivid.push(sol[0]);
        listNaif.push(sol[1]);
      }
    }
    console.log(listNaif);
    console.log(listDivid);

    return new Chart(this.ctxChart, {
      type: 'line',
      options: {
        maintainAspectRatio: true,
      },
      data: {
        labels: abs,
        datasets: [{
          label: 'My First Dataset',
          data: listNaif,
          fill: true,
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1
        }, {
          label: 'My First Dataset',
          data: listDivid,
          fill: true,
          borderColor: 'rgb(75, 0, 192)',
          tension: 0.1
        }
        ],

      }
    });
  }

  setCanvas(canvas: CanvasRenderingContext2D, chartCanvas: CanvasRenderingContext2D) {
    this.ctxChart = chartCanvas;
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
    this.sortCriticPoints();
  }

  calculSolution(methode: number): number[] {
    let output: number[] = [];
    let startTime = performance.now()
    let sol: Vec2[] = [];
    sol.push(this.origin);
    for (let point of this.recursifAlgo(this.listBuildings)) {
      sol.push(point);
    }
    sol;
    let endTime = performance.now()
    this.setTimeExecution('Divide', (endTime - startTime).toFixed(12).toString(), 20, 60)
    output.push((endTime - startTime));
    startTime = performance.now()
    this.naifAlgorithm();
    endTime = performance.now()
    this.setTimeExecution('Naif', (endTime - startTime).toFixed(12).toString(), 20, 20)
    output.push((endTime - startTime));
    this.listCriticPoints = sol;
    this.drawHorizon(sol);

    return output;
  }

  setTimeExecution(algorithme: string, time: string, posX: number, posY: number) {
    this.ctx.font = "18px Arial";
    this.ctx.fillText(algorithme + ": " + time + " milliseconds", posX, posY);
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

  naifAlgorithm(): Vec2[] {
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
    //this.listCriticPoints = solution;
    //console.log('solution', solution);
    //this.drawHorizon(solution);
    return solution;
  }

  dividAlgorithme(listBuilding: Vec3[]): Vec2[] {
    let listCriticPointsA: Vec2[] = [];
    let listCriticPointsB: Vec2[] = [];

    if (listBuilding.length === 2) {
      listCriticPointsA.push({ x: this.origin.x + listBuilding[0].x1, y: this.origin.y - listBuilding[0].h });
      listCriticPointsA.push({ x: this.origin.x + listBuilding[0].x1 + Math.abs(listBuilding[0].x2 - listBuilding[0].x1), y: this.origin.y })
      listCriticPointsB.push({ x: this.origin.x + listBuilding[1].x1, y: this.origin.y - listBuilding[1].h });
      listCriticPointsB.push({ x: this.origin.x + listBuilding[1].x1 + Math.abs(listBuilding[1].x2 - listBuilding[1].x1), y: this.origin.y })
      return this.fusion(listCriticPointsA, listCriticPointsB);
    } else if (listBuilding.length === 1) {
      listCriticPointsA.push({ x: this.origin.x + listBuilding[0].x1, y: this.origin.y - listBuilding[0].h });
      listCriticPointsA.push({ x: this.origin.x + listBuilding[0].x1 + Math.abs(listBuilding[0].x2 - listBuilding[0].x1), y: this.origin.y })
      return listCriticPointsA;
    }
    else {
      return [];
    }
  }

  sortList(list: Vec2[]) {
    list.sort(function (a, b) {
      return a.x - b.x;
    });
  }

  fusion(listA: Vec2[], listB: Vec2[]) {
    let solution: Vec2[] = [];
    let listCriticPoints: Vec2[] = [];
    for (let point of listA) {
      listCriticPoints.push(point)
    }
    for (let point of listB) {
      listCriticPoints.push(point)
    }


    this.sortList(listCriticPoints);
    solution.push(listCriticPoints[0]);
    let lineA: number = 10000;
    let lineB: number = 10000;
    for (let i = 0; i < listCriticPoints.length; i++) {
      if (this.checkIfIsInList(listCriticPoints[i], listA)) {
        lineA = listCriticPoints[i].y;
      } else {
        lineB = listCriticPoints[i].y;
      }
      listCriticPoints[i].y = Math.min(lineA, lineB);
      if (i >= 1) {
        if (listCriticPoints[i].y !== listCriticPoints[i - 1].y) {
          solution.push(listCriticPoints[i]);
        }
      }
    }
    return solution;
  }

  checkIfIsInList(pointToFind: Vec2, listA: Vec2[]): boolean {
    // return listA.find((x) => {
    //   x === point
    // })
    for (let point of listA) {
      if (pointToFind === point) {
        return true;
      }
    }
    return false;
  }

  recursifAlgo(listBuilding: Vec3[]): Vec2[] {
    if (listBuilding.length <= 2) {
      return this.dividAlgorithme(listBuilding);
    } else {
      const lenghtA = Math.floor(listBuilding.length / 2);
      let listA: Vec3[] = [];
      let listB: Vec3[] = [];
      this.splitList(listBuilding, listA, listB, lenghtA);
      let critcPointsA: Vec2[] = this.recursifAlgo(listA);
      let critcPointsB: Vec2[] = this.recursifAlgo(listB);
      return this.fusion(critcPointsA, critcPointsB)
    }
  }

  splitList(listTosplit: Vec3[], listA: Vec3[], listB: Vec3[], lenghtA: number) {
    for (let i = 0; i < listTosplit.length; i++) {
      if (i < lenghtA) {
        listA.push(listTosplit[i]);
      } else {
        listB.push(listTosplit[i]);
      }
    }
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
