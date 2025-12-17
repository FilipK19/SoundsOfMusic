import { Routes } from '@angular/router';
import { Home } from './home/home';
import { GetMusic } from './get-music/get-music';
import { GetPlaylist } from './get-playlist/get-playlist';
import { Library } from './library/library';

export const routes: Routes = [
    {path:'', component: Home},
    {path:'getmusic', component: GetMusic},
    {path:'getplaylist', component: GetPlaylist},
    {path:'library', component: Library}
];
