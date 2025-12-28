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
  groupedSongs: any[] = [];

  constructor(private musicService: LibraryService, private cdr: ChangeDetectorRef) {}

  ngOnInit(): void {
    this.loadSongs();
  }

  loadSongs() {
    this.musicService.getMusic().subscribe(data => {
      this.songs = data;
      this.groupedSongs = this.getGroupedSongs(this.songs); // group after loading
      this.cdr.detectChanges();
    });
  }

  getDisplayName(name: string): string {
  return name.replace(/\.[^/.]+$/, '');
}

  // Group solo songs and playlists
  getGroupedSongs(songs: Song[]): any[] {
    const groups: any[] = [];
    let soloBuffer: Song[] = [];

    for (let song of songs) {
      if (!song.playlist) {
        soloBuffer.push(song);
      } else {
        // Flush any solo songs first
        if (soloBuffer.length) {
          groups.push({ type: 'solo', songs: [...soloBuffer] });
          soloBuffer = [];
        }

        // Consecutive playlist songs grouped together
        const lastGroup = groups[groups.length - 1];
        if (lastGroup && lastGroup.type === 'playlist' && lastGroup.name === song.playlist) {
          lastGroup.songs.push(song);
        } else {
          groups.push({ type: 'playlist', name: song.playlist, songs: [song] });
        }
      }
    }

    // Flush remaining solo songs
    if (soloBuffer.length) {
      groups.push({ type: 'solo', songs: [...soloBuffer] });
    }

    return groups;
  }
}
