import { Component } from '@angular/core';
import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field';
import {FormsModule} from '@angular/forms';

import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-get-music',
  imports: [FormsModule, MatFormFieldModule, MatInputModule],
  templateUrl: './get-music.html',
  styleUrl: './get-music.css',
})
export class GetMusic {
  link = '';

    constructor(private http: HttpClient) {}

  submit() {
  this.http.post<{ result: string }>(
    'http://127.0.0.1:8000/test',
    { text: this.link }
  ).subscribe(res => {
    alert(res.result);
  });
}

}
