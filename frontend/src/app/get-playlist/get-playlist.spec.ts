import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GetPlaylist } from './get-playlist';

describe('GetPlaylist', () => {
  let component: GetPlaylist;
  let fixture: ComponentFixture<GetPlaylist>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GetPlaylist]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GetPlaylist);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
