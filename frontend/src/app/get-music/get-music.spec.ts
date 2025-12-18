import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GetMusic } from './get-music';

import { ApplicationConfig } from '@angular/core';
import { provideHttpClient } from '@angular/common/http';

describe('GetMusic', () => {
  let component: GetMusic;
  let fixture: ComponentFixture<GetMusic>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GetMusic]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GetMusic);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

export const appConfig: ApplicationConfig = {
  providers: [provideHttpClient()]
};