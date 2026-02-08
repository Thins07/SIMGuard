import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app.component';
import { provideZoneChangeDetection } from '@angular/core';
import { provideHttpClient, withFetch } from '@angular/common/http';

bootstrapApplication(AppComponent, {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideHttpClient(withFetch())
  ]
}).catch((err) => console.error(err));