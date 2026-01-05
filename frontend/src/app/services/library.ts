import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

export interface Song {
  name: string;
  url: string;
  playlist?: string;
}

@Injectable({
  providedIn: 'root'
})
export class LibraryService {
  private apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  getMusic(): Observable<Song[]> {
    return this.http.get<Song[]>(`${this.apiUrl}/music`);
  }
}
