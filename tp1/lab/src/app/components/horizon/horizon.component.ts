import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { HorizonService } from 'src/app/services/horizon.service';

export interface PeriodicElement {
  name: string;
  position: number;
  weight: number;
  symbol: string;
}

const ELEMENT_DATA: PeriodicElement[] = [
  { position: 1, name: 'Hydrogen', weight: 1.0079, symbol: 'H' },
  { position: 2, name: 'Helium', weight: 4.0026, symbol: 'He' },
  { position: 3, name: 'Lithium', weight: 6.941, symbol: 'Li' },
  { position: 4, name: 'Beryllium', weight: 9.0122, symbol: 'Be' },
  { position: 5, name: 'Boron', weight: 10.811, symbol: 'B' },
  { position: 6, name: 'Carbon', weight: 12.0107, symbol: 'C' },
  { position: 7, name: 'Nitrogen', weight: 14.0067, symbol: 'N' },
  { position: 8, name: 'Oxygen', weight: 15.9994, symbol: 'O' },
  { position: 9, name: 'Fluorine', weight: 18.9984, symbol: 'F' },
  { position: 10, name: 'Neon', weight: 20.1797, symbol: 'Ne' },
];

@Component({
  selector: 'app-horizon',
  templateUrl: './horizon.component.html',
  styleUrls: ['./horizon.component.scss']
})
export class HorizonComponent implements OnInit {
  @ViewChild('myCanvas', { static: false }) myCanvas: ElementRef;
  public ctx: CanvasRenderingContext2D;
  displayedColumns: string[] = ['x', 'y'];
  dataSource = [];
  fileUrl;

  constructor(public horizonService: HorizonService, private sanitizer: DomSanitizer) { }

  ngOnInit(): void {
  }

  ngAfterViewInit(): void {
    this.ctx = this.myCanvas.nativeElement.getContext('2d');
    this.ctx.canvas.width = window.innerWidth * 0.65;
    this.ctx.canvas.height = window.innerHeight * 0.95;
    this.horizonService.setCanvas(this.ctx);
    this.dataSource = this.horizonService.listCriticPoints;
    this.generateFileTxt();
  }

  generateFileTxt(){
    let output : string = '';
    for(let point of this.dataSource){
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

  download(){

  }


}
