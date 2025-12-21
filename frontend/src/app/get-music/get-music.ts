import { Component } from '@angular/core';
import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field';
import {FormsModule} from '@angular/forms';
import { CommonModule } from '@angular/common';

import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-get-music',
  imports: [FormsModule, MatFormFieldModule, MatInputModule, CommonModule],
  templateUrl: './get-music.html',
  styleUrl: './get-music.css',
})
export class GetMusic {
  url = '';
  result: any = null;
  loading = false;
  error = '';

  constructor(private http: HttpClient) {}


  download() {
    this.loading = true;
    this.error = '';
    this.result = null;

    this.http.post<any>('http://127.0.0.1:8000/testYT', {
      url: this.url,
      mode: 'music'
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
