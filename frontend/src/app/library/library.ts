import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LibraryService, Song } from '../services/library';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-library',
  imports: [CommonModule, HttpClientModule],
  templateUrl: './library.html',
  styleUrl: './library.css',
})
export class Library implements OnInit {
  songs: Song[] = [];

  constructor(private musicService: LibraryService, private cdr: ChangeDetectorRef) {}

  ngOnInit(): void {
    this.loadSongs();
  }

  loadSongs() {
    this.musicService.getMusic().subscribe(data => {
      this.songs = data;
      this.cdr.detectChanges();
    });
  }
}
