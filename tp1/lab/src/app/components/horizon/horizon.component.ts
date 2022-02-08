import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { HorizonService } from 'src/app/services/horizon.service';
import Chart from 'chart.js/auto';
interface Algorithme {
  value: number;
  viewValue: string;
}
@Component({
  selector: 'app-horizon',
  templateUrl: './horizon.component.html',
  styleUrls: ['./horizon.component.scss']
})
export class HorizonComponent implements OnInit {
  @ViewChild('myCanvas', { static: false }) myCanvas: ElementRef;
  @ViewChild('myChartCanvas', { static: false }) myChartCanvas: ElementRef;

  public ctx: CanvasRenderingContext2D;
  public ctxChart: CanvasRenderingContext2D;
  displayedColumns: string[] = ['x', 'y'];
  dataSource = [];
  fileUrl;
  algo: Algorithme[] = [
    { value: 1, viewValue: 'Naif' },
    { value: 2, viewValue: 'Diviser pour reigner' },
    { value: 3, viewValue: 'hybride' },
  ];
  public displayChart = 'none';
  public displayBuilding = 'block';
  myChart;

  constructor(public horizonService: HorizonService, private sanitizer: DomSanitizer) { }

  ngOnInit(): void {
  }

  ngAfterViewInit(): void {
    this.ctx = this.myCanvas.nativeElement.getContext('2d');
    this.ctx.canvas.width = window.innerWidth * 0.65;
    this.ctx.canvas.height = window.innerHeight * 0.95;

    this.ctxChart = this.myChartCanvas.nativeElement.getContext('2d');

    this.horizonService.setCanvas(this.ctx, this.ctxChart);
    this.dataSource = this.horizonService.listCriticPoints;
    this.generateFileTxt();
  }

  showPlot() {
    if (this.displayChart === 'block') {
      this.displayChart = 'none';
      this.displayBuilding = 'block';
    } else {
      this.displayChart = 'block';
      this.displayBuilding = 'none';
    }
  }

  generateFileTxt() {
    let output: string = '';
    for (let point of this.dataSource) {
      output += point.x.toString() + ' ' + point.y.toString() + '\n';
    }
    const blob = new Blob([output], { type: 'application/octet-stream' });
    this.fileUrl = this.sanitizer.bypassSecurityTrustResourceUrl(window.URL.createObjectURL(blob));
  }

  reset() {
    this.horizonService.reset();
    this.dataSource = this.horizonService.listCriticPoints;
  }

  changeNbBuildings(event: any) {
    this.horizonService.changeNbBuildings(event.value);
    this.reset();
  }

  showCriticsPoints() {
    this.horizonService.showCriticsPoints();
  }

  download() {

  }

  calculSolution() {
    this.horizonService.calculSolution(1);
    this.dataSource = this.horizonService.listCriticPoints;
  }

  genratePlot() {
    this.myChart = this.horizonService.generatePlot();
    //this.ctxChart.canvas.width = window.innerWidth * 0.50;
    //this.ctxChart.canvas.height = window.innerHeight * 0.95;
  }


}
