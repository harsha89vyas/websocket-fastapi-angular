import { Injectable } from '@angular/core';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { environment } from '../environments/environment';
import { HttpClient } from '@angular/common/http';

interface MessageData {
  message: string;
  time?: string;
}

@Injectable({
  providedIn: 'root',
})
export class UploadService {
    constructor(private http: HttpClient) {}
    fileName = '';
    public uploadFile(uploadedFile:File, type:string, session: string): void {
        const file:File = uploadedFile;
        if (file) {

            this.fileName = file.name;

            const formData = new FormData();

            formData.append("file", file);
            formData.append("fileName", file.name);
            formData.append("type", type);
            formData.append("session", session);

            const upload$ = this.http.post(`${environment.apiUrl}/upload`, formData);

            upload$.subscribe();
        }
    
  }

  /**
     * processFiles
     */
  public processFiles(session: string) {
    const formData = new FormData();
    formData.append("session", session);
    this.http.post(`${environment.apiUrl}/process`, formData).subscribe();
  }

}
