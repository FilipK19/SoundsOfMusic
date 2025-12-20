import { Component } from '@angular/core';
import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field';
import {FormsModule} from '@angular/forms';
import { CommonModule } from '@angular/common';

import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-get-playlist',
  imports: [FormsModule, MatFormFieldModule, MatInputModule, CommonModule],
  templateUrl: './get-playlist.html',
  styleUrl: './get-playlist.css',
})
export class GetPlaylist {
  url = '';
  result: any = null;
  loading = false;
  error = '';

  constructor(private http: HttpClient) {}


  download() {
    this.loading = true;
    this.error = '';
    this.result = null;

    this.http.post<any>('http://127.0.0.1:8000/testYT2', {
      url: this.url
    }).subscribe({
      next: res => {
        this.result = res;
        this.loading = false;
        alert('Download completed!');
      },
      error: err => {
        this.loading = false;
        this.error = err.error?.detail || 'Something went wrong';
      }
    });
  }
}

