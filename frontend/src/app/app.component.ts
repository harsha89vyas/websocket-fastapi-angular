import { Component, OnDestroy } from '@angular/core';
import { WebSocketService } from './websocket.service';
import { UploadService } from './upload.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent implements OnDestroy {
  message = '';
  sessionId = '';
  constructor(public webSocketService: WebSocketService, 
    public uploadService: UploadService) {
    this.sessionId = crypto.randomUUID();
    this.webSocketService.connect(this.sessionId);
  }

  sendMessage(message: string) {
    this.webSocketService.sendMessage(message);
  }

  ngOnDestroy() {
    this.webSocketService.close();
  }
  uploadTableFile(event: any){
    this.uploadService.uploadFile(event.target.files[0], 'table', this.sessionId);
  }
  uploadTemplateFile(event: any){
    this.uploadService.uploadFile(event.target.files[0], 'template', this.sessionId);
  }

  startProcessing(){
    this.uploadService.processFiles(this.sessionId);
  }
  
}
