import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { HorizonService } from 'src/app/services/horizon.service';

@Component({
  selector: 'app-horizon',
  templateUrl: './horizon.component.html',
  styleUrls: ['./horizon.component.scss']
})
export class HorizonComponent implements OnInit {
  @ViewChild('myCanvas', { static: false }) myCanvas: ElementRef;

  public ctx: CanvasRenderingContext2D;

  constructor(public horizonService: HorizonService) { }

  ngOnInit(): void {
  }

  ngAfterViewInit(): void {
    this.ctx = this.myCanvas.nativeElement.getContext('2d');
    this.ctx.canvas.width = window.innerWidth * 0.78;
    this.ctx.canvas.height = window.innerHeight * 0.95;
    this.horizonService.setCanvas(this.ctx);
  }

  reset() {
    this.horizonService.reset();
  }

  changeNbBuildings(event: any) {
    this.horizonService.changeNbBuildings(event.value);
    this.reset();
  }

  showCriticsPoints(){
    this.horizonService.showCriticsPoints();
  }


}
